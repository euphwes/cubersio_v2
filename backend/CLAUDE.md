# CLAUDE.md - Backend Conventions

Python + FastAPI project. Read this alongside the root `CLAUDE.md`, which applies everywhere.

---

## Stack

- **Framework:** FastAPI
- **Language:** Python (strict typing)
- **Request/response validation:** Pydantic v2

---

## Naming

- **Files and modules:** `snake_case` - `events.py`, `solve_utils.py`
- **Variables and functions:** `snake_case`
- **Classes (including Pydantic models):** `PascalCase` - `EventResponse`, `SolveSubmission`
- **Constants:** `UPPER_SNAKE_CASE`

---

## Folder Structure

```
backend/
  cubersio/
    routers/      # One file per resource/domain
      events.py
      users.py
      solves.py
    models/       # Pydantic request/response models
      events.py
      users.py
      solves.py
    services/     # Business logic, decoupled from routing
    main.py        # App entry point, router registration only
```

- Routers handle HTTP concerns only - no business logic inline.
- Business logic lives in `services/`.
- Do not put logic directly in `main.py`.

---

## Routes

One file per resource/domain in `routers/`. Each router file contains only the routes for that resource and registers its own `APIRouter`.

```python
# routers/events.py
from fastapi import APIRouter

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/", response_model=list[EventResponse])
async def list_events() -> list[EventResponse]:
    ...
```

Routers are registered in `main.py` and nowhere else:

```python
# main.py
app.include_router(events.router)
app.include_router(solves.router)
```

---

## Pydantic Models

Use Pydantic models for **all** request bodies and response shapes - no raw dicts in or out of route handlers.

- Define models in `models/<resource>.py`, mirroring the router structure.
- Separate request and response models when their shapes differ.
- Use `response_model=` on every route decorator.

```python
# ✅
class SolveSubmission(BaseModel):
    event_id: int
    time_ms: int
    dnf: bool = False

class SolveResponse(BaseModel):
    id: int
    event_id: int
    time_ms: int
    dnf: bool
    rank: int

@router.post("/", response_model=SolveResponse)
async def submit_solve(body: SolveSubmission) -> SolveResponse:
    ...

# ❌
@router.post("/")
async def submit_solve(body: dict):
    ...
```

---

## Type Hints

Every function must be fully annotated - parameters and return type - with no exceptions.

```python
# ✅
def compute_average(times: list[int]) -> float | None:
    ...

# ❌
def compute_average(times):
    ...
```

- Use `X | None` (Python 3.10+ union syntax) over `Optional[X]`.
- Use `list[X]` and `dict[K, V]` over `List[X]` / `Dict[K, V]`.
- Never use `Any` from `typing`.

---

## Comments & Documentation

Use docstrings only on complex or non-obvious logic - not on self-evident functions.

```python
# ✅
def trimmed_average(times: list[int]) -> float | None:
    """
    Returns the average of solve times after dropping the best and worst.
    Returns None if fewer than 3 times are provided.
    """
    ...

# ❌
def get_event(event_id: int) -> EventResponse:
    """Gets an event by ID."""
    ...
```

Use inline comments for workarounds or anything non-obvious in behavior.

---

## General

- Keep route handlers thin - delegate to services for anything beyond trivial logic.
- Raise `HTTPException` for expected error cases; let unhandled exceptions bubble to a global handler.
- Do not add database access patterns until a DB layer is introduced; ask first before establishing any persistence conventions.