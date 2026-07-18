from abc import ABC, abstractmethod
from typing import Any


class LLMProvider(ABC):
    @abstractmethod
    def chat(self, messages: list[dict[str, str]], temperature: float = 0.2) -> str:
        raise NotImplementedError
