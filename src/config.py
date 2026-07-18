import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    api_host: str = os.getenv("SUBTITLE_API_HOST", "127.0.0.1")
    api_port: int = int(os.getenv("SUBTITLE_API_PORT", "8000"))
    api_base_url: str = os.getenv("SUBTITLE_API_BASE_URL", "http://127.0.0.1:8000")
    data_dir: Path = Path(os.getenv("SUBTITLE_DATA_DIR", "data"))
    upload_dir: Path = Path(os.getenv("SUBTITLE_UPLOAD_DIR", "data/uploads"))
    output_dir: Path = Path(os.getenv("SUBTITLE_OUTPUT_DIR", "data/outputs"))
    maximum_upload_size_mb: int = int(os.getenv("SUBTITLE_MAX_UPLOAD_MB", "50"))
    progress_poll_interval_seconds: float = float(os.getenv("SUBTITLE_PROGRESS_POLL", "1"))

    def initialize(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)


def get_settings() -> Settings:
    settings = Settings()
    settings.initialize()
    return settings
