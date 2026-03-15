import { useEffect, useMemo, useState } from "react";

import { MetaText, TableWrap, Toolbar, WorkspaceCard, WorkspaceLead, WorkspaceTitle } from "shared/library";
import type { SpreadsheetRowsResponse } from "shared/types/api";
import { asText, truncateText } from "shared/utils/text";

interface ValidationsTabProps {
  loading: boolean;
  source: string;
  validationSheets: string[];
  cellCharLimit: number;
  onLoadValidationRows: (sheet: string) => Promise<SpreadsheetRowsResponse | null>;
}

export function ValidationsTab(props: ValidationsTabProps) {
  const [sheet, setSheet] = useState("");
  const [columns, setColumns] = useState<string[]>([]);
  const [rows, setRows] = useState<Record<string, unknown>[]>([]);
  const [meta, setMeta] = useState("Select a validation sheet.");

  useEffect(() => {
    const first = props.validationSheets[0] || "";
    setSheet((current) => (current && props.validationSheets.includes(current) ? current : first));
  }, [props.validationSheets]);

  useEffect(() => {
    if (!sheet) {
      setColumns([]);
      setRows([]);
      setMeta("No validation sheet available.");
      return;
    }

    void (async () => {
      const payload = await props.onLoadValidationRows(sheet);
      if (!payload) {
        return;
      }
      setColumns(payload.columns || []);
      setRows(payload.rows || []);
      setMeta(`${payload.sheet} | ${payload.total_rows} rows`);
    })();
  }, [props, sheet]);

  const colCount = useMemo(() => Math.max(1, columns.length), [columns.length]);

  return (
    <WorkspaceCard>
      <WorkspaceTitle>Validations</WorkspaceTitle>
      <WorkspaceLead>Validation sheets are the source for dropdown and enum-like choices in details editing.</WorkspaceLead>

      <Toolbar>
        <label>
          Validation Sheet
          <select value={sheet} onChange={(event) => setSheet(event.target.value)} disabled={props.loading}>
            {props.validationSheets.map((name) => (
              <option key={name} value={name}>
                {name}
              </option>
            ))}
          </select>
        </label>
      </Toolbar>

      <MetaText>{meta}</MetaText>

      <TableWrap>
        <table>
          <thead>
            <tr>
              {columns.map((column) => (
                <th key={column}>{column}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, index) => (
              <tr key={`${sheet}-${index}`}>
                {columns.map((column) => {
                  const full = asText(row[column]);
                  const short = truncateText(full, props.cellCharLimit);
                  return (
                    <td key={`${index}-${column}`} title={short !== full ? full : undefined}>
                      {short}
                    </td>
                  );
                })}
              </tr>
            ))}
            {!rows.length && (
              <tr>
                <td colSpan={colCount}>No rows found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </TableWrap>
    </WorkspaceCard>
  );
}
