from __future__ import annotations

from typing import Any

from DNDBeyond.core.Helpers.converter import (
    convert_background_to_ddb,
    convert_feat_to_ddb,
    convert_monster_to_ddb,
    convert_species_to_ddb,
    convert_spell_to_ddb,
    extract_spell_conditions,
    extract_spell_modifiers,
    extract_spell_scaling,
)

MapperFunc = Any

_MAPPERS: dict[str, MapperFunc] = {
    "spell": convert_spell_to_ddb,
    "monster": convert_monster_to_ddb,
    "species": convert_species_to_ddb,
    "background": convert_background_to_ddb,
    "feat": convert_feat_to_ddb,
}


def map_entity_payload(entity_type: str, entity: dict[str, Any]) -> dict[str, Any]:
    key = str(entity_type).strip().lower()
    if key not in _MAPPERS:
        raise ValueError(f"Unsupported entity type '{entity_type}'.")
    return _MAPPERS[key](entity)


def map_spell_extras(spell: dict[str, Any]) -> dict[str, Any]:
    return {
        "conditions": extract_spell_conditions(spell),
        "modifiers": extract_spell_modifiers(spell),
        "scaling": extract_spell_scaling(spell),
    }


def list_mappable_entity_types() -> tuple[str, ...]:
    return tuple(_MAPPERS.keys())

