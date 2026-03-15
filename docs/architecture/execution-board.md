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
Status: `completed`

### C1. Converters and DTO boundaries
- [x] Keep `models` domain-only.
- [x] Keep sheet converters in `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/converters`.
- [x] Move app-specific DTO shaping out of dataset scripts into app mappers.
  - Extracted species/deities/languages/diseases/magic_items/conditions/feats/backgrounds/items/features/subclasses/classes/spells/monster DTO mappers to `/Users/rocko/dev/Perso/VelumCineris/FiveETools/mappers`.

### C2. Remove compatibility shims
- [x] Delete shim paths listed in migration map after zero refs.
  - Removed `/Users/rocko/dev/Perso/VelumCineris/FiveETools/gsheets_client.py`.
  - Removed `/Users/rocko/dev/Perso/VelumCineris/Spreadsheet/core/translator/gsheets_client.py`.
  - Removed `/Users/rocko/dev/Perso/VelumCineris/models/converters/*`.

## Phase D: Project structure normalization
Status: `completed`

### D1. Per-project folder normalization
- [x] Ensure each app follows: `datasets`, `mappers`, `services`, `exports`, `tests`.
  - Completed: `FiveETools`, `Book`, `DNDBeyond`, `Homebrewery`, and `Spreadsheet` expose normalized adapter folders over canonical internals.
- [x] Add minimal entrypoints/CLI modules per app.
  - Completed: `python -m FiveETools.cli export`, `python -m Book.cli preview|generate`, `python -m DNDBeyond.cli export-payloads`, `python -m Homebrewery.cli export-markdown`, and `python -m Spreadsheet.cli list-sheets|sheet-preview|workbook-summary`.

### D2. Shared quality gates
- [x] Root-level lint/type/test matrix.
  - File: `/Users/rocko/dev/Perso/VelumCineris/.github/workflows/python-quality-matrix.yml`
  - Runner: `/Users/rocko/dev/Perso/VelumCineris/scripts/run_quality_matrix.py` (`--stage lint|type|test|all`)
- [x] Strict import-boundary check in CI workflow.
  - File: `/Users/rocko/dev/Perso/VelumCineris/.github/workflows/architecture-guardrails.yml`
- [x] Notebook legacy-import guardrail in architecture scan.
  - File: `/Users/rocko/dev/Perso/VelumCineris/scripts/check_import_boundaries.py`
  - Blocks `.ipynb` code-cell imports of `src.sources` and `FiveETools.core.Helpers.gsheets_client`.
- [x] Import-time sheet-read guardrail auto-discovers data modules.
  - File: `/Users/rocko/dev/Perso/VelumCineris/FiveETools/tests/test_architecture_guardrails.py`
  - Covers all `FiveETools/core/fantasy/*.py`, `FiveETools/core/modern/*.py`, and `models/datasets/*.py` modules.
- [x] Static AST guardrail for module top-level sheet reads.
  - File: `/Users/rocko/dev/Perso/VelumCineris/scripts/check_import_boundaries.py`
  - Blocks top-level `get_sheet*` calls in `FiveETools/core/fantasy`, `FiveETools/core/modern`, and `models/datasets`.
- [x] Scanner regression tests wired into quality matrix.
  - Tests: `/Users/rocko/dev/Perso/VelumCineris/scripts/tests/test_check_import_boundaries.py`
  - Runner: `/Users/rocko/dev/Perso/VelumCineris/scripts/run_quality_matrix.py`

## Baseline progress notes
- Sheets client consolidation is functionally complete.
- Workbook model loader continues to work with the consolidated data provider.
- Import-boundary scanner is active and provides measurable migration progress.
- Legacy `.py` and notebook imports of `FiveETools.core.Helpers.gsheets_client` were migrated to `Spreadsheet.sheets`.
- Removed `/Users/rocko/dev/Perso/VelumCineris/FiveETools/core/Helpers/gsheets_client.py` after zero remaining references.
- Remaining work is primarily deep migration cleanup in legacy helper internals.
