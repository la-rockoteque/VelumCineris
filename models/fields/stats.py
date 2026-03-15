"""
Reusable field types for creature stats (speeds, ability scores, HP, AC).

These correspond to 5etools JSON format for D&D 5e monsters and species.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
import re

from ..row_access import is_missing, optional_int, row_value


class Speed(BaseModel):
    """Creature movement speeds."""

    walk: Optional[int] = Field(None, description="Walking speed in feet")
    fly: Optional[int] = Field(None, description="Flying speed in feet")
    swim: Optional[int] = Field(None, description="Swimming speed in feet")
    burrow: Optional[int] = Field(None, description="Burrowing speed in feet")
    climb: Optional[int] = Field(None, description="Climbing speed in feet")

    @classmethod
    def from_row(cls, row) -> 'Speed':
        """
        Parse speeds from DataFrame row.

        Expects columns like: "Speed (Walking)", "Speed (Flying)", etc.

        Args:
            row: DataFrame row with speed columns

        Returns:
            Speed instance
        """
        def parse_speed(value):
            """Extract numeric speed from various formats."""
            if is_missing(value):
                return None
            if isinstance(value, (int, float)):
                return int(value)
            if isinstance(value, str):
                match = re.search(r'(\d+)', value)
                return int(match.group(1)) if match else None
            return None

        return cls(
            walk=parse_speed(row_value(row, "Speed (Walking)")),
            fly=parse_speed(row_value(row, "Speed (Flying)")),
            swim=parse_speed(row_value(row, "Speed (Swimming)")),
            burrow=parse_speed(row_value(row, "Speed (Burrowing)")),
            climb=parse_speed(row_value(row, "Speed (Climbing)"))
        )

    def to_5etools(self) -> Dict[str, int]:
        """Export in 5etools format (only non-null speeds)."""
        return {k: v for k, v in self.model_dump().items() if v is not None}


class AbilityScores(BaseModel):
    """D&D 5e ability scores."""

    str_: Optional[int] = Field(None, description="Strength", alias="str")
    dex: Optional[int] = Field(None, description="Dexterity")
    con: Optional[int] = Field(None, description="Constitution")
    int_: Optional[int] = Field(None, description="Intelligence", alias="int")
    wis: Optional[int] = Field(None, description="Wisdom")
    cha: Optional[int] = Field(None, description="Charisma")

    @classmethod
    def from_row(cls, row) -> 'AbilityScores':
        """
        Parse ability scores from DataFrame row.

        Expects columns: "STR", "DEX", "CON", "INT", "WIS", "CHA"

        Args:
            row: DataFrame row with ability score columns

        Returns:
            AbilityScores instance
        """
        return cls(
            str_=None if is_missing(row_value(row, "STR")) else optional_int(row_value(row, "STR")),
            dex=None if is_missing(row_value(row, "DEX")) else optional_int(row_value(row, "DEX")),
            con=None if is_missing(row_value(row, "CON")) else optional_int(row_value(row, "CON")),
            int_=None if is_missing(row_value(row, "INT")) else optional_int(row_value(row, "INT")),
            wis=None if is_missing(row_value(row, "WIS")) else optional_int(row_value(row, "WIS")),
            cha=None if is_missing(row_value(row, "CHA")) else optional_int(row_value(row, "CHA")),
        )


class HP(BaseModel):
    """Hit points definition."""

    average: Optional[int] = Field(None, description="Average HP")
    formula: Optional[str] = Field(None, description="HP formula (e.g., '2d8+2')")
    special: Optional[str] = Field(None, description="Special HP rules")


class AC(BaseModel):
    """Armor class definition."""

    ac: int = Field(..., description="AC value")
    from_: Optional[List[str]] = Field(None, alias="from", description="AC source (armor, natural, etc.)")
    condition: Optional[str] = Field(None, description="Conditional AC modifier")


class Skills(BaseModel):
    """Creature skill proficiencies."""

    acrobatics: Optional[str] = Field(None, description="Acrobatics modifier")
    animal_handling: Optional[str] = Field(None, alias="animal handling", description="Animal Handling modifier")
    arcana: Optional[str] = Field(None, description="Arcana modifier")
    athletics: Optional[str] = Field(None, description="Athletics modifier")
    deception: Optional[str] = Field(None, description="Deception modifier")
    history: Optional[str] = Field(None, description="History modifier")
    insight: Optional[str] = Field(None, description="Insight modifier")
    intimidation: Optional[str] = Field(None, description="Intimidation modifier")
    investigation: Optional[str] = Field(None, description="Investigation modifier")
    medicine: Optional[str] = Field(None, description="Medicine modifier")
    nature: Optional[str] = Field(None, description="Nature modifier")
    perception: Optional[str] = Field(None, description="Perception modifier")
    performance: Optional[str] = Field(None, description="Performance modifier")
    persuasion: Optional[str] = Field(None, description="Persuasion modifier")
    religion: Optional[str] = Field(None, description="Religion modifier")
    sleight_of_hand: Optional[str] = Field(None, alias="sleight of hand", description="Sleight of Hand modifier")
    stealth: Optional[str] = Field(None, description="Stealth modifier")
    survival: Optional[str] = Field(None, description="Survival modifier")


class Saves(BaseModel):
    """Saving throw proficiencies."""

    str_: Optional[str] = Field(None, alias="str", description="Strength save modifier")
    dex: Optional[str] = Field(None, description="Dexterity save modifier")
    con: Optional[str] = Field(None, description="Constitution save modifier")
    int_: Optional[str] = Field(None, alias="int", description="Intelligence save modifier")
    wis: Optional[str] = Field(None, description="Wisdom save modifier")
    cha: Optional[str] = Field(None, description="Charisma save modifier")
