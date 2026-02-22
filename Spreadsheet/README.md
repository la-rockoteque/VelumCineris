# Vestigium

## Shared Sheets Client

Canonical Google Sheets access now lives in `Spreadsheet/sheets.py`.

- `ContentSheetsClient` and `SpreadsheetClient` for Orimond/modern content data.
- `TranslatorSheetsClient` and `OfflineTranslatorSheetsClient` for translator tabs.
- Legacy modules `FiveETools/gsheets_client.py` and `Spreadsheet/translator/gsheets_client.py`
  are compatibility wrappers and should not hold logic.

## Workbook Models

`Spreadsheet/workbook_models` provides dynamic Pydantic models for every sheet in Orimond.

- Default source is Google Sheets (`source=\"google\"` or `\"auto\"`).
- Local `Spreadsheet/Orimond.xlsx` is supported as offline fallback/bootstrap.
- Validation sheets (`Validation`, `Validations`, common misspellings) are parsed into reusable enum-like constants and applied as field validators.
- Cross-sheet virtual relations are attached (for example `Classes -> subclasses`).

Quick check:

```bash
./.venv/bin/python -m Spreadsheet.workbook_models --source auto
```
