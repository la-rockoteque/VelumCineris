import pandas as pd
from FiveETools.fantasy.sources import source, json_source
from FiveETools.gsheets_client import fantasy_sheets
import inflection

df_species = fantasy_sheets.get_sheet("993815941")
df_species.head()


def row_to_species(row):
    language_known = (
        [f"{{@language {lang}|ORIO}}" for lang in row.get("Languages").split(",")]
        if pd.notnull(row.get("Languages"))
        else []
    )
    language_list_pretext = (
        f"and {row.get('Number of Languages')} additional languages"
        if pd.notnull(row.get("Languages"))
        else "You know 2 standard languages of your choice"
    )
    formated_language_known = [language_list_pretext, *language_known]
    language_list = (
        [
            f"{{@language {lang}|ORIO}}"
            for lang in row.get("Language Choices").split(",")
        ]
        if pd.notnull(row.get("Language Choices"))
        else []
    )
    language_list_pretext = (
        f"You may choose from the list of"
        if pd.notnull(row.get("Language Choices"))
        else ""
    )
    formated_language_list = [
        language_list_pretext,
        *list(set(language_list) - set(language_known)),
    ]
    exotic_language_known = (
        f"You may choose up to {row.get('Number of Exotic Language')} exotic language instead"
        if pd.notnull(row.get("Number of Exotic Language"))
        else None
    )

    # Build ability scores dictionary, handling null/NaN values
    abilities = {}
    ability_1 = row.get('Ability 1')
    ability_2 = row.get('Ability 2')
    score_1 = row.get("Score 1")
    score_2 = row.get("Score 2")

    if pd.notnull(ability_1) and isinstance(ability_1, str) and ability_1.strip():
        if pd.notnull(score_1):
            abilities[ability_1[:3].lower()] = int(score_1)

    if pd.notnull(ability_2) and isinstance(ability_2, str) and ability_2.strip():
        if pd.notnull(score_2):
            abilities[ability_2[:3].lower()] = int(score_2)

    # Get size, handling null values
    size_abrv = row.get("Size ABRV")
    if pd.notnull(size_abrv) and isinstance(size_abrv, str) and size_abrv:
        size = [size_abrv[:1].upper()]
    else:
        size = ["M"]  # Default to Medium

    return {
        "name": row.get("Name"),
        "source": row.get("Source"),
        "page": 1,
        "ability": [abilities] if abilities else [],
        "size": size,
        **(
            {"traitTags": row.get("Tag").split(", ")}
            if pd.notnull(row.get("Tag"))
            else {}
        ),
        **({"alias": [row.get("Alias")]} if pd.notnull(row.get("Alias")) else {}),
        "speed": row.get("Walk Speed"),
        "entries": [
            f"{row.get('Name')} Traits",
            {"type": "entries", "name": "Age", "entries": [row.get("Age") if pd.notnull(row.get("Age")) else ""]},
            {"type": "entries", "name": "Size", "entries": [row.get("Size") if pd.notnull(row.get("Size")) else ""]},
            {"type": "entries", "name": "Speed", "entries": [row.get("Speed") if pd.notnull(row.get("Speed")) else ""]},
            {"type": "entries", "name": "Vision", "entries": [row.get("Vision") if pd.notnull(row.get("Vision")) else ""]},
            *(
                {
                    "name": row.get(f"Trait {index}").split("|")[0],
                    "entries": [row.get(f"Trait {index}").split("|")[1]],
                    "type": "entries",
                }
                for index in [1, 2, 3, 4, 5, 6]
                if pd.notnull(row.get(f"Trait {index}"))
            ),
            {
                "name": "Languages",
                "entries": [
                    *(
                        [", ".join(formated_language_known)]
                        if not language_known
                        else []
                    ),
                    *([", ".join(formated_language_list)] if not language_list else []),
                    *(
                        [exotic_language_known]
                        if exotic_language_known is not None
                        else []
                    ),
                ],
                "type": "entries",
            },
        ],
        "languageProficiencies": [
            {
                **(
                    {"any": row.get("Number of Exotic Language")}
                    if pd.notnull(row.get("Number of Exotic Language"))
                    else {}
                ),
                "anyStandard": row.get("Number of Languages"),
            }
        ],
        "fluff": {
            "entries": [
                {
                    "name": col,
                    "entries": [row[col]],
                    "type": "entries",
                }
                for col in df_species.columns[
                    df_species.columns.get_loc("Intro") : df_species.columns.get_loc(
                        "Life in Orimond"
                    )
                    + 1
                ]
                if pd.notnull(row[col])
            ],
            **(
                {
                    "images": [
                        {
                            "type": "image",
                            "href": {"type": "external", "url": row.get("Image Male")},
                        }
                    ]
                }
                if pd.notnull(row.get("Image Male"))
                else {}
            ),
        },
    }


species_list = [
    row_to_species(row)
    for index, row in df_species.iterrows()
    if pd.notnull(row.get("Name"))
]
