from copy import deepcopy
from src.translation.models import TranslationUnit
from src.translation.context import ContextBuilder
from src.glossary.service import GlossaryService
from src.translation.validator import validate_glossary
from src.memory.service import TranslationMemory
from src.evaluation.judge import TranslationJudge
from src.evaluation.database import EvaluationDatabase
from src.jobs.database import JobDatabase
from src.translation.prompts import batch_messages
from src.translation.validator import validate_translations


class SubtitleTranslator:
    def __init__(self, batch_size: int = 20, max_retries: int = 2, context_mode: str = "window", context_window: int = 3, glossary_path=None, glossary=None, memory=None, memory_path=None, judge=None, quality_mode: str = "disabled", evaluation_path=None):
        if batch_size < 1:
            raise ValueError("batch_size must be positive")
        self.batch_size = batch_size
        self.max_retries = max_retries
        if context_mode not in {"none", "window"}:
            raise ValueError("context_mode must be 'none' or 'window'")
        self.context_mode = context_mode
        self.context_builder = ContextBuilder(context_window)
        self.glossary = glossary or GlossaryService(path=glossary_path) if glossary_path else (glossary or GlossaryService())
        self.memory = memory if memory is not None else (TranslationMemory(memory_path) if memory_path else None)
        if quality_mode not in {"disabled", "fast", "standard", "strict"}:
            raise ValueError("quality_mode must be disabled, fast, standard, or strict")
        self.quality_mode = quality_mode
        self.judge = judge
        self.evaluations = EvaluationDatabase(evaluation_path) if evaluation_path else None

    def extract_units(self, document) -> list[TranslationUnit]:
        return [TranslationUnit(
            id=i,
            text=line.text,
            context=self.context_builder.build(document.subtitles, i) if self.context_mode == "window" else None,
            glossary=self.glossary.find_terms(line.text),
        ) for i, line in enumerate(document.subtitles)]

    def _translate_batch(self, units, provider):
        last_error = None
        for _ in range(self.max_retries + 1):
            try:
                raw = provider.chat(batch_messages(units), temperature=0.2)
                result = validate_translations(raw, [unit.id for unit in units])
                validate_glossary(result, {unit.id: [entry.target for entry in (unit.glossary or [])] for unit in units})
                return result
            except (ValueError, TypeError) as exc:
                last_error = exc
        if len(units) > 1:
            result = {}
            for unit in units:
                result.update(self._translate_batch([unit], provider))
            return result
        raise ValueError(f"Unable to validate translation for subtitle {units[0].id}: {last_error}")

    def translate_document(self, document, provider, job_id=None, source_file="", output_file="", job_database=None):
        units = self.extract_units(document)
        translations = {}
        checkpoints = {}
        jobs = job_database or (JobDatabase() if job_id else None)
        if jobs and job_id:
            if not jobs.checkpoints(job_id):
                jobs.create(job_id, source_file, output_file, len(units))
            checkpoints = jobs.checkpoints(job_id)
            translations.update(checkpoints)
        pending = []
        for unit in units:
            if unit.id in checkpoints:
                continue
            cached = self.memory.lookup(unit.text, [entry.target for entry in (unit.glossary or [])]) if self.memory else None
            if cached is not None:
                translations[unit.id] = cached
                if jobs and job_id:
                    jobs.save_checkpoint(job_id, unit.id, cached)
            else:
                pending.append(unit)
        for start in range(0, len(pending), self.batch_size):
            batch = pending[start:start + self.batch_size]
            result = self._translate_batch(batch, provider)
            if self.judge and self.quality_mode != "disabled":
                for unit in batch:
                    score = self.judge.evaluate(unit.text, result[unit.id], glossary=[e.target for e in (unit.glossary or [])])
                    if self.evaluations:
                        self.evaluations.save(unit.id, score)
                    if not score.passed and self.quality_mode in {"standard", "strict"}:
                        retry = [dict(role="system", content="Correct the translation using these review issues: " + "; ".join(score.issues)), dict(role="user", content=unit.text)]
                        corrected = provider.chat(retry, temperature=0.1)
                        if corrected.strip():
                            result[unit.id] = corrected.strip()
            translations.update(result)
            if self.memory:
                for unit in batch:
                    self.memory.save(unit.text, result[unit.id])
            if jobs and job_id:
                for unit in batch:
                    jobs.save_checkpoint(job_id, unit.id, result[unit.id])
        if jobs and job_id:
            jobs.set_status(job_id, "completed")
        result = deepcopy(document)
        for unit, line in zip(units, result.subtitles):
            line.text = translations[unit.id]
        return result
