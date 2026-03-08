---
name: dnd-beyond
description: D&D Beyond synchronization and API-form payload workflow for this repository. Use when updating DnDBeyond helpers, sync scripts, request/page captures, or notebook-driven publish/update routines in the DNDBeyond project.
---

# DND Beyond

Maintain the D&D Beyond integration layer and sync tooling.

## Follow This Workflow

1. Implement API and payload behavior in `DNDBeyond/core/Helpers/`.
2. Use request/page captures in `DNDBeyond/core/requests/` and `DNDBeyond/core/pages/` as ground truth for form fields and endpoints.
3. Update orchestration scripts in `DNDBeyond/scripts/` for sync flows and diagnostics.
4. Keep notebook imports aligned with canonical helper paths.
5. Preserve legacy import shims in `DNDBeyond/helpers/` unless hard-cut migration is requested.

## Project Anchors

- `DNDBeyond/core/Helpers/`
- `DNDBeyond/core/requests/`
- `DNDBeyond/core/pages/`
- `DNDBeyond/scripts/`
- `DNDBeyond/dnd_beyond_*.ipynb`

## Guardrails

- Avoid changing endpoint paths without matching request evidence.
- Keep create/update/delete operations explicit and auditable.
- Track sync status fields when writing back spreadsheet state.
