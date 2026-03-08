"""
Language formatter for converting 5etools format to Google Docs.
"""

from typing import Dict, List, Any
from Book.core.formatters.base import BaseFormatter


class LanguageFormatter(BaseFormatter):
    """Formatter for D&D languages."""

    def format_entity(self, language: Dict[str, Any]) -> List[str]:
        """
        Format a language entry.

        Args:
            language: Language dictionary in 5etools format

        Returns:
            List of formatted text lines
        """
        lines = []

        # Language name (Heading 4)
        name = language.get("name", "Unknown Language")
        lines.extend(self.format_heading(name, level=4))

        # Type
        lang_type = language.get("type", "Standard")
        lines.extend(self.format_text(f"*{lang_type} language*", italic=True))

        # Script
        if "script" in language:
            script = language.get("script", "")
            lines.extend(self.format_property("Script", script))

        # Typical speakers
        if "typicalSpeakers" in language:
            speakers = language.get("typicalSpeakers", [])
            if isinstance(speakers, list):
                speakers_str = ", ".join(speakers)
            else:
                speakers_str = str(speakers)
            lines.extend(self.format_property("Typical Speakers", speakers_str))

        # Description
        entries = language.get("entries", [])
        if entries:
            lines.append("")
            lines.extend(self.format_entries(entries))

        # Add spacing
        lines.append("")

        return lines
