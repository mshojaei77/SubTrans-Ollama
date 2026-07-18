import json
import tempfile
import time
from pathlib import Path
from src.subtitle_engine import SubtitleDocument
from src.translation.engine import SubtitleTranslator


class Provider:
    calls = 0
    def chat(self, messages, temperature=0.2):
        Provider.calls += 1
        items = json.loads(messages[-1]["content"].split("\n", 1)[1])
        time.sleep(0.01)
        return json.dumps([{"id": x["id"], "translation": f"T{x['id']}"} for x in items])


with tempfile.TemporaryDirectory() as directory:
    path = Path(directory) / "many.srt"
    path.write_text("\n\n".join(f"{i}\n00:00:00,000 --> 00:00:01,000\nLine {i}" for i in range(100)), encoding="utf-8")
    document = SubtitleDocument.load(path)
    result = SubtitleTranslator(batch_size=10, max_workers=5, context_mode="none").translate_document(document, Provider())
    assert [line.text for line in result.subtitles] == [f"T{i}" for i in range(100)]
    assert Provider.calls == 10
print("parallel translation check passed")
