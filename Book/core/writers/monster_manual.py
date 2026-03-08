"""
Monster Manual writer - contains monsters only.
"""

from typing import List, Tuple, Optional, Callable
from Book.core.writers.base import BaseWriter


class MonsterManualWriter(BaseWriter):
    """Writer for Monster Manual style book."""

    def get_book_title(self) -> str:
        """Get the title of the book."""
        if self.source == "fantasy":
            return "Orimond Monster Manual"
        else:
            return "Vestigium Monster Manual"

    def get_sections(self) -> List[Tuple[str, str, Optional[Callable]]]:
        """
        Get sections for Monster Manual.

        Returns:
            List of (section_name, entity_type, filter_func) tuples
        """
        # Monster Manual contains only monsters, sorted by CR
        return [
            (
                "Monsters",
                "monster",
                lambda m: sorted(m, key=lambda x: (x.get("cr", 0), x.get("name", ""))),
            ),
        ]
