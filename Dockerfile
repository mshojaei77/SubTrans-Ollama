FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock README.md ./
RUN pip install uv && uv sync --frozen
COPY . .
EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
