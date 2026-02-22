"""
Omnibook writer - generates complete book with ALL entity types.
"""

from typing import List, Tuple, Optional, Callable
from Book.writers.base import BaseWriter


class OmnibookWriter(BaseWriter):
    """Writer for complete omnibus book containing all content."""

    def get_book_title(self) -> str:
        """Get the title of the book."""
        if self.source == "fantasy":
            return "Orimond Omnibook"
        else:
            return "Vestigium Omnibook"

    def get_sections(self) -> List[Tuple[str, str, Optional[Callable]]]:
        """
        Get all sections for the omnibus book.

        Returns:
            List of (section_name, entity_type, filter_func) tuples
        """
        if self.source == "fantasy":
            return self._get_fantasy_sections()
        else:
            return self._get_modern_sections()

    def _get_fantasy_sections(self) -> List[Tuple[str, str, Optional[Callable]]]:
        """Get sections for fantasy setting."""
        return [
            ("Races", "species", None),
            ("Monsters", "monster", lambda m: sorted(m, key=lambda x: x.get("cr", 0))),
            (
                "Spells",
                "spell",
                lambda s: sorted(s, key=lambda x: (x.get("level", 0), x.get("name", ""))),
            ),
            ("Magic Items", "magicitem", None),
            ("Languages", "language", None),
            ("Diseases", "disease", None),
        ]

    def _get_modern_sections(self) -> List[Tuple[str, str, Optional[Callable]]]:
        """Get sections for modern setting."""
        return [
            ("Races", "species", None),
            ("Classes", "class", None),
            ("Subclasses", "subclass", None),
            ("Backgrounds", "background", None),
            ("Feats", "feat", None),
            (
                "Spells",
                "spell",
                lambda s: sorted(s, key=lambda x: (x.get("level", 0), x.get("name", ""))),
            ),
            ("Items", "item", None),
            ("Magic Items", "magicitem", None),
            ("Monsters", "monster", lambda m: sorted(m, key=lambda x: x.get("cr", 0))),
            ("Languages", "language", None),
            ("Diseases", "disease", None),
        ]
