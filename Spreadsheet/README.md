# Vestigium

## Shared Sheets Client

Canonical Google Sheets access now lives in `Spreadsheet/sheets.py`.

- `ContentSheetsClient` and `SpreadsheetClient` for Orimond/modern content data.
- `TranslatorSheetsClient` and `OfflineTranslatorSheetsClient` for translator tabs.
- Legacy modules `FiveETools/gsheets_client.py` and `Spreadsheet/core/translator/gsheets_client.py`
  were removed after migration to `Spreadsheet/sheets.py`.

## Workbook Models

`Spreadsheet/core/workbook_models` provides dynamic Pydantic models for every sheet in Orimond.

- Default source is Google Sheets (`source=\"google\"` or `\"auto\"`).
- Local `Spreadsheet/Orimond.xlsx` is supported as offline fallback/bootstrap.
- Validation sheets (`Validation`, `Validations`, common misspellings) are parsed into reusable enum-like constants and applied as field validators.
- Cross-sheet virtual relations are attached (for example `Classes -> subclasses`).

Quick check:

```bash
./.venv/bin/python -m Spreadsheet.core.workbook_models --source auto
```

## Normalized CLI

```bash
# List named modern sheets (no network call)
poetry run python -m Spreadsheet.cli list-sheets --content-type modern

# Build workbook summary report from local XLSX
poetry run python -m Spreadsheet.cli workbook-summary --source xlsx --out /tmp/workbook_summary.json
```

## Architecture

```
Spreadsheet/
├── cli.py                         # Normalized CLI entrypoint
├── datasets/                      # Content/workbook dataset adapters
├── mappers/                       # DataFrame/record mapping helpers
├── services/                      # Sheet/workbook orchestration service
├── exports/                       # JSON report writers
├── sheets.py                      # Canonical shared sheets clients
├── core/workbook_models/          # Canonical workbook model internals
├── core/converters/               # Canonical sheet converters
└── tests/
```
