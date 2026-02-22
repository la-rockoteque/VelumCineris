"""
Language entity model for D&D 5e.

Provides type-safe validation for language data from Google Sheets.
"""

from pydantic import Field
from typing import Optional, List
import pandas as pd
import inflection

from ..base import BaseEntity


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
    def from_row(cls, row: pd.Series, source: str, json_source: str) -> 'Language':
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
        if pd.notnull(row.get("Races")):
            speakers = [speaker.strip() for speaker in row.get("Races").split(",")]
            typical_speakers = [
                f"{{@filter {inflection.pluralize(speaker)}|bestiary|type=humanoid|tag= any race;{speaker}}}"
                for speaker in speakers
            ]

        # Parse script
        script = None
        if pd.notnull(row.get("Script")):
            script = row.get("Script").lower()

        # Parse description
        entries = []
        if pd.notnull(row.get("Description")):
            entries.append(row.get("Description"))

        return cls(
            source=json_source,
            name=row.get("Name", "Unnamed Language"),
            type=row.get("Type", "standard").lower(),
            typicalSpeakers=typical_speakers,
            script=script,
            page=0,
            entries=entries
        )
