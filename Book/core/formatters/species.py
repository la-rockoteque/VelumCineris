"""
Species/Race formatter — PHB-style layout.

Entry layout:
  ## Species Name          (H2: section break, one-column header, then two-column body)
  *Subtitle / quote*       (italic)
  Intro paragraphs         (untitled body copy)
  #### Lore Section        (H4: stays in two-column flow)
  ─────────────────        (ornamental gold rule below each H4)
  Lore body text
  #### Species Traits      (H4 + rule)
  **Trait Name.** Description text (inline bold label, PHB style)
"""

from typing import Dict, List, Any

from Book.core.formatters.base import BaseFormatter

_ORNAMENTAL_RULE = "─" * 30
_LORE_SECTION_ORDER = [
    "Origin",
    "Appearance",
    "Culture & Identity",
    "Societal Roles",
    "Naming Conventions",
    "Life in Orimond",
    "Life in the City",
    "Playstyle & Roleplaying",
]
_ABILITY_NAMES = {
    "str": "Strength",
    "dex": "Dexterity",
    "con": "Constitution",
    "int": "Intelligence",
    "wis": "Wisdom",
    "cha": "Charisma",
}


class SpeciesFormatter(BaseFormatter):
    """Formatter for D&D species/races — PHB-style."""

    def format_entity(self, race: Dict[str, Any]) -> List[str]:
        lines: List[str] = []
        name = race.get("name", "Unknown Race")

        lines.extend(self.format_heading(name, level=2))

        subtitle = self._subtitle_for_species(race)
        if subtitle:
            lines.extend(self.format_text(subtitle, italic=True))
            lines.append("")

        quote = race.get("quote")
        if isinstance(quote, str) and quote.strip():
            lines.extend(self.format_text(quote.strip(), italic=True))
            lines.append("")

        fluff_sections = self._collect_fluff_sections(race)

        intro_entries = fluff_sections.pop("Intro", [])
        if intro_entries:
            lines.extend(self.format_entries(intro_entries))
            lines.append("")

        for section_name, section_entries in self._ordered_fluff_sections(fluff_sections):
            lines.extend(self.format_heading(section_name, level=4))
            lines.append(_ORNAMENTAL_RULE)
            lines.extend(self.format_entries(section_entries))
            lines.append("")

        raw_entries = race.get("entries", [])
        trait_dicts = [entry for entry in raw_entries if isinstance(entry, dict)]
        trait_body_lines = [
            entry
            for entry in raw_entries
            if isinstance(entry, str) and entry.strip() and entry.strip() != f"{name} Traits"
        ]

        ability = race.get("ability") or []
        has_content = bool(ability or trait_dicts or trait_body_lines)

        if has_content:
            lines.extend(self.format_heading(f"{name} Traits", level=4))
            lines.append(_ORNAMENTAL_RULE)

            if ability:
                ability_text = self._format_ability_scores(ability)
                lines.extend(self._format_trait_inline("Ability Score Increase", [ability_text]))

            for trait_line in trait_body_lines:
                lines.append(trait_line)
                lines.append("")

            for entry in trait_dicts:
                trait_name = str(entry.get("name", "")).strip()
                trait_body = entry.get("entries", [])
                if trait_name:
                    lines.extend(self._format_trait_inline(trait_name, trait_body))

        lines.append("")
        return lines

    # ── helpers ────────────────────────────────────────────────────────────────

    def _format_trait_inline(self, name: str, body: List[Any]) -> List[str]:
        """Render as  **Name.** First-paragraph text  (PHB inline style)."""
        if not body:
            return [f"**{name}.**", ""]

        first, rest = body[0], body[1:]
        lines: List[str] = []

        if isinstance(first, str):
            lines.append(f"**{name}.** {first.strip()}")
        elif isinstance(first, (int, float, bool)):
            lines.append(f"**{name}.** {first}")
        else:
            lines.append(f"**{name}.**")
            lines.extend(self.format_entries([first]))

        for item in rest:
            if isinstance(item, str):
                lines.append(item.strip())
            elif isinstance(item, (int, float, bool)):
                lines.append(str(item))
            else:
                lines.extend(self.format_entries([item]))

        lines.append("")
        return lines

    def _format_ability_scores(self, ability_list: List[Dict[str, Any]]) -> str:
        """Summarise ability score increases in PHB-style prose."""
        parts: List[str] = []
        for entry in ability_list:
            if "choose" in entry:
                choose = entry["choose"]
                from_list = choose.get("from", [])
                count = choose.get("count", 1)
                amount = choose.get("amount", 1)
                if from_list:
                    abilities = ", ".join(
                        _ABILITY_NAMES.get(str(ability)[:3].lower(), str(ability))
                        for ability in from_list
                    )
                    parts.append(
                        f"increase {count} of these scores by {amount}: {abilities}"
                    )
                else:
                    parts.append(
                        f"increase {count} ability score{'s' if count != 1 else ''} "
                        f"of your choice by {amount}"
                    )
            else:
                for ability, value in entry.items():
                    if ability in ("str", "dex", "con", "int", "wis", "cha"):
                        parts.append(
                            f"your {_ABILITY_NAMES[ability]} score increases by {value}"
                        )

        if not parts:
            return "None"
        if len(parts) == 1:
            return self._sentence_case(parts[0]) + "."
        return self._sentence_case(", ".join(parts[:-1])) + f", and {parts[-1]}."

    def _subtitle_for_species(self, race: Dict[str, Any]) -> str:
        subtitle_parts: List[str] = []

        alias_values = race.get("alias") or []
        if alias_values:
            alias_value = str(alias_values[0]).strip()
            if alias_value:
                subtitle_parts.append(alias_value)

        slogan = race.get("slogan")
        if isinstance(slogan, str) and slogan.strip():
            subtitle_parts.append(slogan.strip())

        return " • ".join(subtitle_parts)

    def _collect_fluff_sections(self, race: Dict[str, Any]) -> Dict[str, List[Any]]:
        sections: Dict[str, List[Any]] = {}
        for section in race.get("fluff", {}).get("entries", []):
            if not isinstance(section, dict):
                continue
            section_name = str(section.get("name", "")).strip()
            if not section_name:
                continue
            section_entries = section.get("entries", [])
            if section_entries:
                sections[section_name] = section_entries
        return sections

    def _ordered_fluff_sections(
        self,
        sections: Dict[str, List[Any]],
    ) -> List[tuple[str, List[Any]]]:
        ordered: List[tuple[str, List[Any]]] = []
        seen: set[str] = set()

        for section_name in _LORE_SECTION_ORDER:
            if section_name in sections:
                ordered.append((section_name, sections[section_name]))
                seen.add(section_name)

        for section_name, entries in sections.items():
            if section_name not in seen:
                ordered.append((section_name, entries))

        return ordered

    def _sentence_case(self, text: str) -> str:
        if not text:
            return text
        return text[0].upper() + text[1:]
