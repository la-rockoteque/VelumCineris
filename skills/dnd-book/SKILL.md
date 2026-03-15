---
name: dnd-book
description: D&D book generation workflow for this repository. Use when editing formatter or writer architecture, Google Docs generation behavior, section composition, or book-output assembly in the Book project.
---

# DND Book

Build and maintain structured book generation pipelines.

## Follow This Workflow

1. Put public orchestration in `Book/cli.py`, `Book/services/`, `Book/datasets/`, `Book/mappers/`, and `Book/exports/`.
2. Change Google Docs and document write internals in `Book/core/Helpers/`.
3. Implement entity presentation in `Book/core/formatters/` and register new types in `Book/mappers/formatter_registry.py`.
4. Implement composition logic in `Book/core/writers/` and keep `Book/exports/writer_registry.py` aligned.
5. Preserve compatibility shims such as `Book/book_api.py`, `Book/google_docs_client.py`, and `Book/styles.py` unless a hard-cut migration is requested.
6. Update generation entrypoints in `Book/scripts/`, `Book/book_generation.ipynb`, and `Book/tests/`.

## Project Anchors

- `Book/cli.py`
- `Book/services/generation_service.py`
- `Book/datasets/`
- `Book/mappers/formatter_registry.py`
- `Book/exports/writer_registry.py`
- `Book/core/Helpers/book_api.py`
- `Book/core/Helpers/google_docs_client.py`
- `Book/core/formatters/`
- `Book/core/writers/`
- `Book/scripts/`
- `Book/book_generation.ipynb`

## Guardrails

- Avoid adding new business logic to compatibility shims when the canonical change belongs in `services`, `mappers`, `exports`, or `core`.
- Keep formatter output deterministic and markdown-safe.
- Keep writer ordering and section contracts explicit.
- Avoid embedding source-specific business rules in generic base formatters.
