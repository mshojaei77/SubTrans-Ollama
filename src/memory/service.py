from difflib import SequenceMatcher
from .database import MemoryDatabase


class TranslationMemory:
    def __init__(self, path="data/translation_memory.db", source_lang="auto", target_lang="fa", similarity_threshold=0.92):
        self.database = MemoryDatabase(path)
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.similarity_threshold = similarity_threshold

    def lookup(self, text: str, glossary_targets: list[str] | None = None):
        exact = self.database.get_exact(text, self.source_lang, self.target_lang)
        if exact and all(target in exact for target in (glossary_targets or [])):
            return exact
        if not text.strip():
            return None
        db = self.database._connect()
        try:
            rows = db.execute("SELECT source_text, translated_text FROM translations WHERE source_lang=? AND target_lang=?", (self.source_lang, self.target_lang)).fetchall()
        finally:
            db.close()
        normalized = text.strip().lower()
        for source, translation in rows:
            if SequenceMatcher(None, normalized, source.strip().lower()).ratio() >= self.similarity_threshold and all(target in translation for target in (glossary_targets or [])):
                return translation
        return None

    def save(self, source: str, translation: str):
        self.database.put(source, translation, self.source_lang, self.target_lang)
