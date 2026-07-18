from dataclasses import dataclass
from datetime import datetime


@dataclass
class TranslationJob:
    id: str
    source_file: str
    output_file: str
    total_units: int
    completed_units: int
    status: str
    created_at: datetime
