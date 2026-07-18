from dataclasses import dataclass


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
    translated: str | None = None
