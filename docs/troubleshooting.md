# Troubleshooting

Start the API before the UI: `uvicorn src.api.main:app --reload`. Check `GET /health`. For local models, verify the provider base URL and model name. Cancelled jobs retain checkpoints and can be resumed when their original configuration is available.
