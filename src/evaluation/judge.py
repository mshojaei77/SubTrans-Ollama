import json
from .models import TranslationScore
from .prompts import judge_messages


class TranslationJudge:
    def __init__(self, provider, threshold: float = 7.0):
        self.provider = provider
        self.threshold = threshold

    def evaluate(self, source, translation, context=None, glossary=None):
        raw = self.provider.chat(judge_messages(source, translation, context, glossary), temperature=0.0)
        try:
            data = json.loads(raw)
            score = float(data["score"])
            passed = bool(data["passed"]) and score >= self.threshold
            issues = data["issues"]
            suggestions = data.get("suggestions", [])
            if not 1 <= score <= 10 or not isinstance(issues, list) or not isinstance(suggestions, list):
                raise ValueError
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise ValueError("Judge returned an invalid evaluation") from exc
        return TranslationScore(score, passed, issues, suggestions)
