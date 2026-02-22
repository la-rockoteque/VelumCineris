"""
Main BookAPI orchestrator that coordinates formatters and writers.
"""

from typing import List, Dict, Any, Optional
import importlib
from Book.google_docs_client import GoogleDocsClient


class BookAPI:
    """Main orchestrator for book generation."""

    def __init__(self, google_docs_client: GoogleDocsClient, gsheets_client):
        """
        Initialize BookAPI.

        Args:
            google_docs_client: Google Docs API client
            gsheets_client: Google Sheets client (fantasy_sheets or modern_sheets)
        """
        self.gdocs = google_docs_client
        self.gsheets = gsheets_client

        # Entity type to module mapping
        self.entity_modules = {
            "spell": {"fantasy": "FiveETools.fantasy.spells", "modern": "FiveETools.modern.spells"},
            "monster": {"fantasy": "FiveETools.fantasy.monster", "modern": "FiveETools.modern.monster"},
            "species": {"fantasy": "FiveETools.fantasy.species", "modern": "FiveETools.modern.species"},
            "race": {"fantasy": "FiveETools.fantasy.species", "modern": "FiveETools.modern.species"},
            "class": {"modern": "FiveETools.modern.classes"},
            "subclass": {"modern": "FiveETools.modern.subclasses"},
            "background": {"modern": "FiveETools.modern.backgrounds"},
            "feat": {"modern": "FiveETools.modern.feats"},
            "item": {"modern": "FiveETools.modern.items"},
            "magicitem": {"fantasy": "FiveETools.fantasy.magic_items", "modern": "FiveETools.modern.magic_items"},
            "language": {"fantasy": "FiveETools.fantasy.languages", "modern": "FiveETools.modern.languages"},
            "disease": {"fantasy": "FiveETools.fantasy.diseases", "modern": "FiveETools.modern.diseases"},
        }

        # Entity type to list variable name mapping
        self.entity_list_names = {
            "spell": "spells_list",
            "monster": "monster_list",
            "species": "species_list",
            "race": "species_list",
            "class": "classes_list",
            "subclass": "subclass_list",
            "background": "background_list",
            "feat": "feat_list",
            "item": "items_list",
            "magicitem": "magic_items_list",
            "language": "language_list",
            "disease": "disease_list",
        }

    def load_entities(
        self, entity_type: str, source: str = "fantasy"
    ) -> List[Dict[str, Any]]:
        """
        Load entities from appropriate converter module.

        Args:
            entity_type: Type of entity (spell, monster, species, etc.)
            source: Content source ("fantasy" or "modern")

        Returns:
            List of entity dictionaries in 5etools format
        """
        entity_type_lower = entity_type.lower()

        if entity_type_lower not in self.entity_modules:
            raise ValueError(f"Unknown entity type: {entity_type}")

        module_path = self.entity_modules[entity_type_lower].get(source)
        if not module_path:
            raise ValueError(
                f"Entity type '{entity_type}' not available for source '{source}'"
            )

        # Import the module
        try:
            module = importlib.import_module(module_path)
        except ImportError as e:
            raise ImportError(f"Failed to import module '{module_path}': {e}")

        # Get the list variable
        list_name = self.entity_list_names[entity_type_lower]
        if not hasattr(module, list_name):
            raise AttributeError(
                f"Module '{module_path}' does not have '{list_name}' attribute"
            )

        entities = getattr(module, list_name)

        return entities

    def generate_book(self, writer, doc_id: Optional[str] = None) -> None:
        """
        Generate a complete book using the specified writer.

        Args:
            writer: Writer instance (e.g., OmnibookWriter)
            doc_id: Optional document ID (uses client's doc_id if not provided)
        """
        if doc_id:
            self.gdocs.doc_id = doc_id

        print("Starting book generation...")

        # Clear existing content
        print("Clearing document...")
        self.gdocs.clear_document()

        # Generate content
        all_lines = []

        # Cover page
        print("Adding cover page...")
        all_lines.extend(writer.write_cover_page())

        # Table of contents placeholder
        print("Adding table of contents...")
        all_lines.extend(writer.write_table_of_contents())

        # Get sections from writer
        sections = writer.get_sections()

        # Process each section
        for section_name, entity_type, filter_func in sections:
            print(f"Processing section: {section_name}...")

            try:
                # Load entities
                entities = self.load_entities(
                    entity_type, source=writer.source
                )

                # Apply filter if provided
                if filter_func:
                    entities = filter_func(entities)

                # Get formatter for this entity type
                formatter = writer.get_formatter(entity_type)

                # Write section with error handling
                section_lines = writer.write_section_with_error_handling(
                    section_name, entities, formatter
                )
                all_lines.extend(section_lines)

            except Exception as e:
                print(f"  Error processing {section_name}: {e}")
                import traceback
                traceback.print_exc()
                continue

        # Write all content to document
        print("Writing content to Google Docs...")
        self._write_lines_to_doc(all_lines)

        # Apply two-column layout
        print("Applying PHB-style layout...")
        self.gdocs.apply_two_column_layout()

        print("Book generation complete!")

    def preview_section(
        self, entity_type: str, source: str = "fantasy", limit: int = 5
    ) -> None:
        """
        Preview formatting for a section without writing to document.

        Args:
            entity_type: Type of entity to preview
            source: Content source
            limit: Number of entities to preview
        """
        print(f"Previewing {entity_type} formatting (limit: {limit})...")

        # Load entities
        entities = self.load_entities(entity_type, source=source)[:limit]

        # Get appropriate formatter
        from Book.formatters import SpellFormatter, SpeciesFormatter, MonsterFormatter

        formatter_map = {
            "spell": SpellFormatter(),
            "species": SpeciesFormatter(),
            "race": SpeciesFormatter(),
            "monster": MonsterFormatter(),
        }

        formatter = formatter_map.get(entity_type.lower())
        if not formatter:
            print(f"No formatter available for {entity_type}")
            return

        # Format and display
        for entity in entities:
            lines = formatter.format_entity(entity)
            print("\n" + "=" * 80)
            for line in lines:
                print(line)

        print("\n" + "=" * 80)
        print(f"Preview complete ({len(entities)} entities)")

    def _write_lines_to_doc(self, lines: List[str]) -> None:
        """
        Write lines of text to the document using batched requests.

        Args:
            lines: List of text lines (with markdown-style formatting)
        """
        # Build all requests first, then batch them
        requests = []
        index = 1

        # Batch size to stay under rate limits
        BATCH_SIZE = 50

        for line_idx, line in enumerate(lines):
            if not line:
                # Skip empty lines
                continue

            # Parse markdown-style formatting
            if line.startswith("#### "):
                # Heading 4
                text = line[5:] + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": index, "endIndex": index + len(text)},
                        "paragraphStyle": {"namedStyleType": "HEADING_4"},
                        "fields": "namedStyleType",
                    }
                })
                index += len(text)

            elif line.startswith("### "):
                # Heading 3
                text = line[4:] + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": index, "endIndex": index + len(text)},
                        "paragraphStyle": {"namedStyleType": "HEADING_3"},
                        "fields": "namedStyleType",
                    }
                })
                index += len(text)

            elif line.startswith("## "):
                # Heading 2
                text = line[3:] + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": index, "endIndex": index + len(text)},
                        "paragraphStyle": {"namedStyleType": "HEADING_2"},
                        "fields": "namedStyleType",
                    }
                })
                index += len(text)

            elif line.startswith("# "):
                # Heading 1
                text = line[2:] + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                requests.append({
                    "updateParagraphStyle": {
                        "range": {"startIndex": index, "endIndex": index + len(text)},
                        "paragraphStyle": {"namedStyleType": "HEADING_1"},
                        "fields": "namedStyleType",
                    }
                })
                index += len(text)

            elif line.startswith("---"):
                # Page break
                requests.append({"insertPageBreak": {"location": {"index": index}}})
                index += 1

            else:
                # Regular paragraph
                text = line + "\n"

                # Check for markdown styling
                bold = "**" in line
                italic = "*" in line and not bold

                # Strip markdown for text
                clean_text = line.replace("***", "").replace("**", "").replace("*", "") + "\n"

                requests.append({"insertText": {"location": {"index": index}, "text": clean_text}})

                # Apply styling if needed
                if bold or italic:
                    text_style = {}
                    if bold:
                        text_style["bold"] = True
                    if italic:
                        text_style["italic"] = True

                    requests.append({
                        "updateTextStyle": {
                            "range": {
                                "startIndex": index,
                                "endIndex": index + len(clean_text) - 1,  # Exclude newline
                            },
                            "textStyle": text_style,
                            "fields": ",".join(text_style.keys()),
                        }
                    })

                index += len(clean_text)

            # Execute batch when we reach batch size
            if len(requests) >= BATCH_SIZE:
                print(f"  Writing batch ({len(requests)} requests)...")
                self.gdocs.batch_update(requests)
                requests = []

                # Add delay to avoid rate limiting
                import time
                time.sleep(1.2)  # 60 requests/min = 1 per second, add buffer

        # Execute remaining requests
        if requests:
            print(f"  Writing final batch ({len(requests)} requests)...")
            self.gdocs.batch_update(requests)
