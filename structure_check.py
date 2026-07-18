from pathlib import Path
import tempfile
from src.subtitle_engine import SubtitleDocument
from src.translation.engine import SubtitleTranslator


class FakeProvider:
    def chat(self, messages, temperature=0.2):
        import json
        items = json.loads(messages[-1]["content"].split("\n", 1)[1])
        return json.dumps([{"id": item["id"], "translation": "سلام دنیا"} for item in items], ensure_ascii=False)


source = "1\n00:00:01,000 --> 00:00:03,000\nHello world\n"
with tempfile.TemporaryDirectory() as directory:
    input_path = Path(directory) / "input.srt"
    output_path = Path(directory) / "output.srt"
    input_path.write_text(source, encoding="utf-8")
    original = SubtitleDocument.load(input_path)
    translated = SubtitleTranslator(batch_size=20).translate_document(original, FakeProvider())
    translated.save(output_path)
    output = output_path.read_text(encoding="utf-8")
    assert output == "1\n00:00:01,000 --> 00:00:03,000\nسلام دنیا\n"
    assert original.subtitles[0].start == translated.subtitles[0].start
    assert original.subtitles[0].end == translated.subtitles[0].end
print("structure-aware translation check passed")
