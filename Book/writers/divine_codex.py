"""
Divine Codex writer - contains deities and related lore.
"""

from typing import List, Tuple, Optional, Callable
from Book.writers.base import BaseWriter


class DivineCodexWriter(BaseWriter):
    """Writer for Divine Codex style book."""

    def get_book_title(self) -> str:
        """Get the title of the book."""
        if self.source == "fantasy":
            return "Orimond Divine Codex"
        else:
            return "Vestigium Divine Codex"

    def get_sections(self) -> List[Tuple[str, str, Optional[Callable]]]:
        """
        Get sections for Divine Codex.

        Returns:
            List of (section_name, entity_type, filter_func) tuples
        """
        # Divine Codex would contain deities, but that entity type isn't implemented yet
        # Placeholder for now
        return [
            # ("Deities", "deity", None),  # TODO: Implement deity formatter
        ]
