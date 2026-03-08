"""
Item formatter for converting 5etools format to Google Docs.
"""

from typing import Dict, List, Any
from Book.core.formatters.base import BaseFormatter


class ItemFormatter(BaseFormatter):
    """Formatter for D&D items and equipment."""

    def format_entity(self, item: Dict[str, Any]) -> List[str]:
        """
        Format an item entry.

        Args:
            item: Item dictionary in 5etools format

        Returns:
            List of formatted text lines
        """
        lines = []

        # Item name (Heading 4)
        name = item.get("name", "Unknown Item")
        lines.extend(self.format_heading(name, level=4))

        # Type and rarity
        item_type = item.get("type", "Item")
        rarity = item.get("rarity", "common")
        lines.extend(self.format_text(f"*{item_type}, {rarity}*", italic=True))

        # Cost
        if "value" in item:
            cost = item.get("value", 0)
            lines.extend(self.format_property("Cost", f"{cost} gp"))

        # Weight
        if "weight" in item:
            weight = item.get("weight", 0)
            lines.extend(self.format_property("Weight", f"{weight} lb."))

        # Description
        entries = item.get("entries", [])
        if entries:
            lines.append("")
            lines.extend(self.format_entries(entries))

        # Add spacing
        lines.append("")

        return lines
