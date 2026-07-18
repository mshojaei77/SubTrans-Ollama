from dataclasses import dataclass


@dataclass
class TranslationConfig:
    batch_size: int = 20
    max_workers: int = 4
    concurrency_mode: str = "async"
