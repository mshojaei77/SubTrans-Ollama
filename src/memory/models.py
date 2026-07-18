from dataclasses import dataclass
from datetime import datetime


@dataclass
class MemoryEntry:
    source_text: str
    translated_text: str
    source_lang: str
    target_lang: str
    created_at: datetime
