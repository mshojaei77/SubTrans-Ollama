from dataclasses import dataclass
from pathlib import Path
import pysubs2


SUPPORTED_EXTENSIONS = {".srt", ".ass", ".ssa", ".vtt", ".lrc"}


@dataclass
class SubtitleDocument:
    path: Path
    subtitles: pysubs2.SSAFile

    @classmethod
    def load(cls, path: str | Path) -> "SubtitleDocument":
        source = Path(path)
        if source.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported subtitle format: {source.suffix}")
        return cls(source, pysubs2.load(str(source)))

    def save(self, path: str | Path) -> None:
        self.subtitles.save(str(path))

    def records(self) -> list[dict]:
        return [
            {"id": index, "start": line.start, "end": line.end, "text": line.text}
            for index, line in enumerate(self.subtitles)
        ]
