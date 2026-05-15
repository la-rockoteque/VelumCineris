"""
Background formatter for converting 5etools format to Google Docs.
"""

from typing import Dict, List, Any
from Book.core.formatters.base import BaseFormatter


class BackgroundFormatter(BaseFormatter):
    """Formatter for D&D backgrounds."""

    def format_entity(self, background: Dict[str, Any]) -> List[str]:
        """
        Format a background entry.

        Args:
            background: Background dictionary in 5etools format

        Returns:
            List of formatted text lines
        """
        lines = []

        # Background name (Heading 3)
        name = background.get("name", "Unknown Background")
        lines.extend(self.format_heading(name, level=3))

        # Description
        entries = background.get("entries", [])
        lines.extend(self.format_entries(entries))

        # Skill proficiencies
        if "skillProficiencies" in background:
            skill_str = self._format_skill_proficiencies(background["skillProficiencies"])
            lines.extend(self.format_property("Skill Proficiencies", skill_str))

        # Language proficiencies
        if "languageProficiencies" in background:
            lang_str = self._format_language_proficiencies(background["languageProficiencies"])
            lines.extend(self.format_property("Languages", lang_str))

        # Tool proficiencies
        if "toolProficiencies" in background:
            tool_str = self._format_tool_proficiencies(background["toolProficiencies"])
            lines.extend(self.format_property("Tool Proficiencies", tool_str))

        # Equipment
        if "startingEquipment" in background:
            equip_str = self._format_equipment(background["startingEquipment"])
            lines.extend(self.format_property("Equipment", equip_str))

        # Feature
        if "feature" in background:
            lines.append("")
            for feature in background["feature"]:
                lines.extend(self._format_feature(feature))

        # Add spacing
        lines.append("")
        lines.append("")

        return lines

    def _format_skill_proficiencies(self, skills: List[Dict[str, Any]]) -> str:
        """Format skill proficiencies."""
        # Stub implementation
        return str(skills)

    def _format_language_proficiencies(self, languages: List[Dict[str, Any]]) -> str:
        """Format language proficiencies."""
        # Stub implementation
        return str(languages)

    def _format_tool_proficiencies(self, tools: List[Dict[str, Any]]) -> str:
        """Format tool proficiencies."""
        # Stub implementation
        return str(tools)

    def _format_equipment(self, equipment: List[Any]) -> str:
        """Format starting equipment."""
        # Stub implementation
        return str(equipment)

    def _format_feature(self, feature: Dict[str, Any]) -> List[str]:
        """Format a background feature."""
        lines = []

        name = feature.get("name", "")
        if name:
            lines.extend(self.format_text(name, bold=True))

        entries = feature.get("entries", [])
        lines.extend(self.format_entries(entries))

        lines.append("")

        return lines
