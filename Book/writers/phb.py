"""
Player's Handbook writer - contains player-facing content only.
"""

from typing import List, Tuple, Optional, Callable
from Book.writers.base import BaseWriter


class PHBWriter(BaseWriter):
    """Writer for Player's Handbook style book."""

    def get_book_title(self) -> str:
        """Get the title of the book."""
        if self.source == "fantasy":
            return "Orimond Player's Handbook"
        else:
            return "Vestigium Player's Handbook"

    def get_sections(self) -> List[Tuple[str, str, Optional[Callable]]]:
        """
        Get sections for Player's Handbook.

        Returns:
            List of (section_name, entity_type, filter_func) tuples
        """
        # PHB contains player-facing content only
        sections = [
            ("Races", "species", None),
            ("Backgrounds", "background", None),
            ("Feats", "feat", None),
            (
                "Spells",
                "spell",
                lambda s: sorted(s, key=lambda x: (x.get("level", 0), x.get("name", ""))),
            ),
        ]

        # Add classes for modern setting
        if self.source == "modern":
            sections.insert(1, ("Classes", "class", None))
            sections.insert(2, ("Subclasses", "subclass", None))
            sections.insert(-1, ("Equipment", "item", None))

        return sections
