from dataclasses import dataclass


@dataclass
class TranslationUnit:
    id: int
    source: str
    translated: str | None = None
    context: dict | None = None
