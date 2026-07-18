import hashlib
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


def text_hash(text: str) -> str:
    return hashlib.sha256(text.strip().lower().encode("utf-8")).hexdigest()


class MemoryDatabase:
    def __init__(self, path: str | Path = "data/translation_memory.db"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS translations (
                id INTEGER PRIMARY KEY, source_text TEXT NOT NULL,
                translated_text TEXT NOT NULL, source_lang TEXT NOT NULL,
                target_lang TEXT NOT NULL, created_at TEXT NOT NULL,
                hash TEXT NOT NULL, UNIQUE(hash, source_lang, target_lang))""")

    def _connect(self):
        return sqlite3.connect(self.path)

    def get_exact(self, text, source_lang, target_lang):
        db = self._connect()
        try:
            row = db.execute("SELECT translated_text FROM translations WHERE hash=? AND source_lang=? AND target_lang=?", (text_hash(text), source_lang, target_lang)).fetchone()
        finally:
            db.close()
        return row[0] if row else None

    def put(self, source, translation, source_lang, target_lang):
        db = self._connect()
        try:
            db.execute("INSERT OR REPLACE INTO translations(source_text, translated_text, source_lang, target_lang, created_at, hash) VALUES (?, ?, ?, ?, ?, ?)", (source, translation, source_lang, target_lang, datetime.now(timezone.utc).isoformat(), text_hash(source)))
            db.commit()
        finally:
            db.close()
