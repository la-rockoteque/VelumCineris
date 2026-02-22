import pandas as pd
from FiveETools.modern.sources import source, json_source
from FiveETools.gsheets_client import modern_sheets

df_background = modern_sheets.get_sheet("1186398440")
df_background.head()

background_list = [
    {
        "name": row.get("Background"),
        "source": json_source,
        **({
               "skillProficiencies": [
                   {skill.lower(): True for skill in row.get("Skills").split(", ")}
               ]
           } if pd.notnull(row.get("Skills")) and row.get("Skills") else {}),
        "entries": [
            {
                "type": "list",
                "style": "list-hang-notitle",
                "items": [
                    *([{
                        "type": "item",
                        "name": "Skill Proficiencies",
                        "entry": ", ".join(
                            f"{{@skill {skill}}}"
                            for skill in row.get("Skills").split(", ")
                        ),
                    }] if pd.notnull(row.get("Skills")) and row.get("Skills") else []),
                    *([{
                        "type": "item",
                        "name": "Tool Proficiencies",
                        "entry": row.get("Tools"),
                    }] if pd.notnull(row.get("Tools")) and row.get("Tools") else []),
                    *([{
                         "type": "item",
                         "name": "Languages",
                         "entry": ", ".join(
                                 f"{{@language {language}}}"
                                 for language in row.get("Languages").split(", ")
                             ),
                     }] if pd.notnull(row.get("Languages")) else []),
                    *([{
                        "type": "item",
                        "name": "Equipment",
                        "entry": ", ".join(row.get("Items").split(", ")),
                    }] if pd.notnull(row.get("Items")) and row.get("Items") else []),
                ],
            },
            *([{
                "name": row.get("Feature Name"),
                "type": "entries",
                "entries": [row.get("Feature")],
                "data": {"isFeature": True},
            }] if pd.notnull(row.get("Feature Name")) else []),
        ],
        **({
            "startingEquipment": [
                {"_": [{"special": item} for item in row.get("Starting Equipment").split(", ")]}
            ]
        } if pd.notnull(row.get("Starting Equipment")) and row.get("Starting Equipment") else {}),
    }
    for index, row in df_background.iterrows()
    if pd.notnull(row.get("Background")) and row.get("Source") == source
]

# NEW: Pydantic-based conversion for type safety
from Spreadsheet.converters.background import BackgroundConverter
from models.entities.background import Background
from typing import List

converter = BackgroundConverter(modern_sheets)
background_pydantic: List[Background] = converter.convert_all(
    source_filter=source,
    source=source,
    json_source=json_source
)
