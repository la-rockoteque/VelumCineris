# Consolidation Migration Map

## Current Canonical Paths
- Shared sheets access: `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`
- Shared domain models: `/Users/rocko/dev/Perso/VelumCineris/models`
- Sheet ingestion converters: `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/converters`
- Workbook model registry/providers: `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/workbook_models`

## Compatibility Shims (Keep Temporarily)
- `/Users/rocko/dev/Perso/VelumCineris/FiveETools/gsheets_client.py`
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/translator/gsheets_client.py`
- `/Users/rocko/dev/Perso/VelumCineris/models/converters/*`
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/models/converters/*`

## Still To Migrate
- Remove all direct CSV-export URL consumers in app code.
- Replace ad-hoc source sheet access with `ContentSheetsClient` sheet-name registry usage.
- Normalize app internals into common layout pattern (`datasets`, `mappers`, `services`, `exports`, `tests`).
- Remove shim layers once imports are fully migrated.

## Deletion Order (when no references remain)
1. `models/converters/*` shims
2. `Spreadsheet/models/converters/*` shims
3. `FiveETools/gsheets_client.py` wrapper (callers import `Spreadsheet.sheets` directly)
4. `Spreadsheet/core/translator/gsheets_client.py` wrapper

## Risk Hotspots
- Scripts run from subdirectories with implicit Python paths.
- Notebook-driven workflows with frozen imports.
- Modules using `_build_csv_url` or private APIs.

## Verification Checklist
- `python -m compileall -q` on touched packages.
- Run `/Users/rocko/dev/Perso/VelumCineris/scripts/check_import_boundaries.py --strict`.
- Smoke test workbook loader against XLSX fallback.
- Smoke test representative project pipelines (FiveETools, DNDBeyond, translator).
