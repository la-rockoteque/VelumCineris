"""
Dungeon Master's Guide writer - contains DM-facing content.
"""

from typing import List, Tuple, Optional, Callable
from Book.core.writers.base import BaseWriter


class DMGWriter(BaseWriter):
    """Writer for Dungeon Master's Guide style book."""

    def get_book_title(self) -> str:
        """Get the title of the book."""
        if self.source == "fantasy":
            return "Orimond Dungeon Master's Guide"
        else:
            return "Vestigium Dungeon Master's Guide"

    def get_sections(self) -> List[Tuple[str, str, Optional[Callable]]]:
        """
        Get sections for Dungeon Master's Guide.

        Returns:
            List of (section_name, entity_type, filter_func) tuples
        """
        # DMG contains DM-facing content
        return [
            ("Magic Items", "magicitem", None),
            ("Diseases", "disease", None),
            ("Languages", "language", None),
        ]
