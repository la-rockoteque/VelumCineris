# Repository Guidelines

## Project Structure & Module Organization
VelumCineris is a Python-first monorepo with domain modules at the top level: `Book/`, `DNDBeyond/`, `FiveETools/`, `Homebrewery/`, `Spreadsheet/`, `WorldAnvil/`, `ObsidianPortal/`, and `Kenji/`. Most modules follow a shared layout:
- `core/` for implementation code and helpers
- `scripts/` for maintenance/migration utilities
- `tests/` for pytest suites
- `DOCS/` for workflow and integration notes

Desktop app code lives in `apps/velum-studio/` (`backend/`, `frontend/`, `desktop/`). Shared automation and checks live in root `scripts/`.

## Build, Test, and Development Commands
- `poetry install`: install root dependencies (Python 3.12).
- `poetry run pytest`: run Python tests from repo root.
- `poetry run ruff check .`: lint code.
- `poetry run ruff format .`: format code (88-char line length).
- `poetry run pyright`: static type checks.
- `poetry run check-architecture`: enforce import-boundary rules.
- `poetry run jupyter notebook`: open notebook workflows used by content pipelines.
- `poetry run playwright install chromium`: required before D&D Beyond token automation.

Velum Studio:
- `poetry run uvicorn app.main:app --host 127.0.0.1 --port 8765 --app-dir apps/velum-studio/backend`
- `cd apps/velum-studio/frontend && npm install && npm run dev`

## Coding Style & Naming Conventions
Use 4-space indentation, double quotes, and max line length 88 (Ruff config in each module). Follow Python naming standards: `snake_case` for functions/variables/modules, `PascalCase` for classes, `UPPER_SNAKE_CASE` for constants. Keep modules focused by feature/entity (`spells.py`, `species.py`, `converter.py`).

Prefer canonical domain names in new code (`deities`, `deity`, `scriptures`). Legacy spellings (`dieties`, `diety`, `sciptures`) still appear in historical files/sheets and should be handled via compatibility aliases, not breaking renames.

## Testing Guidelines
Use `pytest` with files named `test_*.py` and functions/classes named `test_*`/`Test*`. Add tests in the nearest module `tests/` directory (or `apps/velum-studio/backend/tests` for backend API logic). Cover converter edge cases, schema/typing behavior, and regressions when changing sync pipelines.

For every behavioral change, run at least: `poetry run pytest`, plus focused tests for touched areas (for example `poetry run pytest apps/velum-studio/backend/tests -q`).

## Commit & Pull Request Guidelines
Current history favors short, imperative summaries (for example: `fix json`, `update urls`, `add fantasy sources`). Keep commits scoped to one logical change. PRs should include:
- what changed and why
- affected modules/directories
- commands run (`pytest`, `ruff`, `pyright`)
- screenshots for UI updates and sanitized request samples for API/sync changes

## Security & Configuration Tips
Never commit secrets. Keep credentials in local `.env` files (for example D&D Beyond tokens, World Anvil cookies) and keep service keys such as Google Sheets credentials out of git. Sanitize exported request/response artifacts before committing.
