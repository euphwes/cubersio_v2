# CLAUDE.md - Project Conventions

This file defines **project-wide** rules that apply everywhere in the codebase - frontend and backend. Each subdirectory has its own `CLAUDE.md` with language-specific conventions.

---

## Project Structure

```
/
  /backend    # Python + FastAPI
  /frontend   # Svelte + Vite
```

---

## Rules That Apply Everywhere

### Style

In comments and docstrings: don't use em dashes (`—`), en dashes (`–`), or box-drawing characters
(`─`, `═`, `──`, `══`, etc.). Use standard hyphens (`-`) and semicolons (`;`) instead.

This restriction applies only to comments and docstrings. String literals in actual code may
contain any of these characters when they are part of the intended content (e.g. UI placeholder
text, display values).

### New files & utilities

**Do not create new utility files, helper modules, or stores without asking first.**

If you think a helper or shared utility would be useful, say so and describe what it would contain; then wait for approval. This applies even to small, self-contained files.

### Prefer explicit over clever

Clear, readable code over concise but opaque code. If you have to think twice about what a line does, it needs a comment or a refactor.

### No magic numbers

Any non-obvious numeric or string constant must either use a named token/constant or have an inline comment explaining its origin.

### Comments

Don't comment obvious code; names should do that work. Do comment non-obvious logic, workarounds, and anything with a non-trivial side effect. See each subdirectory's `CLAUDE.md` for language-specific documentation style.

### Formatting

After editing any file, run the appropriate formatter before finishing.
`cd` into the relevant project directory first, then run the formatter.

- **Python** (any `.py` file): `cd backend`, then `uv run ruff format <file>`
- **Svelte** (any `.svelte` file): `cd frontend`, then `npx prettier --write <file>`
