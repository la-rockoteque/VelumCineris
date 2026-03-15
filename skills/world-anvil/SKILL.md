---
name: world-anvil
description: World Anvil content sync and mapping workflow for this repository. Use when working on WorldAnvil article create/update logic, payload shape, mapping files, category routing, or notebook-based sync tasks under the WorldAnvil project.
---

# World Anvil

Operate World Anvil integrations for this workspace.

## Follow This Workflow

1. Identify the target article type and source dataset.
2. Inspect mapping files in `WorldAnvil/core/mapping/` and update field mappings first.
3. Update API interaction logic in `WorldAnvil/core/Helpers/WorldAnvilAPI.py` only when payload shape or endpoint behavior changes.
4. Use captured examples in `WorldAnvil/core/requests/` to verify request and response expectations.
5. Keep the compatibility shim at `WorldAnvil/WorldAnvilAPI.py` aligned if the canonical API surface changes.
6. Adjust notebook/script usage in `WorldAnvil/world_anvil_sync.ipynb` after mapping/API changes.
7. Compile changed modules and report migration notes.

## Project Anchors

- `WorldAnvil/WorldAnvilAPI.py`
- `WorldAnvil/core/Helpers/WorldAnvilAPI.py`
- `WorldAnvil/core/mapping/`
- `WorldAnvil/core/requests/`
- `WorldAnvil/world_anvil_sync.ipynb`

## Guardrails

- Prefer mapping updates over hardcoding one-off transforms.
- Preserve backward-compatible identifiers and slugs unless migration is explicit.
- Avoid destructive delete flows unless user requests cleanup.
- Keep request examples synchronized with actual payload changes.
