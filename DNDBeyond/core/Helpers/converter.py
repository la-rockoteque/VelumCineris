"""Convert source data formats to D&D Beyond form payloads."""
from pathlib import Path
import re
from typing import Dict, Iterable, List, Optional


def convert_spell_to_ddb(spell: Dict) -> Dict:
    """Convert 5etools spell format to D&D Beyond format

    Implements strict validation rules based on D&D Beyond's form requirements:
    - Duration ID 2 (Concentration), 3 (Time), or 4 (Special) REQUIRES interval + unit
    - Range/Origin must be logically consistent
    - HTML must be properly closed and under length limits
    - Higher-level scaling must match can_cast flag
    - School IDs are 3-10, not 1-8!
    """

    # School mapping - D&D Beyond uses 3-10, not 1-8!
    school_map = {
        "A": 3,   # Abjuration
        "C": 4,   # Conjuration
        "D": 5,   # Divination
        "E": 6,   # Enchantment
        "V": 7,   # Evocation
        "I": 8,   # Illusion
        "N": 9,   # Necromancy
        "T": 10   # Transmutation
    }
    school = spell.get("school", "A")
    school_id = school_map.get(school, 3)

    # Components
    components = spell.get("components", {})
    if isinstance(components, dict):
        verbal = components.get("v", False)
        somatic = components.get("s", False)
        material = components.get("m", False)
    else:
        components_str = str(components).upper()
        verbal = "V" in components_str
        somatic = "S" in components_str
        material = "M" in components_str

    # Casting time
    time_data = spell.get("time", [{}])[0] if spell.get("time") else {}
    casting_unit = time_data.get("unit", "action").lower()
    casting_time_map = {
        "action": 1,
        "bonus": 2,
        "reaction": 3,
        "minute": 4,
        "hour": 5
    }
    casting_time_id = casting_time_map.get(casting_unit, 1)
    activation_id = 3 if casting_unit == "reaction" else 1
    casting_time_desc = ""
    if casting_unit == "reaction":
        casting_time_desc = time_data.get("condition", "")

    # Range and Origin - Handle nested distance structures
    range_data = spell.get("range", {})
    range_amount = 0
    origin_id = 1

    if isinstance(range_data, dict):
        distance = range_data.get("distance", {})

        if isinstance(distance, dict):
            distance_type = distance.get("type", "").lower()

            if distance_type == "self":
                origin_id = 1
                range_amount = 0
            elif distance_type == "touch":
                origin_id = 2
                range_amount = 0
            elif distance_type == "sight":
                origin_id = 4
                range_amount = 0
            elif distance_type == "unlimited":
                origin_id = 9
                range_amount = 0
            elif "amount" in distance:
                range_amount = int(distance.get("amount", 60))
                origin_id = 3
            else:
                range_type = range_data.get("type", "self").lower()
                if range_type in ["self", "touch", "sight", "unlimited"]:
                    origin_map = {"self": 1, "touch": 2, "sight": 4, "unlimited": 9}
                    origin_id = origin_map.get(range_type, 1)
                    range_amount = 0
                else:
                    origin_id = 3
                    range_amount = 60
        else:
            range_type = range_data.get("type", "self").lower()
            if range_type == "self":
                origin_id = 1
                range_amount = 0
            elif range_type == "touch":
                origin_id = 2
                range_amount = 0
            elif range_type == "sight":
                origin_id = 4
                range_amount = 0
            elif range_type == "unlimited":
                origin_id = 9
                range_amount = 0
            else:
                origin_id = 3
                range_amount = 60

    # Duration
    duration_data = spell.get("duration", [{}])[0] if spell.get("duration") else {}
    duration_type = duration_data.get("type", "instant").lower()
    concentration = duration_data.get("concentration", False)

    duration_id = 1
    duration_interval = ""
    duration_unit = ""

    if concentration:
        duration_id = 2
        if "duration" in duration_data:
            dur_val = duration_data["duration"]
            if isinstance(dur_val, dict):
                amount = dur_val.get("amount", 1)
                unit = dur_val.get("type", "minute").lower()
            else:
                amount = 1
                unit = "minute"
        else:
            amount = 1
            unit = "minute"

        duration_interval = str(amount)
        unit_map = {"round": 1, "rounds": 1, "minute": 2, "minutes": 2, "hour": 3, "hours": 3, "day": 4, "days": 4}
        duration_unit = str(unit_map.get(unit, 2))

    elif duration_type in ["instant", "instantaneous"]:
        duration_id = 1
        duration_interval = ""
        duration_unit = ""
    elif duration_type == "permanent":
        if "dispel" in str(duration_data).lower():
            duration_id = 5
            duration_interval = ""
            duration_unit = ""
        else:
            duration_id = 4
            duration_interval = "1"
            duration_unit = "2"
    elif duration_type == "special":
        duration_id = 4
        if "duration" in duration_data:
            dur_val = duration_data["duration"]
            if isinstance(dur_val, dict):
                amount = dur_val.get("amount", 1)
                unit = dur_val.get("type", "minute").lower()
            else:
                amount = 1
                unit = "minute"
        else:
            amount = 1
            unit = "minute"

        duration_interval = str(amount)
        unit_map = {"round": 1, "rounds": 1, "minute": 2, "minutes": 2, "hour": 3, "hours": 3, "day": 4, "days": 4}
        duration_unit = str(unit_map.get(unit, 2))
    elif duration_type == "timed":
        duration_id = 3

        if "duration" in duration_data:
            dur_val = duration_data["duration"]
            if isinstance(dur_val, dict):
                amount = dur_val.get("amount", 1)
                unit = dur_val.get("type", "round").lower()
            else:
                amount = 1
                unit = "round"
        else:
            amount = 1
            unit = "round"

        duration_interval = str(amount)
        unit_map = {"round": 1, "rounds": 1, "minute": 2, "minutes": 2, "hour": 3, "hours": 3, "day": 4, "days": 4}
        duration_unit = str(unit_map.get(unit, 1))
    else:
        if "duration" in duration_data:
            dur_val = duration_data.get("duration", {})
            if isinstance(dur_val, dict) and "amount" in dur_val:
                duration_id = 3
                amount = dur_val.get("amount", 1)
                unit = dur_val.get("type", "round").lower()
                duration_interval = str(amount)
                unit_map = {"round": 1, "rounds": 1, "minute": 2, "minutes": 2, "hour": 3, "hours": 3, "day": 4, "days": 4}
                duration_unit = str(unit_map.get(unit, 1))
            else:
                duration_id = 1
                duration_interval = ""
                duration_unit = ""
        else:
            duration_id = 1
            duration_interval = ""
            duration_unit = ""

    # Description
    entries = spell.get("entries", [])
    description_parts = []

    for entry in entries:
        if isinstance(entry, str):
            description_parts.append(entry)
        elif isinstance(entry, dict):
            if entry.get("type") == "entries":
                name = entry.get("name", "")
                sub_entries = entry.get("entries", [])
                sub_text = " ".join([str(e) for e in sub_entries])
                if name:
                    description_parts.append(f"**{name}:** {sub_text}")
                else:
                    description_parts.append(sub_text)
            else:
                description_parts.append(str(entry))

    description = "\n\n".join(description_parts)

    MAX_DESC_LENGTH = 9500
    paragraphs = description.split("\n\n")
    html_parts = []
    current_length = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        html_para = f"<p>{para}</p>"

        if current_length + len(html_para) > MAX_DESC_LENGTH:
            remaining = MAX_DESC_LENGTH - current_length
            if remaining > 20:
                truncated = para[:remaining-20] + "..."
                html_parts.append(f"<p>{truncated}</p>")
            break

        html_parts.append(html_para)
        current_length += len(html_para)

    description_html = "\n".join(html_parts)

    # Higher level casting
    has_higher_level = False
    higher_level_scale = 0

    if "entriesHigherLevel" in spell:
        higher_entries = spell["entriesHigherLevel"]
        if higher_entries and isinstance(higher_entries, list) and len(higher_entries) > 0:
            has_higher_level = True
            higher_level_scale = 3

    if not has_higher_level:
        higher_level_scale = 0

    # Classes
    classes_data = spell.get("classes", {})
    class_list = []

    if isinstance(classes_data, dict):
        from_class_list = classes_data.get("fromClassList", [])
        for cls in from_class_list:
            if isinstance(cls, dict):
                class_name = cls.get("name", "").lower()
                class_list.append(class_name)

    # Map to D&D Beyond class IDs (from HTML form)
    class_id_map = {
        "artificer": 2656866,
        "bard": 2190876,
        "cleric": 2190877,
        "druid": 2190878,
        "paladin": 2190881,
        "ranger": 2190882,
        "sorcerer": 2190884,
        "sorceror": 2190884,  # Common typo
        "warlock": 2190885,
        "wizard": 2190886
    }

    classes = []
    for class_name in class_list:
        if class_name in class_id_map:
            classes.append(class_id_map[class_name])

    # Additional fields for update endpoints
    # AOE (Area of Effect) - prioritize CSV data over range parsing
    aoe_type = ""
    aoe_size = ""

    # Check for DDB-specific CSV fields first
    if spell.get("ddb_area_type"):
        # Map CSV area type to D&D Beyond IDs
        area_type_map = {
            "cone": "1",
            "cube": "2",
            "cylinder": "3",
            "line": "4",
            "sphere": "5",
            "radius": "5",
            "hemisphere": "5"
        }
        csv_area = spell.get("ddb_area_type", "").lower().strip()
        aoe_type = area_type_map.get(csv_area, "")

    if spell.get("ddb_area_distance"):
        try:
            aoe_size = str(int(float(spell.get("ddb_area_distance", 0))))
        except (ValueError, TypeError):
            aoe_size = ""

    # Fallback to range parsing if CSV fields not available
    if not aoe_type and isinstance(range_data, dict):
        aoe_data = range_data.get("type", "")
        if aoe_data in ["cone", "cube", "cylinder", "line", "sphere", "radius"]:
            aoe_map = {"cone": "1", "cube": "2", "cylinder": "3", "line": "4", "sphere": "5", "radius": "5"}
            aoe_type = aoe_map.get(aoe_data, "")

            # Get AOE size
            distance = range_data.get("distance", {})
            if isinstance(distance, dict) and "amount" in distance:
                aoe_size = str(int(distance.get("amount", 0)))

    # Save type - prioritize savingThrow field over text analysis
    save_type = ""

    # Check savingThrow field from CSV (e.g., "dexterity", "strength")
    saving_throw_data = spell.get("savingThrow", [])
    if isinstance(saving_throw_data, list) and saving_throw_data:
        first_save = str(saving_throw_data[0]).lower().strip()
        save_map = {
            "strength": "1",
            "str": "1",
            "dexterity": "2",
            "dex": "2",
            "constitution": "3",
            "con": "3",
            "intelligence": "4",
            "int": "4",
            "wisdom": "5",
            "wis": "5",
            "charisma": "6",
            "cha": "6"
        }
        save_type = save_map.get(first_save, "")

    # Fallback to text analysis if not in CSV
    if not save_type:
        full_text = description.lower()
        if "strength saving throw" in full_text or "strength save" in full_text:
            save_type = "1"
        elif "dexterity saving throw" in full_text or "dexterity save" in full_text:
            save_type = "2"
        elif "constitution saving throw" in full_text or "constitution save" in full_text:
            save_type = "3"
        elif "intelligence saving throw" in full_text or "intelligence save" in full_text:
            save_type = "4"
        elif "wisdom saving throw" in full_text or "wisdom save" in full_text:
            save_type = "5"
        elif "charisma saving throw" in full_text or "charisma save" in full_text:
            save_type = "6"

    # Attack type - check damage field or text analysis
    attack_type = ""

    # Check ddb_damage field for attack indicators
    damage_info = spell.get("ddb_damage", "").lower()
    if "ranged" in damage_info or "range" in damage_info:
        attack_type = "1"  # Ranged spell attack
    elif "melee" in damage_info or "touch" in damage_info:
        attack_type = "2"  # Melee spell attack

    # Fallback to text analysis
    if not attack_type:
        full_text = description.lower()
        if "ranged spell attack" in full_text:
            attack_type = "1"
        elif "melee spell attack" in full_text:
            attack_type = "2"

    # Effect on save success/fail - from CSV fields
    save_success = spell.get("ddb_save_success", "").strip()
    save_fail = spell.get("ddb_save_fail", "").strip()

    # Map text descriptions to D&D Beyond IDs if needed
    # (You may need to adjust these mappings based on your CSV values)
    save_effect_map = {
        "half": "1",
        "half damage": "1",
        "none": "2",
        "no damage": "2",
        "no effect": "2"
    }

    if save_success and save_success.lower() in save_effect_map:
        save_success = save_effect_map[save_success.lower()]

    if save_fail and save_fail.lower() in save_effect_map:
        save_fail = save_effect_map[save_fail.lower()]

    # Version - from CSV or spreadsheet column
    version = spell.get("ddb_version", "").strip() or spell.get("version", "").strip()

    # Build result
    result = {
        "name": spell.get("name", "Unnamed Spell"),
        "level": int(spell.get("level", 0)),
        "school_id": school_id,
        "casting_time_id": casting_time_id,
        "activation_id": activation_id,
        "casting_time_desc": casting_time_desc,
        "verbal": verbal,
        "somatic": somatic,
        "material": material,
        "components_desc": spell.get("componentsRaw", "") or spell.get("material", "") or "",
        "origin_id": origin_id,
        "range": range_amount,
        "duration_id": duration_id,
        "duration_interval": duration_interval,
        "duration_unit": duration_unit,
        "description_html": description_html,
        "can_cast_at_higher_level": has_higher_level,
        "higher_level_scale": higher_level_scale,
        "classes": classes,
        # Additional fields for update endpoints (now from CSV columns)
        "aoe_type": aoe_type,
        "aoe_size": aoe_size,
        "save_type": save_type,
        "attack_type": attack_type,
        "on_miss": "",  # Not available in current CSV
        "save_success": save_success,  # From CSV "Success" column
        "save_fail": save_fail,  # From CSV "Fail" column
        "version": version,  # Version for homebrew tracking
    }

    return result


_MONSTER_FIELD_IDS = {
    "initiative_bonus": "",
    "str_score": "",
    "dex_score": "",
    "con_score": "",
    "int_score": "",
    "wis_score": "",
    "cha_score": "",
    "avatar_small": "",
    "avatar_large": "",
}
_SPECIES_FIELD_IDS = {
    "avatar_small": "",
    "avatar_large": "",
}

_SPECIES_AVATAR_LABELS = {
    "avatar_small": "Small Avatar",
    "avatar_large": "Large Avatar",
}
_MONSTER_FIELD_ID_SELECTORS = {
    "initiative_bonus": "field-initiative-bonus",
    "str_score": "field-strength",
    "dex_score": "field-dexterity",
    "con_score": "field-constitution",
    "int_score": "field-intelligence",
    "wis_score": "field-wisdom",
    "cha_score": "field-charisma",
    "avatar_small": "field-avatar",
    "avatar_large": "field-large-avatar",
}
_DEFAULT_MONSTER_CREATE_HTML = (
    Path(__file__).resolve().parents[1]
    / "pages"
    / "Create - Create a Monster - Creations - Homebrew - D&D Beyond.html"
)


def _update_monster_field_ids_from_html_text(html_text: str) -> None:
    if not html_text:
        return
    for key, field_id in _MONSTER_FIELD_ID_SELECTORS.items():
        tag_match = re.search(
            rf'<input[^>]*\bid="{re.escape(field_id)}"[^>]*>',
            html_text,
            re.IGNORECASE,
        )
        if not tag_match:
            continue
        tag = tag_match.group(0)
        name_match = re.search(r'\bname="([^"]+)"', tag)
        if name_match:
            _MONSTER_FIELD_IDS[key] = name_match.group(1)


def _update_monster_field_ids_from_html(html_path: Path) -> None:
    if not html_path.exists():
        return
    text = html_path.read_text(encoding="utf-8", errors="ignore")
    _update_monster_field_ids_from_html_text(text)


def refresh_monster_field_ids(html_path: Path | None = None) -> Dict[str, str]:
    target = html_path or _DEFAULT_MONSTER_CREATE_HTML
    _update_monster_field_ids_from_html(target)
    return dict(_MONSTER_FIELD_IDS)


def refresh_monster_field_ids_from_html_text(html_text: str) -> Dict[str, str]:
    _update_monster_field_ids_from_html_text(html_text)
    return dict(_MONSTER_FIELD_IDS)


def refresh_species_field_ids_from_html_text(html_text: str) -> Dict[str, str]:
    if not html_text:
        return dict(_SPECIES_FIELD_IDS)
    for key, label in _SPECIES_AVATAR_LABELS.items():
        match = re.search(
            rf'{re.escape(label)}</div>.*?<input[^>]+type="file"[^>]+name="([^"]+)"',
            html_text,
            re.IGNORECASE | re.S,
        )
        if match:
            _SPECIES_FIELD_IDS[key] = match.group(1)
    return dict(_SPECIES_FIELD_IDS)


def get_species_field_ids() -> Dict[str, str]:
    return dict(_SPECIES_FIELD_IDS)

_STAT_BLOCK_TYPE_MAP = {
    "2014": "0",
    "2024": "1",
    "0": "0",
    "1": "1",
}

_MONSTER_TYPE_MAP = {
    "aberration": "1",
    "beast": "2",
    "celestial": "3",
    "construct": "4",
    "dragon": "6",
    "elemental": "7",
    "fey": "8",
    "fiend": "9",
    "giant": "10",
    "humanoid": "11",
    "monstrosity": "13",
    "ooze": "14",
    "plant": "15",
    "undead": "16",
    "unknown": "17",
}

_SIZE_MAP = {
    "tiny": "2",
    "small": "3",
    "medium": "4",
    "large": "5",
    "huge": "6",
    "gargantuan": "7",
    "medium or small": "10",
}

_SIZE_SHORT_MAP = {
    "T": "tiny",
    "S": "small",
    "M": "medium",
    "L": "large",
    "H": "huge",
    "G": "gargantuan",
}

_ALIGNMENT_MAP = {
    "lawful good": "1",
    "neutral good": "2",
    "chaotic good": "3",
    "lawful neutral": "4",
    "neutral": "5",
    "chaotic neutral": "6",
    "lawful evil": "7",
    "neutral evil": "8",
    "chaotic evil": "9",
    "unaligned": "10",
    "any alignment": "11",
    "any evil alignment": "13",
    "any good alignment": "14",
    "any chaotic alignment": "15",
    "any lawful alignment": "16",
    "any non-good alignment": "18",
    "any non-lawful alignment": "19",
    "any neutral alignment": "29",
    "any non-chaotic alignment": "30",
    "typically lawful good": "22",
    "typically neutral good": "21",
    "typically chaotic good": "25",
    "typically lawful neutral": "28",
    "typically neutral": "26",
    "typically chaotic neutral": "20",
    "typically lawful evil": "27",
    "typically neutral evil": "24",
    "typically chaotic evil": "23",
}

_ALIGNMENT_SHORT_MAP = {
    "LG": "lawful good",
    "NG": "neutral good",
    "CG": "chaotic good",
    "LN": "lawful neutral",
    "N": "neutral",
    "CN": "chaotic neutral",
    "LE": "lawful evil",
    "NE": "neutral evil",
    "CE": "chaotic evil",
    "U": "unaligned",
}

_CHALLENGE_RATING_MAP = {
    "0": "1",
    "1/8": "2",
    "1/4": "3",
    "1/2": "4",
    "1": "5",
    "2": "6",
    "3": "7",
    "4": "8",
    "5": "9",
    "6": "10",
    "7": "11",
    "8": "12",
    "9": "13",
    "10": "14",
    "11": "15",
    "12": "16",
    "13": "17",
    "14": "18",
    "15": "19",
    "16": "20",
    "17": "21",
    "18": "22",
    "19": "23",
    "20": "24",
    "21": "25",
    "22": "26",
    "23": "27",
    "24": "29",
    "25": "30",
    "26": "31",
    "27": "32",
    "28": "33",
    "29": "34",
    "30": "35",
}

_HIT_DIE_MAP = {
    "d4": "4",
    "d6": "6",
    "d8": "8",
    "d10": "10",
    "d12": "12",
    "d20": "20",
}

_SAVING_THROW_MAP = {
    "str": "1",
    "dex": "2",
    "con": "3",
    "int": "4",
    "wis": "5",
    "cha": "6",
}


def _map_enum(value, mapping, default=""):
    if value is None:
        return default
    if isinstance(value, (int, float)):
        return str(int(value))
    value_str = str(value).strip()
    if not value_str:
        return default
    import re

    if re.fullmatch(r"\d+(\.0+)?", value_str):
        value_str = str(int(float(value_str)))
    value_key = value_str.lower()
    return mapping.get(value_key, mapping.get(value_str, value_str))


def _listify(values: Iterable) -> list:
    if values is None:
        return []
    if isinstance(values, (list, tuple, set)):
        return [str(v) for v in values if str(v).strip()]
    return [str(values)] if str(values).strip() else []

def _normalize_monster_type(monster: Dict) -> str:
    monster_type = monster.get("monster_type")
    if not monster_type:
        monster_type = monster.get("type", "")
        if isinstance(monster_type, dict):
            monster_type = monster_type.get("type", "")
    return monster_type


def _normalize_size(monster: Dict) -> str:
    size = monster.get("size", "")
    if isinstance(size, (list, tuple)) and size:
        size = size[0]
    size_str = str(size).strip()
    if not size_str:
        return ""
    size_str = _SIZE_SHORT_MAP.get(size_str.upper(), size_str)
    return size_str


def _normalize_alignment(monster: Dict) -> str:
    alignment = monster.get("alignment", "")
    if isinstance(alignment, (list, tuple)) and alignment:
        alignment = alignment[0]
    alignment_str = str(alignment).strip()
    if not alignment_str:
        return ""
    alignment_str = _ALIGNMENT_SHORT_MAP.get(alignment_str.upper(), alignment_str)
    return alignment_str


def _normalize_cr(monster: Dict) -> str:
    cr = monster.get("challenge_rating")
    if not cr:
        cr = monster.get("cr", "")
    return str(cr).strip()


def _extract_ac(monster: Dict) -> str:
    armor_class = monster.get("armor_class")
    if armor_class is not None and armor_class != "":
        return _clean_number(armor_class)
    ac = monster.get("ac")
    if isinstance(ac, list) and ac:
        first = ac[0]
        if isinstance(first, dict) and "ac" in first:
            return _clean_number(first.get("ac", ""))
        return _clean_number(first)
    if isinstance(ac, dict):
        return _clean_number(ac.get("ac", ""))
    return ""


def _extract_hp(monster: Dict) -> Dict[str, str]:
    average = monster.get("average_hit_points")
    if average is None or average == "":
        hp = monster.get("hp", {})
        if isinstance(hp, dict):
            average = hp.get("average", "")
    hit_dice = monster.get("hit_points_die_count")
    hit_die_value = monster.get("hit_points_die_value")
    hit_mod = monster.get("hit_points_modifier")
    if not hit_dice or not hit_die_value:
        hp = monster.get("hp", {})
        if isinstance(hp, dict):
            formula = str(hp.get("formula", "")).strip()
            if formula:
                import re

                match = re.search(r"(\d+)d(\d+)(?:\s*([+-])\s*(\d+))?", formula)
                if match:
                    hit_dice = hit_dice or match.group(1)
                    hit_die_value = hit_die_value or f"d{match.group(2)}"
                    if hit_mod in (None, "") and match.group(3) and match.group(4):
                        sign = 1 if match.group(3) == "+" else -1
                        hit_mod = str(sign * int(match.group(4)))
    return {
        "average": _clean_number(average or ""),
        "die_count": _clean_number(hit_dice or ""),
        "die_value": str(hit_die_value or ""),
        "modifier": _clean_number(hit_mod or ""),
    }


def _clean_number(value) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, (int, float)):
        return str(int(value)) if float(value).is_integer() else str(value)
    value_str = str(value).strip()
    try:
        as_float = float(value_str)
    except ValueError:
        return value_str
    return str(int(as_float)) if as_float.is_integer() else value_str


def convert_monster_to_ddb(monster: Dict) -> Dict:
    """Convert monster data to D&D Beyond form fields for monster creation."""
    hp = _extract_hp(monster)
    size_value = _normalize_size(monster)
    alignment_value = _normalize_alignment(monster)
    monster_type = _normalize_monster_type(monster)
    cr_value = _normalize_cr(monster)
    dex_score = monster.get("dex")
    initiative_bonus = monster.get("initiative_bonus")
    if initiative_bonus in (None, "") and isinstance(dex_score, (int, float)):
        initiative_bonus = int((int(dex_score) - 10) // 2)
    saving_throws = monster.get("saving_throws")
    if saving_throws is None and isinstance(monster.get("save"), dict):
        saving_throws = list(monster.get("save", {}).keys())
    form_data = {
        "stat-block-type": _map_enum(
            monster.get("stat_block_type", "2014"), _STAT_BLOCK_TYPE_MAP
        ),
        "Name": monster.get("name", ""),
        "version": "",
        "monster-type": _map_enum(monster_type, _MONSTER_TYPE_MAP),
        "monster-sub-type": _listify(monster.get("monster_sub_type", [])),
        "size": _map_enum(size_value, _SIZE_MAP),
        "swarm-monster": _map_enum(monster.get("swarm_base", ""), {}),
        "alignment": _map_enum(alignment_value, _ALIGNMENT_MAP),
        "challenge-rating": _map_enum(cr_value, _CHALLENGE_RATING_MAP),
        "special-traits-description-type": "1",
        "special-traits-description-wysiwyg": monster.get("special_traits_html", ""),
        "special-traits-description": monster.get("special_traits_html", ""),
        "actions-description-type": "1",
        "actions-description-wysiwyg": monster.get("actions_html", ""),
        "actions-description": monster.get("actions_html", ""),
        "bonus-actions-description-type": "1",
        "bonus-actions-description-wysiwyg": monster.get("bonus_actions_html", ""),
        "bonus-actions-description": monster.get("bonus_actions_html", ""),
        "reactions-description-type": "1",
        "reactions-description-wysiwyg": monster.get("reactions_html", ""),
        "reactions-description": monster.get("reactions_html", ""),
        "monster-characteristics-description-type": "1",
        "monster-characteristics-description-wysiwyg": monster.get(
            "characteristics_html", ""
        ),
        "monster-characteristics-description": monster.get("characteristics_html", ""),
        "is-legendary": "y" if monster.get("is_legendary") else "",
        "legendary-actions-description-type": "1",
        "legendary-actions-description-wysiwyg": monster.get("legendary_actions_html", ""),
        "legendary-actions-description": monster.get("legendary_actions_html", ""),
        "is-mythic": "y" if monster.get("is_mythic") else "",
        "mythic-actions-description-type": "1",
        "mythic-actions-description-wysiwyg": monster.get("mythic_actions_html", ""),
        "mythic-actions-description": monster.get("mythic_actions_html", ""),
        "has-lair": "y" if monster.get("has_lair") else "",
        "lair-challenge-rating": _map_enum(monster.get("lair_challenge_rating", ""), {}),
        "lair-description-type": "1",
        "lair-description-wysiwyg": monster.get("lair_description_html", ""),
        "lair-description": monster.get("lair_description_html", ""),
        "armor-class": _extract_ac(monster),
        "armor-class-type": monster.get("armor_class_type", ""),
        _MONSTER_FIELD_IDS["initiative_bonus"]: _clean_number(initiative_bonus or ""),
        "passive-perception": _clean_number(
            monster.get("passive_perception", monster.get("passive", ""))
        ),
        "average-hit-points": hp["average"],
        "hit-points-die-count": hp["die_count"],
        "hit-points-die-value": _map_enum(hp["die_value"], _HIT_DIE_MAP),
        "hit-points-modifier": hp["modifier"],
        _MONSTER_FIELD_IDS["str_score"]: str(monster.get("str", "")),
        _MONSTER_FIELD_IDS["dex_score"]: str(monster.get("dex", "")),
        _MONSTER_FIELD_IDS["con_score"]: str(monster.get("con", "")),
        _MONSTER_FIELD_IDS["int_score"]: str(monster.get("int", "")),
        _MONSTER_FIELD_IDS["wis_score"]: str(monster.get("wis", "")),
        _MONSTER_FIELD_IDS["cha_score"]: str(monster.get("cha", "")),
        "monster-saving-throw": [
            _map_enum(v, _SAVING_THROW_MAP) for v in _listify(saving_throws)
        ],
        "damage-adjustment": _listify(monster.get("damage_adjustments")),
        "condition-immunity": _listify(monster.get("condition_immunities")),
        "monster-environments": _listify(monster.get("environments")),
        "gear-description": monster.get("gear_description", ""),
        "languages-note": monster.get("languages_note", ""),
        "monster-tags-public": _listify(monster.get("monster_tags")),
        "treasure": _listify(monster.get("treasure")),
    }

    extra = monster.get("extra_form_data")
    if isinstance(extra, dict):
        form_data.update(extra)

    return form_data


def _normalize_species_size(size_value) -> str:
    size = size_value
    if isinstance(size, (list, tuple)) and size:
        size = size[0]
    size_str = str(size or "").strip()
    if not size_str:
        return ""
    size_str = _SIZE_SHORT_MAP.get(size_str.upper(), size_str)
    return size_str


def _species_entries_to_html(entries) -> str:
    if not entries:
        return ""
    parts = []
    for entry in entries:
        if isinstance(entry, str):
            text = entry.strip()
            if text:
                parts.append(f"<p>{text}</p>")
            continue
        if isinstance(entry, dict) and entry.get("type") == "entries":
            name = entry.get("name", "").strip()
            sub_entries = entry.get("entries", [])
            sub_text = " ".join(str(e).strip() for e in sub_entries if str(e).strip())
            if name and sub_text:
                parts.append(f"<p><strong>{name}.</strong> {sub_text}</p>")
            elif sub_text:
                parts.append(f"<p>{sub_text}</p>")
            continue
        text = str(entry).strip()
        if text:
            parts.append(f"<p>{text}</p>")
    return "\n".join(parts)


def _species_intro_from_entries(entries, fallback_name: str) -> str:
    if entries:
        for entry in entries:
            if isinstance(entry, str):
                text = entry.strip()
                if text:
                    return text
    name = fallback_name.strip() if fallback_name else "This species"
    return f"{name} traits are described below."


def convert_species_to_ddb(species: Dict) -> Dict:
    """Convert species data to D&D Beyond form fields for species creation."""
    size_value = _normalize_species_size(species.get("size", ""))
    speed = species.get("speed", "")
    speed_walking = ""
    speed_burrowing = ""
    speed_climbing = ""
    speed_flying = ""
    speed_swimming = ""
    if isinstance(speed, dict):
        speed_walking = speed.get("walk", "") or speed.get("walking", "")
        speed_burrowing = speed.get("burrow", "") or speed.get("burrowing", "")
        speed_climbing = speed.get("climb", "") or speed.get("climbing", "")
        speed_flying = speed.get("fly", "") or speed.get("flying", "")
        speed_swimming = speed.get("swim", "") or speed.get("swimming", "")
    else:
        speed_walking = speed
    description_html = species.get("description_html") or _species_entries_to_html(
        species.get("entries", [])
    )
    description_text = _strip_html(description_html)
    if not description_text:
        description_text = str(species.get("name", "")).strip()
    racial_trait_intro = species.get("racial_trait_intro")
    if not racial_trait_intro:
        racial_trait_intro = _species_intro_from_entries(
            species.get("entries", []), str(species.get("name", ""))
        )
    return {
        "name": species.get("name", ""),
        "version": "",
        "size": _map_enum(size_value, _SIZE_MAP),
        "speed-walking": _clean_number(speed_walking or ""),
        "speed-burrowing": _clean_number(speed_burrowing or ""),
        "speed-climbing": _clean_number(speed_climbing or ""),
        "speed-flying": _clean_number(speed_flying or ""),
        "speed-swimming": _clean_number(speed_swimming or ""),
        "short-description-type": "1",
        "short-description-wysiwyg": species.get("short_description_html", ""),
        "short-description": "",
        "race-group": species.get("race_group", ""),
        "description-type": "1",
        "description-wysiwyg": description_html,
        "description": description_text,
        "racial-trait-introduction": racial_trait_intro,
    }


def _background_text_to_html(text) -> str:
    if not text:
        return ""
    if isinstance(text, list):
        chunks = [str(t).strip() for t in text if str(t).strip()]
        return "\n".join(f"<p>{chunk}</p>" for chunk in chunks)
    value = str(text).strip()
    if not value:
        return ""
    paragraphs = [p.strip() for p in value.split("\n") if p.strip()]
    return "\n".join(f"<p>{p}</p>" for p in paragraphs)


def _strip_html(value: str) -> str:
    if not value:
        return ""
    return re.sub(r"<[^>]+>", "", value).strip()


def _extract_background_items(entries) -> Dict[str, str]:
    sections = {
        "skill_proficiencies": "",
        "tool_proficiencies": "",
        "languages": "",
        "equipment": "",
        "feature_name": "",
        "feature_description": "",
    }
    if not entries:
        return sections
    for entry in entries:
        if isinstance(entry, dict) and entry.get("type") == "list":
            for item in entry.get("items", []) or []:
                if not isinstance(item, dict):
                    continue
                name = str(item.get("name", "")).strip().lower()
                value = item.get("entry", "")
                if name == "skill proficiencies":
                    sections["skill_proficiencies"] = value
                elif name == "tool proficiencies":
                    sections["tool_proficiencies"] = value
                elif name == "languages":
                    sections["languages"] = value
                elif name == "equipment":
                    sections["equipment"] = value
        if (
            isinstance(entry, dict)
            and entry.get("type") == "entries"
            and entry.get("data", {}).get("isFeature")
        ):
            sections["feature_name"] = str(entry.get("name", "")).strip()
            sections["feature_description"] = entry.get("entries", [])
    return sections


def convert_background_to_ddb(background: Dict) -> Dict:
    """Convert background data to D&D Beyond form fields for background creation."""
    entries = background.get("entries", [])
    sections = _extract_background_items(entries)
    short_description = background.get("short_description_html") or ""
    if not short_description:
        summary_parts = []
        if sections["skill_proficiencies"]:
            summary_parts.append(
                f"Skill Proficiencies: {sections['skill_proficiencies']}"
            )
        if sections["tool_proficiencies"]:
            summary_parts.append(
                f"Tool Proficiencies: {sections['tool_proficiencies']}"
            )
        if sections["languages"]:
            summary_parts.append(f"Languages: {sections['languages']}")
        if sections["equipment"]:
            summary_parts.append(f"Equipment: {sections['equipment']}")
        if sections["feature_description"] and not summary_parts:
            summary_parts.append(sections["feature_description"])
        short_description = _background_text_to_html(summary_parts)

    short_description_text = _strip_html(short_description)
    form_data = {
        "name": background.get("name", ""),
        "version": "",
        "short-description-type": "1",
        "short-description-wysiwyg": short_description,
        "short-description": short_description_text,
        "feature-name": sections["feature_name"],
        "feature-description-type": "1",
        "feature-description-wysiwyg": _background_text_to_html(
            sections["feature_description"]
        ),
        "feature-description": "",
        "skill-proficiencies-description-type": "1",
        "skill-proficiencies-description-wysiwyg": _background_text_to_html(
            sections["skill_proficiencies"]
        ),
        "skill-proficiencies-description": "",
        "tool-proficiencies-description-type": "1",
        "tool-proficiencies-description-wysiwyg": _background_text_to_html(
            sections["tool_proficiencies"]
        ),
        "tool-proficiencies-description": "",
        "languages-description-type": "1",
        "languages-description-wysiwyg": _background_text_to_html(
            sections["languages"]
        ),
        "languages-description": "",
        "equipment-description-type": "1",
        "equipment-description-wysiwyg": _background_text_to_html(
            sections["equipment"]
        ),
        "equipment-description": "",
        "background-tags-public": _listify(
            background.get("traitTags") or background.get("tags")
        ),
    }

    keep_empty = (
        "short-description",
        "feature-description",
        "skill-proficiencies-description",
        "tool-proficiencies-description",
        "languages-description",
        "equipment-description",
    )
    return {k: v for k, v in form_data.items() if v != "" or k in keep_empty}


def _feat_entries_to_html(entries) -> str:
    if not entries:
        return ""
    parts = []
    for entry in entries:
        if isinstance(entry, str):
            text = entry.strip()
            if text:
                parts.append(f"<p>{text}</p>")
            continue
        if isinstance(entry, dict) and entry.get("type") == "entries":
            name = entry.get("name", "").strip()
            sub_entries = entry.get("entries", [])
            sub_text = " ".join(str(e).strip() for e in sub_entries if str(e).strip())
            if name and sub_text:
                parts.append(f"<p><strong>{name}.</strong> {sub_text}</p>")
            elif sub_text:
                parts.append(f"<p>{sub_text}</p>")
            continue
        text = str(entry).strip()
        if text:
            parts.append(f"<p>{text}</p>")
    return "\n".join(parts)


def convert_feat_to_ddb(feat: Dict) -> Dict:
    """Convert feat data to D&D Beyond form fields for feat creation."""
    description_html = feat.get("description_html") or _feat_entries_to_html(
        feat.get("entries", [])
    )
    description_text = _strip_html(description_html)
    snippet = feat.get("snippet")
    if not snippet:
        snippet = description_text.split(".")[0].strip()

    return {
        "name": feat.get("name", ""),
        "version": "",
        "item-description-type": "1",
        "item-description-wysiwyg": description_html,
        "item-description": description_text,
        "snippet": snippet,
        "feat-tags-public": _listify(feat.get("feat_tags") or feat.get("tags")),
    }


# ============================================
# Spell Conditions and Scaling Helpers
# ============================================

_CONDITION_MAP = {
    "blinded": "1",
    "charmed": "2",
    "deafened": "3",
    "exhaustion": "4",
    "frightened": "5",
    "grappled": "6",
    "incapacitated": "7",
    "invisible": "8",
    "paralyzed": "9",
    "petrified": "10",
    "poisoned": "11",
    "prone": "12",
    "restrained": "13",
    "stunned": "14",
    "unconscious": "15",
}


def extract_spell_conditions(spell: Dict) -> List[Dict]:
    """Extract condition data from spell for D&D Beyond condition creation.

    Args:
        spell: Spell dict with optional 'ddb_condition' field

    Returns:
        List of condition data dicts ready for create_condition API call
    """
    conditions = []
    condition_text = spell.get("ddb_condition", "").strip()

    if not condition_text:
        return conditions

    # Split by comma if multiple conditions
    condition_names = [c.strip().lower() for c in condition_text.split(",")]

    for condition_name in condition_names:
        if condition_name in _CONDITION_MAP:
            conditions.append({
                "condition_effect": "1",  # Grants condition
                "condition": _CONDITION_MAP[condition_name],
                "condition_duration": "",  # Leave blank for "spell duration"
                "duration_unit": "",
                "condition_exception": ""
            })

    return conditions


def extract_spell_modifiers(spell: Dict) -> List[Dict]:
    """Extract modifier data from spell for D&D Beyond modifier creation.

    Prioritizes the "Modifiers JSON" column which can contain multiple modifiers.
    Falls back to individual columns if JSON is not available.

    Args:
        spell: Spell dict with optional 'ddb_modifiers_json' or 'ddb_modifier_*' fields

    Returns:
        List of modifier data dicts ready for create_modifier API call
    """
    modifiers = []

    # First, try to load from JSON column (supports multiple modifiers)
    modifiers_json = spell.get("ddb_modifiers_json", "").strip()
    if modifiers_json:
        try:
            import json
            parsed = json.loads(modifiers_json)
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass  # Fall back to individual columns

    # Fallback: Check if modifier data exists in individual CSV columns
    modifier_type = spell.get("ddb_modifier_type", "").strip()

    if not modifier_type:
        return modifiers

    # Build modifier dict from CSV columns (single modifier)
    modifier = {
        "type": modifier_type,
        "subtype": spell.get("ddb_modifier_subtype", "").strip(),
        "dice_count": spell.get("ddb_modifier_dice_count", "").strip(),
        "dice_type": spell.get("ddb_modifier_dice_type", "").strip(),
        "fixed_value": spell.get("ddb_modifier_fixed_value", "").strip(),
        "duration": spell.get("ddb_modifier_duration", "").strip(),
        "duration_unit": spell.get("ddb_modifier_duration_unit", "").strip(),
    }

    modifiers.append(modifier)
    return modifiers


def extract_spell_scaling(spell: Dict) -> Optional[str]:
    """Extract scaling description from spell.

    This returns the "At Higher Levels" text description.
    For structured dice scaling, see parse_dice_scaling().

    Args:
        spell: Spell dict with optional 'ddb_scaling' field

    Returns:
        Scaling description text or None
    """
    scaling = spell.get("ddb_scaling", "").strip()
    if scaling:
        return scaling

    # Fallback to entriesHigherLevel if available
    higher_entries = spell.get("entriesHigherLevel", [])
    if higher_entries and isinstance(higher_entries, list):
        for entry in higher_entries:
            if isinstance(entry, dict):
                entries = entry.get("entries", [])
                if entries:
                    return " ".join(str(e) for e in entries)

    return None


def parse_dice_scaling(scaling_text: str) -> List[Dict]:
    """Parse dice scaling from text (e.g., "1d6 per spell level above 1st").

    This is for structured scaling like:
    - "The damage increases by 1d6 for each slot level above 1st"
    - "Add 1d8 fire damage per level"

    Args:
        scaling_text: Free-form scaling description

    Returns:
        List of higher level data dicts for create_higher_level API

    Note: This is a simple parser. For complex scaling, you may need to
          manually format the Scaling column with structured data like:
          "3:2d6,5:3d6,7:4d6" (level:dice format)
    """
    higher_levels = []

    if not scaling_text:
        return higher_levels

    # Try to parse structured format: "3:2d6,5:3d6,7:4d6"
    if ":" in scaling_text and "," in scaling_text:
        try:
            for pair in scaling_text.split(","):
                level_str, dice_str = pair.strip().split(":")
                level = int(level_str.strip())

                # Parse dice (e.g., "2d6")
                match = re.match(r"(\d+)d(\d+)(?:\+(\d+))?", dice_str.strip())
                if match:
                    dice_count = match.group(1)
                    dice_value = match.group(2)
                    dice_fixed = match.group(3) or ""

                    higher_levels.append({
                        "level": str(level),
                        "modifier": "",  # Not used for damage scaling
                        "effect_type": "16",  # Damage
                        "dice_count": dice_count,
                        "dice_value": dice_value,
                        "dice_fixed": dice_fixed,
                        "dice_details": ""
                    })
        except (ValueError, AttributeError):
            pass  # Fall through to text parsing

    # Simple text parsing (fallback)
    # Look for patterns like "1d6" or "2d8+3"
    dice_matches = re.findall(r"(\d+)d(\d+)(?:\+(\d+))?", scaling_text)
    if dice_matches and not higher_levels:
        # Create a simple scaling entry
        dice_count, dice_value, dice_fixed = dice_matches[0]
        higher_levels.append({
            "level": "1",  # Default: starts at spell level + 1
            "modifier": "",
            "effect_type": "16",  # Damage
            "dice_count": dice_count,
            "dice_value": dice_value,
            "dice_fixed": dice_fixed or "",
            "dice_details": scaling_text[:100]  # Include original text
        })

    return higher_levels
