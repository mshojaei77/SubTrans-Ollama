from dataclasses import dataclass


@dataclass(frozen=True)
class GlossaryEntry:
    source: str
    target: str
    description: str | None = None
    case_sensitive: bool = False
