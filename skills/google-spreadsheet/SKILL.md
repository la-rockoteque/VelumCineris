---
name: google-spreadsheet
description: Central Google Spreadsheet data-layer workflow for this repository. Use when modifying shared sheet clients, workbook model generation, converter logic, translator sheets, or Xlsx/Google source switching in the Spreadsheet project.
---

# Google Spreadsheet

Own the shared spreadsheet data layer and model assembly.

## Follow This Workflow

1. Make client and sheet-registry changes in `Spreadsheet/core/Helpers/sheets.py` first.
2. Update domain row transforms in `Spreadsheet/core/converters/`.
3. Update dynamic model loading in `Spreadsheet/core/workbook_models/` when tabs/columns change.
4. Adjust translator tab integrations in `Spreadsheet/core/translator/` if language tabs change.
5. Keep compatibility shims at `Spreadsheet/sheets.py` and `Spreadsheet/sources.py` intact unless full migration is requested.
6. Validate both Google and xlsx paths for regressions.

## Project Anchors

- `Spreadsheet/core/Helpers/sheets.py`
- `Spreadsheet/core/converters/`
- `Spreadsheet/core/workbook_models/`
- `Spreadsheet/core/translator/`
- `Spreadsheet/Orimond.xlsx`

## Guardrails

- Treat validation tabs as enum/constant sources for downstream model validation.
- Prefer named sheet access over raw gid usage.
- Keep data-layer logic centralized and avoid client duplication.
