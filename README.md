# 🎬 SubTrans-Ollama 

A simple tool that translates movie subtitles (.srt files) to Persian using AI



## What This App Does

This app helps you translate subtitle files from any language to Persian. All you need to do is upload your subtitle file, click a button, and download the translated version!

![image](https://github.com/user-attachments/assets/cd64df5e-e622-4671-8336-fb1b64707b15)

## Before You Start: What You'll Need

1. **A Computer** with Windows, Mac, or Linux
2. **Python** (version 3.12 or newer) installed on your computer
3. **Ollama** - a free AI tool that runs on your computer
4. **Internet Connection** to download the necessary files


## Easy Installation Guide

### Step 1: Install Python

If you don't already have Python installed:

1. Go to [Python.org](https://www.python.org/downloads/)
2. Click the big "Download Python" button
3. Run the installer and make sure to check "Add Python to PATH" during installation

### Step 2: Install Ollama

Ollama is the AI engine that powers the translations:

1. Visit [Ollama.ai/download](https://ollama.ai/download)
2. Download the version for your computer (Windows, Mac, or Linux)
3. Install it by following the on-screen instructions
4. Once installed, Ollama will run in the background (you'll see its icon in your system tray or menu bar)

### Step 3: Get the Subtitle Translator App

**Option A: Direct Download (Easiest)**
1. Click the green "Code" button at the top of this page
2. Select "Download ZIP"
3. Unzip the downloaded file to a folder on your computer

**Option B: Using Command Line**
```bash
git clone https://github.com/mshojaei77/SubTrans-Ollama.git
cd SubTrans-Ollama
```

### Step 4: Install the App

1. Open your computer's command prompt or terminal
   - On Windows: Press Win+R, type "cmd" and press Enter
   - On Mac: Open the Terminal app from Applications > Utilities
2. Navigate to the folder where you saved the app:
   ```
   cd path/to/SubTrans-Ollama
   ```
3. Install the required components:
   ```
   pip install -r requirements.txt
   ```

## How to Use the App

![image](https://github.com/user-attachments/assets/75d32c9a-c33d-45c0-b640-2ee47e89c127)

1. Start Ollama if it's not already running
   - On Windows: Find Ollama in your Start menu
   - On Mac: Find Ollama in your Applications folder

2. Start the translation app:
   - Open your command prompt/terminal
   - Navigate to the app folder
   - Type: `streamlit run app.py`
   - Your web browser will automatically open with the app

3. Using the app (with pictures):
   - Upload your subtitle file by clicking "Browse files"
   - Choose your settings (or leave as default)
   - Click "Translate Subtitles" and wait for it to finish
   - Click "Download Translated SRT" to save your Persian subtitles

## What the Settings Mean (Made Simple)

- **Ollama Model**: Which AI to use for translation. The default option is best for most users.
- **Context Window Size**: How many surrounding subtitles the AI looks at. Larger number = better translations but slower.
- **Batch Size**: How many subtitles to translate at once. Larger number = faster but uses more computer power.
- **Delay Between Batches**: How long to wait between groups of translations. Helps prevent your computer from getting too hot.

## Troubleshooting: Common Problems and Solutions

### "I can't install Python"
- Make sure you have administrator access on your computer.
- Try downloading Python from the Microsoft Store if you're on Windows 10 or 11.

### "Ollama isn't working"
- Make sure Ollama is running (check for its icon in your system tray).
- Restart your computer and try again.
- For Mac users: You might need to right-click the app and select "Open" the first time.
- ensure no proxy is running on your computer in 127.0.0.1:11434 (this is the default port for ollama)

### "I see errors when running the app"
- Make sure you installed all requirements: `pip install -r requirements.txt`
- Try restarting Ollama.
- Check that you're using Python 3.12 or newer: type `python --version` in your terminal.

### "The translations aren't good"
- Try increasing the "Context Window Size" to 5 or higher.
- Make sure you're using the recommended model (mshojaei77/gemma3persian).

### "The translation is very slow, or my computer is overheating / using too much CPU"
- Reduce the "Batch Size". A smaller batch size uses less processing power at once.
- Increase the "Delay Between Batches". This gives your computer more time to cool down between processing chunks of subtitles.
- Consider using a lighter model like gemma3:1b instead of gemma3persian for faster processing, though translations may be less accurate.
- If you have a dedicated GPU, ensure Ollama is configured to use it. Consult the Ollama documentation for GPU configuration.
- Close other applications that may be using significant CPU or GPU resources.

## Need More Help?

- Create an "Issue" on this GitHub page

## License

MIT License - Free to use for everyone!
