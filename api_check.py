from fastapi.testclient import TestClient
from src.api.main import app, jobs

job_id = "api-check"
jobs.create(job_id, "input.srt", "output.srt", 10)
client = TestClient(app)
response = client.get(f"/jobs/{job_id}")
assert response.status_code == 200
assert response.json()["total"] == 10
assert client.post(f"/jobs/{job_id}/cancel").json()["status"] == "cancelled"
print("api check passed")
