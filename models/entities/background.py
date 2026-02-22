"""
Background entity model for D&D 5e.

Provides type-safe validation for background data from Google Sheets.
"""

from pydantic import Field
from typing import Optional, List, Dict, Any
import pandas as pd
from ..base import BaseEntity


class Background(BaseEntity):
    """
    D&D 5e Background model.

    Represents a character background in 5etools JSON format.
    """

    # Optional fields
    skillProficiencies: Optional[List[Dict[str, bool]]] = Field(
        None, description="Skill proficiencies"
    )
    startingEquipment: Optional[List[Dict[str, Any]]] = Field(
        None, description="Starting equipment"
    )

    @classmethod
    def from_row(cls, row: pd.Series, source: str, json_source: str) -> 'Background':
        """
        Create Background from DataFrame row.

        Args:
            row: DataFrame row from Google Sheets
            source: Source filter (e.g., "VSTGCC")
            json_source: JSON source identifier

        Returns:
            Validated Background instance
        """
        # Parse skill proficiencies
        skill_profs = None
        if pd.notnull(row.get("Skills")) and row.get("Skills"):
            skills = [s.strip() for s in row.get("Skills").split(",")]
            skill_profs = [{skill.lower(): True for skill in skills}]

        # Build entries list
        entries = []

        # Add proficiencies list
        items = []
        if pd.notnull(row.get("Skills")) and row.get("Skills"):
            skills = [s.strip() for s in row.get("Skills").split(",")]
            items.append({
                "type": "item",
                "name": "Skill Proficiencies",
                "entry": ", ".join(f"{{@skill {skill}}}" for skill in skills)
            })

        if pd.notnull(row.get("Tools")) and row.get("Tools"):
            items.append({
                "type": "item",
                "name": "Tool Proficiencies",
                "entry": row.get("Tools")
            })

        if pd.notnull(row.get("Languages")):
            languages = [lang.strip() for lang in row.get("Languages").split(",")]
            items.append({
                "type": "item",
                "name": "Languages",
                "entry": ", ".join(f"{{@language {lang}}}" for lang in languages)
            })

        if pd.notnull(row.get("Items")) and row.get("Items"):
            items.append({
                "type": "item",
                "name": "Equipment",
                "entry": ", ".join(row.get("Items").split(", "))
            })

        if items:
            entries.append({
                "type": "list",
                "style": "list-hang-notitle",
                "items": items
            })

        # Add feature
        if pd.notnull(row.get("Feature Name")):
            entries.append({
                "name": row.get("Feature Name"),
                "type": "entries",
                "entries": [row.get("Feature")] if pd.notnull(row.get("Feature")) else [],
                "data": {"isFeature": True}
            })

        # Parse starting equipment
        starting_equipment = None
        if pd.notnull(row.get("Starting Equipment")) and row.get("Starting Equipment"):
            items = [item.strip() for item in row.get("Starting Equipment").split(",")]
            starting_equipment = [{"_": [{"special": item} for item in items]}]

        return cls(
            source=json_source,
            name=row.get("Background", "Unnamed Background"),
            skillProficiencies=skill_profs,
            entries=entries,
            startingEquipment=starting_equipment
        )
