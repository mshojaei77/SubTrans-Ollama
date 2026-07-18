"""Simple, non-technical Streamlit front end for the translation API."""
import json
from pathlib import Path

import streamlit as st

from src.client import SubtitleAPIClient, SubtitleAPIError
from src.config import get_settings


st.set_page_config(page_title="Easy Subtitle Translator", page_icon="🎬", layout="centered")
settings = get_settings()
client = SubtitleAPIClient(settings.api_base_url)
st.session_state.setdefault("active_job_id", None)

st.title("🎬 Easy Subtitle Translator")
st.caption("Translate your subtitles with a few clicks. Your files stay on your computer.")

try:
    discovery = client.discover()
except SubtitleAPIError:
    st.error("The translator is still starting. Please try again in a moment.")
    st.stop()

if not discovery.get("available"):
    st.warning("AI engine not found")
    st.write("Subtitle Translator needs Ollama or LM Studio running on this computer.")
    with st.expander("How to set it up"):
        recommended = discovery.get("recommended_model", "google/gemma-4-E2B")
        st.markdown(f"**Recommended model:** `{recommended}`\n\n**Ollama:** Install Ollama, download the recommended model, and leave it running.\n\n**LM Studio:** Open LM Studio, load a model, start its local server, then click **Check again**.")
    if st.button("Check again"):
        st.rerun()
    st.stop()

provider = discovery["provider"]
base_url = discovery["base_url"]
model = discovery["model"]
available_models = discovery.get("models", [model])
preferred = "google/gemma-4-E2B"
available_models = sorted(available_models, key=lambda name: 0 if name == preferred else 1)

with st.form("easy_translation_form"):
    uploaded = st.file_uploader(
        "1. Choose a subtitle file",
        type=["srt", "ass", "ssa", "vtt", "lrc"],
        help="Supported files: SRT, ASS, SSA, VTT, and LRC.",
    )
    model = st.selectbox("AI model", available_models, index=0, help="These are the models already installed in your local AI engine.")

    with st.expander("Advanced settings (optional)"):
        base_url = st.text_input("Provider address", base_url)
        api_key = st.text_input("API key (only needed for online services)", type="password")
        custom_model = st.text_input("Use a model name not shown above (optional)", "")
        batch_size = st.slider("Processing batch size", 1, 100, 20)
        max_workers = st.slider("Parallel workers", 1, 8, 1)
        quality_mode = st.selectbox("Quality checking", ["disabled", "standard", "strict"], index=1)
        glossary_enabled = st.checkbox("Use the built-in terminology glossary", True)

    submitted = st.form_submit_button("🚀 Translate subtitles", type="primary", disabled=uploaded is None, use_container_width=True)

if submitted and uploaded:
    model = custom_model.strip() or model
    request = json.dumps({
        "source_language": "auto", "target_language": "fa", "provider": provider,
        "model": model, "base_url": base_url, "api_key": api_key,
        "batch_size": batch_size, "max_workers": max_workers,
        "quality_mode": quality_mode, "glossary_enabled": glossary_enabled,
    })
    try:
        result = client.create_translation(uploaded, request)
        st.session_state.active_job_id = result["job_id"]
        st.rerun()
    except SubtitleAPIError as exc:
        st.error(f"Could not start translation: {exc.message}")

job_id = st.session_state.active_job_id
if job_id:
    st.divider()
    st.subheader("Translation progress")
    try:
        job = client.job(job_id)
        completed = job.get("completed", job.get("completed_units", 0))
        total = job.get("total", job.get("total_units", 0))
        progress = max(0.0, min(1.0, float(job.get("progress", job.get("percentage", 0) / 100))))
        st.progress(progress, text=f"{completed} of {total} subtitles")
        status = job["status"]
        if status in {"pending", "running"}:
            st.info("Translation is running. You can leave this page open.")
            if st.button("Stop translation"):
                client.cancel(job_id)
                st.rerun()
        elif status == "cancelled":
            st.warning("Translation stopped. Your progress was saved.")
            if st.button("Continue translation"):
                client.resume(job_id)
                st.rerun()
        elif status == "completed":
            data, _, media_type = client.download(job_id)
            st.success("Translation complete!")
            st.download_button("⬇️ Download translated subtitles", data=data, file_name="translated_subtitles.srt", mime=media_type, use_container_width=True)
        else:
            st.error("Translation stopped unexpectedly. Saved progress can be resumed when the service is available.")
            if st.button("Try again"):
                client.resume(job_id)
                st.rerun()
    except SubtitleAPIError as exc:
        st.error(f"Could not read progress: {exc.message}")
