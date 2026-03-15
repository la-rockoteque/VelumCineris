# Consolidation Migration Map

## Current Canonical Paths
- Shared sheets public facade: `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`
- Shared sheets implementation: `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/Helpers/sheets.py`
- Shared domain models: `/Users/rocko/dev/Perso/VelumCineris/models`
- Sheet ingestion converters: `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/converters`
- Workbook model registry/providers: `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/workbook_models`
- Public cross-app content loaders: `/Users/rocko/dev/Perso/VelumCineris/FiveETools/datasets`

## Compatibility Shims (Keep Temporarily)
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sources.py`
- `/Users/rocko/dev/Perso/VelumCineris/Book/book_api.py`
- `/Users/rocko/dev/Perso/VelumCineris/Book/google_docs_client.py`
- `/Users/rocko/dev/Perso/VelumCineris/Book/styles.py`
- `/Users/rocko/dev/Perso/VelumCineris/DNDBeyond/helpers/*`
- `/Users/rocko/dev/Perso/VelumCineris/WorldAnvil/WorldAnvilAPI.py`
- `/Users/rocko/dev/Perso/VelumCineris/Homebrewery/*.py` helper facades

## Removed Shims
- `/Users/rocko/dev/Perso/VelumCineris/FiveETools/gsheets_client.py` (callers migrated to `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`)
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/translator/gsheets_client.py` (callers migrated to `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`)
- `/Users/rocko/dev/Perso/VelumCineris/models/converters/*` (callers migrated to `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/converters/*`)
- `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/models/converters/*` (directory removed/absent)

## Still To Migrate
- Keep removing adapter imports of sibling app internals and route them through explicit public surfaces.
- Retire compatibility facades after zero import references remain.
- Expand normalized adapters from baseline folder/CLI surfaces into deeper internals (legacy helpers/scripts/notebooks).
  - Baseline complete: `FiveETools`, `Book`, `DNDBeyond`, `Homebrewery`, and `Spreadsheet` expose `datasets/mappers/services/exports/tests` and CLI entrypoints.
  - Progress: active `.py` modules and notebooks now use `Spreadsheet.sheets` directly for shared sheet access, and adapter-facing entity loading is being centralized in `FiveETools.datasets`.

## Deletion Order (when no references remain)
1. Replace adapter imports of sibling app internals with public dataset or facade APIs.
2. Remove same-app shim imports from normalized service and dataset layers.
3. Delete compatibility facades after references reach zero.

## Risk Hotspots
- Scripts run from subdirectories with implicit Python paths.
- Notebook-driven workflows with frozen imports.
- Modules using `_build_csv_url` or private APIs.
- Cross-app imports that target sibling `core.*` instead of a public adapter surface.

## Verification Checklist
- `python -m compileall -q` on touched packages.
- Run `/Users/rocko/dev/Perso/VelumCineris/scripts/check_import_boundaries.py --strict`.
- Run `/Users/rocko/dev/Perso/VelumCineris/scripts/run_quality_matrix.py --stage all`.
- Smoke test workbook loader against XLSX fallback.
- Smoke test representative project pipelines (FiveETools, DNDBeyond, translator).
