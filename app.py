import re
import os
import time
import tempfile
import streamlit as st
from ollama import chat
import subprocess  # Add this import
from typing import List, Dict, Tuple


st.set_page_config(page_title="SRT Translator", page_icon="🎬", layout="wide")

# 1. Parse SRT files
def parse_srt(file_path: str) -> List[Dict]:
    """Parse an SRT file into a list of subtitle dictionaries."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by double newline to get individual subtitle blocks
    subtitle_blocks = re.split(r'\n\n+', content.strip())
    subtitles = []
    
    for block in subtitle_blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:  # Valid subtitle has at least 3 lines
            subtitle_id = lines[0]
            timestamp = lines[1]
            text = '\n'.join(lines[2:])
            
            subtitles.append({
                'id': subtitle_id,
                'timestamp': timestamp,
                'text': text
            })
    
    return subtitles

# 2. Translate text using Ollama
def translate_to_persian(text: str, model: str, previous_context=None) -> str:
    """Translate text to Persian using Ollama with previous context."""
    try:
        # Create the base messages with system prompt
        messages = [
            {
                'role': 'system',
                'content': 'شما یک مترجم دقیق فارسی هستید. متن را به فارسی روزمره و محاوره‌ای که توسط فارسی‌زبانان استفاده می‌شود ترجمه کنید. از اصطلاحات طبیعی فارسی و لحن گفتگویی استفاده کنید و از ترجمه‌های رسمی یا تحت‌اللفظی خودداری کنید. ترجمه‌های شما باید طوری باشد که انگار از ابتدا به فارسی نوشته شده است. فقط ترجمه فارسی را خروجی دهید - بدون توضیحات، یادداشت‌ها یا متن اصلی.'
            }
        ]
        # Add previous context to help maintain conversation flow
        if previous_context:
            for prev in previous_context:
                messages.append({'role': 'user', 'content': f'translate this subtitle to Persian: "{prev["original"]}"'})
                messages.append({'role': 'assistant', 'content': prev["translated"]})
        
        # Add current subtitle to translate
        messages.append({
            'role': 'user',
            'content': f'translate this subtitle to Persian: "{text}"',
        })
        
        response = chat(model=model, messages=messages)
        
        return response.message.content.strip()
    except Exception as e:
        st.error(f"Translation error: {e}")
        return text  # Return original text if translation fails

# 3. Create overlapping chunks for better context
def create_context_chunks(subtitles: List[Dict], window_size: int = 3) -> List[Tuple[List[Dict], int]]:
    """Create chunks of subtitles with overlapping context."""
    chunks = []
    for i in range(len(subtitles)):
        # Get surrounding subtitles for context
        start = max(0, i - window_size // 2)
        end = min(len(subtitles), i + window_size // 2 + 1)
        chunk = subtitles[start:end]
        chunks.append((chunk, i - start))  # (chunk, index of current subtitle in chunk)
    
    return chunks

# 4. Translate subtitles with context and batching
def translate_subtitles(subtitles: List[Dict], model: str, 
                        context_size: int = 3, batch_size: int = 10, 
                        delay: float = 0.5, progress_bar=None) -> List[Dict]:
    """Translate subtitles while maintaining translation context in model memory."""
    translated_subtitles = subtitles.copy()
    
    # Create a placeholder for the real-time preview
    preview_container = st.empty()
    
    # Process in batches to save memory and allow cooling
    for batch_start in range(0, len(subtitles), batch_size):
        batch_end = min(batch_start + batch_size, len(subtitles))
        
        # Track context for this batch
        context_history = []
        
        for idx in range(batch_start, batch_end):
            # Get the current subtitle
            current_subtitle = subtitles[idx]['text']
            
            # Prepare context from previous subtitles (limited by context_size)
            previous_context = []
            
            # First use context from previous batch if needed
            if idx == batch_start and batch_start > 0:
                # Add context from the end of the previous batch
                for j in range(max(0, batch_start - context_size), batch_start):
                    previous_context.append({
                        "original": subtitles[j]['text'],
                        "translated": translated_subtitles[j]['text']
                    })
            else:
                # Use context from the current batch
                for j in range(max(batch_start, idx - context_size), idx):
                    previous_context.append({
                        "original": subtitles[j]['text'],
                        "translated": translated_subtitles[j]['text']
                    })
            
            # Translate with context
            translated_text = translate_to_persian(current_subtitle, model, previous_context)
            
            # Store the translation
            translated_subtitles[idx]['text'] = translated_text
            
            # Update the real-time preview with the latest translation
            preview_container.markdown(f"""
            ### Currently Translating: Line {idx+1}/{len(subtitles)}
            **ID:** {subtitles[idx]['id']} | **Time:** {subtitles[idx]['timestamp']}
            
            **Original:**
            ```
            {current_subtitle}
            ```
            
            **Persian Translation:**
            ```
            {translated_text}
            ```
            """)
            
            # Update overall progress
            if progress_bar:
                progress_bar.progress((idx + 1) / len(subtitles),
                                    text=f"Translated {idx + 1}/{len(subtitles)} subtitles")
        
        # Add delay after processing each batch to cool down GPU
        if batch_end < len(subtitles):  # Don't delay after the final batch
            with st.spinner(f"Cooling down GPU for {delay} seconds..."):
                time.sleep(delay)
    
    # Clear the preview container when done
    preview_container.empty()
    
    return translated_subtitles

# 5. Write translated subtitles back to SRT file
def write_srt(subtitles: List[Dict], output_path: str):
    """Write subtitles to an SRT file."""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, sub in enumerate(subtitles):
            if i > 0:
                f.write('\n')
            f.write(f"{sub['id']}\n")
            f.write(f"{sub['timestamp']}\n")
            f.write(f"{sub['text']}\n")

# Function to ensure Ollama is running
def ensure_ollama_running():
    """Run 'ollama list' to verify Ollama is running."""
    try:
        # Run the ollama list command
        subprocess.run(["ollama", "list"], check=False, capture_output=False)
        st.success("Ollama is running correctly.")
    except subprocess.CalledProcessError:
        st.error("Failed to run 'ollama list'. Ollama is not responding properly.")
    except FileNotFoundError:
        st.error("Ollama command not found. Please make sure Ollama is installed and in your PATH.")

# Main Streamlit app
def main():
    # Create sidebar for configuration
    with st.sidebar:
        st.title("⚙️ Settings")
        
        st.markdown("### Translation Model")
        model = st.selectbox(
            "Choose a language model",
            ["mshojaei77/gemma3persian", "gemma3:1b", "gemma3:4b", "llama3.2:1b" , "qwen2:0.5b"],
            index=0,
            help="The AI model that will translate your subtitles"
        )
        
        st.markdown("### Advanced Settings")
        with st.expander("Advanced Options", expanded=False):
            # Add GPU warning message
            st.warning("⚠️ **Low-End GPU Warning**: If you have a low-end GPU or integrated graphics, please reduce the Processing Speed (batch size) and increase the Cooling Time to prevent crashes or overheating.")
            
            context_size = st.slider(
                "Context Awareness",
                min_value=1,
                max_value=10,
                value=3,
                help="How many previous subtitles to consider for better context (higher = more accurate but slower)"
            )
            
            batch_size = st.slider(
                "Processing Speed",
                min_value=1,
                max_value=50,
                value=10,
                help="How many subtitles to process at once (higher = faster but may use more computer resources)"
            )
            
            delay = st.slider(
                "Cooling Time (seconds)",
                min_value=0.0,
                max_value=5.0,
                value=0.5,
                step=0.1,
                help="Time to wait between processing groups of subtitles (higher = slower but prevents overheating)"
            )
        
        st.markdown("---")
        with st.expander("❓ Help & FAQ", expanded=False):
            st.markdown("""
            **What does this app do?**  
            Translates movie/video subtitles (.srt files) from any language to Persian using AI running on your computer.

            **Do I need to install anything?**  
            Yes, you need [Ollama](https://ollama.ai/) running on your computer. This app won't work without Ollama.
                        
            **The translation is very slow or my computer is overheating**
            - Reduce the "Batch Size" in Advanced Settings. A smaller batch size uses less processing power.
            - Increase the "Cooling Time" in Advanced Settings. This gives your computer more time to cool down.
            - Try a lighter model like gemma3:1b instead of gemma3persian for faster processing (though translations may be less accurate).
            - If you have a dedicated GPU, ensure Ollama is configured to use it.
            - Close other applications that may be using significant CPU or GPU resources.
            
            **How long will translation take?**  
            It depends on your computer's processing power, the model selected, and the size of your subtitle file. Larger files with many subtitles will take longer to process.

            **Which model should I choose for best results?**  
            The mshojaei77/gemma3persian model is specifically fine-tuned for Persian translation and usually gives the best results, but it's also the most resource-intensive.
            
            **How can I improve translation accuracy?**  
            Increase the "Context Awareness" setting to help the AI better understand the context of conversations.
            
            **Does my computer need internet access?**  
            No, once Ollama and the models are installed, everything runs offline.
            """)
    
    # Main content area
    st.title("🎬 Persian Subtitle Translator")
    st.markdown("Easily translate your subtitle files (.srt) to Persian - no technical knowledge required!")
    
    # Check Ollama status
    ollama_status = st.empty()
    
    try:
        subprocess.run(["ollama", "list"], check=False, capture_output=True)
        ollama_status.success("✅ Ollama is running correctly")
    except Exception as e:
        ollama_status.error("❌ Ollama is not running. Please start Ollama before continuing.")
        st.info("Don't have Ollama? [Click here to download and install](https://ollama.ai/)")
    
    # Step 1: File Upload
    st.markdown("### Step 1: Upload your subtitle file")
    uploaded_file = st.file_uploader("Drop your .srt file here", type=["srt"], 
                                   help="Only .srt subtitle files are supported")
    
    # Only show step 2 if file is uploaded
    if uploaded_file is not None:
        # Preview original content
        with st.expander("Preview Original Subtitles", expanded=False):
            # Save uploaded file temporarily to preview
            with tempfile.NamedTemporaryFile(delete=False, suffix='.srt') as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name
            
            # Show a sample of the original subtitles
            try:
                subtitles = parse_srt(temp_path)
                sample_size = min(3, len(subtitles))
                for i in range(sample_size):
                    st.text(f"{subtitles[i]['id']} - {subtitles[i]['timestamp']}\n{subtitles[i]['text']}")
            except Exception as e:
                st.error(f"Could not preview subtitles. The file might be invalid.")
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
        
        # Step 2: Translation
        st.markdown("### Step 2: Start translation")
        translate_button = st.button("🔄 Translate to Persian", use_container_width=True)
        
        if translate_button:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.srt') as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name
            
            try:
                # Parse SRT with friendly status updates
                parsing_status = st.empty()
                parsing_status.info("📄 Reading your subtitle file...")
                subtitles = parse_srt(temp_path)
                
                if not subtitles:
                    parsing_status.error("No subtitles found in this file. Please check if it's a valid SRT file.")
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                    st.stop()
                
                parsing_status.success(f"✅ Found {len(subtitles)} subtitles")
                
                # Create output file path
                output_path = temp_path.replace('.srt', '.fa.srt')
                
                # Show translation status
                st.markdown("### Step 3: Translation in progress")
                st.info(f"Using model: {model} - Please wait while your file is being translated")
                
                # Create progress indicators
                progress_container = st.container()
                with progress_container:
                    progress_text = st.empty()
                    progress_bar = st.progress(0.0)
                    
                    # Translate subtitles
                    translated_subtitles = translate_subtitles(
                        subtitles, 
                        model=model,
                        context_size=context_size, 
                        batch_size=batch_size,
                        delay=delay,
                        progress_bar=progress_bar
                    )
                
                # Write output file
                with st.spinner("📝 Creating your translated subtitle file..."):
                    write_srt(translated_subtitles, output_path)
                
                # Read the file for download
                with open(output_path, 'r', encoding='utf-8') as file:
                    translated_content = file.read()
                
                # Determine original filename without path
                original_name = uploaded_file.name
                output_name = original_name.replace('.srt', '.fa.srt')
                
                # Step 4: Download results
                st.markdown("### Step 4: Download your translated subtitles")
                st.success("✅ Translation complete! Your file is ready to download.")
                
                # Download button
                st.download_button(
                    label="⬇️ Download Persian Subtitles",
                    data=translated_content,
                    file_name=output_name,
                    mime="text/plain",
                    use_container_width=True
                )
                
                # Cleanup temporary files
                os.unlink(temp_path)
                os.unlink(output_path)
                
            except Exception as e:
                st.error(f"Something went wrong: {str(e)}")
                st.info("Please try again or try with a different subtitle file")
                # Clean up temp file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
    else:
        # Show helpful message when no file is uploaded
        st.info("👆 Upload your subtitle file to get started")

if __name__ == "__main__":
    main()