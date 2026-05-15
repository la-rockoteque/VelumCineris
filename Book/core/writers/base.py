"""
Base writer class for all book writers.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple, Optional, Callable, Dict, Any
from Book.core.formatters.base import BaseFormatter


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

        # Initialize formatters cache
        self._formatters = {}

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

    def build_document_lines(self) -> List[str]:
        """
        Build the complete document body for this writer.

        Writers with more complex structure can override this instead of relying on
        the default flat section loop.
        """
        lines: List[str] = []

        lines.extend(self.write_cover_page())
        lines.extend(self.write_table_of_contents())

        for section_name, entity_type, filter_func in self.get_sections():
            try:
                entities = self.book_api.load_entities(entity_type, source=self.source)

                if filter_func:
                    entities = filter_func(entities)

                formatter = self.get_formatter(entity_type)
                section_lines = self.write_section_with_error_handling(
                    section_name, entities, formatter
                )
                lines.extend(section_lines)
            except Exception as e:
                print(f"  Error processing {section_name}: {e}")
                import traceback

                traceback.print_exc()
                continue

        return lines

    def get_formatter(self, entity_type: str) -> BaseFormatter:
        """
        Get the appropriate formatter for an entity type.

        Args:
            entity_type: Type of entity

        Returns:
            Formatter instance
        """
        # Cache formatters to avoid recreating them
        if entity_type in self._formatters:
            return self._formatters[entity_type]

        # Import formatters
        from Book.core.formatters import (
            SpellFormatter,
            SpeciesFormatter,
            MonsterFormatter,
            BackgroundFormatter,
            FeatFormatter,
            ClassFormatter,
            SubclassFormatter,
            ItemFormatter,
            MagicItemFormatter,
            LanguageFormatter,
            DiseaseFormatter,
        )

        # Map entity types to formatters
        formatter_map = {
            "spell": SpellFormatter(),
            "species": SpeciesFormatter(),
            "race": SpeciesFormatter(),
            "monster": MonsterFormatter(),
            "background": BackgroundFormatter(),
            "feat": FeatFormatter(),
            "class": ClassFormatter(),
            "subclass": SubclassFormatter(),
            "item": ItemFormatter(),
            "magicitem": MagicItemFormatter(),
            "language": LanguageFormatter(),
            "disease": DiseaseFormatter(),
        }

        formatter = formatter_map.get(entity_type.lower())
        if not formatter:
            raise ValueError(f"No formatter available for entity type: {entity_type}")

        self._formatters[entity_type] = formatter
        return formatter

    def write_cover_page(self) -> List[str]:
        """Write PHB-style cover: tagline → title → art → subtitle → page break."""
        lines: List[str] = []

        setting = "Orimond" if self.source == "fantasy" else "Vestigium"
        lines.append("COVER_TAGLINE: A Homebrew Compendium · D&D 5th Edition")
        lines.append("")
        lines.append(f"COVER_TITLE: {setting}")
        lines.append("")
        if self.cover_image_url:
            lines.append(f"COVER_IMAGE: {self.cover_image_url}")
            lines.append("")
        lines.append(f"COVER_SUBTITLE: {self.get_book_title()}")
        lines.append("")
        lines.append("---")
        lines.append("")

        return lines

    def write_table_of_contents(self) -> List[str]:
        """
        Write the table of contents.

        Returns:
            List of formatted text lines
        """
        lines = []

        lines.append("## Table of Contents")
        lines.append("")

        # List all sections
        sections = self.get_sections()
        for idx, (section_name, entity_type, _) in enumerate(sections, 1):
            lines.append(f"{idx}. {section_name}")

        lines.append("")
        lines.append("---")  # Page break
        lines.append("")

        return lines

    def write_section(
        self,
        section_name: str,
        entities: List[Dict[str, Any]],
        formatter: BaseFormatter,
    ) -> List[str]:
        """
        Format and write a complete section.

        Args:
            section_name: Name of the section
            entities: List of entity dictionaries
            formatter: Formatter to use

        Returns:
            List of formatted text lines
        """
        lines = []

        # Section header
        lines.append(f"# {section_name}")
        lines.append("")

        # Format each entity
        for entity in entities:
            try:
                entity_lines = formatter.format_entity(entity)
                lines.extend(entity_lines)
            except Exception as e:
                # Log error but continue
                print(f"  Error formatting entity {entity.get('name', 'unknown')}: {e}")
                continue

        # Add page break after section
        lines.append("")
        lines.append("---")
        lines.append("")

        return lines

    def write_section_with_error_handling(
        self,
        section_name: str,
        entities: List[Dict[str, Any]],
        formatter: BaseFormatter,
    ) -> List[str]:
        """
        Format and write a complete section with detailed error handling and progress.

        Args:
            section_name: Name of the section
            entities: List of entity dictionaries
            formatter: Formatter to use

        Returns:
            List of formatted text lines
        """
        lines = []

        # Section header
        lines.append(f"# {section_name}")
        lines.append("")

        success_count = 0
        error_count = 0

        # Format each entity with error handling
        for idx, entity in enumerate(entities):
            try:
                entity_lines = formatter.format_entity(entity)
                lines.extend(entity_lines)
                success_count += 1

                # Progress indicator for large sections
                if (idx + 1) % 50 == 0:
                    print(f"  Formatted {idx + 1}/{len(entities)} entities...")

            except Exception as e:
                error_count += 1
                entity_name = entity.get("name", "unknown")
                print(f"  Warning: Error formatting {entity_name}: {e}")
                # Continue with next entity

        # Add page break after section
        lines.append("")
        lines.append("---")
        lines.append("")

        print(f"  Added {success_count} entities ({error_count} errors)")

        return lines
