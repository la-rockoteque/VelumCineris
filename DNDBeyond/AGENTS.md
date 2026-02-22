# Repository Guidelines

## Project Structure & Module Organization
- `helpers/` contains core Python modules (API client and converters).
- `tests/` holds pytest-based unit tests mirroring helper modules.
- `requests/` includes saved HTTP request/response examples and headers.
- `DOCS/` captures design notes and integration write-ups.
- `dnd_beyond_sync.ipynb` is a Jupyter notebook for interactive workflows.

## Build, Test, and Development Commands
- `poetry install` sets up the virtual environment and dependencies.
- `poetry run pytest` runs the unit test suite.
- `poetry run ruff check .` runs lint checks.
- `poetry run ruff format .` applies formatting.
- `poetry run pyright` performs static type checks.
- `poetry run jupyter lab` opens the notebook environment.
- `poetry run download-wordnet` installs NLTK WordNet data for NLP tasks.

## Coding Style & Naming Conventions
- Indentation: 4 spaces; line length target is 88 characters.
- Strings use double quotes (per Ruff formatter).
- Use `snake_case` for functions/variables, `PascalCase` for classes.
- Keep module names lowercase and descriptive (e.g., `converter.py`).

## Testing Guidelines
- Framework: `pytest` (see `tests/`).
- Test files use `test_*.py`; test functions use `test_*`.
- Prefer focused unit tests with mocked I/O and network calls.

## Commit & Pull Request Guidelines
- Commit messages in history are short, imperative summaries (e.g., "Fixed json").
- Keep commits scoped and describe intent, not implementation details.
- PRs should include a short summary, testing results, and links to related issues.
- Include screenshots or request/response samples when changing API behavior.

## Security & Configuration Tips
- Store secrets in `.env`; never commit credentials or tokens.
- When adding new request samples, remove auth headers and user identifiers.
