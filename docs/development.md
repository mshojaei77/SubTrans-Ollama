# Developer setup

For local development:

```powershell
uv sync
uvicorn src.api.main:app --reload
streamlit run app.py
```
