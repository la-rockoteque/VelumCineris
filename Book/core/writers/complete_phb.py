"""
Complete Player's Handbook writer with species, classes (with nested subclasses), and more.
"""

from typing import List, Tuple, Optional, Callable
from Book.core.markdown import normalize_markdown, page_break
from Book.core.writers.base import BaseWriter


class CompletePHBWriter(BaseWriter):
    """Writer for complete Player's Handbook with species, classes, and subclasses."""

    def get_book_title(self) -> str:
        """Get the title of the book."""
        if self.source == "fantasy":
            return "Orimond Complete Player's Handbook"
        else:
            return "Vestigium Complete Player's Handbook"

    def get_sections(self) -> List[Tuple[str, str, Optional[Callable]]]:
        """
        Get sections for complete Player's Handbook.

        Returns:
            List of (section_name, entity_type, filter_func) tuples
        """
        if self.source == "fantasy":
            return self._get_fantasy_sections()
        else:
            return self._get_modern_sections()

    def _get_fantasy_sections(self) -> List[Tuple[str, str, Optional[Callable]]]:
        """Get sections for fantasy setting."""
        return [
            ("Species", "species", None),
            (
                "Spells",
                "spell",
                lambda s: sorted(s, key=lambda x: (x.get("level", 0), x.get("name", ""))),
            ),
            ("Languages", "language", None),
        ]

    def _get_modern_sections(self) -> List[Tuple[str, str, Optional[Callable]]]:
        """Get sections for modern setting."""
        return [
            ("Species", "species", None),
            # Classes will be handled specially with subclasses
            ("Backgrounds", "background", None),
            ("Feats", "feat", None),
            (
                "Spells",
                "spell",
                lambda s: sorted(s, key=lambda x: (x.get("level", 0), x.get("name", ""))),
            ),
            ("Items", "item", None),
            ("Languages", "language", None),
        ]

    def build_markdown(self) -> str:
        parts = [self.write_cover_page(), self.write_table_of_contents()]

        sections = self.get_sections()
        for chapter_number, (section_name, entity_type, filter_func) in enumerate(
            sections,
            start=1,
        ):
            print(f"Processing section: {section_name}...")

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
                continue

        if self.source == "modern":
            print("Processing section: Classes (with subclasses)...")
            parts.append(self.write_classes_with_subclasses(chapter_number=len(sections) + 1))

        return normalize_markdown("\n".join(parts))

    def build_document_lines(self) -> List[str]:
        return self.build_markdown().splitlines()

    def write_classes_with_subclasses(self, *, chapter_number: int | None = None) -> str:
        """
        Write classes section with subclasses nested under each class.

        Returns:
            Canonical markdown string
        """
        lines = []
        if chapter_number is not None:
            lines.extend(self.write_section_cover_page("Classes", chapter_number).splitlines())

        lines.append("# Classes")
        lines.append("")

        # Load classes and subclasses
        try:
            classes = self.book_api.load_entities("class", source=self.source)
            all_subclasses = self.book_api.load_entities("subclass", source=self.source)
        except Exception as e:
            print(f"  Error loading classes/subclasses: {e}")
            return "\n".join(lines)

        # Get renderers
        try:
            class_renderer = self.get_entity_renderer("class")
            subclass_renderer = self.get_entity_renderer("subclass")
        except Exception as e:
            print(f"  Error getting renderers: {e}")
            return "\n".join(lines)

        # Process each class
        success_count = 0
        error_count = 0

        for idx, cls in enumerate(classes):
            try:
                class_name = cls.get("name", "Unknown Class")

                lines.extend(class_renderer.render_markdown(cls).splitlines())

                # Find subclasses for this class
                class_subclasses = [
                    sc for sc in all_subclasses
                    if sc.get("className") == class_name
                ]

                if class_subclasses:
                    lines.append("")
                    lines.append(f"## {class_name} Subclasses")
                    lines.append("")

                    # Format each subclass
                    for subclass in class_subclasses:
                        try:
                            lines.extend(subclass_renderer.render_markdown(subclass).splitlines())
                        except Exception as e:
                            print(f"  Warning: Error formatting subclass {subclass.get('name', 'unknown')}: {e}")

                success_count += 1

                # Progress indicator
                if (idx + 1) % 5 == 0:
                    print(f"  Formatted {idx + 1}/{len(classes)} classes...")

            except Exception as e:
                error_count += 1
                print(f"  Warning: Error formatting class {cls.get('name', 'unknown')}: {e}")
                continue

        # Add page break after section
        lines.append("")
        lines.append(page_break())
        lines.append("")

        print(f"  Added {success_count} classes with subclasses ({error_count} errors)")

        return normalize_markdown("\n".join(lines))
