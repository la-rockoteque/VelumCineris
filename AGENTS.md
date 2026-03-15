# Repository Guidelines

## Project Structure & Module Organization
VelumCineris is a Python-first monorepo. Core domains live at the root (`Book/`, `DNDBeyond/`, `FiveETools/`, `Spreadsheet/`, `WorldAnvil/`, etc.) and generally follow:
- `core/` implementation
- `scripts/` tooling/migrations
- `tests/` pytest coverage
- `DOCS/` workflow notes

Velum Studio app code is in `apps/velum-studio/` (`backend/`, `frontend/`, `desktop/`).  
Frontend tests must live in colocated `__tests__/` folders under `apps/velum-studio/frontend/src`.

## Build, Test, and Development Commands
- `poetry install`: install Python deps.
- `poetry run pytest`: run backend/domain tests.
- `poetry run ruff check .` and `poetry run ruff format .`: lint/format.
- `poetry run pyright`: static type checking.
- `poetry run check-architecture`: import-boundary checks.
- `poetry run uvicorn app.main:app --host 127.0.0.1 --port 8765 --app-dir apps/velum-studio/backend`: run backend.
- `cd apps/velum-studio/frontend && bun run dev`: run frontend.
- `cd apps/velum-studio/frontend && bun run typecheck && bun run test`: TS checks + Vitest.

## Coding Style & Naming Conventions
Use 4-space indentation, double quotes, and 88-char max line length.  
Python: `snake_case` functions/modules, `PascalCase` classes, `UPPER_SNAKE_CASE` constants.

Frontend convention: use Styletron (`styled`) over CSS classes for component styling. Reuse shared primitives before adding one-off styles.

## Frontend Style Architecture (Preferred)
Keep shared UI in small, focused files:
- `shared/library/layout/`: structural blocks (`Card`, `Section`, `Subsection`)
- `shared/library/primitives/`: reusable UI atoms by concern (`Buttons`, `Workspace`, `Feedback`)
- `shared/library/index.ts`: barrel exports only

Avoid reintroducing monolithic files like a single `Layout.tsx` or `primitives.tsx`. When adding shared components, place them in the most specific existing module or create a new focused file.

## Testing Guidelines
Python tests: `test_*.py` with pytest.  
Frontend tests: `*.test.ts(x)` under `__tests__/`.

For behavior changes, run focused tests for touched areas plus relevant type checks.

## Commit & Pull Request Guidelines
Use short, imperative commit messages (for example `fix parser`, `add formatter test`). Keep commits scoped to one change.  
PRs should include purpose, affected paths, test commands run, and screenshots for UI changes.

## Security & Configuration Tips
Never commit secrets. Keep API keys/tokens in local `.env` files and sanitize captured payloads before committing.
