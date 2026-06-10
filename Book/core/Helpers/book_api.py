"""
Main BookAPI orchestrator that coordinates markdown renderers and writers.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional
import importlib

from Book.core.markdown import GoogleDocsMarkdownRenderer, normalize_markdown

if TYPE_CHECKING:
    from Book.core.Helpers.google_docs_client import GoogleDocsClient


BATCH_REQUEST_CHUNK_SIZE = 500
BATCH_REQUEST_PAUSE_SECONDS = 1.1


class BookAPI:
    """Main orchestrator for book generation."""

    def __init__(self, google_docs_client: "GoogleDocsClient", gsheets_client):
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
            "spell": {"fantasy": "FiveETools.core.fantasy.spells", "modern": "FiveETools.core.modern.spells"},
            "monster": {"fantasy": "FiveETools.core.fantasy.monster", "modern": "FiveETools.core.modern.monster"},
            "species": {"fantasy": "FiveETools.core.fantasy.species", "modern": "FiveETools.core.modern.species"},
            "race": {"fantasy": "FiveETools.core.fantasy.species", "modern": "FiveETools.core.modern.species"},
            "class": {"modern": "FiveETools.core.modern.classes"},
            "subclass": {"modern": "FiveETools.core.modern.subclasses"},
            "background": {"modern": "FiveETools.core.modern.backgrounds"},
            "feat": {"modern": "FiveETools.core.modern.feats"},
            "item": {"modern": "FiveETools.core.modern.items"},
            "magicitem": {"fantasy": "FiveETools.core.fantasy.magic_items", "modern": "FiveETools.core.modern.magic_items"},
            "language": {"fantasy": "FiveETools.core.fantasy.languages", "modern": "FiveETools.core.modern.languages"},
            "disease": {"fantasy": "FiveETools.core.fantasy.diseases", "modern": "FiveETools.core.modern.diseases"},
            "deity": {
                "fantasy": "FiveETools.core.fantasy.dieties",
                "modern": "FiveETools.core.modern.dieties",
            },
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
            "deity": "diety_list",
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

        self._validate_cover_image(writer)

        print("Building canonical markdown...")
        if hasattr(writer, "build_markdown"):
            markdown = writer.build_markdown()
        else:
            markdown = "\n\n".join(writer.build_document_lines()) + "\n"

        # Write all content to document
        print("Writing content to Google Docs...")
        self._write_markdown_to_doc(markdown)

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

        from Book.core.entities import get_entity_renderer

        renderer = get_entity_renderer(entity_type)

        # Format and display
        for entity in entities:
            print("\n" + "=" * 80)
            for line in renderer.render_markdown(entity).splitlines():
                print(line)

        print("\n" + "=" * 80)
        print(f"Preview complete ({len(entities)} entities)")

    def _validate_cover_image(self, writer) -> None:
        """Pre-flight check: clear cover_image_url if the URL is not publicly accessible."""
        url = getattr(writer, "cover_image_url", None)
        if not url:
            return
        if not self._is_image_url_accessible(url):
            print(
                f"  Warning: cover image URL not publicly accessible — skipping image.\n"
                f"  URL tried: {url}\n"
                f"  Make sure the Drive file is shared as 'Anyone with the link'."
            )
            writer.cover_image_url = None

    def _is_image_url_accessible(self, url: str) -> bool:
        """Return True if url resolves to an image without auth."""
        import urllib.request
        import urllib.error

        try:
            req = urllib.request.Request(
                url,
                headers={"Range": "bytes=0-255", "User-Agent": "Mozilla/5.0"},
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                return resp.status in (200, 206)
        except urllib.error.HTTPError as exc:
            return exc.code in (200, 206)
        except Exception:
            return False

    def _write_markdown_to_doc(self, markdown: str) -> None:
        """
        Write markdown to the document using chunked transactions.
        """
        requests, _ = self._build_requests_for_markdown(markdown, index=1)

        if not requests:
            return

        line_count = len(markdown.splitlines())
        estimated_batches = max(
            1,
            (len(requests) + BATCH_REQUEST_CHUNK_SIZE - 1) // BATCH_REQUEST_CHUNK_SIZE,
        )
        print(
            f"  Writing {line_count} markdown lines as {len(requests)} requests "
            f"across about {estimated_batches} Google Docs batches..."
        )
        self.gdocs.batch_update_in_chunks(
            requests,
            chunk_size=BATCH_REQUEST_CHUNK_SIZE,
            pause_seconds=BATCH_REQUEST_PAUSE_SECONDS,
        )

    def _write_lines_to_doc(self, lines: List[str]) -> None:
        """
        Compatibility adapter for older tests/callers.

        Args:
            lines: List of text lines (with markdown-style formatting)
        """
        self._write_markdown_to_doc("\n\n".join(self._normalize_lines(lines)))

    def _normalize_lines(self, lines: List[str]) -> List[str]:
        """Collapse runs of consecutive empty lines to a single empty line."""
        result: List[str] = []
        prev_empty = False
        for line in lines:
            is_empty = line == ""
            if is_empty and prev_empty:
                continue
            result.append(line)
            prev_empty = is_empty
        return result

    def _build_requests_for_lines(
        self,
        lines: List[str],
        index: int,
    ) -> tuple[List[Dict[str, Any]], int]:
        """Compatibility adapter; canonical rendering takes markdown."""
        return self._build_requests_for_markdown("\n\n".join(lines), index=index)

    def _build_requests_for_markdown(
        self,
        markdown: str,
        index: int,
    ) -> tuple[List[Dict[str, Any]], int]:
        return GoogleDocsMarkdownRenderer(self.gdocs).build_requests(
            normalize_markdown(markdown),
            index=index,
        )

    def _build_requests_for_lines_legacy(
        self,
        lines: List[str],
        index: int,
    ) -> tuple[List[Dict[str, Any]], int]:
        requests: List[Dict[str, Any]] = []
        current_layout: str | None = None
        pending_layout: str | None = None

        for line in lines:
            if line == "":
                line_start = index
                requests.append({"insertText": {"location": {"index": index}, "text": "\n"}})
                index += 1
                if pending_layout is not None:
                    requests.append(
                        self.gdocs.create_section_style_request(
                            start_index=line_start,
                            end_index=index,
                            columns=1 if pending_layout == "one_column" else 2,
                        )
                    )
                    current_layout = pending_layout
                    pending_layout = None
                continue

            if not line:
                continue

            heading_level, heading_text = self._heading_for_line(line)

            if heading_level in {1, 2, 3}:
                if index > 1:
                    requests.append(
                        {
                            "insertSectionBreak": {
                                "sectionType": "CONTINUOUS",
                                "location": {"index": index},
                            }
                        }
                    )
                    index += 2

                line_start = index
                text = heading_text + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                index += len(text)
                requests.extend(
                    self.gdocs.create_heading_style_requests(
                        start_index=line_start,
                        end_index=index,
                        level=heading_level,
                    )
                )
                requests.append(
                    self.gdocs.create_section_style_request(
                        start_index=line_start,
                        end_index=index,
                        columns=1,
                    )
                )
                requests.append(
                    {
                        "insertSectionBreak": {
                            "sectionType": "CONTINUOUS",
                            "location": {"index": index},
                        }
                    }
                )
                index += 2
                current_layout = None
                pending_layout = "two_column"
                continue

            desired_layout = pending_layout or self._layout_for_line(line)
            layout_switched = desired_layout is not None and desired_layout != current_layout

            if layout_switched and current_layout is not None:
                requests.append(
                    {
                        "insertSectionBreak": {
                            "sectionType": "CONTINUOUS",
                            "location": {"index": index},
                        }
                    }
                )
                index += 2

            line_start = index
            if heading_level == 4:
                text = heading_text + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                index += len(text)
                requests.extend(
                    self.gdocs.create_heading_style_requests(
                        start_index=line_start,
                        end_index=index,
                        level=heading_level,
                    )
                )
            elif line.startswith("---"):
                requests.append({"insertPageBreak": {"location": {"index": index}}})
                index += 1
                continue
            elif line.startswith("COVER_TAGLINE: "):
                text = line[15:] + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                index += len(text)
                requests.extend(
                    self.gdocs.create_cover_tagline_style_requests(
                        start_index=line_start, end_index=index
                    )
                )
            elif line.startswith("COVER_TITLE: "):
                text = line[13:] + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                index += len(text)
                requests.extend(
                    self.gdocs.create_cover_title_style_requests(
                        start_index=line_start, end_index=index
                    )
                )
            elif line.startswith("COVER_SUBTITLE: "):
                text = line[16:] + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                index += len(text)
                requests.extend(
                    self.gdocs.create_cover_subtitle_style_requests(
                        start_index=line_start, end_index=index
                    )
                )
            elif line.startswith("COVER_IMAGE: "):
                uri = line[13:].strip()
                from Book.core.Helpers.styles import COVER_IMAGE_HEIGHT_PT, COVER_IMAGE_WIDTH_PT
                requests.append({
                    "insertInlineImage": {
                        "uri": uri,
                        "location": {"index": index},
                        "objectSize": {
                            "height": {"magnitude": COVER_IMAGE_HEIGHT_PT, "unit": "PT"},
                            "width": {"magnitude": COVER_IMAGE_WIDTH_PT, "unit": "PT"},
                        },
                    }
                })
                index += 1
                requests.append({"insertText": {"location": {"index": index}, "text": "\n"}})
                index += 1
                requests.append(
                    self.gdocs.create_paragraph_style_request(
                        start_index=line_start,
                        end_index=index,
                        paragraph_style={
                            "alignment": "CENTER",
                            "spaceAbove": {"magnitude": 8, "unit": "PT"},
                            "spaceBelow": {"magnitude": 8, "unit": "PT"},
                        },
                        fields=["alignment", "spaceAbove", "spaceBelow"],
                    )
                )
            elif self._is_horizontal_rule(line):
                text = line + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": text}})
                index += len(text)
                requests.extend(
                    self.gdocs.create_rule_style_requests(
                        start_index=line_start,
                        end_index=index,
                    )
                )
            else:
                clean_text = line.replace("***", "").replace("**", "").replace("*", "") + "\n"
                requests.append({"insertText": {"location": {"index": index}, "text": clean_text}})
                index += len(clean_text)
                requests.extend(
                    self.gdocs.create_body_style_requests(
                        start_index=line_start,
                        end_index=index,
                    )
                )

                bold = "**" in line
                italic = "*" in line and not bold

                if bold or italic:
                    requests.append(
                        self.gdocs.create_inline_text_style_request(
                            start_index=line_start,
                            end_index=index - 1,
                            bold=bold,
                            italic=italic,
                        )
                    )

            if layout_switched:
                requests.append(
                    self.gdocs.create_section_style_request(
                        start_index=line_start,
                        end_index=index,
                        columns=1 if desired_layout == "one_column" else 2,
                    )
                )
            if desired_layout is not None:
                current_layout = desired_layout
                if pending_layout == desired_layout:
                    pending_layout = None

        return requests, index

    def _layout_for_line(self, line: str) -> str | None:
        if line.startswith(("# ", "## ", "### ", "COVER_")):
            return "one_column"
        if line.startswith("---"):
            return None
        return "two_column"

    def _heading_for_line(self, line: str) -> tuple[int | None, str]:
        if line.startswith("#### "):
            return 4, line[5:]
        if line.startswith("### "):
            return 3, line[4:]
        if line.startswith("## "):
            return 2, line[3:]
        if line.startswith("# "):
            return 1, line[2:]
        return None, line

    def _is_horizontal_rule(self, line: str) -> bool:
        stripped_line = line.strip()
        return bool(stripped_line) and set(stripped_line) == {"─"}
