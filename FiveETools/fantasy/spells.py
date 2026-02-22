import pandas as pd
from FiveETools.fantasy.sources import source, json_source
try:
    from scripts.image_generator import generate_icon
except ImportError:
    generate_icon = None  # Optional dependency
from FiveETools.gsheets_client import fantasy_sheets
import inflection
import urllib.parse
import json
import time

df_spells = fantasy_sheets.get_sheet("625265890")
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
        # DDB-specific fields for Additional Information section
        **(
            {"ddb_save_success": str(row.get("Success", "")).strip()}
            if not pd.isnull(row.get("Success")) and str(row.get("Success")).strip()
            else {}
        ),
        **(
            {"ddb_save_fail": str(row.get("Fail", "")).strip()}
            if not pd.isnull(row.get("Fail")) and str(row.get("Fail")).strip()
            else {}
        ),
        **(
            {"ddb_area_type": str(row.get("Area Type", "")).strip()}
            if not pd.isnull(row.get("Area Type")) and str(row.get("Area Type")).strip()
            else {}
        ),
        **(
            {"ddb_area_distance": str(row.get("Area Distance", "")).strip()}
            if not pd.isnull(row.get("Area Distance")) and str(row.get("Area Distance")).strip()
            else {}
        ),
        **(
            {"ddb_damage": str(row.get("Damage", "")).strip()}
            if not pd.isnull(row.get("Damage")) and str(row.get("Damage")).strip()
            else {}
        ),
        # DDB-specific: Conditions and Scaling
        **(
            {"ddb_condition": str(row.get("Condition", "")).strip()}
            if not pd.isnull(row.get("Condition")) and str(row.get("Condition")).strip()
            else {}
        ),
        **(
            {"ddb_scaling": str(row.get("Scaling", "")).strip()}
            if not pd.isnull(row.get("Scaling")) and str(row.get("Scaling")).strip()
            else {}
        ),
        # DDB-specific: Modifiers (JSON column for all modifiers)
        **(
            {"ddb_modifiers_json": str(row.get("Modifiers JSON", "")).strip()}
            if not pd.isnull(row.get("Modifiers JSON")) and str(row.get("Modifiers JSON")).strip()
            else {}
        ),
        # DDB-specific: Individual modifier columns (primary modifier for readability)
        **(
            {"ddb_modifier_type": str(row.get("Modifier Type", "")).strip()}
            if not pd.isnull(row.get("Modifier Type")) and str(row.get("Modifier Type")).strip()
            else {}
        ),
        **(
            {"ddb_modifier_subtype": str(row.get("Modifier Subtype", "")).strip()}
            if not pd.isnull(row.get("Modifier Subtype")) and str(row.get("Modifier Subtype")).strip()
            else {}
        ),
        **(
            {"ddb_modifier_dice_count": str(row.get("Modifier Dice Count", "")).strip()}
            if not pd.isnull(row.get("Modifier Dice Count")) and str(row.get("Modifier Dice Count")).strip()
            else {}
        ),
        **(
            {"ddb_modifier_dice_type": str(row.get("Modifier Dice Type", "")).strip()}
            if not pd.isnull(row.get("Modifier Dice Type")) and str(row.get("Modifier Dice Type")).strip()
            else {}
        ),
        **(
            {"ddb_modifier_fixed_value": str(row.get("Modifier Fixed Value", "")).strip()}
            if not pd.isnull(row.get("Modifier Fixed Value")) and str(row.get("Modifier Fixed Value")).strip()
            else {}
        ),
        **(
            {"ddb_modifier_duration": str(row.get("Modifier Duration", "")).strip()}
            if not pd.isnull(row.get("Modifier Duration")) and str(row.get("Modifier Duration")).strip()
            else {}
        ),
        **(
            {"ddb_modifier_duration_unit": str(row.get("Modifier Duration Unit", "")).strip()}
            if not pd.isnull(row.get("Modifier Duration Unit")) and str(row.get("Modifier Duration Unit")).strip()
            else {}
        ),
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
from Spreadsheet.converters.spell import SpellConverter
from models.entities.spell import Spell
from typing import List

converter = SpellConverter(fantasy_sheets)
spells_pydantic: List[Spell] = converter.convert_all(
    source_filter=source,
    source=source,
    json_source=json_source
)
