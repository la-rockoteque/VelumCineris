import pandas as pd
from FiveETools.core.modern.sources import source, json_source
from FiveETools.core.Helpers.gsheets_client import modern_sheets
import inflection
try:
    from scripts.image_generator import generate_icon
except ImportError:
    generate_icon = None  # Optional dependency

df_item_properties = modern_sheets.get_sheet_by_name("item_properties")
df_item_properties.head()


def row_to_property(row):
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


item_property_list = [
    row_to_property(row)
    for index, row in df_item_properties.iterrows()
    if pd.notnull(row.get("Name")) and str(row.get("Name")).strip() != ""
]
# %%
df_items = modern_sheets.get_sheet_by_name("items")
df_items.head()


def row_to_item(row):
    properties = (
        row.get("Property ABRV") if not pd.isnull(row.get("Property ABRV")) else []
    )
    attached_spells = (
        row.get("Attached Spells") if not pd.isnull(row.get("Attached Spells")) else []
    )
    type = row.get("Type ABRV") if not pd.isnull(row.get("Type ABRV")) else "OTH"
    item = {
        "name": row.get("Name", "Generic Item"),
        "source": json_source,
        "type": type,
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
        # "currencyConversion": "credit",
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
        # "images": [
        #   {
        #     "type": "image",
        #     "href": {
        #       "type": "external",
        #       "url": generate_icon("Item", row.get("Name", "Magic Item"))
        #     }
        #   }
        # ]
    }
    return item


items_list = [
    row_to_item(row)
    for index, row in df_items.iterrows()
    if pd.notnull(row.get("Name"))
    and str(row.get("Name")).strip() != ""
    and row.get("Source") == source
]

# NEW: Pydantic-based conversion for type safety
from Spreadsheet.core.converters.item import ItemConverter
from models.entities.item import Item
from typing import List

converter = ItemConverter(modern_sheets)
items_pydantic: List[Item] = converter.convert_all(
    source_filter=source,
    source=source,
    json_source=json_source
)
