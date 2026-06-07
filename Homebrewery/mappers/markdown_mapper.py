from __future__ import annotations

import re
from typing import Any


def _stringify_entries(entries: Any) -> str:
    if isinstance(entries, list):
        return "\n".join(str(entry) for entry in entries if entry is not None)
    if entries is None:
        return ""
    return str(entries)


def _strip_fivetools_tags(value: Any) -> str:
    return re.sub(r"\{@(?:skill|language) ([^}]+)\}", r"\1", str(value or ""))


def _map_background_entry(entry: Any) -> str:
    if not isinstance(entry, dict):
        return str(entry)
    if entry.get("type") == "list":
        lines = []
        for item in entry.get("items", []):
            if not isinstance(item, dict):
                lines.append(f"- {item}")
                continue
            name = item.get("name", "")
            value = _strip_fivetools_tags(item.get("entry", ""))
            lines.append(f"- **{name}:** {value}" if name else f"- {value}")
        return "\n".join(lines)
    name = entry.get("name", "")
    body = "\n".join(str(value) for value in entry.get("entries", []) if value)
    return f"### {name}\n{body}".strip() if name else body


def _map_spell(spell: dict[str, Any]) -> str:
    name = spell.get("name", "Unnamed Spell")
    level = spell.get("level", 0)
    school = spell.get("school", "")
    time = spell.get("time", [])
    duration = spell.get("duration", [])
    spell_range = spell.get("range", {})

    return "\n".join(
        [
            f"## {name}",
            f"*Level {level} {school}*",
            f"**Casting Time:** {time}",
            f"**Range:** {spell_range}",
            f"**Duration:** {duration}",
            "",
            _stringify_entries(spell.get("entries", [])),
        ]
    ).strip()


def _map_species(species: dict[str, Any]) -> str:
    name = species.get("name", "Unnamed Species")
    size = species.get("size", "")
    speed = species.get("speed", "")
    entries = species.get("entries", [])
    return "\n".join(
        [
            f"## {name}",
            f"**Size:** {size}",
            f"**Speed:** {speed}",
            "",
            _stringify_entries(entries),
        ]
    ).strip()


def _map_class(class_data: dict[str, Any]) -> str:
    name = class_data.get("name", "Unnamed Class")
    hit_dice = class_data.get("hd", {})
    proficiency = class_data.get("proficiency", [])
    class_features = class_data.get("classFeatures", [])
    return "\n".join(
        [
            f"## {name}",
            f"**Hit Dice:** {hit_dice}",
            f"**Proficiencies:** {proficiency}",
            "",
            _stringify_entries(class_features),
        ]
    ).strip()


def _map_feat(feat: dict[str, Any]) -> str:
    name = feat.get("name", "Unnamed Feat")
    return "\n".join(
        [
            f"## {str(name).title()}",
            _stringify_entries(feat.get("entries", [])),
        ]
    ).strip()


def _map_background(background: dict[str, Any]) -> str:
    name = background.get("name", "Unnamed Background")
    entries = "\n\n".join(
        block
        for block in (
            _map_background_entry(entry) for entry in background.get("entries", [])
        )
        if block
    )
    return "\n".join([f"## {name}", entries]).strip()


def _map_item(item: dict[str, Any]) -> str:
    name = item.get("name", "Unnamed Item")
    value = item.get("value", "")
    weight = item.get("weight", "")
    entries = item.get("entries", [])
    return "\n".join(
        [
            f"## {name}",
            f"**Value:** {value}",
            f"**Weight:** {weight}",
            "",
            _stringify_entries(entries),
        ]
    ).strip()


def _map_magic_item(item: dict[str, Any]) -> str:
    name = item.get("name", "Unnamed Magic Item")
    rarity = item.get("rarity", "")
    item_type = item.get("type", "")
    entries = item.get("entries", [])
    return "\n".join(
        [
            f"## {name}",
            f"**Type:** {item_type}",
            f"**Rarity:** {rarity}",
            "",
            _stringify_entries(entries),
        ]
    ).strip()


_MAPPERS = {
    "spell": _map_spell,
    "species": _map_species,
    "class": _map_class,
    "feat": _map_feat,
    "background": _map_background,
    "item": _map_item,
    "magic_item": _map_magic_item,
}


def map_entity_markdown(entity_type: str, entity: dict[str, Any]) -> str:
    key = str(entity_type).strip().lower()
    if key not in _MAPPERS:
        raise ValueError(f"Unsupported entity type '{entity_type}'.")
    return _MAPPERS[key](entity)


def list_mappable_entity_types() -> tuple[str, ...]:
    return tuple(_MAPPERS.keys())
