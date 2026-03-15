---
name: fiveetools
description: 5etools export workflow for fantasy and modern datasets in this repository. Use when updating entity conversion modules, source filtering, json assembly, or sheet-to-5etools pipelines in the FiveETools project.
---

# 5etools

Maintain 5etools-compatible exporters for both settings.

## Follow This Workflow

1. Start with the public export flow in `FiveETools/cli.py`, `FiveETools/services/`, `FiveETools/datasets/`, `FiveETools/mappers/`, and `FiveETools/exports/`.
2. Change source-specific transform logic in `FiveETools/core/fantasy/` or `FiveETools/core/modern/`.
3. Keep sheet access centralized through `Spreadsheet.datasets`, `Spreadsheet.services`, and the shared sheets/workbook model layer rather than duplicating clients.
4. Use `Spreadsheet/core/converters/` and `Spreadsheet/core/workbook_models/` for shared row and schema primitives.
5. Validate generated output structure against expected 5etools schema and output naming.

## Project Anchors

- `FiveETools/cli.py`
- `FiveETools/services/export_service.py`
- `FiveETools/datasets/`
- `FiveETools/mappers/`
- `FiveETools/exports/compendium.py`
- `FiveETools/core/fantasy/`
- `FiveETools/core/modern/`
- `Spreadsheet/datasets/`
- `Spreadsheet/services/`
- `Spreadsheet/core/workbook_models/`
- `Spreadsheet/core/converters/`
- `FiveETools/out/`

## Guardrails

- Keep fantasy and modern source routing explicit.
- Avoid duplicating spreadsheet client or dataset-selection logic.
- Preserve stable keys and ids in exported json structures.
