"""
Disease formatter for converting 5etools format to Google Docs.
"""

from typing import Dict, List, Any
from Book.core.formatters.base import BaseFormatter


class DiseaseFormatter(BaseFormatter):
    """Formatter for D&D diseases."""

    def format_entity(self, disease: Dict[str, Any]) -> List[str]:
        """
        Format a disease entry.

        Args:
            disease: Disease dictionary in 5etools format

        Returns:
            List of formatted text lines
        """
        lines = []

        # Disease name (Heading 4)
        name = disease.get("name", "Unknown Disease")
        lines.extend(self.format_heading(name, level=4))

        # Rarity/Type
        if "type" in disease:
            disease_type = disease.get("type", "")
            lines.extend(self.format_text(f"*{disease_type}*", italic=True))

        # Description
        entries = disease.get("entries", [])
        lines.extend(self.format_entries(entries))

        # Add spacing
        lines.append("")

        return lines
