"""
Class formatter for converting 5etools format to Google Docs.
"""

from typing import Dict, List, Any
from Book.core.formatters.base import BaseFormatter


class ClassFormatter(BaseFormatter):
    """Formatter for D&D classes."""

    def format_entity(self, cls: Dict[str, Any]) -> List[str]:
        """
        Format a class entry.

        Args:
            cls: Class dictionary in 5etools format

        Returns:
            List of formatted text lines
        """
        lines = []

        # Class name (Heading 2)
        name = cls.get("name", "Unknown Class")
        lines.extend(self.format_heading(name, level=2))

        # Description
        entries = cls.get("entries", [])
        lines.extend(self.format_entries(entries))

        # Class features (stub - would need complex formatting)
        if "classFeatures" in cls:
            lines.append("")
            lines.extend(self.format_heading("Class Features", level=3))
            # TODO: Format class features

        # Add spacing
        lines.append("")
        lines.append("")

        return lines
