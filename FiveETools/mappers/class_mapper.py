from __future__ import annotations

import string
from collections.abc import Callable
from typing import Any

import pandas as pd


def map_class_row(
    row: Any,
    *,
    source: str,
    json_source: str,
    default_source: str,
    df_spells: pd.DataFrame,
    df_subclasses: pd.DataFrame,
    df_class_tables: pd.DataFrame,
    df_class_features: pd.DataFrame,
    split_csv: Callable[[Any], list[str]],
    to_table_fn: Callable[..., dict[str, Any]],
    to_spell_progression_table_fn: Callable[..., dict[str, Any]],
    get_features_for_class_fn: Callable[..., list[str]],
) -> dict[str, Any]:
    class_name = row.get("Name") if not pd.isnull(row.get("Name", "Generic Class")) else ""
    subclass_title = row.get("Subclass Title") if not pd.isnull(row.get("Subclass Title")) else ""
    skills = row.get("Skills") if not pd.isnull(row.get("Skills")) else ""
    armors = row.get("Armor") if not pd.isnull(row.get("Armor")) else ""
    weapons = row.get("Weapons") if not pd.isnull(row.get("Weapons")) else ""
    proficiency = row.get("Saving Throws") if not pd.isnull(row.get("Saving Throws")) else ""

    class_spells = [
        spell_row.get("Spell Name")
        for _, spell_row in df_spells.iterrows()
        if pd.notnull(spell_row.get("Class")) == class_name
    ]
    cantrip_progression = [
        int(table_row.get("0"))
        for _, table_row in df_class_tables.iterrows()
        if pd.notnull(table_row.get("Class")) == class_name
    ]

    option_a = split_csv(row.get("A", ""))
    option_b = split_csv(row.get("B", ""))
    common_items = split_csv(row.get("Common", ""))
    spellcasting_ability = row.get("Spellcasting Ability")

    equipment_a = {
        string.ascii_lowercase[i]: [f"{item}|{source}"]
        for i, item in enumerate(option_a)
    }
    equipment_b = {
        string.ascii_lowercase[i]: [f"{item}|{source}"]
        for i, item in enumerate(option_b)
    }
    common = {"_": [f"{item}|{source}" for item in common_items]}

    default_equipment = [
        ", ".join([f"{{@item {item}|{source}}}" for item in option_a]),
        ", ".join([f"{{@item {item}|{source}}}" for item in option_b]),
        ", ".join([f"{{@item {item}|{source}}}" for item in common_items]),
    ]

    def get_subclass(subclass_row):
        return {"name": subclass_row.get("Name"), "source": json_source}

    subclasses = [
        get_subclass(subclass_row)
        for _, subclass_row in df_subclasses.iterrows()
        if subclass_row.get("Class") == class_name
    ]
    del subclasses

    return {
        "source": json_source,
        "name": class_name,
        **({"hd": {"faces": row.get("Hit Points at 1st Level"), "number": 1}}),
        "proficiency": [prof[:3].lower() for prof in split_csv(proficiency)],
        "startingProficiencies": {
            "armor": [armor.lower() for armor in split_csv(armors)],
            "weapons": [
                *[
                    f"{{@item {weapon.lower()}|{default_source}|{weapon.lower()}}}"
                    for weapon in split_csv(weapons)
                    if weapon not in ["simple", "martial"]
                ],
                "simple",
            ],
            "skills": [
                {
                    "choose": {
                        "from": [skill.lower() for skill in split_csv(skills)],
                        "count": 3,
                    }
                }
            ],
        },
        "startingEquipment": {
            "additionalFromBackground": True,
            "default": default_equipment,
            "defaultData": [equipment_a, equipment_b, common],
        },
        **(
            {"spellcastingAbility": spellcasting_ability[:3].lower()}
            if not pd.isnull(spellcasting_ability)
            else {}
        ),
        **(
            {"casterProgression": row.get("Caster Progression")}
            if not pd.isnull(row.get("Caster Progression"))
            else {}
        ),
        **(
            {
                "preparedSpells": f"<$level$> + <${spellcasting_ability[:3].lower()}_mod$>"
            }
            if str(row.get("Prepares Spells", "")).strip() == "TRUE"
            and not pd.isnull(spellcasting_ability)
            else {}
        ),
        "classTableGroups": [
            to_table_fn(class_name, df_class_tables=df_class_tables),
            *(
                [to_spell_progression_table_fn(class_name, df_class_tables=df_class_tables)]
                if not pd.isnull(row.get("spellcastingAbility"))
                else []
            ),
        ],
        **(
            {"subclassTitle": row.get("Subclass Title")}
            if not pd.isnull(row.get("Subclass Title"))
            else {}
        ),
        "classFeatures": get_features_for_class_fn(
            class_name,
            subclass_title,
            json_source=json_source,
            df_class_features=df_class_features,
        ),
        **(
            {"classSpells": class_spells}
            if not pd.isnull(row.get("spellcastingAbility"))
            else {}
        ),
        **(
            {"cantripProgression": cantrip_progression}
            if not pd.isnull(row.get("spellcastingAbility"))
            else {}
        ),
    }
