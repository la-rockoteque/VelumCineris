---
name: obsidian-portal
description: Obsidian Portal extraction and transformation workflow for this repository. Use when converting Obsidian Portal exports, cleaning extracted files, mapping entries toward WorldAnvil, or maintaining ObsidianPortal project automation.
---

# Obsidian Portal

Handle Obsidian Portal export ingestion and transformation tasks.

## Follow This Workflow

1. Start from the export source in `ObsidianPortal/extracted/`.
2. Confirm the intended output schema and destination (usually WorldAnvil sync inputs).
3. Normalize structure and metadata in notebook/script transforms.
4. Update compatibility assumptions in `ObsidianPortal/ObsidiantoWorldAnvil.ipynb` when source format changes.
5. Keep transformed outputs reproducible and deterministic.

## Project Anchors

- `ObsidianPortal/ObsidiantoWorldAnvil.ipynb`
- `ObsidianPortal/extracted/`
- `WorldAnvil/core/mapping/` for downstream field alignment

## Guardrails

- Preserve original export artifacts; write derived data to generated folders.
- Keep parser logic tolerant of missing fields and legacy entries.
- Document any schema assumptions when adding new transforms.
