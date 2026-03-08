---
name: dnd-5e
description: General D&D 5e rules-aware content engineering guidance. Use when designing, converting, validating, or reviewing 5e entities such as spells, monsters, species, classes, subclasses, feats, conditions, and items.
---

# DND 5e

Apply 5e-consistent structure and terminology across content work.

## Use This Checklist

1. Validate entity schema: required fields, naming consistency, and source metadata.
2. Validate rules semantics: action economy, save/attack typing, duration/range units, scaling behavior.
3. Validate text quality: concise rules text, no contradictory clauses, clear trigger/effect timing.
4. Validate downstream compatibility: identifiers, tags, and machine-readable fields for toolchains.

## High-Value Review Focus

- Missing or contradictory mechanics
- Ambiguous timing words and undefined references
- Inconsistent scaling or progression tables
- Invalid dice notation or malformed stat blocks

## Guardrails

- Prefer explicit mechanical language over flavor-only descriptions.
- Separate flavor, rules text, and metadata fields cleanly.
- Flag assumptions when source text is incomplete.
