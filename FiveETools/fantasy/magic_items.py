import pandas as pd
from FiveETools.fantasy.sources import source, json_source
try:
    from scripts.image_generator import generate_icon
except ImportError:
    generate_icon = None  # Optional dependency
from FiveETools.gsheets_client import fantasy_sheets
import inflection

df_magic_items = fantasy_sheets.get_sheet("695912920")
df_magic_items.head()


def row_to_magic_item(row):
    properties = row.get("Property") if not pd.isnull(row.get("Property")) else []
    attached_spells = (
        row.get("Attached Spells") if not pd.isnull(row.get("Attached Spells")) else []
    )
    item = {
        "name": row.get("Name", "Magic Item"),
        "source": json_source,
        "type": row.get("Type ABRV", "") or "OTH",
        "rarity": row.get("Rarity", "").lower(),
        "value": row.get("Value", ""),
        "weight": row.get("Weight", ""),
        "page": 0,
        # "currencyConversion": "credit",
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
        # "images": [
        #   {
        #     "type": "image",
        #     "href": {
        #       "type": "external",
        #       "url": generate_icon("Magic Item", row.get("Name", "Magic Item"))
        #     }
        #   }
        # ]
    }
    return item


magic_items_list = [
    row_to_magic_item(row)
    for index, row in df_magic_items.iterrows()
    if pd.notnull(row.get("Name"))
    and str(row.get("Name")).strip() != ""
    and row.get("Source") == source
]

# NEW: Pydantic-based conversion for type safety
from Spreadsheet.converters.magic_item import MagicItemConverter
from models.entities.magic_item import MagicItem
from typing import List

converter = MagicItemConverter(fantasy_sheets)
magic_items_pydantic: List[MagicItem] = converter.convert_all(
    source_filter=source,
    source=source,
    json_source=json_source
)
