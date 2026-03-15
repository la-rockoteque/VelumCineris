# Velum Studio

Desktop-style app workflow for VelumCineris.

- Backend: FastAPI (`apps/velum-studio/backend`)
- Frontend: React + TypeScript + Vite + TanStack Query (`apps/velum-studio/frontend`)
- Desktop shell: Electron (`apps/velum-studio/desktop`)

## Features

- Tabbed workspace:
  - `Compendium` (spreadsheet explorer)
  - `Validations` (validation sheets only)
  - `Details Editor` (opens when selecting a row, includes per-item actions)
  - `Book Formatter` (Homebrewery + Google Docs dry-run output)
  - `Intelligence` (local LLM or heuristic balancing assistant)
  - `Translator` (translation + romanized/script output + audio pronunciation)
  - `Image Generator` (ChatGPT prompt planning for entity art)
  - `Settings` (persisted in `~/.velum`)
- Per-item integration actions for: WorldAnvil, D&D Beyond, Homebrewery, 5eTools, Obsidian Portal
- Spreadsheet defaults:
  - minimal columns visible by default
  - right-click a header to show/hide columns
  - cell text truncated with ellipsis (default 150 chars, configurable)
  - details editor fields use validation-backed dropdowns/multiselects when available
- Parent-child detail sections:
  - `Species` includes `SpeciesAppearance`
  - `Dieties`/`Deities` includes `Cults` and `Scriptures` (legacy sheet alias: `Sciptures`)

## Run backend only

From repo root:

```bash
poetry run uvicorn app.main:app --host 127.0.0.1 --port 8765 --app-dir apps/velum-studio/backend
```

Open:

- <http://127.0.0.1:5173/app/>
- Health: <http://127.0.0.1:8765/health>

## Run frontend only

From `apps/velum-studio/frontend`:

```bash
bun install
bun run dev
```

Build static frontend bundle (served by backend at `/app/` when `dist/` exists):

```bash
bun run build
```

## Run Electron desktop

From `apps/velum-studio/desktop`:

```bash
bun install
bun run dev
```

Electron starts FastAPI and Vite automatically, then opens the React app.

## Frontend structure (vertical slices)

- `src/app/`: app shell state/hooks
- `src/components/`: shared UI components (loading/toasts/multiselect)
- `src/features/compendium/`: spreadsheet explorer
- `src/features/validations/`: validation sheet explorer
- `src/features/details/`: contextual details editor + field components
- `src/features/formatter/`: Homebrewery/Docs/5eTools formatter workflows
- `src/features/intelligence/`: LLM suggestions
- `src/features/translator/`: translation + romanized/symbolized outputs
- `src/features/image/`: image prompt planning
- `src/features/money/`: money matrix conversion
- `src/features/timeline/`: timeline editor + present calendar view
- `src/features/settings/`: persisted user preferences

## Backend endpoints

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

## Environment variables

- `VELUM_HOST` (default: `127.0.0.1`)
- `VELUM_PORT` (default: `8765`)
- `VELUM_SPREADSHEET_ID` (default: Orimond ID)
- `VELUM_XLSX_PATH` (default: `<repo>/Spreadsheet/Orimond.xlsx`)
- `VELUM_GSHEETS_KEY_PATH` (default: `<repo>/Spreadsheet/key.json`)
- `VELUM_SETTINGS_PATH` (default: `~/.velum`)
- `WA_COOKIES` (required for live WorldAnvil item actions)
- `WA_WORLD_ID` (required for live WorldAnvil item actions)
- `WA_WORLD_SLUG` (required for live WorldAnvil item actions)
- `WA_CATEGORY_MAP_JSON` (optional JSON object mapping sheet name -> WorldAnvil category UUID)
- `WA_CATEGORY_ID` (optional fallback category UUID for unmapped sheets)

## Notes

- `auto` source prioritizes XLSX for fast startup and local resilience; choose `google` explicitly when needed.
- The data layer stays centralized in `Spreadsheet/core/workbook_models`.
- In Details Editor, `Item Action Mode = Live Execute` currently executes real requests for `WorldAnvil` only; others are dry-run/unsupported in live mode.
