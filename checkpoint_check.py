import json
import tempfile
from pathlib import Path
from src.jobs.database import JobDatabase

with tempfile.TemporaryDirectory() as directory:
    db = JobDatabase(Path(directory) / "jobs.db")
    db.create("job", "movie.srt", "movie.fa.srt", 3)
    db.save_checkpoint("job", 0, "one")
    db.save_checkpoint("job", 1, "two")
    restored = db.checkpoints("job")
    assert restored == {0: "one", 1: "two"}
    # A restarted worker skips 0 and 1 and only processes unit 2.
    remaining = [i for i in range(3) if i not in restored]
    assert remaining == [2]
print("checkpoint check passed")
