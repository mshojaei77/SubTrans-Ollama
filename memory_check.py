import json
import tempfile
from pathlib import Path
from src.memory.service import TranslationMemory
from src.subtitle_engine import SubtitleDocument
from src.translation.engine import SubtitleTranslator


class Provider:
    calls = 0
    def chat(self, messages, temperature=0.2):
        Provider.calls += 1
        items = json.loads(messages[-1]["content"].split("\n", 1)[1])
        return json.dumps([{"id": x["id"], "translation": "سلام"} for x in items], ensure_ascii=False)


with tempfile.TemporaryDirectory() as directory:
    db = Path(directory) / "memory.db"
    memory = TranslationMemory(db, source_lang="en", target_lang="fa")
    memory.save("Hello", "سلام")
    assert memory.lookup("hello") == "سلام"
    source = Path(directory) / "one.srt"
    source.write_text("1\n00:00:01,000 --> 00:00:02,000\nHello\n", encoding="utf-8")
    document = SubtitleDocument.load(source)
    translator = SubtitleTranslator(memory=memory, context_mode="none")
    translator.translate_document(document, Provider())
    assert Provider.calls == 0
print("translation memory check passed")
