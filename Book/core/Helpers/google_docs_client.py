"""
Google Docs API client with PHB-specific formatting capabilities.
"""

from typing import List, Dict, Any, Optional
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Book.core.Helpers.styles import (
    FONT_NAME,
    BODY_FONT_SIZE,
    HEADING_1_SIZE,
    HEADING_2_SIZE,
    HEADING_3_SIZE,
    HEADING_4_SIZE,
    HEADING_COLOR,
    BLACK_COLOR,
    COLUMN_GAP,
    MARGIN_TOP,
    MARGIN_BOTTOM,
    MARGIN_LEFT,
    MARGIN_RIGHT,
    HEADING_1,
    HEADING_2,
    HEADING_3,
    HEADING_4,
    NORMAL_TEXT,
)


class GoogleDocsClient:
    """Wrapper around Google Docs API with PHB-specific formatting."""

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
        """Apply two-column PHB-style layout to the document."""
        # Note: Column widths cannot be set explicitly via API
        # Instead, we just enable two columns with separator
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
            },
            {
                "updateSectionStyle": {
                    "range": {"startIndex": 1, "endIndex": self.get_end_index()},
                    "sectionStyle": {
                        "columnSeparatorStyle": "BETWEEN_EACH_COLUMN",
                        "contentDirection": "LEFT_TO_RIGHT",
                        # Note: columnProperties cannot be set - API limitation
                        # Google Docs will automatically size columns equally
                    },
                    "fields": "columnSeparatorStyle,contentDirection",
                }
            },
        ]

        self.batch_update(requests)

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
