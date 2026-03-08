"""
Complete Player's Handbook writer with species, classes (with nested subclasses), and more.
"""

from typing import List, Tuple, Optional, Callable
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

    def write_classes_with_subclasses(self) -> List[str]:
        """
        Write classes section with subclasses nested under each class.

        Returns:
            List of formatted text lines
        """
        lines = []

        # Section header
        lines.append("# Classes")
        lines.append("")

        # Load classes and subclasses
        try:
            classes = self.book_api.load_entities("class", source=self.source)
            all_subclasses = self.book_api.load_entities("subclass", source=self.source)
        except Exception as e:
            print(f"  Error loading classes/subclasses: {e}")
            return lines

        # Get formatters
        try:
            class_formatter = self.get_formatter("class")
            subclass_formatter = self.get_formatter("subclass")
        except Exception as e:
            print(f"  Error getting formatters: {e}")
            return lines

        # Process each class
        success_count = 0
        error_count = 0

        for idx, cls in enumerate(classes):
            try:
                class_name = cls.get("name", "Unknown Class")

                # Format the class
                class_lines = class_formatter.format_entity(cls)
                lines.extend(class_lines)

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
                            subclass_lines = subclass_formatter.format_entity(subclass)
                            lines.extend(subclass_lines)
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
        lines.append("---")
        lines.append("")

        print(f"  Added {success_count} classes with subclasses ({error_count} errors)")

        return lines
