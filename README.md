# FastAPI Pandas API Example

A simple example REST API built with FastAPI that uses pandas. Example datasets are included.

To run:

```
uv sync
uv run uvicorn app.main:app --reload
```

To connect to a Render web service:

- Build Command: `pip install uv && uv sync`
- Start Command: `uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT`
