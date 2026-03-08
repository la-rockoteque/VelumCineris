"""
Monster formatter for converting 5etools format to Google Docs.
"""

from typing import Dict, List, Any
from Book.core.formatters.base import BaseFormatter


class MonsterFormatter(BaseFormatter):
    """Formatter for D&D monsters."""

    # Size abbreviations
    SIZE_MAP = {
        "T": "Tiny",
        "S": "Small",
        "M": "Medium",
        "L": "Large",
        "H": "Huge",
        "G": "Gargantuan",
    }

    # Ability scores
    ABILITIES = ["str", "dex", "con", "int", "wis", "cha"]

    def format_entity(self, monster: Dict[str, Any]) -> List[str]:
        """
        Format a monster stat block.

        Args:
            monster: Monster dictionary in 5etools format

        Returns:
            List of formatted text lines
        """
        lines = []

        # Monster name (Heading 3)
        name = monster.get("name", "Unknown Monster")
        lines.extend(self.format_heading(name, level=3))

        # Size, type, alignment (italic)
        size_type_alignment = self._format_size_type_alignment(monster)
        lines.extend(self.format_text(size_type_alignment, italic=True))

        # Horizontal rule
        lines.append("─" * 40)

        # AC
        ac_str = self._format_ac(monster.get("ac", []))
        lines.extend(self.format_property("Armor Class", ac_str))

        # HP
        hp_str = self._format_hp(monster.get("hp", {}))
        lines.extend(self.format_property("Hit Points", hp_str))

        # Speed
        speed_str = self._format_speed(monster.get("speed", {}))
        lines.extend(self.format_property("Speed", speed_str))

        # Horizontal rule
        lines.append("─" * 40)

        # Ability scores
        lines.extend(self._format_ability_scores(monster))

        # Horizontal rule
        lines.append("─" * 40)

        # Saves
        if "save" in monster:
            save_str = self._format_saves(monster["save"])
            lines.extend(self.format_property("Saving Throws", save_str))

        # Skills
        if "skill" in monster:
            skill_str = self._format_skills(monster["skill"])
            lines.extend(self.format_property("Skills", skill_str))

        # Damage resistances
        if "resist" in monster:
            resist_str = self._format_damage_types(monster["resist"])
            lines.extend(self.format_property("Damage Resistances", resist_str))

        # Damage immunities
        if "immune" in monster:
            immune_str = self._format_damage_types(monster["immune"])
            lines.extend(self.format_property("Damage Immunities", immune_str))

        # Condition immunities
        if "conditionImmune" in monster:
            condition_str = self._format_conditions(monster["conditionImmune"])
            lines.extend(self.format_property("Condition Immunities", condition_str))

        # Senses
        if "senses" in monster or "passive" in monster:
            senses_str = self._format_senses(monster)
            lines.extend(self.format_property("Senses", senses_str))

        # Languages
        if "languages" in monster:
            lang_str = self._format_languages(monster["languages"])
            lines.extend(self.format_property("Languages", lang_str))

        # CR
        cr = monster.get("cr", "0")
        lines.extend(self.format_property("Challenge", f"{cr} ({self._get_xp(cr)} XP)"))

        # Horizontal rule
        lines.append("─" * 40)

        # Traits
        if "trait" in monster:
            for trait in monster["trait"]:
                lines.extend(self._format_feature(trait))

        # Actions
        if "action" in monster:
            lines.append("")
            lines.extend(self.format_heading("Actions", level=4))
            for action in monster["action"]:
                lines.extend(self._format_feature(action))

        # Bonus Actions
        if "bonus" in monster:
            lines.append("")
            lines.extend(self.format_heading("Bonus Actions", level=4))
            for bonus in monster["bonus"]:
                lines.extend(self._format_feature(bonus))

        # Reactions
        if "reaction" in monster:
            lines.append("")
            lines.extend(self.format_heading("Reactions", level=4))
            for reaction in monster["reaction"]:
                lines.extend(self._format_feature(reaction))

        # Legendary Actions
        if "legendary" in monster:
            lines.append("")
            lines.extend(self.format_heading("Legendary Actions", level=4))
            for legendary in monster["legendary"]:
                lines.extend(self._format_feature(legendary))

        # Add spacing after monster
        lines.append("")
        lines.append("---")  # Page break
        lines.append("")

        return lines

    def _format_size_type_alignment(self, monster: Dict[str, Any]) -> str:
        """Format size, type, and alignment line."""
        size = monster.get("size", ["M"])
        if isinstance(size, list):
            size = size[0]
        size_name = self.SIZE_MAP.get(size, "Medium")

        creature_type = monster.get("type", "")
        if isinstance(creature_type, dict):
            type_name = creature_type.get("type", "humanoid")
            tags = creature_type.get("tags", [])
            if tags:
                tag_str = ", ".join(tags)
                type_name += f" ({tag_str})"
        else:
            type_name = creature_type if creature_type else "humanoid"

        alignment = monster.get("alignment", [])
        if isinstance(alignment, list):
            align_parts = []
            for align in alignment:
                if isinstance(align, dict):
                    # Complex alignment
                    align_parts.append("any alignment")
                elif isinstance(align, str):
                    align_parts.append(align)
            alignment_str = " or ".join(align_parts) if align_parts else "unaligned"
        else:
            alignment_str = alignment if alignment else "unaligned"

        return f"{size_name} {type_name}, {alignment_str}"

    def _format_ac(self, ac_list: List[Any]) -> str:
        """Format armor class."""
        if not ac_list:
            return "10"

        ac_entry = ac_list[0]
        if isinstance(ac_entry, int):
            return str(ac_entry)

        if isinstance(ac_entry, dict):
            ac_value = ac_entry.get("ac", 10)
            ac_from = ac_entry.get("from", [])

            if ac_from:
                from_str = ", ".join(ac_from)
                return f"{ac_value} ({from_str})"

            return str(ac_value)

        return "10"

    def _format_hp(self, hp: Dict[str, Any]) -> str:
        """Format hit points."""
        if not hp:
            return "1 (1d4)"

        average = hp.get("average", 1)
        formula = hp.get("formula", "1d4")

        return f"{average} ({formula})"

    def _format_speed(self, speed: Any) -> str:
        """Format speed."""
        if not speed:
            return "30 ft."

        # Handle string speed (e.g., "30 ft.")
        if isinstance(speed, str):
            return speed

        # Handle numeric speed
        if isinstance(speed, (int, float)):
            return f"{int(speed)} ft."

        # Handle dict speed
        if not isinstance(speed, dict):
            return "30 ft."

        parts = []

        # Walk speed
        walk = speed.get("walk", 0)
        if isinstance(walk, str):
            # Already formatted string like "30 ft."
            parts.append(walk)
        elif isinstance(walk, (int, float)):
            parts.append(f"{int(walk)} ft.")
        elif isinstance(walk, dict):
            amount = walk.get("number", walk.get("amount", 30))
            if isinstance(amount, (int, float)):
                amount = int(amount)
            parts.append(f"{amount} ft.")

        # Other movement types
        for move_type in ["fly", "swim", "climb", "burrow"]:
            if move_type in speed:
                value = speed[move_type]
                if isinstance(value, str):
                    # Already formatted
                    parts.append(f"{move_type} {value}")
                elif isinstance(value, (int, float)):
                    parts.append(f"{move_type} {int(value)} ft.")
                elif isinstance(value, dict):
                    amount = value.get("number", value.get("amount", 0))
                    if isinstance(amount, (int, float)):
                        amount = int(amount)
                    condition = value.get("condition", "")
                    move_str = f"{move_type} {amount} ft."
                    if condition:
                        move_str += f" ({condition})"
                    parts.append(move_str)

        return ", ".join(parts) if parts else "30 ft."

    def _format_ability_scores(self, monster: Dict[str, Any]) -> List[str]:
        """Format ability score table."""
        lines = []

        # Headers
        headers = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        values = []

        for ability in self.ABILITIES:
            score = monster.get(ability, 10)
            modifier = (score - 10) // 2
            mod_str = f"+{modifier}" if modifier >= 0 else str(modifier)
            values.append(f"{score} ({mod_str})")

        # Format as table
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join(["---"] * 6) + " |")
        lines.append("| " + " | ".join(values) + " |")

        return lines

    def _format_saves(self, saves: Dict[str, str]) -> str:
        """Format saving throws."""
        parts = []
        for ability, value in saves.items():
            parts.append(f"{ability.upper()} {value}")
        return ", ".join(parts)

    def _format_skills(self, skills: Dict[str, str]) -> str:
        """Format skills."""
        parts = []
        for skill, value in skills.items():
            skill_name = skill.replace("_", " ").title()
            parts.append(f"{skill_name} {value}")
        return ", ".join(parts)

    def _format_damage_types(self, damage_types: List[Any]) -> str:
        """Format damage types (resistances/immunities)."""
        if isinstance(damage_types, list):
            return ", ".join(str(dt) for dt in damage_types)
        return str(damage_types)

    def _format_conditions(self, conditions: List[str]) -> str:
        """Format condition immunities."""
        return ", ".join(conditions)

    def _format_senses(self, monster: Dict[str, Any]) -> str:
        """Format senses."""
        parts = []

        senses = monster.get("senses", [])
        if isinstance(senses, list):
            parts.extend(senses)

        passive = monster.get("passive", 10)
        parts.append(f"passive Perception {passive}")

        return ", ".join(parts)

    def _format_languages(self, languages: List[str]) -> str:
        """Format languages."""
        if not languages:
            return "—"
        return ", ".join(languages)

    def _get_xp(self, cr: str) -> str:
        """Get XP value for CR."""
        xp_map = {
            "0": "0 or 10",
            "1/8": "25",
            "1/4": "50",
            "1/2": "100",
            "1": "200",
            "2": "450",
            "3": "700",
            "4": "1,100",
            "5": "1,800",
            "6": "2,300",
            "7": "2,900",
            "8": "3,900",
            "9": "5,000",
            "10": "5,900",
            "11": "7,200",
            "12": "8,400",
            "13": "10,000",
            "14": "11,500",
            "15": "13,000",
            "16": "15,000",
            "17": "18,000",
            "18": "20,000",
            "19": "22,000",
            "20": "25,000",
            "21": "33,000",
            "22": "41,000",
            "23": "50,000",
            "24": "62,000",
            "25": "75,000",
            "26": "90,000",
            "27": "105,000",
            "28": "120,000",
            "29": "135,000",
            "30": "155,000",
        }
        return xp_map.get(str(cr), "0")

    def _format_feature(self, feature: Dict[str, Any]) -> List[str]:
        """Format a trait/action/reaction/legendary action."""
        lines = []

        # Feature name
        name = feature.get("name", "")
        if name:
            lines.extend(self.format_text(name, bold=True))

        # Feature entries
        entries = feature.get("entries", [])
        lines.extend(self.format_entries(entries))

        lines.append("")

        return lines
