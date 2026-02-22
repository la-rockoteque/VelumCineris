"""
Spell formatter for converting 5etools spell format to Google Docs.
"""

from typing import Dict, List, Any
from Book.formatters.base import BaseFormatter


class SpellFormatter(BaseFormatter):
    """Formatter for D&D spells."""

    # School abbreviation to full name
    SCHOOL_NAMES = {
        "A": "Abjuration",
        "C": "Conjuration",
        "D": "Divination",
        "E": "Enchantment",
        "V": "Evocation",
        "I": "Illusion",
        "N": "Necromancy",
        "T": "Transmutation",
    }

    def format_entity(self, spell: Dict[str, Any]) -> List[str]:
        """
        Format a spell entry.

        Args:
            spell: Spell dictionary in 5etools format

        Returns:
            List of formatted text lines
        """
        lines = []

        # Spell name (Heading 4)
        name = spell.get("name", "Unknown Spell")
        lines.extend(self.format_heading(name, level=4))

        # Level and school (italic)
        level = spell.get("level", 0)
        school = spell.get("school", "A")
        school_name = self.SCHOOL_NAMES.get(school, "Abjuration")

        if level == 0:
            level_text = f"{school_name} cantrip"
        else:
            level_text = f"{self._ordinal(level)}-level {school_name}"

        lines.extend(self.format_text(level_text, italic=True))

        # Casting time
        time_str = self._format_time(spell.get("time", []))
        lines.extend(self.format_property("Casting Time", time_str))

        # Range
        range_str = self._format_range(spell.get("range", {}))
        lines.extend(self.format_property("Range", range_str))

        # Components
        components_str = self._format_components(spell.get("components", {}))
        lines.extend(self.format_property("Components", components_str))

        # Duration
        duration_str = self._format_duration(spell.get("duration", []))
        lines.extend(self.format_property("Duration", duration_str))

        # Add blank line before description
        lines.append("")

        # Description
        entries = spell.get("entries", [])
        lines.extend(self.format_entries(entries))

        # Higher levels
        if "entriesHigherLevel" in spell:
            lines.append("")
            lines.extend(self.format_text("At Higher Levels.", bold=True))
            higher_entries = spell["entriesHigherLevel"]

            if isinstance(higher_entries, list):
                lines.extend(self.format_entries(higher_entries))
            elif isinstance(higher_entries, dict):
                # Sometimes it's wrapped in a dict
                higher_list = higher_entries.get("entries", [])
                lines.extend(self.format_entries(higher_list))

        # Add spacing after spell
        lines.append("")

        return lines

    def _ordinal(self, n: int) -> str:
        """Convert number to ordinal string (1 -> 1st, 2 -> 2nd, etc.)."""
        if 10 <= n % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"

    def _format_time(self, time_list: List[Dict[str, Any]]) -> str:
        """Format casting time."""
        if not time_list:
            return "1 action"

        time_entry = time_list[0]
        number = time_entry.get("number", 1)
        unit = time_entry.get("unit", "action")

        time_str = f"{number} {unit}"
        if number != 1:
            time_str += "s"

        # Check for conditions
        condition = time_entry.get("condition", "")
        if condition:
            time_str += f", {condition}"

        return time_str

    def _format_range(self, range_dict: Dict[str, Any]) -> str:
        """Format spell range."""
        if not range_dict:
            return "Self"

        range_type = range_dict.get("type", "point")

        if range_type == "point":
            distance = range_dict.get("distance", {})
            dist_type = distance.get("type", "self")

            if dist_type == "self":
                return "Self"
            elif dist_type == "touch":
                return "Touch"
            elif dist_type == "sight":
                return "Sight"
            elif dist_type == "unlimited":
                return "Unlimited"
            else:
                amount = distance.get("amount", 0)
                return f"{amount} feet"

        elif range_type in ["radius", "sphere", "cube", "cone", "line", "hemisphere"]:
            distance = range_dict.get("distance", {})
            amount = distance.get("amount", 0)
            return f"Self ({amount}-foot {range_type})"

        return "Special"

    def _format_components(self, components: Dict[str, Any]) -> str:
        """Format spell components."""
        parts = []

        if components.get("v"):
            parts.append("V")
        if components.get("s"):
            parts.append("S")
        if components.get("m"):
            material = components.get("m", "")
            if isinstance(material, str):
                parts.append(f"M ({material})")
            elif isinstance(material, dict):
                # Handle complex material format
                text = material.get("text", "")
                parts.append(f"M ({text})")
            else:
                parts.append("M")

        return ", ".join(parts) if parts else "None"

    def _format_duration(self, duration_list: List[Dict[str, Any]]) -> str:
        """Format spell duration."""
        if not duration_list:
            return "Instantaneous"

        duration_entry = duration_list[0]
        dur_type = duration_entry.get("type", "instant")

        if dur_type == "instant":
            return "Instantaneous"
        elif dur_type == "permanent":
            ends = duration_entry.get("ends", [])
            if ends:
                return f"Until {', '.join(ends)}"
            return "Permanent"
        elif dur_type == "special":
            return "Special"
        else:
            # Timed duration
            number = duration_entry.get("duration", {}).get("amount", 1)
            unit = duration_entry.get("duration", {}).get("type", "minute")

            dur_str = f"{number} {unit}"
            if number != 1:
                dur_str += "s"

            # Check for concentration
            if duration_entry.get("concentration"):
                dur_str = f"Concentration, up to {dur_str}"

            return dur_str
