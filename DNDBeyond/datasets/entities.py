from __future__ import annotations

from typing import Any

from FiveETools.datasets import (
    load_entities as load_fivetools_entities,
    normalize_setting as normalize_fivetools_setting,
    resolve_source_code as resolve_fivetools_source_code,
)

SUPPORTED_SETTINGS: tuple[str, ...] = ("fantasy", "modern")
SUPPORTED_ENTITY_TYPES: tuple[str, ...] = ("spell", "monster", "species", "background", "feat")


def normalize_setting(setting: str) -> str:
    normalized = normalize_fivetools_setting(setting)
    if normalized not in SUPPORTED_SETTINGS:
        raise ValueError(f"Unknown setting '{setting}'. Expected one of: {sorted(SUPPORTED_SETTINGS)}")
    return normalized


def normalize_entity_type(entity_type: str) -> str:
    normalized = str(entity_type).strip().lower()
    if normalized not in SUPPORTED_ENTITY_TYPES:
        raise ValueError(
            f"Unknown entity type '{entity_type}'. Expected one of: {sorted(SUPPORTED_ENTITY_TYPES)}"
        )
    return normalized


def resolve_source_code(setting: str, source_code: str | None = None) -> str:
    normalized_setting = normalize_setting(setting)
    return resolve_fivetools_source_code(setting=normalized_setting, source_code=source_code)


def load_entities(
    *,
    entity_type: str,
    setting: str,
    source_code: str | None = None,
) -> list[dict[str, Any]]:
    normalized_entity_type = normalize_entity_type(entity_type)
    normalized_setting = normalize_setting(setting)
    if normalized_entity_type in {"background", "feat"} and normalized_setting != "modern":
        raise ValueError(
            f"Entity type '{normalized_entity_type}' is not supported for setting '{normalized_setting}'."
        )
    resolved_source_code = resolve_source_code(normalized_setting, source_code)
    return load_fivetools_entities(
        entity_type=normalized_entity_type,
        setting=normalized_setting,
        source_code=resolved_source_code,
    )


def list_entity_types() -> tuple[str, ...]:
    return SUPPORTED_ENTITY_TYPES
