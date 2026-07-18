import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from .models import TranslationJob


class JobDatabase:
    def __init__(self, path="data/jobs.db"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        db = sqlite3.connect(self.path)
        try:
            db.executescript("""CREATE TABLE IF NOT EXISTS jobs (id TEXT PRIMARY KEY, source_file TEXT, output_file TEXT, status TEXT, total_units INTEGER, completed_units INTEGER, created_at TEXT);
            CREATE TABLE IF NOT EXISTS checkpoints (job_id TEXT, unit_id INTEGER, translation TEXT, created_at TEXT, PRIMARY KEY(job_id, unit_id));""")
            db.commit()
        finally:
            db.close()

    def create(self, job_id, source_file, output_file, total_units):
        db = sqlite3.connect(self.path)
        try:
            db.execute("INSERT OR REPLACE INTO jobs VALUES (?, ?, ?, 'running', ?, 0, ?)", (job_id, source_file, output_file, total_units, datetime.now(timezone.utc).isoformat()))
            db.commit()
        finally:
            db.close()

    def checkpoints(self, job_id):
        db = sqlite3.connect(self.path)
        try:
            return dict(db.execute("SELECT unit_id, translation FROM checkpoints WHERE job_id=?", (job_id,)).fetchall())
        finally:
            db.close()

    def save_checkpoint(self, job_id, unit_id, translation):
        db = sqlite3.connect(self.path)
        try:
            db.execute("BEGIN")
            db.execute("INSERT OR REPLACE INTO checkpoints VALUES (?, ?, ?, ?)", (job_id, unit_id, translation, datetime.now(timezone.utc).isoformat()))
            db.execute("UPDATE jobs SET completed_units=(SELECT COUNT(*) FROM checkpoints WHERE job_id=?) WHERE id=?", (job_id, job_id))
            db.commit()
        finally:
            db.close()

    def set_status(self, job_id, status):
        db = sqlite3.connect(self.path)
        try:
            db.execute("UPDATE jobs SET status=? WHERE id=?", (status, job_id))
            db.commit()
        finally:
            db.close()
