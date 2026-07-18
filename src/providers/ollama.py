from ollama import chat as ollama_chat
from .base import LLMProvider


class OllamaProvider(LLMProvider):
    def __init__(self, model: str):
        self.model = model

    def chat(self, messages, temperature=0.2):
        response = ollama_chat(model=self.model, messages=messages, options={"temperature": temperature})
        return response.message.content or ""
