import json
from src.evaluation.judge import TranslationJudge
from src.evaluation.models import TranslationScore


class JudgeProvider:
    def __init__(self, score, passed, issues=None):
        self.score, self.passed, self.issues = score, passed, issues or []
    def chat(self, messages, temperature=0.0):
        return json.dumps({"score": self.score, "passed": self.passed, "issues": self.issues, "suggestions": []})


good = TranslationJudge(JudgeProvider(9, True)).evaluate("Hello world", "سلام دنیا")
assert good.passed and good.score > 8
bad = TranslationJudge(JudgeProvider(4, False, ["Glossary violation"])).evaluate("John Wick", "یوحنا ویک", glossary=["جان ویک"])
assert not bad.passed and bad.issues
print("quality judge check passed")
