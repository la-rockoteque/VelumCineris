"""
Base writer class for all book writers.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Callable, Dict, Any

from Book.core.entities import get_entity_renderer
from Book.core.entities.base import EntityMarkdownRenderer
from Book.core.markdown import normalize_markdown, page_break


class BaseWriter(ABC):
    """Abstract base for all book writers."""

    DEFAULT_COVER_IMAGE_URL = (
        "https://drive.google.com/thumbnail?id=1mERyOdTerZrbBzfbQ9mq52a4cmVYwRbH&sz=w2000"
    )

    def __init__(
        self,
        book_api,
        source: str = "fantasy",
        cover_image_url: Optional[str] = DEFAULT_COVER_IMAGE_URL,
    ):
        """
        Initialize the writer.

        Args:
            book_api: BookAPI instance
            source: Content source ("fantasy" or "modern")
            cover_image_url: HTTPS URL for cover artwork; None to omit the image
        """
        self.book_api = book_api
        self.source = source
        self.cover_image_url = cover_image_url

        self._entity_renderers: dict[str, EntityMarkdownRenderer] = {}

    @abstractmethod
    def get_sections(self) -> List[Tuple[str, str, Optional[Callable]]]:
        """
        Get the sections for this book type.

        Returns:
            List of tuples: (section_name, entity_type, filter_func)
            Example: [("Races", "species", None), ("Spells", "spell", lambda s: s["level"] <= 5)]
        """
        pass

    @abstractmethod
    def get_book_title(self) -> str:
        """
        Get the title of the book.

        Returns:
            Book title
        """
        pass

    def build_markdown(self) -> str:
        """
        Build the complete canonical markdown document for this writer.

        Writers with more complex structure can override this instead of relying on
        the default flat section loop.
        """
        parts: list[str] = [
            self.write_cover_page(),
            self.write_table_of_contents(),
        ]

        for chapter_number, (section_name, entity_type, filter_func) in enumerate(
            self.get_sections(),
            start=1,
        ):
            try:
                entities = self.book_api.load_entities(entity_type, source=self.source)

                if filter_func:
                    entities = filter_func(entities)

                section_markdown = self.write_section_with_error_handling(
                    section_name,
                    entities,
                    entity_type,
                    chapter_number=chapter_number,
                )
                parts.append(section_markdown)
            except Exception as e:
                print(f"  Error processing {section_name}: {e}")
                import traceback

                traceback.print_exc()
                continue

        return normalize_markdown("\n".join(parts))

    def build_document_lines(self) -> List[str]:
        """Compatibility adapter for older callers; markdown is canonical."""
        return self.build_markdown().splitlines()

    def get_entity_renderer(self, entity_type: str) -> EntityMarkdownRenderer:
        """
        Get the appropriate markdown renderer for an entity type.

        Args:
            entity_type: Type of entity

        Returns:
            Entity markdown renderer instance
        """
        if entity_type not in self._entity_renderers:
            self._entity_renderers[entity_type] = get_entity_renderer(entity_type)
        return self._entity_renderers[entity_type]

    def get_formatter(self, entity_type: str):
        """Compatibility shim for old callers."""
        from Book.mappers.formatter_registry import get_formatter

        return get_formatter(entity_type)

    def write_cover_page(self) -> str:
        """Write Homebrewery-style front cover markdown."""
        setting = "Orimond" if self.source == "fantasy" else "Vestigium"
        subtitle = self._cover_subtitle(setting)
        lines: list[str] = [
            "{{frontCover}}",
            "",
            "{{logo ![](https://homebrewery.naturalcrit.com/assets/naturalCritLogoRed.svg)}}",
            "",
            f"# {setting}",
            f"## {subtitle}",
            "___",
            "",
            "{{banner HOMEBREW}}",
            "",
            "{{footnote",
            "  A Homebrew Compendium · D&D 5th Edition",
            "}}",
        ]
        if self.cover_image_url:
            lines.append("")
            lines.append(
                f"![Cover Image]({self.cover_image_url})"
                "{position:absolute,top:0,right:0px,height:100%}"
            )
        lines.append("")
        lines.append(page_break())
        lines.append("")

        return "\n".join(lines)

    def _cover_subtitle(self, setting: str) -> str:
        title = self.get_book_title()
        for prefix in (f"{setting} ", "Orimond ", "Vestigium "):
            if title.startswith(prefix):
                return title[len(prefix) :]
        return title

    def write_table_of_contents(self) -> str:
        """
        Write the table of contents.

        Returns:
            Canonical markdown string
        """
        lines = []

        lines.append("## Table of Contents")
        lines.append("")

        # List all sections
        sections = self.get_sections()
        for idx, (section_name, entity_type, _) in enumerate(sections, 1):
            lines.append(f"{idx}. {section_name}")

        lines.append("")
        lines.append(page_break())
        lines.append("")

        return "\n".join(lines)

    def write_section(
        self,
        section_name: str,
        entities: List[Dict[str, Any]],
        entity_type: str,
        *,
        chapter_number: int | None = None,
    ) -> str:
        """
        Format and write a complete section.

        Args:
            section_name: Name of the section
            entities: List of entity dictionaries
            entity_type: Entity type to render

        Returns:
            Canonical markdown string
        """
        return self.write_section_with_error_handling(
            section_name,
            entities,
            entity_type,
            chapter_number=chapter_number,
        )

    def write_section_with_error_handling(
        self,
        section_name: str,
        entities: List[Dict[str, Any]],
        entity_type: str,
        *,
        chapter_number: int | None = None,
    ) -> str:
        """
        Format and write a complete section with detailed error handling and progress.

        Args:
            section_name: Name of the section
            entities: List of entity dictionaries
            formatter: Formatter to use

        Returns:
            List of formatted text lines
        """
        renderer = self.get_entity_renderer(entity_type)
        parts: list[str] = []
        if chapter_number is not None:
            parts.append(self.write_section_cover_page(section_name, chapter_number))
        parts.extend([f"# {section_name}", ""])

        success_count = 0
        error_count = 0

        # Format each entity with error handling
        for idx, entity in enumerate(entities):
            try:
                parts.append(renderer.render_markdown(entity))
                success_count += 1

                # Progress indicator for large sections
                if (idx + 1) % 50 == 0:
                    print(f"  Formatted {idx + 1}/{len(entities)} entities...")

            except Exception as e:
                error_count += 1
                entity_name = entity.get("name", "unknown")
                print(f"  Warning: Error formatting {entity_name}: {e}")
                # Continue with next entity

        parts.append("")
        parts.append(page_break())
        parts.append("")

        print(f"  Added {success_count} entities ({error_count} errors)")

        return normalize_markdown("\n".join(parts))

    def write_section_cover_page(self, section_name: str, chapter_number: int) -> str:
        chapter_label = self._roman_numeral(chapter_number)
        return "\n".join(
            [
                f"# Chapter {chapter_label}",
                "",
                f"## {section_name}",
                "",
                "{{imageMaskEdge8,--offset:10cm,--rotation:180",
                (
                    f"  ![Chapter {chapter_label} Cover]"
                    "(https://homebrewery.naturalcrit.com/assets/frigate.webp)"
                    "{position:absolute,bottom:0,right:0,height:100%}"
                ),
                "}}",
                "",
                "{{pageNumber,auto}}",
                page_break(),
                "",
            ]
        )

    def _roman_numeral(self, value: int) -> str:
        numerals = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ]
        remaining = value
        result: list[str] = []
        for number, numeral in numerals:
            while remaining >= number:
                result.append(numeral)
                remaining -= number
        return "".join(result)
