from __future__ import annotations

from collections.abc import Callable
from typing import Any

from FiveETools.core.modern import (
    backgrounds,
    conditions,
    dieties,
    diseases,
    feats,
    items,
    languages,
    magic_items,
    monster,
    sources,
    spells,
)
from FiveETools.datasets import modern_assembly
from FiveETools.datasets import species as species_dataset

SectionBuilder = Callable[[str], list[dict[str, Any]]]
EntityBuilder = Callable[[str], list[dict[str, Any]]]


def _build_race(source_code: str) -> list[dict[str, Any]]:
    return species_dataset.build_species_list(setting="modern", source_code=source_code)


def _build_class(source_code: str) -> list[dict[str, Any]]:
    return modern_assembly.build_classes_list(source_code=source_code)


def _build_subclass(source_code: str) -> list[dict[str, Any]]:
    return modern_assembly.build_subclasses_list(source_code=source_code)


def _build_spell(source_code: str) -> list[dict[str, Any]]:
    return spells.build_spells_list(source_code=source_code)


def _build_item(source_code: str) -> list[dict[str, Any]]:
    return [
        *items.build_items_list(source_code=source_code),
        *magic_items.build_magic_items_list(source_code=source_code),
    ]


def _build_item_only(source_code: str) -> list[dict[str, Any]]:
    return items.build_items_list(source_code=source_code)


def _build_magic_item_only(source_code: str) -> list[dict[str, Any]]:
    return magic_items.build_magic_items_list(source_code=source_code)


def _build_monster(source_code: str) -> list[dict[str, Any]]:
    return monster.build_monster_list(source_code=source_code)


def _build_feat(source_code: str) -> list[dict[str, Any]]:
    return feats.build_feat_list(source_code=source_code)


def _build_background(source_code: str) -> list[dict[str, Any]]:
    return backgrounds.build_background_list(source_code=source_code)


def _build_condition(source_code: str) -> list[dict[str, Any]]:
    return conditions.build_condition_list(source_code=source_code)


def _build_disease(source_code: str) -> list[dict[str, Any]]:
    return diseases.build_disease_list(source_code=source_code)


def _build_language(source_code: str) -> list[dict[str, Any]]:
    return languages.build_language_list(source_code=source_code)


def _build_deity(source_code: str) -> list[dict[str, Any]]:
    return dieties.build_diety_list(source_code=source_code)


def _build_class_feature(source_code: str) -> list[dict[str, Any]]:
    return modern_assembly.build_features_list(source_code=source_code)


def _build_subclass_feature(source_code: str) -> list[dict[str, Any]]:
    return modern_assembly.build_sub_class_features_list(source_code=source_code)


def _build_item_property(source_code: str) -> list[dict[str, Any]]:
    return items.build_item_property_list(source_code=source_code)


SECTION_BUILDERS: dict[str, SectionBuilder] = {
    "race": _build_race,
    "class": _build_class,
    "subclass": _build_subclass,
    "spell": _build_spell,
    "item": _build_item,
    "monster": _build_monster,
    "feat": _build_feat,
    "background": _build_background,
    "condition": _build_condition,
    "disease": _build_disease,
    "language": _build_language,
    "deity": _build_deity,
    "classFeature": _build_class_feature,
    "subclassFeature": _build_subclass_feature,
    "itemProperty": _build_item_property,
}

SECTION_ORDER: tuple[str, ...] = tuple(SECTION_BUILDERS.keys())

ENTITY_BUILDERS: dict[str, EntityBuilder] = {
    "race": _build_race,
    "species": _build_race,
    "class": _build_class,
    "subclass": _build_subclass,
    "spell": _build_spell,
    "item": _build_item_only,
    "magic_item": _build_magic_item_only,
    "monster": _build_monster,
    "feat": _build_feat,
    "background": _build_background,
    "condition": _build_condition,
    "disease": _build_disease,
    "language": _build_language,
    "deity": _build_deity,
    "classfeature": _build_class_feature,
    "class_feature": _build_class_feature,
    "subclassfeature": _build_subclass_feature,
    "subclass_feature": _build_subclass_feature,
    "itemproperty": _build_item_property,
    "item_property": _build_item_property,
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
            f"Unknown modern entity type '{entity_type}'. Expected one of: {sorted(ENTITY_BUILDERS)}"
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
