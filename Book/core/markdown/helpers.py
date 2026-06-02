from __future__ import annotations

import re
from typing import Any, Iterable


def clean_5etools_text(value: Any) -> str:
    text = str(value)
    text = re.sub(r"\{@(?:\w+)\s+([^}|]+)(?:\|[^}]*)?\}", r"\1", text)
    text = re.sub(r"\{@(?:\w+)\s*([^}]*)\}", r"\1", text)
    return text.strip()


def markdown_table(headers: Iterable[Any], rows: Iterable[Iterable[Any]]) -> str:
    header_values = [clean_5etools_text(header) for header in headers]
    lines = [
        "| " + " | ".join(header_values) + " |",
        "| " + " | ".join(["---"] * len(header_values)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean_5etools_text(cell) for cell in row) + " |")
    return "\n".join(lines)


def ordinal(value: Any) -> str:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return str(value)
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(number % 10, "th")
    return f"{number}{suffix}"


def spell_level_school(spell: dict[str, Any]) -> str:
    schools = {
        "A": "Abjuration",
        "C": "Conjuration",
        "D": "Divination",
        "E": "Enchantment",
        "V": "Evocation",
        "I": "Illusion",
        "N": "Necromancy",
        "T": "Transmutation",
    }
    school = schools.get(spell.get("school", "A"), "Abjuration")
    level = spell.get("level", 0)
    if level == 0:
        return f"{school} cantrip"
    return f"{ordinal(level)}-level {school}"


def spell_time(time_list: list[dict[str, Any]] | None) -> str:
    if not time_list:
        return "1 action"
    entry = time_list[0]
    number = entry.get("number", 1)
    unit = entry.get("unit", "action")
    text = f"{number} {unit}"
    if number != 1:
        text += "s"
    if entry.get("condition"):
        text += f", {entry['condition']}"
    return text


def spell_range(range_dict: dict[str, Any] | None) -> str:
    if not range_dict:
        return "Self"
    range_type = range_dict.get("type", "point")
    distance = range_dict.get("distance", {})
    if range_type == "point":
        dist_type = distance.get("type", "self")
        names = {
            "self": "Self",
            "touch": "Touch",
            "sight": "Sight",
            "unlimited": "Unlimited",
        }
        if dist_type in names:
            return names[dist_type]
        return f"{distance.get('amount', 0)} feet"
    if range_type in {"radius", "sphere", "cube", "cone", "line", "hemisphere"}:
        return f"Self ({distance.get('amount', 0)}-foot {range_type})"
    return "Special"


def spell_components(components: dict[str, Any] | None) -> str:
    if not components:
        return "None"
    parts: list[str] = []
    if components.get("v"):
        parts.append("V")
    if components.get("s"):
        parts.append("S")
    material = components.get("m")
    if material:
        if isinstance(material, str):
            parts.append(f"M ({material})")
        elif isinstance(material, dict):
            parts.append(f"M ({material.get('text', '')})")
        else:
            parts.append("M")
    return ", ".join(parts) if parts else "None"


def spell_duration(duration_list: list[dict[str, Any]] | None) -> str:
    if not duration_list:
        return "Instantaneous"
    entry = duration_list[0]
    duration_type = entry.get("type", "instant")
    if duration_type == "instant":
        return "Instantaneous"
    if duration_type == "permanent":
        ends = entry.get("ends", [])
        return f"Until {', '.join(ends)}" if ends else "Permanent"
    if duration_type == "special":
        return "Special"
    duration = entry.get("duration", {})
    number = duration.get("amount", 1)
    unit = duration.get("type", "minute")
    text = f"{number} {unit}"
    if number != 1:
        text += "s"
    if entry.get("concentration"):
        text = f"Concentration, up to {text}"
    return text


def higher_level_entries(spell: dict[str, Any]) -> list[Any]:
    entries = spell.get("entriesHigherLevel", [])
    if isinstance(entries, dict):
        return entries.get("entries", [])
    return entries if isinstance(entries, list) else []


def monster_size_type_alignment(monster: dict[str, Any]) -> str:
    size_map = {"T": "Tiny", "S": "Small", "M": "Medium", "L": "Large", "H": "Huge", "G": "Gargantuan"}
    size = monster.get("size", ["M"])
    if isinstance(size, list):
        size = size[0] if size else "M"
    size_name = size_map.get(str(size), "Medium")
    creature_type = monster.get("type") or "humanoid"
    if isinstance(creature_type, dict):
        type_name = creature_type.get("type", "humanoid")
        tags = creature_type.get("tags", [])
        if tags:
            type_name += f" ({', '.join(str(tag) for tag in tags)})"
    else:
        type_name = str(creature_type)
    alignment = monster.get("alignment", [])
    if isinstance(alignment, list):
        parts = ["any alignment" if isinstance(item, dict) else str(item) for item in alignment]
        alignment_text = " or ".join(parts) if parts else "unaligned"
    else:
        alignment_text = str(alignment) if alignment else "unaligned"
    return f"{size_name} {type_name}, {alignment_text}"


def armor_class(ac_list: list[Any] | None) -> str:
    if not ac_list:
        return "10"
    entry = ac_list[0]
    if isinstance(entry, int):
        return str(entry)
    if isinstance(entry, dict):
        value = entry.get("ac", 10)
        sources = entry.get("from", [])
        return f"{value} ({', '.join(str(source) for source in sources)})" if sources else str(value)
    return "10"


def hit_points(hp: dict[str, Any] | None) -> str:
    if not hp:
        return "1 (1d4)"
    return f"{hp.get('average', 1)} ({hp.get('formula', '1d4')})"


def movement_speed(speed: Any) -> str:
    if not speed:
        return "30 ft."
    if isinstance(speed, str):
        return speed
    if isinstance(speed, (int, float)):
        return f"{int(speed)} ft."
    if not isinstance(speed, dict):
        return "30 ft."
    parts: list[str] = []
    walk = speed.get("walk", 0)
    if isinstance(walk, str):
        parts.append(walk)
    elif isinstance(walk, (int, float)):
        parts.append(f"{int(walk)} ft.")
    elif isinstance(walk, dict):
        parts.append(f"{walk.get('number', walk.get('amount', 30))} ft.")
    for move_type in ["fly", "swim", "climb", "burrow"]:
        if move_type not in speed:
            continue
        value = speed[move_type]
        if isinstance(value, str):
            parts.append(f"{move_type} {value}")
        elif isinstance(value, (int, float)):
            parts.append(f"{move_type} {int(value)} ft.")
        elif isinstance(value, dict):
            text = f"{move_type} {value.get('number', value.get('amount', 0))} ft."
            if value.get("condition"):
                text += f" ({value['condition']})"
            parts.append(text)
    return ", ".join(parts) if parts else "30 ft."


def monster_ability_rows(monster: dict[str, Any]) -> str:
    headers = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
    values: list[str] = []
    for ability in ["str", "dex", "con", "int", "wis", "cha"]:
        score = int(monster.get(ability, 10))
        modifier = (score - 10) // 2
        values.append(f"{score} ({modifier:+d})")
    return markdown_table(headers, [values])


def join_mapping(mapping: dict[str, Any] | None, *, upper_keys: bool = False) -> str:
    if not mapping:
        return ""
    parts = []
    for key, value in mapping.items():
        label = key.upper() if upper_keys else key.replace("_", " ").title()
        parts.append(f"{label} {value}")
    return ", ".join(parts)


def join_values(values: Any, default: str = "") -> str:
    if values is None:
        return default
    if isinstance(values, list):
        return ", ".join(str(value) for value in values) if values else default
    return str(values)


def monster_senses(monster: dict[str, Any]) -> str:
    parts: list[str] = []
    senses = monster.get("senses", [])
    if isinstance(senses, list):
        parts.extend(str(sense) for sense in senses)
    parts.append(f"passive Perception {monster.get('passive', 10)}")
    return ", ".join(parts)


def monster_xp(cr: Any) -> str:
    xp_map = {
        "0": "0 or 10", "1/8": "25", "1/4": "50", "1/2": "100", "1": "200",
        "2": "450", "3": "700", "4": "1,100", "5": "1,800", "6": "2,300",
        "7": "2,900", "8": "3,900", "9": "5,000", "10": "5,900",
        "11": "7,200", "12": "8,400", "13": "10,000", "14": "11,500",
        "15": "13,000", "16": "15,000", "17": "18,000", "18": "20,000",
        "19": "22,000", "20": "25,000", "21": "33,000", "22": "41,000",
        "23": "50,000", "24": "62,000", "25": "75,000", "26": "90,000",
        "27": "105,000", "28": "120,000", "29": "135,000", "30": "155,000",
    }
    return xp_map.get(str(cr), "0")


def trait_entries(entries: list[Any]) -> list[dict[str, Any]]:
    return [entry for entry in entries if isinstance(entry, dict)]


def trait_text_entries(entries: list[Any], name: str) -> list[str]:
    return [
        entry for entry in entries
        if isinstance(entry, str) and entry.strip() and entry.strip() != f"{name} Traits"
    ]


def species_subtitle(entity: dict[str, Any]) -> str:
    aliases = entity.get("alias") or []
    alias_text = ""
    if aliases:
        alias_text = str(aliases[0]).strip()
    slogan = entity.get("slogan")
    slogan_text = slogan.strip() if isinstance(slogan, str) else ""
    if alias_text and slogan_text:
        return f"{alias_text} - {slogan_text}"
    return alias_text or slogan_text


def species_image_url(entity: dict[str, Any]) -> str:
    for key in ("imageUrl", "image_url", "artUrl", "art_url"):
        value = entity.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    setting = entity.get("setting", entity.get("source", "fantasy"))
    if isinstance(setting, str) and setting not in {"fantasy", "modern"}:
        setting = "fantasy"
    name = str(entity.get("name", "Unknown")).strip().replace(" ", "_")
    return (
        "https://raw.githubusercontent.com/la-rockoteque/Vestigium/refs/heads/main/"
        f"assets/art/Species/{setting}/{name}_M.png"
    )


def species_lore_pages(entity: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    sections = species_fluff_sections(entity)
    intro = [section for section in sections if section["name"] == "Intro"]
    lore = [section for section in sections if section["name"] != "Intro"]
    return {
        "intro": intro,
        "first": lore[:3],
        "second": lore[3:],
    }


def species_fluff_sections(entity: dict[str, Any]) -> list[dict[str, Any]]:
    order = [
        "Origin", "Appearance", "Culture & Identity", "Societal Roles",
        "Naming Conventions", "Life in Orimond", "Life in the City",
        "Playstyle & Roleplaying",
    ]
    sections: dict[str, list[Any]] = {}
    for section in entity.get("fluff", {}).get("entries", []):
        if isinstance(section, dict) and section.get("name") and section.get("entries"):
            sections[str(section["name"])] = section["entries"]
    result = []
    for name in ["Intro", *order]:
        if name in sections:
            result.append({"name": name, "entries": sections.pop(name)})
    result.extend({"name": name, "entries": entries} for name, entries in sections.items())
    return result


def ability_score_summary(ability_list: list[dict[str, Any]] | None) -> str:
    ability_names = {
        "str": "Strength", "dex": "Dexterity", "con": "Constitution",
        "int": "Intelligence", "wis": "Wisdom", "cha": "Charisma",
    }
    parts: list[str] = []
    for entry in ability_list or []:
        if "choose" in entry:
            choose = entry["choose"]
            from_list = choose.get("from", [])
            count = choose.get("count", 1)
            amount = choose.get("amount", 1)
            if from_list:
                abilities = ", ".join(ability_names.get(str(item)[:3].lower(), str(item)) for item in from_list)
                parts.append(f"increase {count} of these scores by {amount}: {abilities}")
            else:
                parts.append(f"increase {count} ability score{'s' if count != 1 else ''} of your choice by {amount}")
        else:
            for ability, value in entry.items():
                if ability in ability_names:
                    parts.append(f"your {ability_names[ability]} score increases by {value}")
    if not parts:
        return "None"
    if len(parts) == 1:
        return parts[0][0].upper() + parts[0][1:] + "."
    text = ", ".join(parts[:-1]) + f", and {parts[-1]}."
    return text[0].upper() + text[1:]


def item_rarity(value: Any) -> str:
    rarity_map = {
        "common": "Common", "uncommon": "Uncommon", "rare": "Rare",
        "very rare": "Very Rare", "legendary": "Legendary", "artifact": "Artifact",
    }
    return rarity_map.get(str(value), str(value).capitalize())


def attunement_text(value: Any) -> str:
    if value is True:
        return " (requires attunement)"
    if isinstance(value, str) and value:
        return f" (requires attunement {value})"
    return ""


def prerequisite_text(prerequisites: list[dict[str, Any]] | None) -> str:
    parts: list[str] = []
    for prereq in prerequisites or []:
        if isinstance(prereq, str):
            parts.append(prereq)
        elif isinstance(prereq, dict):
            if "ability" in prereq:
                parts.extend(f"{ability.upper()} {value}+" for ability, value in prereq["ability"].items())
            elif "level" in prereq:
                parts.append(f"Level {prereq['level']}+")
            elif "spellcasting" in prereq:
                parts.append("The ability to cast at least one spell")
    return ", ".join(parts) if parts else "None"


def render_entries(entries: Iterable[Any]) -> str:
    lines: list[str] = []
    for entry in entries:
        if isinstance(entry, str):
            lines.append(clean_5etools_text(entry))
            continue

        if not isinstance(entry, dict):
            lines.append(clean_5etools_text(entry))
            continue

        entry_type = entry.get("type", "")
        if entry_type == "list":
            for item in entry.get("items", []):
                if isinstance(item, dict):
                    name = item.get("name")
                    if name:
                        lines.append(f"- **{clean_5etools_text(name)}.**")
                    nested = render_entries(item.get("entries", []))
                    if nested:
                        lines.extend(f"  {line}" if line else "" for line in nested.splitlines())
                else:
                    lines.append(f"- {clean_5etools_text(item)}")
            continue

        if entry_type == "table":
            lines.append(markdown_table(entry.get("colLabels", []), entry.get("rows", [])))
            continue

        name = entry.get("name")
        nested_entries = entry.get("entries", [])
        if name:
            lines.append(f"**{clean_5etools_text(name)}**")
        if nested_entries:
            lines.append(render_entries(nested_entries))

    return normalize_markdown("\n".join(lines))


def normalize_markdown(markdown: str) -> str:
    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.rstrip() for line in markdown.split("\n")]

    normalized: list[str] = []
    previous_empty = False
    for line in lines:
        empty = line == ""
        if empty and previous_empty:
            continue
        normalized.append(line)
        previous_empty = empty

    while normalized and normalized[-1] == "":
        normalized.pop()

    return "\n".join(normalized) + "\n"
