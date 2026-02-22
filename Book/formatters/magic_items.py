"""
Magic item formatter for converting 5etools format to Google Docs.
"""

from typing import Dict, List, Any
from Book.formatters.base import BaseFormatter


class MagicItemFormatter(BaseFormatter):
    """Formatter for D&D magic items."""

    # Rarity abbreviations
    RARITY_MAP = {
        "common": "Common",
        "uncommon": "Uncommon",
        "rare": "Rare",
        "very rare": "Very Rare",
        "legendary": "Legendary",
        "artifact": "Artifact",
    }

    def format_entity(self, item: Dict[str, Any]) -> List[str]:
        """
        Format a magic item entry.

        Args:
            item: Magic item dictionary in 5etools format

        Returns:
            List of formatted text lines
        """
        lines = []

        # Item name (Heading 4)
        name = item.get("name", "Unknown Magic Item")
        lines.extend(self.format_heading(name, level=4))

        # Type and rarity
        item_type = item.get("type", "Wondrous item")
        rarity = item.get("rarity", "uncommon")
        rarity_name = self.RARITY_MAP.get(rarity, rarity.capitalize())

        attunement = item.get("reqAttune", "")
        if attunement:
            if isinstance(attunement, bool):
                attunement_str = " (requires attunement)"
            elif isinstance(attunement, str):
                attunement_str = f" (requires attunement {attunement})"
            else:
                attunement_str = ""
        else:
            attunement_str = ""

        lines.extend(self.format_text(f"*{item_type}, {rarity_name}{attunement_str}*", italic=True))

        # Description
        entries = item.get("entries", [])
        if entries:
            lines.append("")
            lines.extend(self.format_entries(entries))

        # Add spacing
        lines.append("")

        return lines
