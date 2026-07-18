# Developer setup

For local development only:

```powershell
uv sync
uvicorn src.api.main:app --reload
streamlit run app.py
```

Build the Windows one-folder executable on Windows:

```powershell
uv sync --extra build
pyinstaller --noconfirm --windowed --name "Subtitle Translator" --add-data "src;src" --add-data "app.py;." --add-data "data/glossary.json;data" launcher.py
```

The launcher chooses free local ports, starts the API and UI, opens the browser, and stops child processes when it exits.
