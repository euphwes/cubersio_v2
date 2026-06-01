# cubersio v2

## Prerequisites

- [Python 3.14](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Node.js](https://nodejs.org/) (LTS)

## Backend setup

```sh
cd backend
uv sync --dev
```

This creates a `.venv` under `backend/` and installs all dependencies. Run it again any time `pyproject.toml` changes.

### Running the backend

```sh
cd backend
uv run uvicorn cubersio.main:app --reload
```

API will be available at `http://localhost:8000`.

## Frontend setup

```sh
cd frontend
npm install
```

### Running the frontend

```sh
cd frontend
npm run dev
```

App will be available at `http://localhost:5173`.

## Formatting

Formatters are run automatically on save via the Run on Save VS Code extension. To run them manually:

- **Python:** `cd backend && uv run ruff format .`
- **Svelte:** `cd frontend && npx prettier --write .`
