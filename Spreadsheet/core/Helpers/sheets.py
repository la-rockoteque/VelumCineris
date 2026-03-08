from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

import pandas as pd


ContentType = Literal["fantasy", "modern"]
TabKey = Literal["dictionary", "grammar", "scripts", "languages", "phonetics"]


def _resolve_credentials_path(explicit_path: str | Path | None = None) -> str:
    if explicit_path is not None:
        return str(explicit_path)

    candidates = [
        Path("FiveETools/key.json"),
        Path("Spreadsheet/key.json"),
        Path("key.json"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    # Preserve old behavior in several modules: default to key.json and fail on auth if missing.
    return "key.json"


class SpreadsheetClient:
    """
    Generic Google spreadsheet client used across all projects in this repository.

    Supports:
    - CSV export reads (fast DataFrame loading by GID)
    - gspread worksheet access (reads/writes by GID/title)
    - optional named sheet registry (name -> GID)
    """

    def __init__(
        self,
        spreadsheet_id: str,
        *,
        credentials_path: str | Path | None = None,
        sheet_gids: dict[str, str] | None = None,
        cache_namespace: str | None = None,
        scopes: tuple[str, ...] | None = None,
    ) -> None:
        self.spreadsheet_id = spreadsheet_id
        self.credentials_path = _resolve_credentials_path(credentials_path)
        self.sheet_gids = sheet_gids or {}
        self.cache_namespace = cache_namespace or spreadsheet_id
        self.scopes = scopes or (
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        )

        self._df_cache: dict[str, pd.DataFrame] = {}
        self._worksheet_cache_by_gid: dict[str, Any] = {}
        self._worksheet_cache_by_title: dict[str, Any] = {}
        self._gspread_client: Any | None = None
        self._spreadsheet: Any | None = None

    def build_csv_url(self, gid: str) -> str:
        return (
            f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"
            f"/export?format=csv&gid={gid}"
        )

    # Backward-compatible alias used by existing files.
    def _build_csv_url(self, gid: str) -> str:
        return self.build_csv_url(gid)

    def invalidate_cache(self) -> None:
        self._df_cache.clear()

    def get_sheet(self, gid: str, *, header: int = 0) -> pd.DataFrame:
        cache_key = f"{self.cache_namespace}:{gid}:h{header}"
        if cache_key in self._df_cache:
            return self._df_cache[cache_key].copy()

        df = pd.read_csv(self.build_csv_url(gid), header=header)
        df.columns = [str(col).strip() for col in df.columns]
        self._df_cache[cache_key] = df.copy()
        return df

    def get_sheet_by_name(self, name: str, *, header: int = 0) -> pd.DataFrame:
        gid = self.sheet_gids.get(name)
        if not gid:
            raise ValueError(
                f"Unknown sheet name '{name}'. Known sheets: {sorted(self.sheet_gids.keys())}"
            )
        return self.get_sheet(gid, header=header)

    def _get_gspread_client(self) -> Any:
        if self._gspread_client is None:
            import gspread
            from google.oauth2.service_account import Credentials

            creds = Credentials.from_service_account_file(self.credentials_path, scopes=self.scopes)
            self._gspread_client = gspread.authorize(creds)
        return self._gspread_client

    def _get_spreadsheet(self) -> Any:
        if self._spreadsheet is None:
            self._spreadsheet = self._get_gspread_client().open_by_key(self.spreadsheet_id)
        return self._spreadsheet

    def worksheet_by_gid(self, gid: str) -> Any:
        if gid in self._worksheet_cache_by_gid:
            return self._worksheet_cache_by_gid[gid]

        spreadsheet = self._get_spreadsheet()
        for ws in spreadsheet.worksheets():
            if str(ws.id) == str(gid):
                self._worksheet_cache_by_gid[gid] = ws
                self._worksheet_cache_by_title[ws.title] = ws
                return ws
        raise ValueError(f"Worksheet with GID {gid} not found in spreadsheet {self.spreadsheet_id}")

    def worksheet_by_title(self, title: str) -> Any:
        if title in self._worksheet_cache_by_title:
            return self._worksheet_cache_by_title[title]

        ws = self._get_spreadsheet().worksheet(title)
        self._worksheet_cache_by_title[title] = ws
        self._worksheet_cache_by_gid[str(ws.id)] = ws
        return ws

    def list_sheet_names(self) -> list[str]:
        return [ws.title for ws in self._get_spreadsheet().worksheets()]

    def get_rows_by_gid(self, gid: str) -> list[list[Any]]:
        return self.worksheet_by_gid(gid).get_all_values()

    def get_rows_by_title(self, title: str) -> list[list[Any]]:
        return self.worksheet_by_title(title).get_all_values()

    def ensure_column_exists(self, gid: str, column_name: str) -> int:
        worksheet = self.worksheet_by_gid(gid)
        headers = worksheet.row_values(1)
        if column_name in headers:
            return headers.index(column_name) + 1

        col_index = len(headers) + 1
        worksheet.update_cell(1, col_index, column_name)
        self.invalidate_cache()
        return col_index

    def update_cell_by_row_match(
        self,
        gid: str,
        match_column: str,
        match_value: str,
        update_column: str,
        update_value: str,
    ) -> bool:
        worksheet = self.worksheet_by_gid(gid)
        headers = worksheet.row_values(1)

        try:
            match_col_idx = headers.index(match_column) + 1
        except ValueError as exc:
            raise ValueError(f"Column '{match_column}' not found in sheet") from exc

        try:
            update_col_idx = headers.index(update_column) + 1
        except ValueError:
            update_col_idx = self.ensure_column_exists(gid, update_column)

        match_col_values = worksheet.col_values(match_col_idx)
        for row_idx, cell_value in enumerate(match_col_values[1:], start=2):
            if cell_value == match_value:
                worksheet.update_cell(row_idx, update_col_idx, update_value)
                self.invalidate_cache()
                return True
        return False

    def batch_update_cells_by_row_match(
        self,
        gid: str,
        match_column: str,
        updates: list[dict[str, str]],
    ) -> dict[str, bool]:
        import gspread

        worksheet = self.worksheet_by_gid(gid)
        headers = worksheet.row_values(1)

        try:
            match_col_idx = headers.index(match_column) + 1
        except ValueError as exc:
            raise ValueError(f"Column '{match_column}' not found in sheet") from exc

        match_col_values = worksheet.col_values(match_col_idx)
        batch_data: list[dict[str, Any]] = []
        results: dict[str, bool] = {}

        for update in updates:
            match_value = update["match_value"]
            update_column = update["update_column"]
            update_value = update["update_value"]

            try:
                update_col_idx = headers.index(update_column) + 1
            except ValueError:
                update_col_idx = self.ensure_column_exists(gid, update_column)
                headers = worksheet.row_values(1)

            found = False
            for row_idx, cell_value in enumerate(match_col_values[1:], start=2):
                if cell_value == match_value:
                    batch_data.append(
                        {
                            "range": gspread.utils.rowcol_to_a1(row_idx, update_col_idx),
                            "values": [[update_value]],
                        }
                    )
                    results[match_value] = True
                    found = True
                    break
            if not found:
                results[match_value] = False

        if batch_data:
            worksheet.batch_update(batch_data)
            self.invalidate_cache()

        return results


class ContentSheetsClient(SpreadsheetClient):
    SPREADSHEETS: dict[ContentType, str] = {
        "fantasy": "1NBZGu29IfE1ZfAWO1Z6ShR5GMLMMbaSyS0m-46PSYm4",
        "modern": "1I4FHncl40_xx1Udc_Q2rWWWvpL6xaMlpJyY90WBftag",
    }

    SHEET_GIDS: dict[ContentType, dict[str, str]] = {
        "fantasy": {
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
            "deities": "1410134136",
            "sources": "340852453",
        },
        "modern": {
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
            "deities": "1410134136",
            "sources": "340852453",
        },
    }

    def __init__(self, content_type: ContentType = "modern", credentials_path: str | Path | None = None):
        if content_type not in self.SPREADSHEETS:
            raise ValueError("content_type must be 'fantasy' or 'modern'")

        self.content_type = content_type
        super().__init__(
            self.SPREADSHEETS[content_type],
            credentials_path=credentials_path,
            sheet_gids=self.SHEET_GIDS.get(content_type, {}),
            cache_namespace=content_type,
        )


class TranslatorSheetsClient:
    DEFAULT_SHEET_ID = "11tldmRm7Ggx2a0dDdQuPxmxkANDyWjdffRGgvhvJEl0"
    DEFAULT_SCOPES = ("https://www.googleapis.com/auth/spreadsheets",)
    DEFAULT_TABS: dict[TabKey, str] = {
        "dictionary": "Dictionary",
        "grammar": "Grammar",
        "scripts": "Scripts",
        "languages": "Language",
        "phonetics": "Phonetics",
    }

    def __init__(
        self,
        creds_path: str | Path = "key.json",
        scopes: tuple[str, ...] = DEFAULT_SCOPES,
        sheet_id: str = DEFAULT_SHEET_ID,
    ) -> None:
        self.tabs = dict(self.DEFAULT_TABS)
        self._client = SpreadsheetClient(
            sheet_id,
            credentials_path=creds_path,
            cache_namespace=f"translator:{sheet_id}",
            scopes=scopes,
        )
        self._df_cache: dict[str, pd.DataFrame] = {}

    @property
    def client(self) -> Any:
        return self._client._get_gspread_client()

    def ws(self, tab_key: TabKey) -> Any:
        tab_name = self.tabs.get(tab_key)
        if not tab_name:
            raise KeyError(f"Unknown sheet tab '{tab_key}'")
        return self._client.worksheet_by_title(tab_name)

    def get_records(self, tab_key: TabKey) -> list[dict[str, Any]]:
        return self.ws(tab_key).get_all_records()

    def get_df(self, tab_key: TabKey) -> pd.DataFrame:
        if tab_key in self._df_cache:
            return self._df_cache[tab_key].copy()

        df = pd.DataFrame(self.get_records(tab_key))
        df.columns = [str(c).strip() for c in df.columns]
        self._df_cache[tab_key] = df.copy()
        return df

    def invalidate(self, tab_key: TabKey) -> None:
        self._df_cache.pop(tab_key, None)

    def update_cell(self, tab_key: TabKey, row: int, col: int, value: Any) -> None:
        self.ws(tab_key).update_cell(row, col, value)
        self.invalidate(tab_key)

    def update_range(self, tab_key: TabKey, cell_range: str, values: list[list[Any]]) -> None:
        self.ws(tab_key).update(cell_range, values)
        self.invalidate(tab_key)

    def append_row(self, tab_key: TabKey, row_values: list[Any]) -> None:
        self.ws(tab_key).append_row(row_values)
        self.invalidate(tab_key)

    def batch_update(self, tab_key: TabKey, updates: list[tuple[int, int, str]]) -> None:
        from gspread.utils import rowcol_to_a1

        worksheet = self.ws(tab_key)
        tab_name = self.tabs[tab_key]
        body = {
            "valueInputOption": "RAW",
            "data": [
                {"range": f"{tab_name}!{rowcol_to_a1(row, col)}", "values": [[value]]}
                for row, col, value in updates
            ],
        }
        worksheet.spreadsheet.values_batch_update(body)
        self.invalidate(tab_key)


class OfflineTranslatorSheetsClient:
    def __init__(self, path: str = "Language.xlsx"):
        self.path = path
        if not Path(path).exists():
            raise FileNotFoundError(f"Offline sheet not found: {path}")

        self._df_cache: dict[str, pd.DataFrame] = {}
        self.tabs: dict[TabKey, str] = dict(TranslatorSheetsClient.DEFAULT_TABS)

    def get_df(self, tab_key: TabKey) -> pd.DataFrame:
        if tab_key in self._df_cache:
            return self._df_cache[tab_key].copy()

        sheet_name = self.tabs.get(tab_key)
        if not sheet_name:
            raise KeyError(f"Unknown sheet tab '{tab_key}'")

        df = pd.read_excel(self.path, sheet_name=sheet_name)
        df.columns = [str(c).strip() for c in df.columns]
        self._df_cache[tab_key] = df.copy()
        return df

    def invalidate(self, tab_key: TabKey) -> None:
        self._df_cache.pop(tab_key, None)

    def ws(self, tab_key: TabKey) -> Any:
        raise NotImplementedError("Offline mode does not provide worksheet handles.")

    def update_cell(self, tab_key: TabKey, row: int, col: int, value: Any) -> None:
        df = self.get_df(tab_key)
        df.iat[row - 2, col - 1] = value
        self._df_cache[tab_key] = df.copy()
        self._write_xlsx()

    def update_range(self, tab_key: TabKey, cell_range: str, values: list[list[Any]]) -> None:
        import re

        df = self.get_df(tab_key)
        match = re.match(r"([A-Z]+)(\\d+):([A-Z]+)(\\d+)", cell_range)
        if not match:
            raise ValueError(f"Invalid cell range: {cell_range}")
        col1, row1, col2, row2 = match.groups()

        def col_to_idx(value: str) -> int:
            idx = 0
            for ch in value:
                idx = idx * 26 + (ord(ch) - 64)
            return idx - 1

        r1, r2 = int(row1) - 2, int(row2) - 2
        c1, c2 = col_to_idx(col1), col_to_idx(col2)

        for r_offset, row_values in enumerate(values):
            for c_offset, cell in enumerate(row_values):
                r = r1 + r_offset
                c = c1 + c_offset
                if r <= r2 and c <= c2:
                    df.iat[r, c] = cell

        self._df_cache[tab_key] = df.copy()
        self._write_xlsx()

    def append_row(self, tab_key: TabKey, row_values: list[Any]) -> None:
        df = self.get_df(tab_key)
        df.loc[len(df)] = row_values
        self._df_cache[tab_key] = df.copy()
        self._write_xlsx()

    def batch_update(self, tab_key: TabKey, updates: list[tuple[int, int, str]]) -> None:
        df = self.get_df(tab_key)
        for row, col, value in updates:
            df.iat[row - 2, col - 1] = value
        self._df_cache[tab_key] = df.copy()
        self._write_xlsx()

    def _write_xlsx(self) -> None:
        with pd.ExcelWriter(self.path, engine="openpyxl", mode="w") as writer:
            for tab_key, sheet_name in self.tabs.items():
                if tab_key in self._df_cache:
                    self._df_cache[tab_key].to_excel(writer, sheet_name=sheet_name, index=False)


# Shared singletons
fantasy_sheets = ContentSheetsClient("fantasy")
modern_sheets = ContentSheetsClient("modern")
gsheets = TranslatorSheetsClient()
