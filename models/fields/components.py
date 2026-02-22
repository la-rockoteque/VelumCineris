"""
Reusable field types for spell components, time, range, and duration.

These correspond to 5etools JSON format for D&D 5e spells.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


class Components(BaseModel):
    """Spell components (Verbal, Somatic, Material, Royalty)."""

    v: bool = Field(False, description="Verbal component")
    s: bool = Field(False, description="Somatic component")
    m: Optional[bool] = Field(False, description="Material component")
    r: Optional[bool] = Field(False, description="Royalty component (homebrew)")

    @classmethod
    def from_string(cls, components_str: str) -> 'Components':
        """
        Parse components from comma-separated string.

        Args:
            components_str: String like "V, S, M" or "V,S"

        Returns:
            Components instance

        Example:
            >>> Components.from_string("V, S, M")
            Components(v=True, s=True, m=True, r=False)
        """
        if not components_str or str(components_str).strip() == "":
            return cls()

        components_set = {c.strip().upper() for c in str(components_str).split(",")}
        return cls(
            v="V" in components_set,
            s="S" in components_set,
            m="M" in components_set,
            r="R" in components_set
        )


class TimeAction(BaseModel):
    """Time required to perform an action (casting time, etc.)."""

    number: int = Field(1, description="Number of units")
    unit: str = Field("action", description="Time unit (action, bonus, reaction, minute, hour)")
    condition: Optional[str] = Field(None, description="Conditional text (e.g., 'which you take when...')")


class Distance(BaseModel):
    """Distance measurement (range, area of effect)."""

    type: str = Field("self", description="Distance type (self, feet, miles, touch, sight, unlimited)")
    amount: Optional[int] = Field(None, description="Distance amount (e.g., 60 for 60 feet)")


class Range(BaseModel):
    """Spell or ability range."""

    type: str = Field("point", description="Range type (point, radius, sphere, cone, cube, line)")
    distance: Distance = Field(..., description="Distance information")

    @classmethod
    def from_row_simple(cls, range_type: str = "point", range_distance: str = "self", range_unit: Optional[int] = None) -> 'Range':
        """
        Create Range from simple row fields.

        Args:
            range_type: Type of range (point, radius, etc.)
            range_distance: Distance type (self, feet, etc.)
            range_unit: Optional amount (e.g., 60)

        Returns:
            Range instance
        """
        return cls(
            type=range_type.lower() if range_type else "point",
            distance=Distance(
                type=range_distance.lower() if range_distance else "self",
                amount=int(range_unit) if range_unit and str(range_unit).isdigit() else None
            )
        )


class Duration(BaseModel):
    """Duration of spell or effect."""

    type: str = Field("instant", description="Duration type (instant, timed, permanent, special)")
    concentration: Optional[bool] = Field(False, description="Requires concentration")
    duration: Optional[Dict[str, Any]] = Field(None, description="Duration details (for timed durations)")

    @classmethod
    def from_row_simple(cls, duration_type: str = "instant", concentration: bool = False) -> List['Duration']:
        """
        Create Duration list from simple row fields.

        Args:
            duration_type: Type of duration
            concentration: Whether requires concentration

        Returns:
            List with single Duration instance (5etools uses arrays)
        """
        return [cls(
            type=duration_type.lower() if duration_type else "instant",
            concentration=concentration
        )]
