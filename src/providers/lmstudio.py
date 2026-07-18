from .openai_compatible import OpenAICompatibleProvider


class LMStudioProvider(OpenAICompatibleProvider):
    def __init__(self, model: str = "local-model", base_url: str = "http://localhost:1234/v1"):
        super().__init__(model=model, base_url=base_url, api_key="lm-studio")
