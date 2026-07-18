import json
import streamlit as st
from src.client import SubtitleAPIClient, SubtitleAPIError
from src.config import get_settings


st.set_page_config(page_title="Subtitle Translator", page_icon="🎬", layout="wide")
settings = get_settings()
client = SubtitleAPIClient(settings.api_base_url)
st.session_state.setdefault("active_job_id", None)
st.session_state.setdefault("completed_download", None)

st.title("🎬 Subtitle Translator")
try:
    health = client.health()
    st.success(f"API: {health.get('status', 'connected')}")
except SubtitleAPIError as exc:
    st.error(f"API unavailable: {exc.message}")
    st.info("Start the API with: uvicorn src.api.main:app --reload")
    st.stop()

with st.form("translation_form"):
    uploaded = st.file_uploader("Subtitle file", type=["srt", "ass", "ssa", "vtt", "lrc"])
    col1, col2 = st.columns(2)
    with col1:
        source_language = st.text_input("Source language", "auto")
        provider = st.selectbox("Provider", ["ollama", "lmstudio", "openai-compatible"])
        base_url = st.text_input("Base URL", "http://localhost:11434" if provider == "ollama" else "http://localhost:1234/v1")
        model = st.text_input("Model", "local-model")
    with col2:
        target_language = st.text_input("Target language", "fa")
        api_key = st.text_input("API key", type="password")
        batch_size = st.slider("Batch size", 1, 100, 20)
        max_workers = st.slider("Maximum workers", 1, 8, 1)
    quality_mode = st.selectbox("Quality mode", ["disabled", "fast", "standard", "strict"])
    glossary_enabled = st.checkbox("Enable glossary", True)
    submitted = st.form_submit_button("Start translation", disabled=uploaded is None)

if submitted and uploaded:
    config = json.dumps({"source_language": source_language, "target_language": target_language, "provider": provider, "model": model, "base_url": base_url, "api_key": api_key, "batch_size": batch_size, "max_workers": max_workers, "quality_mode": quality_mode, "glossary_enabled": glossary_enabled})
    try:
        result = client.create_translation(uploaded, config)
        st.session_state.active_job_id = result["job_id"]
        st.session_state.completed_download = None
        st.rerun()
    except SubtitleAPIError as exc:
        st.error(f"{exc.code}: {exc.message}")

job_id = st.session_state.active_job_id
if job_id:
    try:
        job = client.job(job_id)
        st.subheader(f"Job {job_id}")
        st.progress(float(job.get("progress", job.get("percentage", 0) / 100)))
        st.write(f"{job['status']} — {job.get('completed', job.get('completed_units', 0))}/{job.get('total', job.get('total_units', 0))}")
        if job["status"] in {"running", "pending"}:
            if st.button("Cancel translation"):
                client.cancel(job_id)
                st.rerun()
        elif job["status"] == "cancelled":
            if st.button("Resume translation"):
                client.resume(job_id)
                st.rerun()
        elif job["status"] == "completed":
            data, disposition, media_type = client.download(job_id)
            st.download_button("Download translated subtitles", data=data, file_name="translated_subtitles.srt", mime=media_type)
    except SubtitleAPIError as exc:
        st.error(f"{exc.code}: {exc.message}")
