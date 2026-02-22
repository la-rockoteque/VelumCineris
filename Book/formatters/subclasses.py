"""
Subclass formatter for converting 5etools format to Google Docs.
"""

from typing import Dict, List, Any
from Book.formatters.base import BaseFormatter


class SubclassFormatter(BaseFormatter):
    """Formatter for D&D subclasses."""

    def format_entity(self, subclass: Dict[str, Any]) -> List[str]:
        """
        Format a subclass entry.

        Args:
            subclass: Subclass dictionary in 5etools format

        Returns:
            List of formatted text lines
        """
        lines = []

        # Subclass name (Heading 3)
        name = subclass.get("name", "Unknown Subclass")
        class_name = subclass.get("className", "")

        if class_name:
            lines.extend(self.format_heading(f"{name} ({class_name})", level=3))
        else:
            lines.extend(self.format_heading(name, level=3))

        # Description
        entries = subclass.get("entries", [])
        lines.extend(self.format_entries(entries))

        # Subclass features (stub - would need complex formatting)
        if "subclassFeatures" in subclass:
            lines.append("")
            lines.extend(self.format_heading("Subclass Features", level=4))
            # TODO: Format subclass features

        # Add spacing
        lines.append("")

        return lines
