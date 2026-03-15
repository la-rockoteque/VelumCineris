from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import random
import sys
import time
from typing import Any

from google.oauth2.service_account import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build

try:
    from Spreadsheet.sheets import ContentSheetsClient
except ModuleNotFoundError:
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "Spreadsheet").is_dir():
            sys.path.insert(0, str(parent))
            break
    from Spreadsheet.sheets import ContentSheetsClient


@dataclass(frozen=True)
class SheetProps:
    sheet_id: int
    title: str
    index: int
    row_count: int
    col_count: int


def execute_with_retry(request: Any, *, action: str, max_attempts: int = 8) -> Any:
    for attempt in range(1, max_attempts + 1):
        try:
            return request.execute()
        except HttpError as exc:
            status = getattr(exc.resp, "status", None)
            message = str(exc)
            retryable = status in (429, 500, 502, 503, 504) or "RATE_LIMIT_EXCEEDED" in message
            if not retryable or attempt == max_attempts:
                raise
            delay = min(30.0, (2 ** (attempt - 1)) + random.uniform(0.0, 1.0))
            print(
                f"[RETRY] {action} failed with HTTP {status}; "
                f"attempt {attempt}/{max_attempts}. Sleeping {delay:.1f}s."
            )
            time.sleep(delay)


def col_to_letters(index_1_based: int) -> str:
    value = index_1_based
    letters: list[str] = []
    while value > 0:
        value, remainder = divmod(value - 1, 26)
        letters.append(chr(65 + remainder))
    return "".join(reversed(letters))


def escape_title(title: str) -> str:
    return title.replace("'", "''")


def get_sheet_props(service: Any, spreadsheet_id: str) -> list[SheetProps]:
    response = execute_with_retry(
        service.spreadsheets()
        .get(
            spreadsheetId=spreadsheet_id,
            fields="sheets(properties(sheetId,title,index,gridProperties(rowCount,columnCount)))",
            includeGridData=False,
        ),
        action=f"get_sheet_props({spreadsheet_id})",
    )
    out: list[SheetProps] = []
    for sheet in response.get("sheets", []):
        props = sheet.get("properties", {})
        grid = props.get("gridProperties", {})
        out.append(
            SheetProps(
                sheet_id=int(props["sheetId"]),
                title=str(props.get("title", "")),
                index=int(props.get("index", 0)),
                row_count=int(grid.get("rowCount", 1000)),
                col_count=int(grid.get("columnCount", 26)),
            )
        )
    return sorted(out, key=lambda item: item.index)


def by_title(sheets: list[SheetProps]) -> dict[str, SheetProps]:
    return {sheet.title: sheet for sheet in sheets}


def by_id(sheets: list[SheetProps]) -> dict[int, SheetProps]:
    return {sheet.sheet_id: sheet for sheet in sheets}


def batch_update(service: Any, spreadsheet_id: str, requests: list[dict[str, Any]]) -> None:
    if not requests:
        return
    execute_with_retry(
        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={"requests": requests}),
        action=f"batch_update({spreadsheet_id})",
    )


def copy_sheet_to_spreadsheet(
    service: Any,
    source_spreadsheet_id: str,
    source_sheet_id: int,
    destination_spreadsheet_id: str,
) -> int:
    response = execute_with_retry(
        service.spreadsheets()
        .sheets()
        .copyTo(
            spreadsheetId=source_spreadsheet_id,
            sheetId=source_sheet_id,
            body={"destinationSpreadsheetId": destination_spreadsheet_id},
        ),
        action=f"copy_sheet({source_sheet_id})",
    )
    return int(response["sheetId"])


def read_old_values_with_formulas(
    service: Any,
    spreadsheet_id: str,
    sheet_title: str,
    row_count: int,
    col_count: int,
    *,
    start_row: int = 2,
) -> list[list[str]]:
    if row_count < start_row or col_count < 1:
        return []
    end_col = col_to_letters(col_count)
    rng = f"'{escape_title(sheet_title)}'!A{start_row}:{end_col}{row_count}"
    response = execute_with_retry(
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=rng,
            valueRenderOption="FORMULA",
            majorDimension="ROWS",
        ),
        action=f"read_values({sheet_title})",
    )
    values = response.get("values", [])
    return [[str(cell) for cell in row] for row in values]


def read_header_row(
    service: Any,
    spreadsheet_id: str,
    sheet_title: str,
    col_count: int,
) -> list[str]:
    if col_count < 1:
        return []
    end_col = col_to_letters(col_count)
    rng = f"'{escape_title(sheet_title)}'!A1:{end_col}1"
    response = execute_with_retry(
        service.spreadsheets()
        .values()
        .get(
            spreadsheetId=spreadsheet_id,
            range=rng,
            valueRenderOption="UNFORMATTED_VALUE",
            majorDimension="ROWS",
        ),
        action=f"read_header_row({sheet_title})",
    )
    values = response.get("values", [])
    first_row = values[0] if values else []
    out: list[str] = []
    for idx in range(col_count):
        value = first_row[idx] if idx < len(first_row) else ""
        out.append("" if value is None else str(value))
    return out


def normalize_header(value: str) -> str:
    return value.strip().lower()


def build_header_column_map(old_headers: list[str], new_headers: list[str]) -> dict[int, int]:
    # 1-based old column index -> 1-based new column index
    new_by_header: dict[str, list[int]] = {}
    for new_idx, header in enumerate(new_headers, start=1):
        key = normalize_header(header)
        if not key:
            continue
        new_by_header.setdefault(key, []).append(new_idx)

    used_new: set[int] = set()
    mapping: dict[int, int] = {}
    for old_idx, header in enumerate(old_headers, start=1):
        key = normalize_header(header)
        if not key:
            continue
        candidates = new_by_header.get(key, [])
        for new_idx in candidates:
            if new_idx not in used_new:
                mapping[old_idx] = new_idx
                used_new.add(new_idx)
                break
    return mapping


def clear_sheet_body_values(
    service: Any,
    spreadsheet_id: str,
    sheet_title: str,
    row_count: int,
    col_count: int,
    *,
    start_row: int = 2,
) -> None:
    if row_count < start_row or col_count < 1:
        return
    end_col = col_to_letters(col_count)
    rng = f"'{escape_title(sheet_title)}'!A{start_row}:{end_col}{row_count}"
    execute_with_retry(
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=rng,
            body={},
        ),
        action=f"clear_sheet_body_values({sheet_title})",
    )


def write_non_empty_values_by_map(
    service: Any,
    spreadsheet_id: str,
    target_title: str,
    rows: list[list[str]],
    old_to_new_col_map: dict[int, int],
    *,
    start_row: int = 2,
    chunk_size: int = 4000,
) -> int:
    escaped = escape_title(target_title)
    updates: list[dict[str, Any]] = []

    for row_index, row in enumerate(rows, start=start_row):
        for old_col_index, cell in enumerate(row, start=1):
            if cell == "":
                continue
            new_col_index = old_to_new_col_map.get(old_col_index)
            if new_col_index is None:
                continue
            updates.append(
                {
                    "range": f"'{escaped}'!{col_to_letters(new_col_index)}{row_index}",
                    "values": [[cell]],
                }
            )

    if not updates:
        return 0

    written = 0
    for offset in range(0, len(updates), chunk_size):
        chunk = updates[offset : offset + chunk_size]
        execute_with_retry(
            service.spreadsheets().values().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={"valueInputOption": "USER_ENTERED", "data": chunk},
            ),
            action=f"write_values_by_map({target_title})",
        )
        written += len(chunk)

    return written


def make_unique_tmp_title(base_title: str, existing_titles: set[str]) -> str:
    candidate = f"__TMP__{base_title}"
    if candidate not in existing_titles:
        return candidate
    counter = 2
    while True:
        candidate = f"__TMP__{base_title}_{counter}"
        if candidate not in existing_titles:
            return candidate
        counter += 1


def sync_modern_to_fantasy_format(
    *,
    service: Any,
    fantasy_spreadsheet_id: str,
    modern_spreadsheet_id: str,
    apply: bool,
    remove_extra_sheets: bool,
) -> None:
    fantasy_sheets = get_sheet_props(service, fantasy_spreadsheet_id)
    fantasy_titles = [sheet.title for sheet in fantasy_sheets]
    fantasy_map = by_title(fantasy_sheets)

    print(f"Fantasy tabs discovered: {len(fantasy_titles)}")
    print(f"Modern spreadsheet: {modern_spreadsheet_id}")
    print(f"Mode: {'APPLY' if apply else 'DRY-RUN'}")

    for target_index, title in enumerate(fantasy_titles):
        modern_sheets = get_sheet_props(service, modern_spreadsheet_id)
        modern_map = by_title(modern_sheets)
        fantasy_sheet = fantasy_map[title]
        existing = modern_map.get(title)

        if existing is None:
            print(f"[ADD] Missing tab '{title}' -> copy from fantasy.")
            if not apply:
                continue

            new_sheet_id = copy_sheet_to_spreadsheet(
                service,
                fantasy_spreadsheet_id,
                fantasy_sheet.sheet_id,
                modern_spreadsheet_id,
            )

            batch_update(
                service,
                modern_spreadsheet_id,
                [
                    {
                        "updateSheetProperties": {
                            "properties": {
                                "sheetId": new_sheet_id,
                                "title": title,
                                "index": target_index,
                            },
                            "fields": "title,index",
                        }
                    }
                ],
            )
            continue

        print(f"[REPLACE] '{title}' -> refresh format from fantasy and reapply modern values/formulas.")
        if not apply:
            continue

        modern_existing_titles = {sheet.title for sheet in modern_sheets}
        tmp_title = make_unique_tmp_title(title, modern_existing_titles)

        old_headers = read_header_row(
            service,
            modern_spreadsheet_id,
            existing.title,
            existing.col_count,
        )
        old_values = read_old_values_with_formulas(
            service,
            modern_spreadsheet_id,
            existing.title,
            existing.row_count,
            existing.col_count,
            start_row=2,
        )

        new_sheet_id = copy_sheet_to_spreadsheet(
            service,
            fantasy_spreadsheet_id,
            fantasy_sheet.sheet_id,
            modern_spreadsheet_id,
        )

        fresh_sheets = get_sheet_props(service, modern_spreadsheet_id)
        new_sheet = by_id(fresh_sheets)[new_sheet_id]
        target_row_count = max(new_sheet.row_count, existing.row_count)
        target_col_count = max(new_sheet.col_count, existing.col_count)

        batch_update(
            service,
            modern_spreadsheet_id,
            [
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": new_sheet_id,
                            "title": tmp_title,
                            "index": target_index,
                            "gridProperties": {
                                "rowCount": target_row_count,
                                "columnCount": target_col_count,
                            },
                        },
                        "fields": "title,index,gridProperties.rowCount,gridProperties.columnCount",
                    }
                }
            ],
        )

        new_headers = read_header_row(
            service,
            modern_spreadsheet_id,
            tmp_title,
            target_col_count,
        )
        old_to_new_col_map = build_header_column_map(old_headers, new_headers)
        clear_sheet_body_values(
            service,
            modern_spreadsheet_id,
            tmp_title,
            target_row_count,
            target_col_count,
            start_row=2,
        )

        written_cells = write_non_empty_values_by_map(
            service,
            modern_spreadsheet_id,
            tmp_title,
            old_values,
            old_to_new_col_map,
            start_row=2,
        )
        print(
            f"  └─ mapped {len(old_to_new_col_map)}/{len(old_headers)} columns by header; "
            f"reapplied {written_cells} non-empty cells from old '{title}'."
        )

        batch_update(
            service,
            modern_spreadsheet_id,
            [{"deleteSheet": {"sheetId": existing.sheet_id}}],
        )

        batch_update(
            service,
            modern_spreadsheet_id,
            [
                {
                    "updateSheetProperties": {
                        "properties": {
                            "sheetId": new_sheet_id,
                            "title": title,
                            "index": target_index,
                        },
                        "fields": "title,index",
                    }
                }
            ],
        )

    if remove_extra_sheets:
        modern_sheets = get_sheet_props(service, modern_spreadsheet_id)
        fantasy_set = set(fantasy_titles)
        extras = [sheet for sheet in modern_sheets if sheet.title not in fantasy_set]
        for extra in extras:
            print(f"[DELETE] Extra modern tab '{extra.title}'")
            if not apply:
                continue
            batch_update(
                service,
                modern_spreadsheet_id,
                [{"deleteSheet": {"sheetId": extra.sheet_id}}],
            )
    else:
        modern_sheets = get_sheet_props(service, modern_spreadsheet_id)
        fantasy_set = set(fantasy_titles)
        extras = [sheet.title for sheet in modern_sheets if sheet.title not in fantasy_set]
        if extras:
            print(f"[KEEP] Extra modern tabs kept: {extras}")

    print("Done.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Consolidate modern Google spreadsheet tabs/format to match fantasy, while preserving existing modern values/formulas."
        )
    )
    parser.add_argument("--credentials", default=None, help="Path to Google service account key.json (optional)")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default is dry-run)")
    parser.add_argument(
        "--remove-extra-sheets",
        action="store_true",
        help="Delete tabs that exist in modern but not in fantasy.",
    )
    args = parser.parse_args()

    fantasy_client = ContentSheetsClient("fantasy", credentials_path=args.credentials)
    modern_client = ContentSheetsClient("modern", credentials_path=args.credentials)

    creds_path = Path(fantasy_client.credentials_path)
    scopes = tuple(fantasy_client.scopes)
    creds = Credentials.from_service_account_file(str(creds_path), scopes=scopes)
    service = build("sheets", "v4", credentials=creds, cache_discovery=False)

    sync_modern_to_fantasy_format(
        service=service,
        fantasy_spreadsheet_id=fantasy_client.spreadsheet_id,
        modern_spreadsheet_id=modern_client.spreadsheet_id,
        apply=args.apply,
        remove_extra_sheets=args.remove_extra_sheets,
    )


if __name__ == "__main__":
    main()
