from __future__ import annotations

from collections import defaultdict
from typing import Any

SCHOOL_NAMES: dict[str, str] = {
    "A": "Abjuration",
    "C": "Conjuration",
    "D": "Divination",
    "E": "Enchantment",
    "V": "Evocation",
    "I": "Illusion",
    "N": "Necromancy",
    "T": "Transmutation",
    "P": "Psionic",
}

_ORDINALS: dict[int, str] = {1: "1st", 2: "2nd", 3: "3rd"}


def _level_display(level: int) -> str:
    if level == 0:
        return "cantrip"
    return f"{_ORDINALS.get(level, f'{level}th')}-level"


def _spell_subtitle(level: int, school: str) -> str:
    school_name = SCHOOL_NAMES.get(school, school)
    if level == 0:
        return f"*{school_name} cantrip*"
    return f"*{_level_display(level)} {school_name}*"


def _format_time(time_list: list[dict]) -> str:
    if not time_list:
        return "?"
    t = time_list[0]
    return f"{t.get('number', '')} {t.get('unit', '')}".strip()


def _format_range(range_dict: dict) -> str:
    dist = range_dict.get("distance", {})
    dist_type = str(dist.get("type", "")).lower()
    dist_amount = dist.get("amount", "")
    range_type = str(range_dict.get("type", "point")).lower()

    if range_type == "point":
        if dist_type in ("self", "touch", "sight", "unlimited"):
            return dist_type.capitalize()
        if dist_amount:
            return f"{dist_amount} {dist_type}"
        return dist_type.capitalize() if dist_type else "?"
    shape_map = {
        "radius": "radius", "cone": "cone", "line": "line",
        "hemisphere": "hemisphere", "cube": "cube", "sphere": "sphere",
    }
    if range_type in shape_map:
        return f"{dist_amount}-foot {shape_map[range_type]}"
    return range_type.capitalize() if range_type else "?"


def _format_duration(duration_list: list[dict]) -> str:
    if not duration_list:
        return "?"
    d = duration_list[0]
    dtype = str(d.get("type", "")).lower()
    if dtype == "instant":
        return "Instantaneous"
    if dtype == "permanent":
        return "Until dispelled"
    if dtype == "special":
        return "Special"
    if dtype == "timed":
        inner = d.get("duration", {})
        amount = inner.get("amount", "")
        unit = inner.get("type", "")
        conc = d.get("concentration", False)
        up_to = inner.get("upTo", False)
        text = f"{amount} {unit}"
        if up_to:
            text = f"up to {text}"
        if conc:
            return f"Concentration, {text}"
        return text
    return dtype.capitalize() if dtype else "?"


def _format_components(components_dict: dict) -> str:
    parts: list[str] = []
    if components_dict.get("v"):
        parts.append("V")
    if components_dict.get("s"):
        parts.append("S")
    if components_dict.get("r"):
        parts.append("R")
    mat = components_dict.get("m")
    if mat:
        if isinstance(mat, dict):
            parts.append(f"M ({mat.get('text', '')})")
        else:
            parts.append("M")
    return ", ".join(parts) if parts else "—"


def _stringify_entries(entries: Any) -> str:
    if isinstance(entries, list):
        return "\n\n".join(str(e) for e in entries if e is not None)
    return str(entries) if entries is not None else ""


def _spell_to_card(spell: dict[str, Any]) -> str:
    name = spell.get("name", "Unnamed Spell")
    level = int(spell.get("level", 0))
    school = str(spell.get("school", ""))
    casting_time = _format_time(spell.get("time", []))
    spell_range = _format_range(spell.get("range", {}))
    components = _format_components(spell.get("components", {}))
    duration = _format_duration(spell.get("duration", []))
    description = _stringify_entries(spell.get("entries", []))

    return (
        f"#### {name}\n"
        f"{_spell_subtitle(level, school)}\n"
        f"**Casting Time:** :: {casting_time}\n"
        f"**Range:**        :: {spell_range}\n"
        f"**Components:**   :: {components}\n"
        f"**Duration:**     :: {duration}\n"
        f"\n"
        f"{description}"
    )


def _level_header(level: int) -> str:
    if level == 0:
        return "##### Cantrip"
    ordinal = _ORDINALS.get(level, f"{level}th")
    return f"##### {ordinal} Level"


def build_fantasy_spell_list_by_class(spells: list[dict[str, Any]]) -> str:
    class_spells: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for spell in spells:
        for cls in spell.get("classes", {}).get("fromClassList", []):
            class_name = cls.get("name", "Unknown")
            class_spells[class_name].append(spell)

    sections: list[str] = []
    for class_name in sorted(class_spells):
        sorted_spells = sorted(
            class_spells[class_name],
            key=lambda s: (int(s.get("level", 0)), str(s.get("name", ""))),
        )

        level_sections: list[str] = []
        current_level: int | None = None
        level_cards: list[str] = []

        for spell in sorted_spells:
            spell_level = int(spell.get("level", 0))
            if spell_level != current_level:
                if level_cards and current_level is not None:
                    level_sections.append(
                        _level_header(current_level) + "\n\n" + "\n\n---\n\n".join(level_cards)
                    )
                current_level = spell_level
                level_cards = []
            level_cards.append(_spell_to_card(spell))

        if level_cards and current_level is not None:
            level_sections.append(
                _level_header(current_level) + "\n\n" + "\n\n---\n\n".join(level_cards)
            )

        sections.append(f"## {class_name}\n\n" + "\n\n".join(level_sections))

    return "\n\n---\n\n".join(sections)
