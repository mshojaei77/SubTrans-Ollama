from pydantic import BaseModel, Field


class TranslationRequest(BaseModel):
    source_language: str = "auto"
    target_language: str = "fa"
    provider: str = "openai-compatible"
    model: str
    base_url: str = "http://localhost:1234/v1"
    api_key: str = ""
    batch_size: int = Field(20, ge=1, le=200)
    max_workers: int = Field(1, ge=1, le=32)
    glossary_enabled: bool = True
    quality_mode: str = "disabled"
