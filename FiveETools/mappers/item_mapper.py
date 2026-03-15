from __future__ import annotations

from typing import Any

import inflection
import pandas as pd


def map_item_property_row(row: Any, *, json_source: str) -> dict[str, Any]:
    return {
        "abbreviation": row.get("ABRV"),
        "source": json_source,
        "entries": [
            {
                "name": inflection.humanize(row.get("Name", "Generic Property")),
                "type": "entries",
                "entries": [row.get("Entry")],
            }
        ],
    }


def map_item_row(row: Any, *, json_source: str) -> dict[str, Any]:
    properties = (
        row.get("Property ABRV") if not pd.isnull(row.get("Property ABRV")) else []
    )
    attached_spells = (
        row.get("Attached Spells") if not pd.isnull(row.get("Attached Spells")) else []
    )
    item_type = row.get("Type ABRV") if not pd.isnull(row.get("Type ABRV")) else "OTH"
    return {
        "name": row.get("Name", "Generic Item"),
        "source": json_source,
        "type": item_type,
        "value": row.get("Value", ""),
        "weight": row.get("Weight", ""),
        "page": row.get("Page", ""),
        "rarity": "none",
        **(
            {"recharge": row.get("Recharge", "")}
            if not pd.isnull(row.get("Recharge"))
            else {}
        ),
        **(
            {"reqAttunement": row.get("Require Attunement", "")}
            if not pd.isnull(row.get("Require Attunement"))
            else {}
        ),
        **(
            {"attachedSpells": [spell for spell in attached_spells.split(", ")]}
            if not pd.isnull(row.get("Attached Spells"))
            else {}
        ),
        **(
            {"baseItem": row.get("Base Item", "")}
            if not pd.isnull(row.get("Base Item"))
            else {}
        ),
        **({"tier": row.get("Tier", "")} if not pd.isnull(row.get("Tier")) else {}),
        **(
            {"weaponCategory": row.get("Category", "")}
            if not pd.isnull(row.get("Category"))
            else {}
        ),
        **(
            {"property": [property for property in properties.split(", ")]}
            if not pd.isnull(row.get("Property"))
            else {}
        ),
        **(
            {"dmg1": row.get("Damage 1", "")}
            if not pd.isnull(row.get("Damage 1"))
            else {}
        ),
        **(
            {"dmg2": row.get("Damage 2", "")}
            if not pd.isnull(row.get("Damage 2"))
            else {}
        ),
        **(
            {"dmgType": row.get("Damage Type", "")}
            if not pd.isnull(row.get("Damage Type"))
            else {}
        ),
        **({"range": row.get("Range", "")} if not pd.isnull(row.get("Range")) else {}),
        **(
            {"bonusWeapon": row.get("Bonus Weapon", "")}
            if not pd.isnull(row.get("Bonus Weapon"))
            else {}
        ),
        **(
            {
                "entries": [row.get("Description", "")],
            }
            if not pd.isnull(row.get("Description"))
            else {}
        ),
    }
