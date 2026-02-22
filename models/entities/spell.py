"""
Spell entity model for D&D 5e.

Provides type-safe validation for spell data from Google Sheets.
"""

from pydantic import Field
from typing import Optional, List, Dict, Any, Literal
import pandas as pd
import urllib.parse
import inflection

from ..base import BaseEntity
from ..fields.components import Components, TimeAction, Range, Duration, Distance

# Valid spell schools (5etools format)
SchoolType = Literal["A", "C", "D", "E", "V", "I", "N", "T"]


class Spell(BaseEntity):
    """
    D&D 5e Spell model.

    Represents a spell in 5etools JSON format with additional DDB fields.
    """

    # Core spell fields
    level: int = Field(..., ge=0, le=9, description="Spell level (0-9)")
    school: SchoolType = Field(..., description="Spell school abbreviation")
    components: Components = Field(..., description="Spell components (V, S, M, R)")
    time: List[TimeAction] = Field(..., description="Casting time")
    range: Range = Field(..., description="Spell range")
    duration: List[Duration] = Field(..., description="Spell duration")

    # Class associations
    classes: Optional[Dict[str, List[Dict[str, str]]]] = Field(
        None, description="Classes that can cast this spell"
    )

    # Higher level casting
    entriesHigherLevel: Optional[List[Dict[str, Any]]] = Field(
        None, description="Higher level casting effects"
    )

    # Optional 5etools tags
    abilityCheck: Optional[List[str]] = Field(None, description="Required ability checks")
    miscTags: Optional[List[str]] = Field(None, description="Miscellaneous tags")
    damageInflict: Optional[List[str]] = Field(None, description="Damage types inflicted")
    savingThrow: Optional[List[str]] = Field(None, description="Required saving throws")
    areaTags: Optional[List[str]] = Field(None, description="Area of effect tags")

    # D&D Beyond-specific fields (for sync)
    ddb_save_success: Optional[str] = Field(None, description="DDB: Save success effect")
    ddb_save_fail: Optional[str] = Field(None, description="DDB: Save failure effect")
    ddb_area_type: Optional[str] = Field(None, description="DDB: Area type")
    ddb_area_distance: Optional[str] = Field(None, description="DDB: Area distance")
    ddb_damage: Optional[str] = Field(None, description="DDB: Damage description")
    ddb_condition: Optional[str] = Field(None, description="DDB: Condition applied")
    ddb_scaling: Optional[str] = Field(None, description="DDB: Scaling description")
    ddb_modifiers_json: Optional[str] = Field(None, description="DDB: Modifiers JSON")
    ddb_modifier_type: Optional[str] = Field(None, description="DDB: Primary modifier type")
    ddb_modifier_subtype: Optional[str] = Field(None, description="DDB: Primary modifier subtype")
    ddb_modifier_dice_count: Optional[str] = Field(None, description="DDB: Modifier dice count")
    ddb_modifier_dice_type: Optional[str] = Field(None, description="DDB: Modifier dice type")
    ddb_modifier_fixed_value: Optional[str] = Field(None, description="DDB: Modifier fixed value")
    ddb_modifier_duration: Optional[str] = Field(None, description="DDB: Modifier duration")
    ddb_modifier_duration_unit: Optional[str] = Field(None, description="DDB: Modifier duration unit")

    @classmethod
    def from_row(cls, row: pd.Series, source: str, json_source: str) -> 'Spell':
        """
        Create Spell from DataFrame row.

        Args:
            row: DataFrame row from Google Sheets
            source: Source filter (e.g., "ORIO")
            json_source: JSON source identifier (e.g., "ORIO")

        Returns:
            Validated Spell instance
        """
        # Parse components
        components_str = row.get("Components ABVR", "")
        components = Components.from_string(components_str)

        # Parse spell classes
        spell_classes = [
            cls.strip() for cls in str(row.get("Class", "")).split(",") if cls.strip()
        ]

        # Parse optional list fields
        ability_checks = [
            cls.strip().lower()
            for cls in str(row.get("Ability Check", "")).split(",")
            if cls.strip()
        ] if not pd.isnull(row.get("Ability Check")) else None

        misc_tags = [
            cls.strip() for cls in str(row.get("Tag ABRV", "")).split(",") if cls.strip()
        ] if not pd.isnull(row.get("Tag ABRV")) else None

        damages = [
            cls.strip().lower()
            for cls in str(row.get("Old Damage Type", "")).split(",")
            if cls.strip()
        ] if not pd.isnull(row.get("Old Damage Type")) else None

        saving_throws = [
            cls.strip().lower()
            for cls in str(row.get("Saving Throw", "")).split(",")
            if cls.strip()
        ] if not pd.isnull(row.get("Saving Throw")) else None

        areas = [
            cls.strip() for cls in str(row.get("Area ABRV", "")).split(",") if cls.strip()
        ] if not pd.isnull(row.get("Area ABRV")) else None

        # Parse time
        time = [TimeAction(
            number=row.get("Casting Unit", 1),
            unit=row.get("Casting Type", "action").lower()
        )]

        # Parse range
        range_distance = (
            row.get("Range Distance").lower()
            if not pd.isnull(row.get("Range Distance"))
            else "self"
        )
        range_obj = Range(
            type=row.get("Range Type", "point").lower(),
            distance=Distance(
                type=range_distance,
                amount=int(row.get("Range Unit")) if not pd.isnull(row.get("Range Unit")) else None
            )
        )

        # Parse duration
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

        duration_dict = {
            "type": duration_type,
        }
        if duration_type == "timed":
            duration_dict["duration"] = {
                "type": duration_unit,
                "amount": duration_amount,
                "upTo": True if row.get("Up To", "FALSE") == "TRUE" else False,
            }
            duration_dict["concentration"] = (
                True if row.get("Concentration", "FALSE") == "TRUE" else False
            )

        duration = [Duration(**duration_dict)]

        # Parse entries
        entries = [row.get("Description")]
        if not pd.isnull(row.get("Clarification")):
            entries.append(row.get("Clarification"))
        if not pd.isnull(row.get("Table")):
            entries.append(row.get("Table"))

        # Parse entriesHigherLevel
        entriesHigherLevel = None
        if not pd.isnull(row.get("Higher Levels")):
            entriesHigherLevel = [
                {
                    "type": "entries",
                    "name": "At Higher Levels",
                    "entries": [row.get("Higher Levels")]
                }
            ]

        # Parse fluff
        base_url = "https://raw.githubusercontent.com/la-rockoteque/Vestigium/refs/heads/main/images/Spell"
        fluff_entries = []
        if not pd.isnull(row.get("Flavor")):
            fluff_entries.append(row.get("Flavor"))
        if not pd.isnull(row.get("Alternative Flavor")):
            fluff_entries.append(row.get("Alternative Flavor"))
        if not pd.isnull(row.get("Quotes")):
            fluff_entries.append(row.get("Quotes"))

        fluff = {
            "entries": fluff_entries,
            "images": [
                {
                    "type": "image",
                    "href": {
                        "type": "external",
                        "url": f"{base_url}/{urllib.parse.quote(inflection.underscore(row.get('Spell Name', 'Unnamed Spell')))}.png",
                    },
                }
            ],
        } if fluff_entries else None

        # Parse classes
        classes = {
            "fromClassList": [
                {"name": cls, "source": json_source} for cls in spell_classes
            ]
        } if spell_classes else None

        # Helper function for optional string fields
        def optional_str(field_name: str) -> Optional[str]:
            value = row.get(field_name)
            if pd.isnull(value):
                return None
            stripped = str(value).strip()
            return stripped if stripped else None

        return cls(
            source=json_source,
            name=row.get("Spell Name", "Unnamed Spell"),
            level=int(row["Level"][0]) if not pd.isnull(row.get("Level")) else 0,
            school=row.get("School ABRV", "E"),
            components=components,
            time=time,
            range=range_obj,
            duration=duration,
            classes=classes,
            entries=entries,
            entriesHigherLevel=entriesHigherLevel,
            fluff=fluff,
            abilityCheck=ability_checks,
            miscTags=misc_tags,
            damageInflict=damages,
            savingThrow=saving_throws,
            areaTags=areas,
            # DDB fields
            ddb_save_success=optional_str("Success"),
            ddb_save_fail=optional_str("Fail"),
            ddb_area_type=optional_str("Area Type"),
            ddb_area_distance=optional_str("Area Distance"),
            ddb_damage=optional_str("Damage"),
            ddb_condition=optional_str("Condition"),
            ddb_scaling=optional_str("Scaling"),
            ddb_modifiers_json=optional_str("Modifiers JSON"),
            ddb_modifier_type=optional_str("Modifier Type"),
            ddb_modifier_subtype=optional_str("Modifier Subtype"),
            ddb_modifier_dice_count=optional_str("Modifier Dice Count"),
            ddb_modifier_dice_type=optional_str("Modifier Dice Type"),
            ddb_modifier_fixed_value=optional_str("Modifier Fixed Value"),
            ddb_modifier_duration=optional_str("Modifier Duration"),
            ddb_modifier_duration_unit=optional_str("Modifier Duration Unit"),
        )
