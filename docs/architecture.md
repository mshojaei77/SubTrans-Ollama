# Architecture

Streamlit is an API client. FastAPI owns upload validation and job state. `SubtitleTranslator` remains the engine and uses provider, context, glossary, memory, evaluation, checkpoint, and worker components. SQLite stores jobs and durable progress; Docker persists `/app/data`.
