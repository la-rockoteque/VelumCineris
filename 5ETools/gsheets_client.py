"""
Google Sheets Client for Content Data Access

This module provides a centralized client for accessing Google Sheets
data used in content files (spells, monsters, species, etc.).

Supports two spreadsheets:
- Non-fantasy (Vestigium Guide to Concord City)
- Fantasy (Orimond)
"""

import pandas as pd
from typing import Literal, Optional, Dict, List
import gspread
from google.oauth2.service_account import Credentials

ContentType = Literal["fantasy", "non-fantasy"]


class ContentSheetsClient:
    """
    Client for accessing content spreadsheets.

    Usage:
        # Get fantasy spreadsheet data
        client = ContentSheetsClient("fantasy")
        df = client.get_sheet("736393386")  # Monster sheet

        # Get non-fantasy spreadsheet data
        client = ContentSheetsClient("non-fantasy")
        df = client.get_sheet("625265890")  # Spells sheet
    """

    # Spreadsheet IDs
    SPREADSHEETS = {
        "fantasy": "1NBZGu29IfE1ZfAWO1Z6ShR5GMLMMbaSyS0m-46PSYm4",
        "non-fantasy": "1I4FHncl40_xx1Udc_Q2rWWWvpL6xaMlpJyY90WBftag",
    }

    # Known sheet GIDs for reference
    SHEET_GIDS = {
        "fantasy": {
            "monsters": "736393386",
            "species": "993815941",
            "languages": "163123529",
        },
        "non-fantasy": {
            "spells": "625265890",
            "monsters": "736393386",
            "species": "993815941",
            "languages": "163123529",
            "magic_items": "695912920",
            "classes": "1924660120",
            "class_tables": "193036738",
            "class_features": "545140625",
            "subclasses": "338247460",
            "feats": "1076107525",
            "backgrounds": "1186398440",
            "item_properties": "1064461316",
            "items": "876046336",
            "conditions": "1321788284",
            "diseases": "1196270347",
            "dieties": "1410134136",
        }
    }

    def __init__(self, content_type: ContentType = "non-fantasy", credentials_path: str = "key.json"):
        """
        Initialize the client for a specific spreadsheet.

        Args:
            content_type: Either "fantasy" or "non-fantasy"
            credentials_path: Path to Google service account credentials JSON
        """
        if content_type not in self.SPREADSHEETS:
            raise ValueError(f"Invalid content_type: {content_type}. Must be 'fantasy' or 'non-fantasy'")

        self.content_type = content_type
        self.spreadsheet_id = self.SPREADSHEETS[content_type]
        self.credentials_path = credentials_path
        self._cache = {}
        self._gspread_client = None
        self._worksheet_cache = {}

    def get_sheet(self, gid: str) -> pd.DataFrame:
        """
        Get a DataFrame from a specific sheet by GID.

        Args:
            gid: The sheet GID (from the URL gid parameter)

        Returns:
            DataFrame with the sheet data

        Example:
            df = client.get_sheet("625265890")
        """
        # Check cache first
        cache_key = f"{self.content_type}:{gid}"
        if cache_key in self._cache:
            return self._cache[cache_key].copy()

        # Build CSV export URL
        url = self._build_csv_url(gid)

        # Load data
        df = pd.read_csv(url)

        # Clean column names
        df.columns = [str(c).strip() for c in df.columns]

        # Cache it
        self._cache[cache_key] = df.copy()

        return df

    def get_sheet_by_name(self, name: str) -> pd.DataFrame:
        """
        Get a DataFrame by sheet name (convenience method).

        Args:
            name: Sheet name like "monsters", "spells", etc.

        Returns:
            DataFrame with the sheet data

        Example:
            df = client.get_sheet_by_name("monsters")
        """
        gids = self.SHEET_GIDS.get(self.content_type, {})
        gid = gids.get(name)

        if not gid:
            raise ValueError(
                f"Unknown sheet name '{name}' for {self.content_type}. "
                f"Known sheets: {list(gids.keys())}"
            )

        return self.get_sheet(gid)

    def invalidate_cache(self):
        """Clear the cache to force fresh data load."""
        self._cache.clear()

    def _build_csv_url(self, gid: str) -> str:
        """Build the CSV export URL for a sheet."""
        return (
            f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"
            f"/export?format=csv&gid={gid}"
        )

    def _get_gspread_client(self):
        """Get or create gspread client with service account credentials."""
        if self._gspread_client is None:
            scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            creds = Credentials.from_service_account_file(self.credentials_path, scopes=scopes)
            self._gspread_client = gspread.authorize(creds)
        return self._gspread_client

    def _get_worksheet_by_gid(self, gid: str):
        """Get gspread worksheet by GID."""
        cache_key = f"{self.content_type}:{gid}"
        if cache_key not in self._worksheet_cache:
            client = self._get_gspread_client()
            spreadsheet = client.open_by_key(self.spreadsheet_id)

            # Find worksheet by GID
            worksheet = None
            for ws in spreadsheet.worksheets():
                if str(ws.id) == str(gid):
                    worksheet = ws
                    break

            if worksheet is None:
                raise ValueError(f"Worksheet with GID {gid} not found")

            self._worksheet_cache[cache_key] = worksheet

        return self._worksheet_cache[cache_key]

    def ensure_column_exists(self, gid: str, column_name: str) -> int:
        """
        Ensure a column exists in the sheet, create it if it doesn't.

        Args:
            gid: The sheet GID
            column_name: Name of the column to ensure exists

        Returns:
            Column index (1-based)
        """
        worksheet = self._get_worksheet_by_gid(gid)

        # Get header row
        headers = worksheet.row_values(1)

        # Check if column exists
        if column_name in headers:
            return headers.index(column_name) + 1

        # Add column at the end
        col_index = len(headers) + 1
        worksheet.update_cell(1, col_index, column_name)

        # Clear cache since we modified the sheet
        cache_key = f"{self.content_type}:{gid}"
        if cache_key in self._cache:
            del self._cache[cache_key]

        return col_index

    def update_cell_by_row_match(self, gid: str, match_column: str, match_value: str,
                                   update_column: str, update_value: str) -> bool:
        """
        Update a cell in a specific column where another column matches a value.

        Args:
            gid: The sheet GID
            match_column: Column name to search in (e.g., "Spell Name")
            match_value: Value to match (e.g., "Fireball")
            update_column: Column name to update (e.g., "DDB")
            update_value: Value to write

        Returns:
            True if updated, False if match not found
        """
        worksheet = self._get_worksheet_by_gid(gid)

        # Get headers
        headers = worksheet.row_values(1)

        # Find column indices
        try:
            match_col_idx = headers.index(match_column) + 1
        except ValueError:
            raise ValueError(f"Column '{match_column}' not found in sheet")

        try:
            update_col_idx = headers.index(update_column) + 1
        except ValueError:
            # Column doesn't exist, create it
            update_col_idx = self.ensure_column_exists(gid, update_column)

        # Get all values in the match column
        match_col_values = worksheet.col_values(match_col_idx)

        # Find the row with matching value (skip header row)
        for row_idx, cell_value in enumerate(match_col_values[1:], start=2):
            if cell_value == match_value:
                # Update the cell
                worksheet.update_cell(row_idx, update_col_idx, update_value)

                # Clear cache since we modified the sheet
                cache_key = f"{self.content_type}:{gid}"
                if cache_key in self._cache:
                    del self._cache[cache_key]

                return True

        return False

    def batch_update_cells_by_row_match(self, gid: str, match_column: str,
                                         updates: List[Dict[str, str]]) -> Dict[str, bool]:
        """
        Update multiple cells by matching rows.

        Args:
            gid: The sheet GID
            match_column: Column name to search in (e.g., "Spell Name")
            updates: List of dicts with 'match_value', 'update_column', 'update_value'

        Returns:
            Dict mapping match_value to success status
        """
        worksheet = self._get_worksheet_by_gid(gid)
        headers = worksheet.row_values(1)

        # Get match column index
        try:
            match_col_idx = headers.index(match_column) + 1
        except ValueError:
            raise ValueError(f"Column '{match_column}' not found in sheet")

        # Get all match column values
        match_col_values = worksheet.col_values(match_col_idx)

        # Prepare batch updates
        batch_data = []
        results = {}

        for update in updates:
            match_value = update['match_value']
            update_column = update['update_column']
            update_value = update['update_value']

            # Ensure update column exists
            try:
                update_col_idx = headers.index(update_column) + 1
            except ValueError:
                update_col_idx = self.ensure_column_exists(gid, update_column)
                headers = worksheet.row_values(1)  # Refresh headers

            # Find matching row
            found = False
            for row_idx, cell_value in enumerate(match_col_values[1:], start=2):
                if cell_value == match_value:
                    batch_data.append({
                        'range': f'{gspread.utils.rowcol_to_a1(row_idx, update_col_idx)}',
                        'values': [[update_value]]
                    })
                    results[match_value] = True
                    found = True
                    break

            if not found:
                results[match_value] = False

        # Execute batch update
        if batch_data:
            worksheet.batch_update(batch_data)

            # Clear cache
            cache_key = f"{self.content_type}:{gid}"
            if cache_key in self._cache:
                del self._cache[cache_key]

        return results


# Global instances for convenience
fantasy_sheets = ContentSheetsClient("fantasy")
modern_sheets = ContentSheetsClient("non-fantasy")
