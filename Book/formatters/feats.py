"""
Feat formatter for converting 5etools format to Google Docs.
"""

from typing import Dict, List, Any
from Book.formatters.base import BaseFormatter


class FeatFormatter(BaseFormatter):
    """Formatter for D&D feats."""

    def format_entity(self, feat: Dict[str, Any]) -> List[str]:
        """
        Format a feat entry.

        Args:
            feat: Feat dictionary in 5etools format

        Returns:
            List of formatted text lines
        """
        lines = []

        # Feat name (Heading 4)
        name = feat.get("name", "Unknown Feat")
        lines.extend(self.format_heading(name, level=4))

        # Prerequisites
        if "prerequisite" in feat:
            prereq_str = self._format_prerequisite(feat["prerequisite"])
            lines.extend(self.format_text(f"*Prerequisite: {prereq_str}*", italic=True))
            lines.append("")

        # Description
        entries = feat.get("entries", [])
        lines.extend(self.format_entries(entries))

        # Add spacing
        lines.append("")

        return lines

    def _format_prerequisite(self, prerequisite: List[Dict[str, Any]]) -> str:
        """Format feat prerequisites."""
        # Stub implementation
        parts = []
        for prereq in prerequisite:
            if isinstance(prereq, str):
                parts.append(prereq)
            elif isinstance(prereq, dict):
                # Handle complex prerequisites
                if "ability" in prereq:
                    for ability, value in prereq["ability"].items():
                        parts.append(f"{ability.upper()} {value}+")
                elif "level" in prereq:
                    parts.append(f"Level {prereq['level']}+")
                elif "spellcasting" in prereq:
                    parts.append("The ability to cast at least one spell")

        return ", ".join(parts) if parts else "None"
