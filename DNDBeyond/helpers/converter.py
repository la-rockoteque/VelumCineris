"""Convert 5etools spell format to D&D Beyond format"""
from typing import Dict


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
    # AOE (Area of Effect)
    aoe_type = ""
    aoe_size = ""
    if isinstance(range_data, dict):
        aoe_data = range_data.get("type", "")
        if aoe_data in ["cone", "cube", "cylinder", "line", "sphere", "radius"]:
            # Map 5etools AOE types to D&D Beyond IDs
            aoe_map = {"cone": "1", "cube": "2", "cylinder": "3", "line": "4", "sphere": "5", "radius": "5"}
            aoe_type = aoe_map.get(aoe_data, "")

            # Get AOE size
            distance = range_data.get("distance", {})
            if isinstance(distance, dict) and "amount" in distance:
                aoe_size = str(int(distance.get("amount", 0)))

    # Save type (from spell text analysis)
    save_type = ""
    attack_type = ""
    full_text = description.lower()

    # Check for saving throws
    if "strength saving throw" in full_text or "strength save" in full_text:
        save_type = "1"  # Strength
    elif "dexterity saving throw" in full_text or "dexterity save" in full_text:
        save_type = "2"  # Dexterity
    elif "constitution saving throw" in full_text or "constitution save" in full_text:
        save_type = "3"  # Constitution
    elif "intelligence saving throw" in full_text or "intelligence save" in full_text:
        save_type = "4"  # Intelligence
    elif "wisdom saving throw" in full_text or "wisdom save" in full_text:
        save_type = "5"  # Wisdom
    elif "charisma saving throw" in full_text or "charisma save" in full_text:
        save_type = "6"  # Charisma

    # Check for spell attacks
    if "ranged spell attack" in full_text:
        attack_type = "1"  # Ranged spell attack
    elif "melee spell attack" in full_text:
        attack_type = "2"  # Melee spell attack

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
        # Additional fields for update endpoints
        "aoe_type": aoe_type,
        "aoe_size": aoe_size,
        "save_type": save_type,
        "attack_type": attack_type,
        "on_miss": "",  # Not extractable from 5etools format
        "save_success": "",  # Not extractable from 5etools format
        "save_fail": "",  # Not extractable from 5etools format
    }

    return result
