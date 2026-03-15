from __future__ import annotations

from collections.abc import Callable
from typing import Any

from FiveETools.core.fantasy import (
    dieties,
    diseases,
    languages,
    monster,
    sources,
    spells,
)
from FiveETools.core.modern import conditions
from FiveETools.datasets import species as species_dataset

SectionBuilder = Callable[[str], list[dict[str, Any]]]
EntityBuilder = Callable[[str], list[dict[str, Any]]]


def _build_race(source_code: str) -> list[dict[str, Any]]:
    return species_dataset.build_species_list(
        setting="fantasy", source_code=source_code
    )


def _build_spell(source_code: str) -> list[dict[str, Any]]:
    return spells.build_spells_list(source_code=source_code)


def _build_monster(source_code: str) -> list[dict[str, Any]]:
    return monster.build_monster_list(source_code=source_code)


def _build_condition(source_code: str) -> list[dict[str, Any]]:
    # Conditions are shared across settings in current sheets layout.
    return conditions.build_condition_list(source_code=source_code)


def _build_disease(source_code: str) -> list[dict[str, Any]]:
    return diseases.build_disease_list(source_code=source_code)


def _build_language(source_code: str) -> list[dict[str, Any]]:
    return languages.build_language_list(source_code=source_code)


def _build_deity(source_code: str) -> list[dict[str, Any]]:
    return dieties.build_diety_list(source_code=source_code)


SECTION_BUILDERS: dict[str, SectionBuilder] = {
    "race": _build_race,
    "spell": _build_spell,
    "monster": _build_monster,
    "condition": _build_condition,
    "disease": _build_disease,
    "language": _build_language,
    "deity": _build_deity,
}

SECTION_ORDER: tuple[str, ...] = tuple(SECTION_BUILDERS.keys())

ENTITY_BUILDERS: dict[str, EntityBuilder] = {
    "race": _build_race,
    "species": _build_race,
    "spell": _build_spell,
    "monster": _build_monster,
    "condition": _build_condition,
    "disease": _build_disease,
    "language": _build_language,
    "deity": _build_deity,
}


def build_sections(source_code: str | None = None) -> dict[str, list[dict[str, Any]]]:
    source_code = source_code or sources.DEFAULT_SOURCE
    return {
        section: builder(source_code) for section, builder in SECTION_BUILDERS.items()
    }


def normalize_entity_type(entity_type: str) -> str:
    normalized = str(entity_type).strip().lower()
    if normalized not in ENTITY_BUILDERS:
        raise ValueError(
            f"Unknown fantasy entity type '{entity_type}'. Expected one of: {sorted(ENTITY_BUILDERS)}"
        )
    return normalized


def resolve_source_code(source_code: str | None = None) -> str:
    return str(source_code).strip() if source_code else sources.DEFAULT_SOURCE


def load_entities(
    entity_type: str, *, source_code: str | None = None
) -> list[dict[str, Any]]:
    builder = ENTITY_BUILDERS[normalize_entity_type(entity_type)]
    return builder(resolve_source_code(source_code))


def list_entity_types() -> tuple[str, ...]:
    return tuple(ENTITY_BUILDERS.keys())


def get_source_catalog():
    return sources


__all__ = [
    "SECTION_ORDER",
    "ENTITY_BUILDERS",
    "build_sections",
    "normalize_entity_type",
    "resolve_source_code",
    "load_entities",
    "list_entity_types",
    "get_source_catalog",
]
