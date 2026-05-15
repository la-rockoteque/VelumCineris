"""
Google Docs API client with PHB-specific formatting capabilities.
"""

import time
from typing import List, Dict, Any, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Book.core.Helpers.styles import (
    ACCENT_COLOR,
    BLACK_COLOR,
    BODY_FONT,
    BODY_FONT_SIZE,
    BODY_INDENT_FIRST_LINE,
    BODY_LINE_SPACING,
    BODY_SPACE_BELOW,
    COLUMN_GAP,
    FONT_NAME,
    HEADING_1_COLOR,
    HEADING_1_FONT,
    HEADING_1_SIZE,
    HEADING_1_SPACE_ABOVE,
    HEADING_1_SPACE_BELOW,
    HEADING_2_COLOR,
    HEADING_2_FONT,
    HEADING_2_SIZE,
    HEADING_2_SPACE_ABOVE,
    HEADING_2_SPACE_BELOW,
    HEADING_3_COLOR,
    HEADING_3_FONT,
    HEADING_3_SIZE,
    HEADING_3_SPACE_ABOVE,
    HEADING_3_SPACE_BELOW,
    HEADING_4_COLOR,
    HEADING_4_FONT,
    HEADING_4_SIZE,
    HEADING_4_SPACE_ABOVE,
    HEADING_4_SPACE_BELOW,
    HEADING_1,
    HEADING_2,
    HEADING_3,
    HEADING_4,
    HEADING_COLOR,
    MARGIN_BOTTOM,
    MARGIN_LEFT,
    MARGIN_RIGHT,
    MARGIN_TOP,
    NORMAL_TEXT,
    RULE_FONT_SIZE,
    RULE_SPACE_ABOVE,
    RULE_SPACE_BELOW,
    COVER_TAGLINE_FONT_SIZE,
    COVER_TAGLINE_COLOR,
    COVER_TITLE_FONT_SIZE,
    COVER_TITLE_COLOR,
    COVER_SUBTITLE_FONT_SIZE,
    COVER_SUBTITLE_COLOR,
    TITLE,
    SUBTITLE,
)


class GoogleDocsClient:
    """Wrapper around Google Docs API with PHB-specific formatting."""

    DEFAULT_BATCH_CHUNK_SIZE = 500
    DEFAULT_BATCH_PAUSE_SECONDS = 1.1
    TWO_COLUMN_STYLE: Dict[str, Any] = {
        "columnProperties": [
            {
                "paddingEnd": {
                    "magnitude": COLUMN_GAP / 2,
                    "unit": "PT",
                }
            },
            {
                "paddingEnd": {
                    "magnitude": 0,
                    "unit": "PT",
                }
            },
        ],
        "columnSeparatorStyle": "NONE",
    }
    ONE_COLUMN_STYLE: Dict[str, Any] = {
        "columnProperties": [
            {
                "paddingEnd": {
                    "magnitude": 0,
                    "unit": "PT",
                }
            }
        ],
        "columnSeparatorStyle": "NONE",
    }

    def __init__(self, doc_id: str, credentials_path: str = "FiveETools/key.json"):
        """
        Initialize Google Docs client.

        Args:
            doc_id: Google Docs document ID
            credentials_path: Path to service account credentials JSON
        """
        self.doc_id = doc_id
        self.credentials_path = credentials_path

        # Set up credentials and service
        scopes = ["https://www.googleapis.com/auth/documents"]
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path, scopes=scopes
        )
        self.service = build("docs", "v1", credentials=credentials)

    def get_document(self) -> Dict[str, Any]:
        """Retrieve the current document."""
        try:
            return self.service.documents().get(documentId=self.doc_id).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise

    def clear_document(self) -> None:
        """Clear all content from the document."""
        doc = self.get_document()
        content = doc.get("body").get("content")

        if len(content) <= 1:
            # Document is already empty
            return

        # Get the full range of content (skip first element which is section break)
        start_index = content[0].get("endIndex", 1)
        end_index = content[-1].get("endIndex", 1) - 1

        if start_index >= end_index:
            return

        requests = [
            {
                "deleteContentRange": {
                    "range": {"startIndex": start_index, "endIndex": end_index}
                }
            }
        ]

        self.batch_update(requests)

    def batch_update(self, requests: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute a batch of update requests.

        Args:
            requests: List of Google Docs API requests

        Returns:
            API response
        """
        if not requests:
            return {}

        try:
            result = (
                self.service.documents()
                .batchUpdate(documentId=self.doc_id, body={"requests": requests})
                .execute()
            )
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            raise

    def batch_update_with_retry(
        self,
        requests: List[Dict[str, Any]],
        *,
        max_retries: int = 6,
        initial_backoff_seconds: float = 5.0,
    ) -> Dict[str, Any]:
        """Execute a batch update and back off on quota throttling."""
        attempt = 0
        backoff_seconds = initial_backoff_seconds

        while True:
            try:
                return self.batch_update(requests)
            except HttpError as error:
                status_code = getattr(getattr(error, "resp", None), "status", None)
                if status_code != 429 or attempt >= max_retries:
                    raise

                wait_seconds = self._retry_after_seconds(error, fallback=backoff_seconds)
                print(
                    f"Quota throttled by Google Docs API; retrying in {wait_seconds:.1f}s "
                    f"(attempt {attempt + 1}/{max_retries})..."
                )
                time.sleep(wait_seconds)
                attempt += 1
                backoff_seconds = min(backoff_seconds * 2, 60.0)

    def batch_update_in_chunks(
        self,
        requests: List[Dict[str, Any]],
        *,
        chunk_size: int = DEFAULT_BATCH_CHUNK_SIZE,
        pause_seconds: float = DEFAULT_BATCH_PAUSE_SECONDS,
    ) -> None:
        """Execute requests in bounded chunks to avoid oversized write bursts."""
        if not requests:
            return

        for start in range(0, len(requests), chunk_size):
            chunk = requests[start : start + chunk_size]
            self.batch_update_with_retry(chunk)

            if start + chunk_size < len(requests):
                time.sleep(pause_seconds)

    def _retry_after_seconds(
        self,
        error: HttpError,
        *,
        fallback: float,
    ) -> float:
        headers = getattr(getattr(error, "resp", None), "headers", None)
        if headers is None:
            return fallback

        retry_after = headers.get("retry-after")
        if retry_after is None:
            return fallback

        try:
            return max(float(retry_after), fallback)
        except (TypeError, ValueError):
            return fallback

    def get_end_index(self) -> int:
        """Get the current end index of the document."""
        doc = self.get_document()
        content = doc.get("body").get("content")
        return content[-1].get("endIndex", 1) - 1

    def insert_text(self, text: str, index: Optional[int] = None) -> int:
        """
        Insert text at the specified index or at the end.

        Args:
            text: Text to insert
            index: Index to insert at (None for end of document)

        Returns:
            Index after insertion
        """
        if index is None:
            index = self.get_end_index()

        requests = [{"insertText": {"location": {"index": index}, "text": text}}]

        self.batch_update(requests)
        return index + len(text)

    def add_heading(
        self, text: str, level: int = 1, index: Optional[int] = None
    ) -> int:
        """
        Add a heading.

        Args:
            text: Heading text
            level: Heading level (1-4)
            index: Index to insert at (None for end)

        Returns:
            Index after insertion
        """
        if index is None:
            index = self.get_end_index()

        # Map level to named style
        style_map = {
            1: HEADING_1,
            2: HEADING_2,
            3: HEADING_3,
            4: HEADING_4,
        }
        named_style = style_map.get(level, HEADING_2)

        requests = [
            {"insertText": {"location": {"index": index}, "text": text + "\n"}},
            {
                "updateParagraphStyle": {
                    "range": {"startIndex": index, "endIndex": index + len(text) + 1},
                    "paragraphStyle": {"namedStyleType": named_style},
                    "fields": "namedStyleType",
                }
            },
        ]

        self.batch_update(requests)
        return index + len(text) + 1

    def add_paragraph(
        self,
        text: str,
        bold: bool = False,
        italic: bool = False,
        index: Optional[int] = None,
    ) -> int:
        """
        Add a paragraph with optional styling.

        Args:
            text: Paragraph text
            bold: Apply bold styling
            italic: Apply italic styling
            index: Index to insert at (None for end)

        Returns:
            Index after insertion
        """
        if index is None:
            index = self.get_end_index()

        requests = [
            {"insertText": {"location": {"index": index}, "text": text + "\n"}}
        ]

        # Apply text styling if needed
        if bold or italic:
            text_style = {}
            if bold:
                text_style["bold"] = True
            if italic:
                text_style["italic"] = True

            requests.append(
                {
                    "updateTextStyle": {
                        "range": {
                            "startIndex": index,
                            "endIndex": index + len(text),
                        },
                        "textStyle": text_style,
                        "fields": ",".join(text_style.keys()),
                    }
                }
            )

        self.batch_update(requests)
        return index + len(text) + 1

    def add_table(
        self, headers: List[str], rows: List[List[str]], index: Optional[int] = None
    ) -> int:
        """
        Add a table.

        Args:
            headers: Column headers
            rows: Table rows
            index: Index to insert at (None for end)

        Returns:
            Index after insertion
        """
        if index is None:
            index = self.get_end_index()

        num_rows = len(rows) + 1  # +1 for header
        num_cols = len(headers)

        requests = [
            {
                "insertTable": {
                    "rows": num_rows,
                    "columns": num_cols,
                    "location": {"index": index},
                }
            }
        ]

        self.batch_update(requests)

        # Note: Populating table cells requires additional API calls
        # This is a simplified implementation
        # Full implementation would require getting table structure and updating cells

        return index + 1

    def add_page_break(self, index: Optional[int] = None) -> int:
        """
        Add a page break.

        Args:
            index: Index to insert at (None for end)

        Returns:
            Index after insertion
        """
        if index is None:
            index = self.get_end_index()

        requests = [
            {
                "insertPageBreak": {
                    "location": {"index": index},
                }
            }
        ]

        self.batch_update(requests)
        return index + 1

    def add_horizontal_rule(self, index: Optional[int] = None) -> int:
        """
        Add a horizontal rule.

        Args:
            index: Index to insert at (None for end)

        Returns:
            Index after insertion
        """
        if index is None:
            index = self.get_end_index()

        # Google Docs doesn't have native horizontal rule
        # Use a line of dashes instead
        return self.add_paragraph("─" * 50, index=index)

    def apply_two_column_layout(self) -> None:
        """Apply document-wide margins without overriding section-level column rules."""
        requests = [
            {
                "updateDocumentStyle": {
                    "documentStyle": {
                        "marginTop": {"magnitude": MARGIN_TOP, "unit": "PT"},
                        "marginBottom": {"magnitude": MARGIN_BOTTOM, "unit": "PT"},
                        "marginLeft": {"magnitude": MARGIN_LEFT, "unit": "PT"},
                        "marginRight": {"magnitude": MARGIN_RIGHT, "unit": "PT"},
                    },
                    "fields": "marginTop,marginBottom,marginLeft,marginRight",
                }
            }
        ]

        self.batch_update(requests)

    def create_section_style_request(
        self,
        *,
        start_index: int,
        end_index: int,
        columns: int,
    ) -> Dict[str, Any]:
        """Create a request that styles the overlapping section as one or two columns."""
        if columns == 1:
            section_style = self.ONE_COLUMN_STYLE
        elif columns == 2:
            section_style = self.TWO_COLUMN_STYLE
        else:
            raise ValueError(f"Unsupported column count: {columns}")

        return {
            "updateSectionStyle": {
                "range": {"startIndex": start_index, "endIndex": end_index},
                "sectionStyle": section_style,
                "fields": "columnProperties,columnSeparatorStyle",
            }
        }

    def create_heading_style_requests(
        self,
        *,
        start_index: int,
        end_index: int,
        level: int,
    ) -> List[Dict[str, Any]]:
        """Create paragraph and text styles for PHB-lite headings."""
        style_map = {
            1: {
                "named_style": HEADING_1,
                "alignment": "CENTER",
                "font": HEADING_1_FONT,
                "color": HEADING_1_COLOR,
                "font_size": HEADING_1_SIZE,
                "space_above": HEADING_1_SPACE_ABOVE,
                "space_below": HEADING_1_SPACE_BELOW,
            },
            2: {
                "named_style": HEADING_2,
                "alignment": "START",
                "font": HEADING_2_FONT,
                "color": HEADING_2_COLOR,
                "font_size": HEADING_2_SIZE,
                "space_above": HEADING_2_SPACE_ABOVE,
                "space_below": HEADING_2_SPACE_BELOW,
            },
            3: {
                "named_style": HEADING_3,
                "alignment": "START",
                "font": HEADING_3_FONT,
                "color": HEADING_3_COLOR,
                "font_size": HEADING_3_SIZE,
                "space_above": HEADING_3_SPACE_ABOVE,
                "space_below": HEADING_3_SPACE_BELOW,
            },
            4: {
                "named_style": HEADING_4,
                "alignment": "START",
                "font": HEADING_4_FONT,
                "color": HEADING_4_COLOR,
                "font_size": HEADING_4_SIZE,
                "space_above": HEADING_4_SPACE_ABOVE,
                "space_below": HEADING_4_SPACE_BELOW,
            },
        }
        heading_style = style_map.get(level, style_map[2])

        return [
            self.create_paragraph_style_request(
                start_index=start_index,
                end_index=end_index,
                paragraph_style={
                    "namedStyleType": heading_style["named_style"],
                    "alignment": heading_style["alignment"],
                    "keepWithNext": True,
                    "lineSpacing": 100,
                    "spaceAbove": self._pt(heading_style["space_above"]),
                    "spaceBelow": self._pt(heading_style["space_below"]),
                },
                fields=[
                    "namedStyleType",
                    "alignment",
                    "keepWithNext",
                    "lineSpacing",
                    "spaceAbove",
                    "spaceBelow",
                ],
            ),
            self.create_text_style_request(
                start_index=start_index,
                end_index=end_index - 1,
                text_style={
                    "weightedFontFamily": {"fontFamily": heading_style["font"]},
                    "fontSize": self._pt(heading_style["font_size"]),
                    "foregroundColor": {"color": {"rgbColor": heading_style["color"]}},
                    "bold": True,
                },
                fields=[
                    "weightedFontFamily",
                    "fontSize",
                    "foregroundColor",
                    "bold",
                ],
            ),
        ]

    def create_body_style_requests(
        self,
        *,
        start_index: int,
        end_index: int,
    ) -> List[Dict[str, Any]]:
        """Create paragraph and text styles for body copy."""
        return [
            self.create_paragraph_style_request(
                start_index=start_index,
                end_index=end_index,
                paragraph_style={
                    "namedStyleType": NORMAL_TEXT,
                    "alignment": "JUSTIFIED",
                    "lineSpacing": BODY_LINE_SPACING,
                    "spaceBelow": self._pt(BODY_SPACE_BELOW),
                    "indentFirstLine": self._pt(BODY_INDENT_FIRST_LINE),
                },
                fields=[
                    "namedStyleType",
                    "alignment",
                    "lineSpacing",
                    "spaceBelow",
                    "indentFirstLine",
                ],
            ),
            self.create_text_style_request(
                start_index=start_index,
                end_index=end_index - 1,
                text_style={
                    "weightedFontFamily": {"fontFamily": BODY_FONT},
                    "fontSize": self._pt(BODY_FONT_SIZE),
                    "foregroundColor": {"color": {"rgbColor": BLACK_COLOR}},
                },
                fields=[
                    "weightedFontFamily",
                    "fontSize",
                    "foregroundColor",
                ],
            ),
        ]

    def create_rule_style_requests(
        self,
        *,
        start_index: int,
        end_index: int,
    ) -> List[Dict[str, Any]]:
        """Create ornamental rule styles using text glyphs."""
        return [
            self.create_paragraph_style_request(
                start_index=start_index,
                end_index=end_index,
                paragraph_style={
                    "namedStyleType": NORMAL_TEXT,
                    "alignment": "CENTER",
                    "lineSpacing": 100,
                    "spaceAbove": self._pt(RULE_SPACE_ABOVE),
                    "spaceBelow": self._pt(RULE_SPACE_BELOW),
                },
                fields=[
                    "namedStyleType",
                    "alignment",
                    "lineSpacing",
                    "spaceAbove",
                    "spaceBelow",
                ],
            ),
            self.create_text_style_request(
                start_index=start_index,
                end_index=end_index - 1,
                text_style={
                    "weightedFontFamily": {"fontFamily": FONT_NAME},
                    "fontSize": self._pt(RULE_FONT_SIZE),
                    "foregroundColor": {"color": {"rgbColor": ACCENT_COLOR}},
                    "bold": True,
                },
                fields=[
                    "weightedFontFamily",
                    "fontSize",
                    "foregroundColor",
                    "bold",
                ],
            ),
        ]

    def create_inline_text_style_request(
        self,
        *,
        start_index: int,
        end_index: int,
        bold: bool = False,
        italic: bool = False,
    ) -> Dict[str, Any]:
        """Create a text style request for whole-line emphasis."""
        text_style: Dict[str, Any] = {}
        fields: List[str] = []

        if bold:
            text_style["bold"] = True
            fields.append("bold")
        if italic:
            text_style["italic"] = True
            fields.append("italic")

        return self.create_text_style_request(
            start_index=start_index,
            end_index=end_index,
            text_style=text_style,
            fields=fields,
        )

    def create_paragraph_style_request(
        self,
        *,
        start_index: int,
        end_index: int,
        paragraph_style: Dict[str, Any],
        fields: List[str],
    ) -> Dict[str, Any]:
        return {
            "updateParagraphStyle": {
                "range": {"startIndex": start_index, "endIndex": end_index},
                "paragraphStyle": paragraph_style,
                "fields": ",".join(fields),
            }
        }

    def create_text_style_request(
        self,
        *,
        start_index: int,
        end_index: int,
        text_style: Dict[str, Any],
        fields: List[str],
    ) -> Dict[str, Any]:
        return {
            "updateTextStyle": {
                "range": {"startIndex": start_index, "endIndex": end_index},
                "textStyle": text_style,
                "fields": ",".join(fields),
            }
        }

    def create_cover_tagline_style_requests(
        self, *, start_index: int, end_index: int
    ) -> List[Dict[str, Any]]:
        """Small red centred tagline for the cover page."""
        return [
            self.create_paragraph_style_request(
                start_index=start_index,
                end_index=end_index,
                paragraph_style={
                    "namedStyleType": NORMAL_TEXT,
                    "alignment": "CENTER",
                    "lineSpacing": 100,
                    "spaceAbove": self._pt(8),
                    "spaceBelow": self._pt(4),
                },
                fields=["namedStyleType", "alignment", "lineSpacing", "spaceAbove", "spaceBelow"],
            ),
            self.create_text_style_request(
                start_index=start_index,
                end_index=end_index - 1,
                text_style={
                    "weightedFontFamily": {"fontFamily": FONT_NAME},
                    "fontSize": self._pt(COVER_TAGLINE_FONT_SIZE),
                    "foregroundColor": {"color": {"rgbColor": COVER_TAGLINE_COLOR}},
                    "bold": False,
                    "italic": True,
                },
                fields=["weightedFontFamily", "fontSize", "foregroundColor", "bold", "italic"],
            ),
        ]

    def create_cover_title_style_requests(
        self, *, start_index: int, end_index: int
    ) -> List[Dict[str, Any]]:
        """Very large centred title (setting name) for the cover page."""
        return [
            self.create_paragraph_style_request(
                start_index=start_index,
                end_index=end_index,
                paragraph_style={
                    "namedStyleType": TITLE,
                    "alignment": "CENTER",
                    "lineSpacing": 100,
                    "spaceAbove": self._pt(16),
                    "spaceBelow": self._pt(12),
                },
                fields=["namedStyleType", "alignment", "lineSpacing", "spaceAbove", "spaceBelow"],
            ),
            self.create_text_style_request(
                start_index=start_index,
                end_index=end_index - 1,
                text_style={
                    "weightedFontFamily": {"fontFamily": FONT_NAME},
                    "fontSize": self._pt(COVER_TITLE_FONT_SIZE),
                    "foregroundColor": {"color": {"rgbColor": COVER_TITLE_COLOR}},
                    "bold": True,
                },
                fields=["weightedFontFamily", "fontSize", "foregroundColor", "bold"],
            ),
        ]

    def create_cover_subtitle_style_requests(
        self, *, start_index: int, end_index: int
    ) -> List[Dict[str, Any]]:
        """Large centred subtitle (book type) at the bottom of the cover."""
        return [
            self.create_paragraph_style_request(
                start_index=start_index,
                end_index=end_index,
                paragraph_style={
                    "namedStyleType": SUBTITLE,
                    "alignment": "CENTER",
                    "lineSpacing": 100,
                    "spaceAbove": self._pt(12),
                    "spaceBelow": self._pt(8),
                },
                fields=["namedStyleType", "alignment", "lineSpacing", "spaceAbove", "spaceBelow"],
            ),
            self.create_text_style_request(
                start_index=start_index,
                end_index=end_index - 1,
                text_style={
                    "weightedFontFamily": {"fontFamily": FONT_NAME},
                    "fontSize": self._pt(COVER_SUBTITLE_FONT_SIZE),
                    "foregroundColor": {"color": {"rgbColor": COVER_SUBTITLE_COLOR}},
                    "bold": True,
                },
                fields=["weightedFontFamily", "fontSize", "foregroundColor", "bold"],
            ),
        ]

    def _pt(self, magnitude: float) -> Dict[str, Any]:
        return {"magnitude": magnitude, "unit": "PT"}

    def create_requests_for_text(
        self,
        text: str,
        index: int,
        bold: bool = False,
        italic: bool = False,
        heading_level: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Create API requests for inserting styled text (without executing them).

        Args:
            text: Text to insert
            index: Index to insert at
            bold: Apply bold styling
            italic: Apply italic styling
            heading_level: If set, format as heading (1-4)

        Returns:
            List of API requests
        """
        requests = [
            {"insertText": {"location": {"index": index}, "text": text + "\n"}}
        ]

        if heading_level:
            style_map = {1: HEADING_1, 2: HEADING_2, 3: HEADING_3, 4: HEADING_4}
            named_style = style_map.get(heading_level, HEADING_2)

            requests.append(
                {
                    "updateParagraphStyle": {
                        "range": {
                            "startIndex": index,
                            "endIndex": index + len(text) + 1,
                        },
                        "paragraphStyle": {"namedStyleType": named_style},
                        "fields": "namedStyleType",
                    }
                }
            )
        elif bold or italic:
            text_style = {}
            if bold:
                text_style["bold"] = True
            if italic:
                text_style["italic"] = True

            requests.append(
                {
                    "updateTextStyle": {
                        "range": {"startIndex": index, "endIndex": index + len(text)},
                        "textStyle": text_style,
                        "fields": ",".join(text_style.keys()),
                    }
                }
            )

        return requests
