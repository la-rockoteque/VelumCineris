"""
Campaign handbook writer with full-book structure for Google Docs output.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional, Tuple

from Book.datasets import load_timeline_catalog
from Book.core.writers.base import BaseWriter

_COSMOLOGY_DOC_ID = "1Jy8hDGNodeoAhjlw8OciuO8ZvOOIiWXt0HTNULQ83Os"

EntityFilter = Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]
SectionSpec = Dict[str, Any]


class CampaignHandbookWriter(BaseWriter):
    """Writer for the full campaign handbook outline."""

    EMPTY_CHAPTER_NOTE = "*Outline scaffold for authored handbook content.*"

    def __init__(self, book_api, source: str = "fantasy", cover_image_url=None):
        if cover_image_url is None:
            cover_image_url = self.DEFAULT_COVER_IMAGE_URL
        super().__init__(book_api, source=source, cover_image_url=cover_image_url)
        self._timeline_catalog_cache: dict[str, Any] | None = None
        self._timeline_catalog_error: str | None = None
        self._cosmology_sections_cache: List[Tuple[str, List[str]]] | None = None

    def get_book_title(self) -> str:
        if self.source == "fantasy":
            return "Orimond Campaign Handbook"
        return "Vestigium Campaign Handbook"

    def get_sections(self) -> List[tuple[str, str, Optional[Callable]]]:
        # This writer uses build_document_lines() instead of flat section iteration.
        return []

    def build_document_lines(self) -> List[str]:
        lines: List[str] = []

        lines.extend(self._build_cover_page())
        lines.extend(self._build_front_matter())
        lines.extend(self._build_world_of_orimond())
        lines.extend(self._build_character_creation())
        lines.extend(self._build_rules_and_character_options())
        lines.extend(self._build_world_reference())
        lines.extend(self._build_appendices())

        return lines

    def _build_cover_page(self) -> List[str]:
        return self.write_cover_page()

    def _build_front_matter(self) -> List[str]:
        toc_lines = [
            "1. Title Page",
            "2. Credits",
            "3. Introduction",
            "4. How to Use This Book",
            "5. Table of Contents",
            "6. Quick Reference",
            "",
            "Part I. The World of Orimond",
            "Chapter 1. Setting Overview",
            "Chapter 2. History",
            "Chapter 3. Cosmology",
            "Chapter 4. Geography",
            "Chapter 5. Nations and Powers",
            "Chapter 6. Factions and Institutions",
            "Chapter 7. Culture and Society",
            "Chapter 8. Languages, Names, and Identity",
            "",
            "Part II. Character Creation",
            "Chapter 9. Creating a Character",
            "Chapter 10. Species",
            "Chapter 11. Cultures and Origins",
            "Chapter 12. Classes",
            "Chapter 13. Subclasses and Specializations",
            "Chapter 14. Backgrounds",
            "Chapter 15. Faith, Allegiance, and Conviction",
            "",
            "Part III. Rules and Character Options",
            "Chapter 16. Core Rules",
            "Chapter 17. Skills, Proficiencies, and Talents",
            "Chapter 18. Equipment",
            "Chapter 19. Magic",
            "Chapter 20. Powers, Gifts, and Special Systems",
            "Chapter 21. Combat",
            "Chapter 22. Exploration",
            "Chapter 23. Social Interaction",
            "Chapter 24. Downtime and Progression",
            "",
            "Part IV. World Reference",
            "Chapter 25. Religion and Divine Powers",
            "Chapter 26. Creatures and Peoples of the World",
            "Chapter 27. Relics, Artifacts, and Significant Objects",
            "Chapter 28. Calendar, Time, and Seasons",
            "Chapter 29. Names, Terms, and Glossary",
            "Chapter 30. Maps and Reference Tables",
            "",
            "Appendices A-I",
        ]

        lines = [
            "# Front Matter",
            "",
            "## 1. Title Page",
            "",
            "See the cover page at the beginning of this document.",
            "",
            "## 2. Credits",
            "",
            "*Production, editing, design, and playtest credits go here.*",
            "",
            "## 3. Introduction",
            "",
            "*Introduce the campaign, scope of the handbook, and intended audience.*",
            "",
            "## 4. How to Use This Book",
            "",
            "*Explain how player-facing sections, world reference, and appendices are organized.*",
            "",
            "## 5. Table of Contents",
            "",
            *toc_lines,
            "",
            "## 6. Quick Reference",
            "",
            "*Summarize recurring rules assumptions, terms, and cross-references here.*",
            "",
            "---",
            "",
        ]

        return lines

    def _build_world_of_orimond(self) -> List[str]:
        return self._build_part(
            "Part I. The World of Orimond",
            [
                (
                    "Chapter 1. Setting Overview",
                    [
                        "1.1 The World at a Glance",
                        "1.2 Core Themes",
                        "1.3 Tone and Atmosphere",
                        "1.4 Adventuring in Orimond",
                    ],
                ),
                (
                    "Chapter 2. History",
                    [
                        "2.1 Origins",
                        "2.2 Early Ages",
                        self._custom_section("2.3 Major Eras", self._render_major_eras),
                        self._custom_section("2.4 Defining Events", self._render_defining_events),
                        "2.5 Recent History",
                        self._custom_section("2.6 Historical Timeline", self._render_historical_timeline),
                    ],
                ),
                (
                    "Chapter 3. Cosmology",
                    self._cosmology_chapter_sections(),
                ),
                (
                    "Chapter 4. Geography",
                    [
                        "4.1 The World Map",
                        "4.2 Major Regions",
                        "4.3 Frontiers and Wilderness",
                        "4.4 Borders and Routes",
                        "4.5 Landmarks and Sites",
                        "4.6 Environmental Features",
                    ],
                ),
                (
                    "Chapter 5. Nations and Powers",
                    [
                        "5.1 Kingdoms and States",
                        "5.2 City-States and Territories",
                        "5.3 Political Orders",
                        "5.4 Military Powers",
                        "5.5 Economic Powers",
                        self._custom_section("5.6 Power Relations", self._render_power_relations),
                    ],
                ),
                (
                    "Chapter 6. Factions and Institutions",
                    [
                        "6.1 Religious Institutions",
                        "6.2 Arcane Institutions",
                        "6.3 Martial Orders",
                        "6.4 Guilds and Associations",
                        "6.5 Secret Societies",
                        "6.6 Other Organized Powers",
                    ],
                ),
                (
                    "Chapter 7. Culture and Society",
                    [
                        "7.1 Social Structures",
                        "7.2 Customs and Etiquette",
                        "7.3 Family and Kinship",
                        "7.4 Law and Justice",
                        "7.5 Economy and Daily Life",
                        "7.6 Art, Ritual, and Celebration",
                    ],
                ),
                (
                    "Chapter 8. Languages, Names, and Identity",
                    [
                        self._entity_section("8.1 Languages", "language"),
                        self._custom_section("8.2 Naming Conventions", self._render_naming_conventions),
                        "8.3 Titles and Honorifics",
                        "8.4 Regional Identities",
                        self._custom_section("8.5 Cultural Markers", self._render_timekeeping_names),
                        "8.6 Shared and Divided Identities",
                    ],
                ),
            ],
        )

    def _build_character_creation(self) -> List[str]:
        return self._build_part(
            "Part II. Character Creation",
            [
                (
                    "Chapter 9. Creating a Character",
                    [
                        "9.1 Character Creation Steps",
                        "9.2 Character Concept",
                        "9.3 Species",
                        "9.4 Culture or Origin",
                        "9.5 Class",
                        "9.6 Background",
                        "9.7 Equipment",
                        "9.8 Personal Details",
                        "9.9 Finalization",
                    ],
                ),
                (
                    "Chapter 10. Species",
                    [
                        self._custom_section("10.1 Species Overview", self._render_species_overview),
                        self._custom_section("10.2 Species Entries", self._render_species_entries),
                        self._custom_section("10.3 Species Traits", self._render_species_trait_reference),
                        "10.4 Variants or Lineages",
                        self._custom_section("10.5 Naming by Species", self._render_species_naming_by_species),
                        self._custom_section("10.6 Species Tables", self._render_species_tables),
                    ],
                ),
                (
                    "Chapter 11. Cultures and Origins",
                    [
                        "11.1 Homeland Options",
                        "11.2 Cultural Backgrounds",
                        "11.3 Regional Upbringings",
                        "11.4 Social Origins",
                        "11.5 Origin Traits or Features",
                        "11.6 Origin Tables",
                    ],
                ),
                (
                    "Chapter 12. Classes",
                    [
                        "12.1 Class Overview",
                        self._entity_section("12.2 Class Entries", "class"),
                        "12.3 Class Features",
                        "12.4 Advancement",
                        "12.5 Class Tables",
                        "12.6 Multiclassing or Equivalent Options",
                    ],
                ),
                (
                    "Chapter 13. Subclasses and Specializations",
                    [
                        "13.1 Specialization Overview",
                        self._entity_section("13.2 Subclass Entries", "subclass"),
                        "13.3 Orders, Schools, or Paths",
                        "13.4 Subclass Features",
                        "13.5 Advancement by Specialization",
                        "13.6 Specialization Tables",
                    ],
                ),
                (
                    "Chapter 14. Backgrounds",
                    [
                        "14.1 Background Overview",
                        self._entity_section("14.2 Background Entries", "background"),
                        "14.3 Skills and Proficiencies",
                        "14.4 Features or Benefits",
                        "14.5 Equipment and Starting Assets",
                        "14.6 Background Tables",
                    ],
                ),
                (
                    "Chapter 15. Faith, Allegiance, and Conviction",
                    [
                        "15.1 Faith Options",
                        "15.2 Personal Beliefs",
                        "15.3 Allegiances",
                        "15.4 Vows, Codes, or Oaths",
                        "15.5 Symbols and Practices",
                        "15.6 Alignment or Equivalent Frameworks",
                    ],
                ),
            ],
        )

    def _build_rules_and_character_options(self) -> List[str]:
        return self._build_part(
            "Part III. Rules and Character Options",
            [
                (
                    "Chapter 16. Core Rules",
                    [
                        "16.1 Ability Scores or Attributes",
                        "16.2 Core Resolution Rules",
                        "16.3 Checks, Saves, or Tests",
                        "16.4 Conditions and States",
                        "16.5 Rest, Recovery, and Healing",
                        "16.6 Advancement Rules",
                    ],
                ),
                (
                    "Chapter 17. Skills, Proficiencies, and Talents",
                    [
                        "17.1 Skills",
                        "17.2 Proficiencies",
                        "17.3 Tools and Training",
                        self._entity_section("17.4 Talents or Feats", "feat"),
                        "17.5 Special Aptitudes",
                        "17.6 Reference Tables",
                    ],
                ),
                (
                    "Chapter 18. Equipment",
                    [
                        "18.1 Currency and Wealth",
                        "18.2 Weapons",
                        "18.3 Armor",
                        self._entity_section("18.4 Adventuring Gear", "item"),
                        "18.5 Tools and Kits",
                        "18.6 Mounts, Travel Gear, and Services",
                    ],
                ),
                (
                    "Chapter 19. Magic",
                    [
                        "19.1 Magic Overview",
                        "19.2 Sources of Magic",
                        "19.3 Spellcasting Rules",
                        self._entity_section(
                            "19.4 Spell Lists",
                            "spell",
                            lambda spells: sorted(
                                spells,
                                key=lambda spell: (
                                    spell.get("level", 0),
                                    spell.get("name", ""),
                                ),
                            ),
                        ),
                        "19.5 Rituals",
                        "19.6 Magical Limitations and Exceptions",
                    ],
                ),
                (
                    "Chapter 20. Powers, Gifts, and Special Systems",
                    [
                        "20.1 Non-Spell Powers",
                        "20.2 Supernatural Gifts",
                        "20.3 Marks, Blessings, or Curses",
                        "20.4 Unique Setting Systems",
                        "20.5 Advancement within Special Systems",
                        "20.6 Reference Tables",
                    ],
                ),
                (
                    "Chapter 21. Combat",
                    [
                        "21.1 Combat Overview",
                        "21.2 Initiative and Turn Order",
                        "21.3 Actions and Movement",
                        "21.4 Attacks and Damage",
                        "21.5 Defense and Protection",
                        "21.6 Special Combat Rules",
                    ],
                ),
                (
                    "Chapter 22. Exploration",
                    [
                        "22.1 Travel",
                        "22.2 Movement Across Regions",
                        "22.3 Survival",
                        "22.4 Navigation",
                        "22.5 Hazards and Obstacles",
                        "22.6 Exploration Procedures",
                    ],
                ),
                (
                    "Chapter 23. Social Interaction",
                    [
                        "23.1 Social Encounters",
                        "23.2 Influence and Persuasion",
                        "23.3 Reputation",
                        "23.4 Status and Standing",
                        self._custom_section("23.5 Negotiation and Conflict", self._render_conflict_dynamics),
                        "23.6 Social Rules Reference",
                    ],
                ),
                (
                    "Chapter 24. Downtime and Progression",
                    [
                        "24.1 Downtime Overview",
                        "24.2 Crafting",
                        "24.3 Research",
                        "24.4 Training",
                        "24.5 Trade and Profession",
                        "24.6 Long-Term Progression Systems",
                    ],
                ),
            ],
        )

    def _build_world_reference(self) -> List[str]:
        return self._build_part(
            "Part IV. World Reference",
            [
                (
                    "Chapter 25. Religion and Divine Powers",
                    [
                        "25.1 Pantheons or Divine Structures",
                        "25.2 Deity Entries",
                        "25.3 Saints, Spirits, or Lesser Powers",
                        "25.4 Religious Orders",
                        "25.5 Holy Symbols and Domains",
                        self._custom_section("25.6 Religious Calendar", self._render_religious_calendar),
                    ],
                ),
                (
                    "Chapter 26. Creatures and Peoples of the World",
                    [
                        "26.1 Creature Categories",
                        "26.2 Non-Player Peoples",
                        self._entity_section(
                            "26.3 Beasts and Monsters",
                            "monster",
                            lambda monsters: sorted(
                                monsters,
                                key=lambda monster: (
                                    monster.get("cr", 0),
                                    monster.get("name", ""),
                                ),
                            ),
                        ),
                        "26.4 Supernatural Entities",
                        "26.5 Legendary Beings",
                        "26.6 Creature Reference Tables",
                    ],
                ),
                (
                    "Chapter 27. Relics, Artifacts, and Significant Objects",
                    [
                        "27.1 Relics",
                        "27.2 Artifacts",
                        "27.3 Historic Objects",
                        self._entity_section("27.4 Magical Objects", "magicitem"),
                        "27.5 Sacred and Forbidden Objects",
                        "27.6 Object Reference Tables",
                    ],
                ),
                (
                    "Chapter 28. Calendar, Time, and Seasons",
                    [
                        self._custom_section("28.1 Calendar Structure", self._render_calendar_structure),
                        self._custom_section("28.2 Months and Seasons", self._render_months_and_seasons),
                        self._custom_section("28.3 Festivals and Holy Days", self._render_festivals_and_holy_days),
                        "28.4 Celestial Cycles",
                        self._custom_section("28.5 Timekeeping", self._render_timekeeping_names),
                        "28.6 Seasonal Reference",
                    ],
                ),
                (
                    "Chapter 29. Names, Terms, and Glossary",
                    [
                        "29.1 Setting Terminology",
                        "29.2 Historical Terms",
                        "29.3 Religious Terms",
                        "29.4 Political Terms",
                        "29.5 Magical Terms",
                        "29.6 Glossary Index",
                    ],
                ),
                (
                    "Chapter 30. Maps and Reference Tables",
                    [
                        "30.1 World Maps",
                        "30.2 Regional Maps",
                        "30.3 Political Maps",
                        "30.4 Travel and Distance Tables",
                        "30.5 Symbol Keys",
                        "30.6 Reference Charts",
                    ],
                ),
            ],
        )

    def _build_appendices(self) -> List[str]:
        appendices = [
            {"title": "Appendix A. Character Sheet"},
            {"title": "Appendix B. Species Tables"},
            {"title": "Appendix C. Class Tables"},
            {"title": "Appendix D. Equipment Tables"},
            {"title": "Appendix E. Spell Lists"},
            {"title": "Appendix F. Conditions Reference", "entity_type": "disease"},
            {"title": "Appendix G. Timeline Summary", "render_func": self._render_timeline_summary},
            {"title": "Appendix H. Glossary Summary"},
            {"title": "Appendix I. Index"},
        ]

        lines = ["# Appendices", ""]

        for appendix in appendices:
            lines.extend(self._build_appendix(appendix))

        return lines

    def _build_part(
        self,
        title: str,
        chapters: List[tuple[str, List[str | SectionSpec]]],
    ) -> List[str]:
        lines = [f"# {title}", ""]

        for chapter_title, sections in chapters:
            lines.extend(self._build_chapter(chapter_title, sections))

        lines.extend(["---", ""])
        return lines

    def _build_chapter(
        self,
        title: str,
        sections: List[str | SectionSpec],
    ) -> List[str]:
        lines = [f"## {title}", ""]

        if not any(
            isinstance(section, dict) and (section.get("entity_type") or section.get("render_func"))
            for section in sections
        ):
            lines.extend([self.EMPTY_CHAPTER_NOTE, ""])

        for section in sections:
            if isinstance(section, str):
                lines.extend([f"### {section}", ""])
                continue

            section_title = section["title"]
            lines.extend([f"### {section_title}", ""])
            if section.get("render_func"):
                lines.extend(section["render_func"]())
            else:
                entity_type = section["entity_type"]
                filter_func = section.get("filter_func")
                lines.extend(self._render_entities(entity_type, filter_func))

        return lines

    def _build_appendix(self, appendix: SectionSpec) -> List[str]:
        title = appendix["title"]
        entity_type = appendix.get("entity_type")
        render_func = appendix.get("render_func")

        lines = [f"## {title}", ""]

        if render_func:
            lines.extend(render_func())
        elif entity_type:
            lines.extend(self._render_entities(entity_type, appendix.get("filter_func")))
        else:
            lines.extend([self.EMPTY_CHAPTER_NOTE, ""])

        return lines

    def _entity_section(
        self,
        title: str,
        entity_type: str,
        filter_func: Optional[EntityFilter] = None,
    ) -> SectionSpec:
        return {
            "title": title,
            "entity_type": entity_type,
            "filter_func": filter_func,
        }

    def _custom_section(
        self,
        title: str,
        render_func: Callable[[], List[str]],
    ) -> SectionSpec:
        return {
            "title": title,
            "render_func": render_func,
        }

    def _render_entities(
        self,
        entity_type: str,
        filter_func: Optional[EntityFilter] = None,
    ) -> List[str]:
        try:
            entities = self.book_api.load_entities(entity_type, source=self.source)
        except Exception as error:
            return [f"*No {entity_type} data is currently available for {self.source}: {error}.*", ""]

        if filter_func:
            entities = filter_func(entities)

        if not entities:
            return [f"*No {entity_type} entries are currently available for this source.*", ""]

        formatter = self.get_formatter(entity_type)
        lines: List[str] = []

        for entity in entities:
            try:
                lines.extend(formatter.format_entity(entity))
            except Exception as error:
                entity_name = entity.get("name", "unknown")
                lines.extend(
                    [f"*Skipped {entity_type} entry '{entity_name}' due to formatting error: {error}.*", ""]
                )

        return lines

    def _species_entities(self) -> List[Dict[str, Any]]:
        try:
            entities = self.book_api.load_entities("species", source=self.source)
        except Exception:
            return []
        return self._sort_species_for_handbook(entities)

    def _entity_unavailable_lines(self, entity_type: str) -> List[str]:
        return [f"*No {entity_type} data is currently available for {self.source}.*", ""]

    def _sort_species_for_handbook(
        self,
        species_list: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        def sort_key(species: Dict[str, Any]) -> tuple[Any, str]:
            handbook_order = species.get("handbookOrder", species.get("bookOrder"))
            if handbook_order is None:
                handbook_order = float("inf")
            return handbook_order, species.get("name", "")

        return sorted(species_list, key=sort_key)

    def _render_species_overview(self) -> List[str]:
        species = self._species_entities()
        if not species:
            return self._entity_unavailable_lines("species")

        names = [entry.get("name", "Unknown Species") for entry in species]
        lines = [
            (
                f"Orimond currently exposes {len(species)} player species in a handbook-first format. "
                "Each entry opens with world-facing identity and lore before presenting its mechanical traits."
            ),
            "",
            "**Species in This Chapter**",
            ", ".join(names),
            "",
            (
                "This chapter follows a PHB-like flow: title, identity line, untitled opening prose, "
                "setting subsections, then a consolidated traits block."
            ),
            "",
        ]
        return lines

    def _render_species_entries(self) -> List[str]:
        return self._render_entities("species", self._sort_species_for_handbook)

    def _render_species_trait_reference(self) -> List[str]:
        species = self._species_entities()
        if not species:
            return self._entity_unavailable_lines("species")

        lines: List[str] = []
        for entry in species:
            trait_names = [
                trait.get("name", "").strip()
                for trait in entry.get("entries", [])
                if isinstance(trait, dict) and trait.get("name")
            ]
            if not trait_names:
                continue
            lines.append(f"**{entry.get('name', 'Unknown Species')}**")
            lines.append(", ".join(trait_names))
            lines.append("")

        return lines or [self.EMPTY_CHAPTER_NOTE, ""]

    def _render_species_naming_by_species(self) -> List[str]:
        species = self._species_entities()
        if not species:
            return self._entity_unavailable_lines("species")

        lines: List[str] = []
        for entry in species:
            naming_entries = self._species_fluff_entries(entry, "Naming Conventions")
            if not naming_entries:
                continue
            lines.append(f"**{entry.get('name', 'Unknown Species')}**")
            lines.extend(naming_entries)
            lines.append("")

        return lines or [self.EMPTY_CHAPTER_NOTE, ""]

    def _render_species_tables(self) -> List[str]:
        species = self._species_entities()
        if not species:
            return self._entity_unavailable_lines("species")

        lines: List[str] = []
        for entry in species:
            lines.append(
                f"**{entry.get('name', 'Unknown Species')}** | "
                f"Ability: {self._species_ability_summary(entry)} | "
                f"Size: {self._species_size_summary(entry)} | "
                f"Speed: {self._species_speed_summary(entry)}"
            )
        lines.append("")
        return lines

    def _species_fluff_entries(
        self,
        species: Dict[str, Any],
        section_name: str,
    ) -> List[str]:
        for section in species.get("fluff", {}).get("entries", []):
            if not isinstance(section, dict):
                continue
            if section.get("name") == section_name:
                return [
                    str(entry)
                    for entry in section.get("entries", [])
                    if isinstance(entry, str) and entry.strip()
                ]
        return []

    def _species_ability_summary(self, species: Dict[str, Any]) -> str:
        ability_names = {
            "str": "STR",
            "dex": "DEX",
            "con": "CON",
            "int": "INT",
            "wis": "WIS",
            "cha": "CHA",
        }
        parts: List[str] = []
        for ability_set in species.get("ability", []):
            if not isinstance(ability_set, dict):
                continue
            for ability, value in ability_set.items():
                ability_name = ability_names.get(ability, ability.upper())
                parts.append(f"{ability_name} +{value}")
        return ", ".join(parts) if parts else "Variable"

    def _species_size_summary(self, species: Dict[str, Any]) -> str:
        size_map = {"T": "Tiny", "S": "Small", "M": "Medium", "L": "Large", "H": "Huge", "G": "Gargantuan"}
        sizes = species.get("size", [])
        if isinstance(sizes, list):
            labels = [size_map.get(size, str(size)) for size in sizes]
            return "/".join(labels) if labels else "Unknown"
        return str(sizes) if sizes else "Unknown"

    def _species_speed_summary(self, species: Dict[str, Any]) -> str:
        speed = species.get("Walk Speed")
        if speed is None or speed == "":
            return "Unknown"
        if isinstance(speed, (int, float)):
            return f"{int(speed)} ft."
        return str(speed)

    def _get_cosmology_sections(self) -> List[Tuple[str, List[str]]]:
        if self._cosmology_sections_cache is not None:
            return self._cosmology_sections_cache
        from Book.core.readers.google_docs import read_doc_sections
        try:
            service = self.book_api.gdocs.service
            self._cosmology_sections_cache = read_doc_sections(service, _COSMOLOGY_DOC_ID)
        except Exception as error:
            print(f"  Warning: Could not load cosmology doc: {error}")
            self._cosmology_sections_cache = []
        return self._cosmology_sections_cache

    def _cosmology_chapter_sections(self) -> List[str | SectionSpec]:
        sections = self._get_cosmology_sections()
        if not sections:
            return [
                "3.1 Structure of Reality",
                "3.2 Realms and Planes",
                "3.3 Divine Order",
                "3.4 Souls, Death, and Afterlife",
                "3.5 Metaphysical Forces",
                "3.6 Cosmological Phenomena",
            ]
        return [
            self._custom_section(f"3.{idx} {title}", self._make_cosmology_renderer(lines))
            for idx, (title, lines) in enumerate(sections, 1)
        ]

    def _make_cosmology_renderer(self, lines: List[str]) -> Callable[[], List[str]]:
        def render() -> List[str]:
            return list(lines) + [""]
        return render

    def _timeline_catalog(self) -> dict[str, Any] | None:
        if self.source != "fantasy":
            return None
        if self._timeline_catalog_cache is not None:
            return self._timeline_catalog_cache
        if self._timeline_catalog_error is not None:
            return None

        try:
            self._timeline_catalog_cache = load_timeline_catalog()
        except Exception as error:
            self._timeline_catalog_error = str(error)
            return None

        return self._timeline_catalog_cache

    def _timeline_unavailable_lines(self) -> List[str]:
        if self._timeline_catalog_error:
            return [f"*Timeline source unavailable: {self._timeline_catalog_error}.*", ""]
        return [self.EMPTY_CHAPTER_NOTE, ""]

    def _render_major_eras(self) -> List[str]:
        catalog = self._timeline_catalog()
        if not catalog:
            return self._timeline_unavailable_lines()

        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        periods = catalog.get("era_periods", [])
        if periods:
            lines: List[str] = []
            for period in periods:
                lines.append(f"**{period.get('era', 'Unspecified Era')}**")
                lines.append(
                    f"{period.get('start_year', 'Unknown')}-{period.get('end_year', 'Unknown')}: "
                    f"{period.get('label', '')}"
                )
                lines.append("")
            return lines

        for event in catalog.get("era_events", []):
            grouped[event.get("era") or "Unspecified Era"].append(event)

        lines: List[str] = []
        for era_name, events in grouped.items():
            years = [event["year"] for event in events if event.get("year") is not None]
            lines.append(f"**{era_name}**")
            if years:
                lines.append(f"Years covered: {min(years)}-{max(years)}.")
            lines.append(f"Recorded events: {len(events)}.")
            lines.append("")
        return lines or self._timeline_unavailable_lines()

    def _render_defining_events(self) -> List[str]:
        catalog = self._timeline_catalog()
        if not catalog:
            return self._timeline_unavailable_lines()

        conflicts = catalog.get("conflicts", [])
        if not conflicts:
            events = catalog.get("era_events", [])
            if not events:
                return ["*No timeline conflicts or era events were found in the timeline source.*", ""]
            spotlight = events[:18]
        else:
            spotlight = conflicts[:18]

        lines = []
        for event in spotlight[:18]:
            year = event.get("year")
            prefix = f"{year}: " if year is not None else ""
            line = f"- {prefix}{event.get('event', '')}"
            consequence = event.get("strategic_consequence")
            if consequence:
                line += f" Consequence: {consequence}"
            lines.append(line)
        lines.append("")
        return lines

    def _render_historical_timeline(self) -> List[str]:
        catalog = self._timeline_catalog()
        if not catalog:
            return self._timeline_unavailable_lines()

        events = catalog.get("conflicts") or catalog.get("era_events", [])
        if not events:
            return ["*No historical timeline events were found in the timeline source.*", ""]

        lines = []
        for event in events:
            year = event.get("year")
            era = event.get("era")
            label = f"{year}" if year is not None else "Unknown year"
            if era:
                label += f" ({era})"
            line = f"- {label}: {event.get('event', '')}"
            consequence = event.get("strategic_consequence")
            if consequence:
                line += f" Strategic consequence: {consequence}"
            lines.append(line)
        lines.append("")
        return lines

    def _render_power_relations(self) -> List[str]:
        catalog = self._timeline_catalog()
        if not catalog:
            return self._timeline_unavailable_lines()

        conflicts = catalog.get("conflicts", [])
        if not conflicts:
            return ["*No conflict records were found in the timeline source.*", ""]

        lines = []
        for conflict in conflicts[:12]:
            year = conflict.get("year")
            event = conflict.get("event") or ""
            consequence = conflict.get("strategic_consequence") or ""
            prefix = f"{year}: " if year is not None else ""
            lines.append(f"- {prefix}{event}")
            if consequence:
                lines.append(f"Strategic consequence: {consequence}")
        lines.append("")
        return lines

    def _render_naming_conventions(self) -> List[str]:
        catalog = self._timeline_catalog()
        if not catalog:
            return self._timeline_unavailable_lines()

        lines = []
        template = catalog.get("naming_template")
        if template:
            lines.extend([f"Template: `{template}`", ""])

        for group in catalog.get("naming_groups", []):
            values = ", ".join(group.get("values", []))
            lines.append(f"**{group.get('label', 'Group')}**")
            if values:
                lines.append(values)
            lines.append("")

        return lines or self._timeline_unavailable_lines()

    def _render_timekeeping_names(self) -> List[str]:
        catalog = self._timeline_catalog()
        if not catalog:
            return self._timeline_unavailable_lines()

        lines = []
        weekdays = catalog.get("weekdays", [])
        if weekdays:
            lines.append(f"Weekdays: {', '.join(weekdays)}")
            lines.append("")

        hours_group = next(
            (group for group in catalog.get("naming_groups", []) if "hour" in group.get("label", "").lower()),
            None,
        )
        if hours_group:
            lines.append("**Named Hours**")
            lines.append(", ".join(hours_group.get("values", [])))
            lines.append("")

        return lines or self._timeline_unavailable_lines()

    def _render_religious_calendar(self) -> List[str]:
        catalog = self._timeline_catalog()
        if not catalog:
            return self._timeline_unavailable_lines()

        months = catalog.get("calendar_months", [])
        if not months:
            return ["*No calendar month records were found in the timeline source.*", ""]

        lines = []
        for month in months:
            month_name = month.get("month_name") or "Unknown month"
            deity_name = month.get("deity_name")
            domain = month.get("domain")
            if deity_name:
                lines.append(f"**{month_name}**")
                details = [f"Deity: {deity_name}"]
                if domain:
                    details.append(f"Domain: {domain}")
                chore = month.get("chore_name")
                if chore:
                    details.append(f"Observance: {chore}")
                lines.append(". ".join(details) + ".")
                lines.append("")
        return lines or self._timeline_unavailable_lines()

    def _render_conflict_dynamics(self) -> List[str]:
        catalog = self._timeline_catalog()
        if not catalog:
            return self._timeline_unavailable_lines()

        conflicts = catalog.get("conflicts", [])
        if not conflicts:
            return ["*No dedicated conflict log was found in the timeline source.*", ""]

        lines = []
        for conflict in conflicts[:10]:
            year = conflict.get("year")
            event = conflict.get("event") or ""
            consequence = conflict.get("strategic_consequence") or ""
            label = f"{year}" if year is not None else "Unknown year"
            lines.append(f"**{label}**")
            lines.append(event)
            if consequence:
                lines.append(f"Strategic consequence: {consequence}")
            lines.append("")
        return lines

    def _render_calendar_structure(self) -> List[str]:
        catalog = self._timeline_catalog()
        if not catalog:
            return self._timeline_unavailable_lines()

        months = catalog.get("calendar_months", [])
        weekdays = catalog.get("weekdays", [])
        lines = []
        if months:
            lines.append(f"The calendar currently defines {len(months)} named months.")
        if weekdays:
            lines.append(f"Weekday cycle: {', '.join(weekdays)}.")
        lines.append("")
        return lines if len(lines) > 1 else self._timeline_unavailable_lines()

    def _render_months_and_seasons(self) -> List[str]:
        catalog = self._timeline_catalog()
        if not catalog:
            return self._timeline_unavailable_lines()

        months = catalog.get("calendar_months", [])
        if not months:
            return ["*No month records were found in the timeline source.*", ""]

        lines = []
        for month in months:
            month_name = month.get("month_name") or "Unknown month"
            month_order = month.get("month_order") or ""
            description = month.get("description") or ""
            lines.append(f"**{month_order} {month_name}**".strip())
            if description:
                lines.append(str(description))
            chore_name = month.get("chore_name")
            chore_description = month.get("chore_description")
            if chore_name:
                chore_line = f"Seasonal labor: {chore_name}"
                if chore_description:
                    chore_line += f" - {chore_description}"
                lines.append(chore_line)
            lines.append("")
        return lines

    def _render_festivals_and_holy_days(self) -> List[str]:
        catalog = self._timeline_catalog()
        if not catalog:
            return self._timeline_unavailable_lines()

        holidays = catalog.get("holidays", [])
        if not holidays:
            return ["*No holiday records were found in the timeline source.*", ""]

        lines = []
        for holiday in holidays:
            when = []
            if holiday.get("month_name"):
                when.append(str(holiday["month_name"]))
            if holiday.get("day") is not None:
                when.append(f"day {holiday['day']}")
            if holiday.get("weekday"):
                when.append(str(holiday["weekday"]))
            prefix = ", ".join(when)
            line = holiday.get("name", "Unnamed holiday")
            if prefix:
                line += f" ({prefix})"
            if holiday.get("notes"):
                line += f": {holiday['notes']}"
            lines.append(f"- {line}")
        lines.append("")
        return lines

    def _render_timeline_summary(self) -> List[str]:
        catalog = self._timeline_catalog()
        if not catalog:
            return self._timeline_unavailable_lines()

        months = catalog.get("calendar_months", [])
        holidays = catalog.get("holidays", [])
        events = catalog.get("era_events", [])
        conflicts = catalog.get("conflicts", [])

        lines = [
            f"Calendar months: {len(months)}",
            f"Holidays and festivals: {len(holidays)}",
            f"Recorded era events: {len(events)}",
            f"Recorded conflicts: {len(conflicts)}",
            "",
        ]
        lines.extend(self._render_major_eras())
        return lines
