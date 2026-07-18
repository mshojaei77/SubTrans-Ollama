from copy import deepcopy
from src.subtitles.models import TranslationUnit
from src.translation.prompts import batch_messages
from src.translation.validator import validate_translations


class SubtitleTranslator:
    def __init__(self, batch_size: int = 20, max_retries: int = 2):
        if batch_size < 1:
            raise ValueError("batch_size must be positive")
        self.batch_size = batch_size
        self.max_retries = max_retries

    def extract_units(self, document) -> list[TranslationUnit]:
        return [TranslationUnit(id=i, source=line.text) for i, line in enumerate(document.subtitles)]

    def _translate_batch(self, units, provider):
        last_error = None
        for _ in range(self.max_retries + 1):
            try:
                raw = provider.chat(batch_messages(units), temperature=0.2)
                return validate_translations(raw, [unit.id for unit in units])
            except (ValueError, TypeError) as exc:
                last_error = exc
        if len(units) > 1:
            result = {}
            for unit in units:
                result.update(self._translate_batch([unit], provider))
            return result
        raise ValueError(f"Unable to validate translation for subtitle {units[0].id}: {last_error}")

    def translate_document(self, document, provider):
        units = self.extract_units(document)
        translations = {}
        for start in range(0, len(units), self.batch_size):
            translations.update(self._translate_batch(units[start:start + self.batch_size], provider))
        result = deepcopy(document)
        for unit, line in zip(units, result.subtitles):
            line.text = translations[unit.id]
        return result
