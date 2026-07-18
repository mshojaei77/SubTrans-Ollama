from dataclasses import dataclass


@dataclass
class TranslationScore:
    score: float
    passed: bool
    issues: list[str]
    suggestions: list[str]
