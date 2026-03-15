from __future__ import annotations

from typing import Any

import pandas as pd


def map_magic_item_row(row: Any, *, json_source: str) -> dict[str, Any]:
    properties = row.get("Property") if not pd.isnull(row.get("Property")) else []
    attached_spells = (
        row.get("Attached Spells") if not pd.isnull(row.get("Attached Spells")) else []
    )
    return {
        "name": row.get("Name", "Magic Item"),
        "source": json_source,
        "type": row.get("Type ABRV", "") or "OTH",
        "rarity": row.get("Rarity", "").lower(),
        "value": row.get("Value", ""),
        "weight": row.get("Weight", ""),
        "page": 0,
        "wondrous": True,
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
            {"properties": [f"VS{property[2:]}" for property in properties]}
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
        **(
            {"range": row.get("Extracted Range", "")}
            if not pd.isnull(row.get("Extracted Range"))
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
