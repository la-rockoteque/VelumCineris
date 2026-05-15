from __future__ import annotations

from typing import Any

import pandas as pd


def _build_language_payload(row: Any, *, default_source: str) -> tuple[list[str], list[str], str | None]:
    language_known = (
        [f"{{@language {lang}|{default_source}}}" for lang in row.get("Languages").split(",")]
        if pd.notnull(row.get("Languages"))
        else []
    )
    language_list_pretext = (
        f"and {row.get('Number of Languages')} additional languages"
        if pd.notnull(row.get("Languages"))
        else "You know 2 standard languages of your choice"
    )
    formatted_language_known = [language_list_pretext, *language_known]

    language_list = (
        [f"{{@language {lang}|{default_source}}}" for lang in row.get("Language Choices").split(",")]
        if pd.notnull(row.get("Language Choices"))
        else []
    )
    language_list_pretext = (
        "You may choose from the list of" if pd.notnull(row.get("Language Choices")) else ""
    )
    formatted_language_list = [language_list_pretext, *list(set(language_list) - set(language_known))]

    exotic_language_known = (
        f"You may choose up to {row.get('Number of Exotic Language')} exotic language instead"
        if pd.notnull(row.get("Number of Exotic Language"))
        else None
    )
    return formatted_language_known, formatted_language_list, exotic_language_known


def _build_ability_scores_fantasy(row: Any) -> dict[str, int]:
    abilities: dict[str, int] = {}
    ability_1 = row.get("Ability 1")
    ability_2 = row.get("Ability 2")
    score_1 = row.get("Score 1")
    score_2 = row.get("Score 2")

    if pd.notnull(ability_1) and isinstance(ability_1, str) and ability_1.strip():
        if pd.notnull(score_1):
            abilities[ability_1[:3].lower()] = int(score_1)

    if pd.notnull(ability_2) and isinstance(ability_2, str) and ability_2.strip():
        if pd.notnull(score_2):
            abilities[ability_2[:3].lower()] = int(score_2)
    return abilities


def _build_fluff_entries(
    row: Any,
    *,
    df_species: pd.DataFrame,
    end_column_fallback: str,
) -> list[dict[str, Any]]:
    columns = list(df_species.columns)
    start_index = columns.index("Intro")

    if "Playstyle & Roleplaying" in columns:
        end_column = "Playstyle & Roleplaying"
    else:
        end_column = end_column_fallback

    end_index = columns.index(end_column)

    return [
        {
            "name": col,
            "entries": [row[col]],
            "type": "entries",
        }
        for col in columns[start_index : end_index + 1]
        if pd.notnull(row.get(col))
    ]


def map_fantasy_species_row(
    row: Any,
    *,
    df_species: pd.DataFrame,
    default_source: str,
) -> dict[str, Any]:
    formatted_language_known, formatted_language_list, exotic_language_known = _build_language_payload(
        row,
        default_source=default_source,
    )
    language_known = (
        [f"{{@language {lang}|{default_source}}}" for lang in row.get("Languages").split(",")]
        if pd.notnull(row.get("Languages"))
        else []
    )
    language_list = (
        [f"{{@language {lang}|{default_source}}}" for lang in row.get("Language Choices").split(",")]
        if pd.notnull(row.get("Language Choices"))
        else []
    )

    abilities = _build_ability_scores_fantasy(row)

    size_abrv = row.get("Size ABRV")
    if pd.notnull(size_abrv) and isinstance(size_abrv, str) and size_abrv:
        size = [size_abrv[:1].upper()]
    else:
        size = ["M"]

    return {
        "name": row.get("Name"),
        "source": row.get("Source"),
        "page": 1,
        **({"demonym": row.get("Demonym")} if pd.notnull(row.get("Demonym")) else {}),
        "ability": [abilities] if abilities else [],
        "size": size,
        **({"traitTags": row.get("Tag").split(", ")} if pd.notnull(row.get("Tag")) else {}),
        **({"alias": [row.get("Alias")]} if pd.notnull(row.get("Alias")) else {}),
        **({"slogan": row.get("Slogan")} if pd.notnull(row.get("Slogan")) else {}),
        **({"quote": row.get("Quote")} if pd.notnull(row.get("Quote")) else {}),
        **({"charGen": row.get("CharGen")} if pd.notnull(row.get("CharGen")) else {}),
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
                    *([", ".join(formatted_language_known)] if not language_known else []),
                    *([", ".join(formatted_language_list)] if not language_list else []),
                    *([exotic_language_known] if exotic_language_known is not None else []),
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
            "entries": _build_fluff_entries(
                row,
                df_species=df_species,
                end_column_fallback="Life in Orimond",
            ),
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


def map_modern_species_row(
    row: Any,
    *,
    df_species: pd.DataFrame,
    default_source: str,
) -> dict[str, Any]:
    formatted_language_known, formatted_language_list, exotic_language_known = _build_language_payload(
        row,
        default_source=default_source,
    )
    language_known = (
        [f"{{@language {lang}|{default_source}}}" for lang in row.get("Languages").split(",")]
        if pd.notnull(row.get("Languages"))
        else []
    )
    language_list = (
        [f"{{@language {lang}|{default_source}}}" for lang in row.get("Language Choices").split(",")]
        if pd.notnull(row.get("Language Choices"))
        else []
    )

    return {
        "name": row.get("Name"),
        "source": row.get("Source"),
        "page": 1,
        **({"demonym": row.get("Demonym")} if pd.notnull(row.get("Demonym")) else {}),
        "ability": [
            {
                f"{row.get('Ability 1')[:3].lower()}": row.get("Score 1"),
                f"{row.get('Ability 2')[:3].lower()}": row.get("Score 2"),
            }
        ],
        "size": [row.get("Size ABRV")[:1].upper()],
        **({"traitTags": row.get("Tag").split(", ")} if pd.notnull(row.get("Tag")) else {}),
        **({"alias": [row.get("Alias")]} if pd.notnull(row.get("Alias")) else {}),
        **({"slogan": row.get("Slogan")} if pd.notnull(row.get("Slogan")) else {}),
        **({"quote": row.get("Quote")} if pd.notnull(row.get("Quote")) else {}),
        **({"charGen": row.get("CharGen")} if pd.notnull(row.get("CharGen")) else {}),
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
                    *([", ".join(formatted_language_known)] if not language_known else []),
                    *([", ".join(formatted_language_list)] if not language_list else []),
                    *([exotic_language_known] if exotic_language_known is not None else []),
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
            "entries": _build_fluff_entries(
                row,
                df_species=df_species,
                end_column_fallback="Life in the City",
            ),
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
