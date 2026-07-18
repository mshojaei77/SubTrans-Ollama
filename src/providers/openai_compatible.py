from openai import OpenAI
from .base import LLMProvider


class OpenAICompatibleProvider(LLMProvider):
    def __init__(self, model: str, base_url: str, api_key: str = ""):
        self.model = model
        self.client = OpenAI(base_url=base_url.rstrip("/"), api_key=api_key or "not-needed")

    def chat(self, messages, temperature=0.2):
        response = self.client.chat.completions.create(
            model=self.model, messages=messages, temperature=temperature
        )
        return response.choices[0].message.content or ""
