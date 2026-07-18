import asyncio
import json
import uuid
from pathlib import Path
from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from src.api.schemas import TranslationRequest
from src.jobs.database import JobDatabase
from src.subtitle_engine import SubtitleDocument, SUPPORTED_EXTENSIONS
from src.translation.engine import SubtitleTranslator
from src.providers import OllamaProvider, LMStudioProvider, OpenAICompatibleProvider

app = FastAPI(title="Subtitle Translation API")
UPLOADS = Path("data/uploads")
UPLOADS.mkdir(parents=True, exist_ok=True)
jobs = JobDatabase()


def _provider(request):
    if request.provider.lower() == "ollama":
        return OllamaProvider(request.model)
    if request.provider.lower() == "lm studio":
        return LMStudioProvider(request.model, request.base_url)
    if request.provider.lower() in {"openai-compatible", "openai"}:
        return OpenAICompatibleProvider(request.model, request.base_url, request.api_key)
    raise HTTPException(400, "Unsupported provider")


async def _run_job(job_id, input_path, output_path, request):
    try:
        document = SubtitleDocument.load(input_path)
        translator = SubtitleTranslator(batch_size=request.batch_size, max_workers=request.max_workers, quality_mode=request.quality_mode, glossary_path="data/glossary.json" if request.glossary_enabled else None, memory_path="data/translation_memory.db")
        result = await asyncio.to_thread(translator.translate_document, document, _provider(request), job_id, str(input_path), str(output_path), jobs)
        result.save(output_path)
    except Exception:
        jobs.set_status(job_id, "failed")


@app.post("/translate")
async def translate(file: UploadFile = File(...), request: str = Form(...), background_tasks: BackgroundTasks = None):
    config = TranslationRequest.model_validate_json(request)
    suffix = Path(file.filename or "").suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(400, f"Unsupported subtitle format: {suffix}")
    job_id = uuid.uuid4().hex
    input_path = UPLOADS / f"{job_id}{suffix}"
    output_path = UPLOADS / f"{job_id}.fa{suffix}"
    input_path.write_bytes(await file.read())
    document = SubtitleDocument.load(input_path)
    jobs.create(job_id, str(input_path), str(output_path), len(document.subtitles))
    if background_tasks is not None:
        background_tasks.add_task(_run_job, job_id, input_path, output_path, config)
    return {"job_id": job_id, "status": "queued"}


@app.get("/jobs/{job_id}")
def status(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(404, "Job not found")
    total = job["total_units"] or 0
    return {"job_id": job_id, "status": job["status"], "completed": job["completed_units"], "total": total, "percentage": round(job["completed_units"] * 100 / total, 2) if total else 0}


@app.post("/jobs/{job_id}/cancel")
def cancel(job_id: str):
    if not jobs.get(job_id):
        raise HTTPException(404, "Job not found")
    jobs.set_status(job_id, "cancelled")
    return {"job_id": job_id, "status": "cancelled"}


@app.get("/jobs/{job_id}/stream")
async def stream(job_id: str):
    if not jobs.get(job_id):
        raise HTTPException(404, "Job not found")
    async def events():
        while True:
            current = jobs.get(job_id)
            yield f"event: progress\ndata: {json.dumps(current)}\n\n"
            if current["status"] in {"completed", "failed", "cancelled"}:
                break
            await asyncio.sleep(0.5)
    return StreamingResponse(events(), media_type="text/event-stream")
