# API

Run `uvicorn src.api.main:app --reload` and open `/docs`.

- `GET /health`
- `GET /providers`
- `POST /translate` (multipart `file` and JSON `request`)
- `GET /jobs/{id}`
- `POST /jobs/{id}/cancel`
- `POST /jobs/{id}/resume`
- `GET /jobs/{id}/stream`
- `GET /jobs/{id}/download`
