---
name: dnd-beyond
description: D&D Beyond synchronization and API-form payload workflow for this repository. Use when updating DnDBeyond helpers, sync scripts, request/page captures, or notebook-driven publish/update routines in the DNDBeyond project.
---

# DND Beyond

Maintain the D&D Beyond integration layer and sync tooling.

## Follow This Workflow

1. Put new public orchestration in `DNDBeyond/cli.py`, `DNDBeyond/services/`, `DNDBeyond/datasets/`, `DNDBeyond/mappers/`, and `DNDBeyond/exports/`.
2. Change low-level API/auth/conversion behavior in `DNDBeyond/core/Helpers/` and `DNDBeyond/core/Helpers/entities/`.
3. Use request/page captures in `DNDBeyond/core/requests/` and `DNDBeyond/core/pages/` as ground truth for form fields and endpoints.
4. Update notebook and script flows in `DNDBeyond/dnd_beyond_*.ipynb` and `DNDBeyond/scripts/` after changing payload or sync behavior.
5. Preserve `DNDBeyond/helpers/` as a compatibility facade unless a hard-cut migration is explicitly requested.

## Project Anchors

- `DNDBeyond/cli.py`
- `DNDBeyond/services/`
- `DNDBeyond/datasets/`
- `DNDBeyond/mappers/`
- `DNDBeyond/exports/`
- `DNDBeyond/core/Helpers/`
- `DNDBeyond/core/Helpers/entities/`
- `DNDBeyond/core/requests/`
- `DNDBeyond/core/pages/`
- `DNDBeyond/scripts/`
- `DNDBeyond/dnd_beyond_*.ipynb`

## Guardrails

- Keep offline payload export flow (`datasets` -> `mappers` -> `services` -> `exports`) aligned with live sync helpers.
- Avoid changing endpoint paths without matching request evidence.
- Keep create/update/delete operations explicit and auditable.
- Track sync status fields when writing back spreadsheet state.
