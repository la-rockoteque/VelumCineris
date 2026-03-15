"""
Language entity model for D&D 5e.

Provides type-safe validation for language data from Google Sheets.
"""

from pydantic import Field
from typing import Optional, List
import inflection

from ..base import BaseEntity
from ..row_access import optional_text, row_value, split_csv


class Language(BaseEntity):
    """
    D&D 5e Language model.

    Represents a language in 5etools JSON format.
    """

    # Language type
    type: str = Field(..., description="Language type (standard, exotic, secret, etc.)")

    # Optional fields
    typicalSpeakers: Optional[List[str]] = Field(
        None, description="Typical speakers (with 5etools filter format)"
    )
    script: Optional[str] = Field(None, description="Writing script used")

    @classmethod
    def from_row(cls, row, source: str, json_source: str) -> 'Language':
        """
        Create Language from DataFrame row.

        Args:
            row: DataFrame row from Google Sheets
            source: Source filter (e.g., "ORIO")
            json_source: JSON source identifier (e.g., "GuideToOrimond")

        Returns:
            Validated Language instance
        """
        # Parse typical speakers
        typical_speakers = None
        speakers = split_csv(row_value(row, "Races"))
        if speakers:
            typical_speakers = [
                f"{{@filter {inflection.pluralize(speaker)}|bestiary|type=humanoid|tag= any race;{speaker}}}"
                for speaker in speakers
            ]

        # Parse script
        script = None
        script_value = optional_text(row_value(row, "Script"))
        if script_value:
            script = script_value.lower()

        # Parse description
        entries = []
        description = optional_text(row_value(row, "Description"))
        if description:
            entries.append(description)

        return cls(
            source=json_source,
            name=optional_text(row_value(row, "Name")) or "Unnamed Language",
            type=(optional_text(row_value(row, "Type")) or "standard").lower(),
            typicalSpeakers=typical_speakers,
            script=script,
            page=0,
            entries=entries
        )
