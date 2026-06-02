"""
Base formatter class for all entity formatters.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any


class BaseFormatter(ABC):
    """Abstract base class for entity formatters."""

    def __init__(self):
        """Initialize the formatter."""
        self.current_index = 1

    @abstractmethod
    def format_entity(self, entity: Dict[str, Any], /) -> List[str]:
        """
        Format an entity into text content.

        Args:
            entity: Entity dictionary in 5etools format

        Returns:
            List of text lines to be added to document
        """
        pass

    def format_heading(self, text: str, level: int = 2) -> List[str]:
        """
        Format a heading.

        Args:
            text: Heading text
            level: Heading level (1-4)

        Returns:
            List containing heading marker and text
        """
        markers = {1: "# ", 2: "## ", 3: "### ", 4: "#### "}
        marker = markers.get(level, "## ")
        return [f"{marker}{text}"]

    def format_property(
        self, label: str, value: Any, bold_label: bool = True
    ) -> List[str]:
        """
        Format a property line (e.g., "Casting Time: 1 action").

        Args:
            label: Property label
            value: Property value
            bold_label: Whether to bold the label

        Returns:
            List containing formatted property
        """
        if bold_label:
            return [f"**{label}:** {value}"]
        return [f"{label}: {value}"]

    def format_list_item(self, text: str, level: int = 0) -> List[str]:
        """
        Format a list item with optional indentation.

        Args:
            text: List item text
            level: Indentation level

        Returns:
            List containing formatted list item
        """
        indent = "  " * level
        return [f"{indent}- {text}"]

    def format_text(self, text: str, bold: bool = False, italic: bool = False) -> List[str]:
        """
        Format regular text with optional styling.

        Args:
            text: Text content
            bold: Apply bold styling
            italic: Apply italic styling

        Returns:
            List containing formatted text
        """
        if bold and italic:
            return [f"***{text}***"]
        elif bold:
            return [f"**{text}**"]
        elif italic:
            return [f"*{text}*"]
        return [text]

    def format_table(
        self, headers: List[str], rows: List[List[str]]
    ) -> List[str]:
        """
        Format a table (simplified markdown-style).

        Args:
            headers: Column headers
            rows: Table rows

        Returns:
            List containing table lines
        """
        lines = []

        # Header row
        lines.append("| " + " | ".join(headers) + " |")

        # Separator
        lines.append("| " + " | ".join(["---"] * len(headers)) + " |")

        # Data rows
        for row in rows:
            lines.append("| " + " | ".join(str(cell) for cell in row) + " |")

        return lines

    def format_entries(self, entries: List[Any]) -> List[str]:
        """
        Format entry content (handles strings and nested structures).

        Args:
            entries: List of entry content (strings or dicts)

        Returns:
            List of formatted text lines
        """
        lines = []

        for entry in entries:
            if isinstance(entry, str):
                lines.append(entry)
            elif isinstance(entry, dict):
                # Handle nested entry types (e.g., lists, tables)
                entry_type = entry.get("type", "")

                if entry_type == "list":
                    for item in entry.get("items", []):
                        if isinstance(item, str):
                            lines.extend(self.format_list_item(item))
                        elif isinstance(item, dict):
                            # Nested item with name
                            item_name = item.get("name", "")
                            item_entries = item.get("entries", [])
                            if item_name:
                                lines.extend(self.format_text(item_name, bold=True))
                            lines.extend(self.format_entries(item_entries))

                elif entry_type == "table":
                    headers = entry.get("colLabels", [])
                    rows = entry.get("rows", [])
                    lines.extend(self.format_table(headers, rows))

                elif entry_type == "entries":
                    # Nested entries with optional name
                    entry_name = entry.get("name", "")
                    if entry_name:
                        lines.extend(self.format_text(entry_name, bold=True))
                    lines.extend(self.format_entries(entry.get("entries", [])))

                else:
                    # Unknown type, try to get entries
                    if "entries" in entry:
                        lines.extend(self.format_entries(entry["entries"]))

        return lines

    def _clean_text(self, text: str) -> str:
        """
        Clean text by removing 5etools tags.

        Args:
            text: Raw text with possible tags

        Returns:
            Cleaned text
        """
        # Remove common 5etools tags like {@spell fireball}, {@dice 1d6}, etc.
        import re

        # Replace tags with just the content
        text = re.sub(r"\{@\w+\s+([^}]+)\}", r"\1", text)

        return text
