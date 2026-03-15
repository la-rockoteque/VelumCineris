"""
Background entity model for D&D 5e.

Provides type-safe validation for background data from Google Sheets.
"""

from pydantic import Field
from typing import Optional, List, Dict, Any

from ..base import BaseEntity
from ..row_access import optional_text, row_value, split_csv


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
    def from_row(cls, row, source: str, json_source: str) -> 'Background':
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
        skills = split_csv(row_value(row, "Skills"))
        if skills:
            skill_profs = [{skill.lower(): True for skill in skills}]

        # Build entries list
        entries = []

        # Add proficiencies list
        items = []
        if skills:
            items.append({
                "type": "item",
                "name": "Skill Proficiencies",
                "entry": ", ".join(f"{{@skill {skill}}}" for skill in skills)
            })

        tools = optional_text(row_value(row, "Tools"))
        if tools:
            items.append({
                "type": "item",
                "name": "Tool Proficiencies",
                "entry": tools
            })

        languages = split_csv(row_value(row, "Languages"))
        if languages:
            items.append({
                "type": "item",
                "name": "Languages",
                "entry": ", ".join(f"{{@language {lang}}}" for lang in languages)
            })

        item_text = optional_text(row_value(row, "Items"))
        if item_text:
            items.append({
                "type": "item",
                "name": "Equipment",
                "entry": ", ".join(item_text.split(", "))
            })

        if items:
            entries.append({
                "type": "list",
                "style": "list-hang-notitle",
                "items": items
            })

        # Add feature
        feature_name = optional_text(row_value(row, "Feature Name"))
        if feature_name:
            feature = optional_text(row_value(row, "Feature"))
            entries.append({
                "name": feature_name,
                "type": "entries",
                "entries": [feature] if feature else [],
                "data": {"isFeature": True}
            })

        # Parse starting equipment
        starting_equipment = None
        starting_equipment_items = split_csv(row_value(row, "Starting Equipment"))
        if starting_equipment_items:
            starting_equipment = [{"_": [{"special": item} for item in starting_equipment_items]}]

        return cls(
            source=json_source,
            name=optional_text(row_value(row, "Background")) or "Unnamed Background",
            skillProficiencies=skill_profs,
            entries=entries,
            startingEquipment=starting_equipment
        )
