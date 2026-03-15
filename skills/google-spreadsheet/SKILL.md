---
name: google-spreadsheet
description: Central Google Spreadsheet data-layer workflow for this repository. Use when modifying shared sheet clients, workbook model generation, converter logic, translator sheets, or Xlsx/Google source switching in the Spreadsheet project.
---

# Google Spreadsheet

Own the shared spreadsheet data layer and model assembly.

## Follow This Workflow

1. Put public spreadsheet workflows in `Spreadsheet/cli.py`, `Spreadsheet/services/`, `Spreadsheet/datasets/`, `Spreadsheet/mappers/`, and `Spreadsheet/exports/`.
2. Make shared client and source changes in `Spreadsheet/core/Helpers/sheets.py` and `Spreadsheet/core/Helpers/sources.py`.
3. Update domain row transforms in `Spreadsheet/core/converters/`.
4. Update dynamic model loading in `Spreadsheet/core/workbook_models/` when tabs, columns, or validation sheets change.
5. Adjust translator tab integrations in `Spreadsheet/core/translator/` if language tabs change.
6. Keep compatibility shims at `Spreadsheet/sheets.py`, `Spreadsheet/sources.py`, and `Spreadsheet/core/lazy_exports.py` aligned unless a full migration is requested.
7. Validate both Google and xlsx paths for regressions.

## Project Anchors

- `Spreadsheet/cli.py`
- `Spreadsheet/services/spreadsheet_service.py`
- `Spreadsheet/datasets/`
- `Spreadsheet/mappers/`
- `Spreadsheet/exports/`
- `Spreadsheet/core/Helpers/sheets.py`
- `Spreadsheet/core/Helpers/sources.py`
- `Spreadsheet/core/converters/`
- `Spreadsheet/core/workbook_models/`
- `Spreadsheet/core/translator/`
- `Spreadsheet/Orimond.xlsx`

## Guardrails

- Prefer dataset/service entrypoints for new orchestration and keep low-level client logic centralized in `core/Helpers`.
- Treat validation tabs as enum/constant sources for downstream model validation.
- Prefer named sheet access over raw gid usage.
- Keep data-layer logic centralized and avoid client duplication.
