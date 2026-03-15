from __future__ import annotations

from fractions import Fraction
from typing import Any

import pandas as pd


def map_modern_monster_row(
    row: Any,
    *,
    json_source: str,
    text_fn,
    parse_speed_fn,
    parse_entries_fn,
    parse_saves_fn,
    parse_skills_fn,
    parse_immunities_fn,
) -> dict[str, Any]:
    name = row.get("Name")
    size = text_fn(row.get("Size"), "M")[:1].upper()
    creature_type = text_fn(row.get("Type"), "humanoid").lower()
    alignment = text_fn(row.get("Alignment"), "U")[:1].upper()
    hit_dice = text_fn(row.get("Hit Dice"))
    con_mod = text_fn(row.get("CON Mod"), "0")
    cr_raw = row.get("CR (Challenge Rating)")
    cr_value = "0"
    if pd.notnull(cr_raw):
        try:
            cr_value = f"{Fraction(cr_raw)}"
        except (ValueError, ZeroDivisionError, TypeError):
            cr_value = text_fn(cr_raw, "0")
    walk_speed = parse_speed_fn(row.get("Speed (Walking)"))
    fly_speed = parse_speed_fn(row.get("Speed (Flying)"))
    swim_speed = parse_speed_fn(row.get("Speed (Swimming)"))
    burrow_speed = parse_speed_fn(row.get("Speed (Burrowing)"))
    if walk_speed is None:
        walk_speed = 0

    return {
        "source": json_source,
        "name": name,
        "size": [size],
        "type": creature_type,
        "alignment": [alignment],
        "ac": [
            {
                "ac": row.get("Armor Class"),
                "from": [
                    row.get("Armor Type")
                    if pd.notnull(row.get("Armor Type"))
                    else "natural armor"
                ],
            }
        ],
        "hp": {
            "average": row.get("Hit Points"),
            "formula": f"{hit_dice.lower()} + {con_mod}",
        },
        **(
            {"save": parse_saves_fn(row.get("Saving Throws"))}
            if pd.notnull(row.get("Saving Throws"))
            else {}
        ),
        "passive": row.get("Passive Perception"),
        "speed": {
            **(
                {"walk": walk_speed}
                if walk_speed is not None
                else {}
            ),
            **(
                {"fly": fly_speed}
                if fly_speed is not None
                else {}
            ),
            **(
                {"swim": swim_speed}
                if swim_speed is not None
                else {}
            ),
            **(
                {"burrow": burrow_speed}
                if burrow_speed is not None
                else {}
            ),
        },
        "str": row.get("STR"),
        "dex": row.get("DEX"),
        "con": row.get("CON"),
        "int": row.get("INT"),
        "wis": row.get("WIS"),
        "cha": row.get("CHA"),
        **(
            {"action": parse_entries_fn(row.get("Actions"))}
            if pd.notnull(row.get("Actions"))
            else {}
        ),
        **(
            {"reaction": parse_entries_fn(row.get("Reactions"))}
            if pd.notnull(row.get("Reactions"))
            else {}
        ),
        **(
            {
                "legendaryActions": 3,
                "legendaryHeader": [
                    (
                        f"The {name} can take 3 legendary actions, choosing from the options "
                        "below. Only one legendary action can be used at a time and only at "
                        f"the end of another creature's turn. The {name} regains spent legendary "
                        "actions at the start of its turn."
                    )
                ],
                "legendary": parse_entries_fn(row.get("Legendary Actions")),
            }
            if pd.notnull(row.get("Legendary Actions"))
            else {}
        ),
        **(
            {"trait": parse_entries_fn(row.get("Traits"))}
            if pd.notnull(row.get("Traits"))
            else {}
        ),
        **(
            {"skill": parse_skills_fn(row.get("Skills"))}
            if pd.notnull(row.get("Skills"))
            else {}
        ),
        **(
            {"immune": parse_immunities_fn(row.get("Damage Immunities"))}
            if pd.notnull(row.get("Damage Immunities"))
            else {}
        ),
        **(
            {
                "conditionImmune": text_fn(row.get("Condition Immunities"))
                .lower()
                .split(", ")
            }
            if pd.notnull(row.get("Condition Immunities"))
            else {}
        ),
        "cr": cr_value,
        "tokenUrl": row.get("Tokens URL"),
        "fluff": {
            "entries": [row.get("Description")],
            "images": [
                {
                    "type": "image",
                    "href": {
                        "type": "external",
                        "url": row.get("Image URL"),
                    },
                }
            ],
        },
    }


def map_fantasy_monster_row(
    row: Any,
    *,
    json_source: str,
    parse_speed_fn,
    parse_entries_fn,
    parse_saves_fn,
    parse_skills_fn,
    parse_immunities_fn,
) -> dict[str, Any]:
    name = row.get("Name")
    return {
        "source": json_source,
        "name": name,
        "size": [row.get("Size")[:1].upper()],
        "type": row.get("Type").lower(),
        "alignment": [row.get("Alignment")[:1].upper()],
        "ac": [
            {
                "ac": row.get("Armor Class"),
                "from": [
                    row.get("Armor Type")
                    if pd.notnull(row.get("Armor Type"))
                    else "natural armor"
                ],
            }
        ],
        "hp": {
            "average": row.get("Hit Points"),
            "formula": f"{row.get('Hit Dice').lower()} + {row.get('CON Mod')}",
        },
        **(
            {"save": parse_saves_fn(row.get("Saving Throws"))}
            if pd.notnull(row.get("save"))
            else {}
        ),
        "passive": row.get("Passive Perception"),
        "speed": {
            **(
                {"walk": walk_speed}
                if (walk_speed := parse_speed_fn(row.get("Speed (Walking)"))) is not None
                else {}
            ),
            **(
                {"fly": fly_speed}
                if (fly_speed := parse_speed_fn(row.get("Speed (Flying)"))) is not None
                else {}
            ),
            **(
                {"swim": swim_speed}
                if (swim_speed := parse_speed_fn(row.get("Speed (Swimming)"))) is not None
                else {}
            ),
            **(
                {"burrow": burrow_speed}
                if (burrow_speed := parse_speed_fn(row.get("Speed (Burrowing)"))) is not None
                else {}
            ),
        },
        "str": int(row.get("STR")),
        "dex": int(row.get("DEX")),
        "con": int(row.get("CON")),
        "int": int(row.get("INT")),
        "wis": int(row.get("WIS")),
        "cha": int(row.get("CHA")),
        **(
            {"action": parse_entries_fn(row.get("Actions"))}
            if pd.notnull(row.get("Actions"))
            else {}
        ),
        **(
            {"reaction": parse_entries_fn(row.get("Reactions"))}
            if pd.notnull(row.get("Reactions"))
            else {}
        ),
        **(
            {
                "legendaryActions": 3,
                "legendaryHeader": [
                    (
                        f"The {name} can take 3 legendary actions, choosing from the options "
                        "below. Only one legendary action can be used at a time and only at "
                        f"the end of another creature's turn. The {name} regains spent legendary "
                        "actions at the start of its turn."
                    )
                ],
                "legendary": parse_entries_fn(row.get("Legendary Actions")),
            }
            if pd.notnull(row.get("Legendary Actions"))
            else {}
        ),
        **(
            {"trait": parse_entries_fn(row.get("Traits"))}
            if pd.notnull(row.get("Traits"))
            else {}
        ),
        **(
            {"skill": parse_skills_fn(row.get("Skills"))}
            if pd.notnull(row.get("Skills"))
            else {}
        ),
        **(
            {"immune": parse_immunities_fn(row.get("Damage Immunities"))}
            if pd.notnull(row.get("Damage Immunities"))
            else {}
        ),
        **(
            {"conditionImmune": row.get("Condition Immunities").lower().split(", ")}
            if pd.notnull(row.get("Condition Immunities"))
            else {}
        ),
        "cr": f"{Fraction(row.get('CR (Challenge Rating)'))}",
        "tokenUrl": row.get("Tokens URL"),
        "fluff": {
            "entries": [row.get("Description")],
            "images": [
                {
                    "type": "image",
                    "href": {
                        "type": "external",
                        "url": row.get("Image URL"),
                    },
                }
            ],
        },
    }
