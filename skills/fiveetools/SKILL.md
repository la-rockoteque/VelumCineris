---
name: fiveetools
description: 5etools export workflow for fantasy and modern datasets in this repository. Use when updating entity conversion modules, source filtering, json assembly, or sheet-to-5etools pipelines in the FiveETools project.
---

# 5etools

Maintain 5etools-compatible exporters for both settings.

## Follow This Workflow

1. Implement dataset transforms in `FiveETools/core/fantasy/` or `FiveETools/core/modern/`.
2. Keep sheet access centralized through `FiveETools/core/Helpers/gsheets_client.py`.
3. Use `Spreadsheet/core/converters/` for shared row conversion primitives.
4. Validate generated output structure against expected 5etools schema.

## Project Anchors

- `FiveETools/core/fantasy/`
- `FiveETools/core/modern/`
- `FiveETools/core/Helpers/gsheets_client.py`
- `FiveETools/out/`

## Guardrails

- Keep fantasy and modern source routing explicit.
- Avoid duplicating spreadsheet client logic.
- Preserve stable keys and ids in exported json structures.
