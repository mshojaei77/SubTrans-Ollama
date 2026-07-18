import json
import re
from pathlib import Path
from .models import GlossaryEntry


class GlossaryService:
    def __init__(self, entries: list[GlossaryEntry] | None = None, path: str | Path | None = None):
        if path:
            entries = [GlossaryEntry(**item) for item in json.loads(Path(path).read_text(encoding="utf-8"))]
        self.entries = entries or []

    def find_terms(self, text: str) -> list[GlossaryEntry]:
        found = []
        for entry in self.entries:
            flags = 0 if entry.case_sensitive else re.IGNORECASE
            if re.search(re.escape(entry.source), text, flags):
                found.append(entry)
        return found
