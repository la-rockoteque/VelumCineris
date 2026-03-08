import pandas as pd
from FiveETools.core.modern.sources import source, json_source
try:
    from scripts.image_generator import generate_icon
except ImportError:
    generate_icon = None  # Optional dependency
from FiveETools.core.Helpers.gsheets_client import modern_sheets
import inflection
import urllib.parse
import json
import time

df_spells = modern_sheets.get_sheet_by_name("spells")
df_spells.head()

import json
import hashlib


def row_to_spell(row):
    # Basic normalization
    components_str = row.get("Components", "")
    components_set = {comp.strip().upper() for comp in str(components_str).split(",")}
    spell_classes = [
        cls.strip() for cls in str(row.get("Class", "")).split(",") if cls.strip()
    ]
    ability_checks = [
        cls.strip().lower()
        for cls in str(row.get("Ability Check", "")).split(",")
        if cls.strip()
    ]
    misc_tags = [
        cls.strip() for cls in str(row.get("Tag ABRV", "")).split(",") if cls.strip()
    ]
    damages = [
        cls.strip().lower()
        for cls in str(row.get("Old Damage Type", "")).split(",")
        if cls.strip()
    ]
    saving_throws = [
        cls.strip().lower()
        for cls in str(row.get("Saving Throw", "")).split(",")
        if cls.strip()
    ]
    areas = [
        cls.strip() for cls in str(row.get("Area ABRV", "")).split(",") if cls.strip()
    ]
    # Parse components if they are stored as a string like "V, S, M"
    components_str = row.get("Components ABVR", "")
    duration_type = (
        row.get("Duration Type").lower()
        if not pd.isnull(row.get("Duration Type"))
        else "timed"
    )
    duration_unit = (
        row.get("Duration Unit").lower()
        if not pd.isnull(row.get("Duration Unit"))
        else "minutes"
    )
    duration_amount = (
        int(row.get("Duration Amount"))
        if not pd.isnull(row.get("Duration Amount"))
        else 1
    )
    range_distance = (
        row.get("Range Distance").lower()
        if not pd.isnull(row.get("Range Distance"))
        else "self"
    )
    base_url = "https://raw.githubusercontent.com/la-rockoteque/Vestigium/refs/heads/main/images/Spell"
    components_set = {comp.strip().upper() for comp in str(components_str).split(",")}
    spell = {
        "source": json_source,
        "name": row.get("Spell Name", "Unnamed Spell"),
        "level": int(row["Level"][0]) if not pd.isnull(row.get("Level")[0]) else 0,
        "school": row.get("School ABRV", "E"),
        "time": [
            {
                "number": row.get("Casting Unit", 1),
                "unit": row.get("Casting Type", "action").lower(),
            }
        ],
        "range": {
            "type": row.get("Range Type", "point").lower(),
            "distance": {
                "type": range_distance,
                **(
                    {"amount": row.get("Range Unit")}
                    if not pd.isnull(row.get("Range Unit"))
                    else {}
                ),
            },
        },
        "duration": [
            {
                "type": duration_type,
                **(
                    {
                        "duration": {
                            "type": duration_unit,
                            "amount": duration_amount,
                            "upTo": True
                            if row.get("Up To", "FALSE") == "TRUE"
                            else False,
                        }
                    }
                    if duration_type == "timed"
                    else {}
                ),
                **(
                    {
                        "concentration": True
                        if row.get("Concentration", "FALSE") == "TRUE"
                        else False
                    }
                    if duration_type == "timed"
                    else {}
                ),
            }
        ],
        "classes": {
            "fromClassList": [
                {"name": cls, "source": "VSTGCC"} for cls in spell_classes
            ]
        },
        "entries": [row.get("Description")]
        + (
            [row.get("Clarification")]
            if not pd.isnull(row.get("Clarification"))
            else []
        )
        + ([row.get("Table")] if not pd.isnull(row.get("Table")) else []),
        "source": "VestigiumGuidetoConcordCity",
        **(
            {
                "entriesHigherLevel": [
                    {
                        "type": "entries",
                        "name": "At Higher Levels",
                        "entries": [row.get("Higher Levels", "")]
                        if not pd.isnull(row.get("Higher Levels"))
                        else [],
                    }
                ]
            }
            if not pd.isnull(row.get("Higher Levels"))
            else {}
        ),
        "components": {
            "v": "V" in components_set,
            "s": "S" in components_set,
            "r": "R" in components_set,
        },
        **(
            {"abilityCheck": ability_checks}
            if not pd.isnull(row.get("Ability Check"))
            else {}
        ),
        **({"miscTags": misc_tags} if not pd.isnull(row.get("Tag ABRV")) else {}),
        **(
            {"damageInflict": damages}
            if not pd.isnull(row.get("Old Damage Type"))
            else {}
        ),
        "fluff": {
            "entries": []
            + ([row.get("Flavor")] if not pd.isnull(row.get("Flavor")) else [])
            + (
                [row.get("Alternative Flavor")]
                if not pd.isnull(row.get("Alternative Flavor"))
                else []
            )
            + ([row.get("Quotes")] if not pd.isnull(row.get("Quotes")) else []),
            "images": [
                {
                    "type": "image",
                    "href": {
                        "type": "external",
                        "url": f"{base_url}/{urllib.parse.quote(inflection.underscore(row.get('Spell Name', 'Unnamed Spell')))}.png",
                    },
                }
            ],
        },
        **(
            {"savingThrow": saving_throws}
            if not pd.isnull(row.get("Saving Throw"))
            else {}
        ),
        **({"areaTags": areas} if not pd.isnull(row.get("Area ABRV")) else {}),
    }
    return spell


spells_list = [
    row_to_spell(row)
    for index, row in df_spells.iterrows()
    if pd.notnull(row.get("Spell Name"))
    and str(row.get("Spell Name")).strip() != ""
    and row.get("Source") == source
]

# NEW: Pydantic-based conversion for type safety
from Spreadsheet.core.converters.spell import SpellConverter
from models.entities.spell import Spell
from typing import List

converter = SpellConverter(modern_sheets)
spells_pydantic: List[Spell] = converter.convert_all(
    source_filter=source,
    source=source,
    json_source=json_source
)
