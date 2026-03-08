# Velum Studio Architecture

## Goals

1. Replace notebook-only workflow with a user-friendly app shell.
2. Keep all spreadsheet model logic centralized in `Spreadsheet/core/workbook_models`.
3. Route all UI data access through one backend API surface.
4. Drive external platforms (WorldAnvil, D&D Beyond, etc.) as per-item actions from selected content rows.

## Layers

- `backend/app/services/spreadsheet_service.py`
  - Owns source selection and registry caching.
  - Calls `load_orimond_registry(...)` from central workbook models.
- `backend/app/main.py`
  - Exposes API endpoints for compendium, row details, formatter, intelligence, translator, image planning, and integration actions.
  - Serves frontend static app.
- `backend/app/services/settings_service.py`
  - Persists user preferences to `~/.velum` (or `VELUM_SETTINGS_PATH`).
  - Stores default source, compendium display behavior, and per-sheet column visibility.
- `frontend/`
  - React + TypeScript + Vite app split by vertical slices (`features/*`).
  - Tabbed UI: Compendium, Validations, Details Editor, Formatters, Intelligence, Translator, Image Generator, Money, Timeline, Settings.
  - Shared UI and helpers in `components/` and `shared/`.
- `desktop/`
  - Electron shell split by responsibility modules:
    - `desktop/src/config.js`
    - `desktop/src/processes.js`
    - `desktop/src/window.js`
    - `desktop/src/main.js`
  - Boots backend + frontend dev server and loads the React app.

## API (current)

- `GET /health`
- `GET /api/spreadsheet/sources`
- `GET /api/spreadsheet/sheets`
- `GET /api/compendium/sheets`
- `GET /api/validations/sheets`
- `GET /api/validations/catalog`
- `GET /api/spreadsheet/schema`
- `GET /api/spreadsheet/rows`
- `GET /api/spreadsheet/row`
- `GET /api/settings`
- `PUT /api/settings`
- `PUT /api/settings/columns`
- `DELETE /api/settings/columns`
- `GET /api/integrations`
- `GET /api/integrations/{integration_key}/status`
- `POST /api/integrations/{integration_key}/preview`
- `POST /api/integrations/{integration_key}/sync`
- `POST /api/items/{integration_key}/action`
- `POST /api/book-formatter/preview`
- `POST /api/intelligence/suggest`
- `GET /api/translator/targets`
- `POST /api/translator/translate`
- `POST /api/image-generator/generate`

## Extension plan

- Add live item action adapters for non-WorldAnvil integrations (D&D Beyond, Homebrewery, etc.).
- Keep write operations behind explicit dry-run/live mode controls.
- Add authentication profiles for external services.
