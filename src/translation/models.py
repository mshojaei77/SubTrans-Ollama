from dataclasses import dataclass
from src.glossary.models import GlossaryEntry


@dataclass
class TranslationContext:
    previous: list[str]
    current: str
    next: list[str]


@dataclass
class TranslationUnit:
    id: int
    text: str
    context: TranslationContext | None = None
    glossary: list[GlossaryEntry] | None = None
    translated: str | None = None
