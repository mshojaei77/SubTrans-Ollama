import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class EvaluationDatabase:
    def __init__(self, path="data/evaluations.db"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(self.path)
        try:
            db.execute("CREATE TABLE IF NOT EXISTS evaluations (translation_id TEXT, score REAL, passed INTEGER, issues TEXT, timestamp TEXT)")
            db.commit()
        finally:
            db.close()

    def save(self, translation_id, score):
        db = sqlite3.connect(self.path)
        try:
            db.execute("INSERT INTO evaluations VALUES (?, ?, ?, ?, ?)", (str(translation_id), score.score, int(score.passed), json.dumps(score.issues, ensure_ascii=False), datetime.now(timezone.utc).isoformat()))
            db.commit()
        finally:
            db.close()
