"""
Species/Race formatter for converting 5etools format to Google Docs.
"""

from typing import Dict, List, Any
from Book.formatters.base import BaseFormatter


class SpeciesFormatter(BaseFormatter):
    """Formatter for D&D species/races."""

    def format_entity(self, race: Dict[str, Any]) -> List[str]:
        """
        Format a species/race entry.

        Args:
            race: Race dictionary in 5etools format

        Returns:
            List of formatted text lines
        """
        lines = []

        # Race name (Heading 3)
        name = race.get("name", "Unknown Race")
        lines.extend(self.format_heading(name, level=3))

        # Flavor text (italic)
        flavor = race.get("flavor", "")
        if flavor:
            lines.extend(self.format_text(flavor, italic=True))
            lines.append("")

        # Description entries
        entries = race.get("entries", [])
        lines.extend(self.format_entries(entries))

        # Racial traits section
        if "trait" in race or "ability" in race:
            lines.append("")
            lines.extend(self.format_heading("Racial Traits", level=4))

        # Ability score increases
        if "ability" in race:
            ability_str = self._format_ability_scores(race["ability"])
            lines.extend(self.format_property("Ability Score Increase", ability_str, bold_label=True))

        # Age
        age = race.get("age", {})
        if age:
            age_text = self._format_age(age)
            if age_text:
                lines.extend(self.format_property("Age", age_text, bold_label=True))

        # Size
        size = race.get("size", "")
        if size:
            size_text = self._format_size(size)
            lines.extend(self.format_property("Size", size_text, bold_label=True))

        # Speed
        speed = race.get("speed", {})
        if speed:
            speed_text = self._format_speed(speed)
            lines.extend(self.format_property("Speed", speed_text, bold_label=True))

        # Languages
        if "languageProficiencies" in race:
            lang_text = self._format_languages(race["languageProficiencies"])
            lines.extend(self.format_property("Languages", lang_text, bold_label=True))

        # Traits
        if "trait" in race:
            lines.append("")
            for trait in race["trait"]:
                lines.extend(self._format_trait(trait))

        # Add spacing after race
        lines.append("")
        lines.append("---")  # Page break or horizontal rule
        lines.append("")

        return lines

    def _format_ability_scores(self, ability_list: List[Dict[str, Any]]) -> str:
        """Format ability score increases."""
        if not ability_list:
            return "None"

        parts = []
        for ability_entry in ability_list:
            # Check for "choose" format
            if "choose" in ability_entry:
                choose = ability_entry["choose"]
                from_list = choose.get("from", [])
                count = choose.get("count", 1)
                amount = choose.get("amount", 1)

                if from_list:
                    abilities = ", ".join(from_list)
                    parts.append(f"Increase {count} of [{abilities}] by {amount}")
                else:
                    parts.append(f"Increase {count} ability scores of your choice by {amount}")

            else:
                # Direct ability scores
                for ability, value in ability_entry.items():
                    if ability in ["str", "dex", "con", "int", "wis", "cha"]:
                        parts.append(f"{ability.upper()} +{value}")

        return ", ".join(parts) if parts else "None"

    def _format_age(self, age: Dict[str, Any]) -> str:
        """Format age information."""
        if isinstance(age, str):
            return age

        mature = age.get("mature", "")
        max_age = age.get("max", "")

        if mature and max_age:
            return f"Mature by {mature}, live up to {max_age} years"
        elif mature:
            return f"Mature by {mature}"
        elif max_age:
            return f"Live up to {max_age} years"

        return ""

    def _format_size(self, size: Any) -> str:
        """Format size information."""
        if isinstance(size, str):
            return size

        if isinstance(size, list):
            return ", ".join(size)

        return "Medium"

    def _format_speed(self, speed: Any) -> str:
        """Format speed information."""
        # Handle string speed (e.g., "30 ft.")
        if isinstance(speed, str):
            return speed

        # Handle numeric speed
        if isinstance(speed, (int, float)):
            return f"{int(speed)} feet"

        if isinstance(speed, dict):
            walk = speed.get("walk", 30)

            # Handle string, int, or float walk speed
            if isinstance(walk, str):
                # Extract number from string like "30 ft."
                import re
                match = re.search(r'\d+', walk)
                walk_value = int(match.group()) if match else 30
            elif isinstance(walk, (int, float)):
                walk_value = int(walk)
            else:
                walk_value = 30

            parts = [f"{walk_value} feet"]

            # Other movement types
            for move_type in ["fly", "swim", "climb", "burrow"]:
                if move_type in speed:
                    value = speed[move_type]
                    if isinstance(value, (int, float)):
                        parts.append(f"{move_type} {int(value)} feet")
                    elif isinstance(value, str):
                        # Already formatted string
                        parts.append(f"{move_type} {value}")
                    elif isinstance(value, dict):
                        amount = value.get("number", value.get("amount", 0))
                        if isinstance(amount, (int, float)):
                            amount = int(amount)
                        condition = value.get("condition", "")
                        move_str = f"{move_type} {amount} feet"
                        if condition:
                            move_str += f" ({condition})"
                        parts.append(move_str)

            return ", ".join(parts)

        return "30 feet"

    def _format_languages(self, lang_list: List[Dict[str, Any]]) -> str:
        """Format language proficiencies."""
        parts = []

        for lang_entry in lang_list:
            # Direct languages
            for lang_key in lang_entry:
                if lang_key == "common":
                    parts.append("Common")
                elif lang_key == "anyStandard":
                    count = lang_entry[lang_key]
                    parts.append(f"Any {count} standard language{'s' if count > 1 else ''}")
                elif lang_key != "choose":
                    parts.append(lang_key.capitalize())

            # Choose format
            if "choose" in lang_entry:
                choose = lang_entry["choose"]
                from_list = choose.get("from", [])
                count = choose.get("count", 1)

                if from_list:
                    langs = ", ".join(from_list)
                    parts.append(f"Choose {count} from: {langs}")
                else:
                    parts.append(f"Choose {count} language{'s' if count > 1 else ''}")

        return ", ".join(parts) if parts else "None"

    def _format_trait(self, trait: Dict[str, Any]) -> List[str]:
        """Format a racial trait."""
        lines = []

        # Trait name
        name = trait.get("name", "")
        if name:
            lines.extend(self.format_text(name, bold=True))

        # Trait entries
        entries = trait.get("entries", [])
        lines.extend(self.format_entries(entries))

        lines.append("")

        return lines
