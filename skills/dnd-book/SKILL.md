---
name: dnd-book
description: D&D book generation workflow for this repository. Use when editing formatter or writer architecture, Google Docs generation behavior, section composition, or book-output assembly in the Book project.
---

# DND Book

Build and maintain structured book generation pipelines.

## Follow This Workflow

1. Keep orchestration logic in `Book/core/Helpers/`.
2. Implement entity presentation in `Book/core/formatters/`.
3. Implement composition logic in `Book/core/writers/`.
4. Update generation entrypoints in `Book/scripts/` and tests in `Book/tests/`.
5. Ensure imported entity modules align with current FiveETools core paths.

## Project Anchors

- `Book/core/Helpers/book_api.py`
- `Book/core/Helpers/google_docs_client.py`
- `Book/core/formatters/`
- `Book/core/writers/`
- `Book/book_generation.ipynb`

## Guardrails

- Keep formatter output deterministic and markdown-safe.
- Keep writer ordering and section contracts explicit.
- Avoid embedding source-specific business rules in generic base formatters.
