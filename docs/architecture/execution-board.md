# Consolidation Execution Board

## Phase A: Foundation (in progress)
Status: `completed`

### A1. Architecture contract docs
- [x] Add target architecture doc.
  - File: `/Users/rocko/dev/Perso/VelumCineris/docs/architecture/target-architecture.md`
- [x] Add migration map doc.
  - File: `/Users/rocko/dev/Perso/VelumCineris/docs/architecture/migration-map.md`

### A2. Single sheets client concept
- [x] Canonical implementation in `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`.
- [x] Convert legacy clients to wrappers.
  - Files: `/Users/rocko/dev/Perso/VelumCineris/FiveETools/gsheets_client.py`, `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/translator/gsheets_client.py`
- [x] Repoint workbook provider to shared client.
  - File: `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/workbook_models/providers.py`

### A3. Add enforcement baseline
- [x] Add import boundary scanner.
  - File: `/Users/rocko/dev/Perso/VelumCineris/scripts/check_import_boundaries.py`
- [x] Add root command/script for scanner.
  - File: `/Users/rocko/dev/Perso/VelumCineris/pyproject.toml` (`check-architecture`)
- [x] Run scanner in report mode and capture baseline violations.
  - Baseline: `11` violations.
  - Primary hotspot: `/Users/rocko/dev/Perso/VelumCineris/models/datasets/*` imports from `FiveETools.*`.
  - Current count after remediation: `0` violations (`--strict` green).

## Phase B: Data access hardening
Status: `in_progress`

### B1. Remove direct Google CSV reads
- [x] Replace all direct `pd.read_csv("https://docs.google.com/spreadsheets/...export?format=csv")` occurrences (active `.py` code).
- [x] Replace private `_build_csv_url` usage where possible with public API.
  - Remaining `_build_csv_url` is a compatibility alias in `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`.

### B2. Central sheet metadata
- [x] Consolidate repeated GID literals into shared registry objects.
  - Expanded `fantasy`/`modern` sheet registries in `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/sheets.py`.
- [x] Migrate call sites to `get_sheet_by_name()` where feasible.
  - Active call sites now use names instead of raw GIDs for shared content sheets.

## Phase C: Domain and mapping cleanup
Status: `pending`

### C1. Converters and DTO boundaries
- [ ] Keep `models` domain-only.
- [ ] Keep sheet converters in `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/converters`.
- [ ] Move app-specific DTO shaping out of dataset scripts into app mappers.

### C2. Remove compatibility shims
- [ ] Delete shim paths listed in migration map after zero refs.

## Phase D: Project structure normalization
Status: `pending`

### D1. Per-project folder normalization
- [ ] Ensure each app follows: `datasets`, `mappers`, `services`, `exports`, `tests`.
- [ ] Add minimal entrypoints/CLI modules per app.

### D2. Shared quality gates
- [ ] Root-level lint/type/test matrix.
- [ ] Strict import-boundary check in CI workflow.

## Baseline progress notes
- Sheets client consolidation is functionally complete.
- Workbook model loader continues to work with the consolidated data provider.
- Import-boundary scanner is active and provides measurable migration progress.
- Remaining work is mostly migration and project-structure normalization.
