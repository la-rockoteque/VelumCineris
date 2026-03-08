import { useMemo, useState } from "react";

import type { SourceInfo } from "shared/types/api";
import { pickItemName } from "shared/utils/fields";
import { asText, truncateText } from "shared/utils/text";

interface CompendiumTabProps {
  loading: boolean;
  sources: SourceInfo[];
  source: string;
  sheets: string[];
  sheet: string;
  query: string;
  limit: number;
  offset: number;
  totalRows: number;
  columns: string[];
  visibleColumns: string[];
  rows: Record<string, unknown>[];
  cellCharLimit: number;
  onSourceChange: (value: string) => void | Promise<void>;
  onSheetChange: (value: string) => void | Promise<void>;
  onQueryChange: (value: string) => void;
  onRunSearch: () => void | Promise<void>;
  onLimitChange: (value: number) => void | Promise<void>;
  onPrevPage: () => void | Promise<void>;
  onNextPage: () => void | Promise<void>;
  onRefresh: () => void | Promise<void>;
  onVisibleColumnsChange: (columns: string[]) => void | Promise<void>;
  onOpenContext: (rowNumber: number, targetTab: "details" | "intelligence" | "image") => void | Promise<void>;
  onIntegrationAction: (rowNumber: number, integration: string, operation: string) => void | Promise<void>;
}

interface HeaderMenuState {
  x: number;
  y: number;
  column: string;
}

const integrationOptions: Array<{ key: string; label: string; operations: string[] }> = [
  { key: "worldanvil", label: "WorldAnvil", operations: ["publish", "delete"] },
  { key: "dndbeyond", label: "D&D Beyond", operations: ["publish", "delete"] },
  { key: "obsidianportal", label: "Obsidian Portal", operations: ["publish", "delete"] },
];

export function CompendiumTab(props: CompendiumTabProps) {
  const [headerMenu, setHeaderMenu] = useState<HeaderMenuState | null>(null);

  const visibleColumns = useMemo(() => {
    if (props.visibleColumns.length) {
      return props.visibleColumns;
    }
    return props.columns;
  }, [props.columns, props.visibleColumns]);

  const page = Math.floor(props.offset / props.limit) + 1;
  const totalPages = Math.max(1, Math.ceil(props.totalRows / props.limit));

  const toggleColumn = async (column: string) => {
    const already = visibleColumns.includes(column);
    const next = already ? visibleColumns.filter((item) => item !== column) : [...visibleColumns, column];
    const safe = next.length ? next : [column];
    await props.onVisibleColumnsChange(safe);
  };

  return (
    <section className="workspace-card">
      <h2>Compendium</h2>
      <p>Explore source sheets and trigger contextual actions from each row.</p>

      <div className="toolbar">
        <label>
          Source
          <select value={props.source} onChange={(event) => void props.onSourceChange(event.target.value)} disabled={props.loading}>
            {props.sources.map((source) => (
              <option key={source.source} value={source.source}>
                {source.source}
                {source.available ? "" : " (unavailable)"}
              </option>
            ))}
          </select>
        </label>

        <label>
          Sheet
          <select value={props.sheet} onChange={(event) => void props.onSheetChange(event.target.value)} disabled={props.loading}>
            {props.sheets.map((sheet) => (
              <option key={sheet} value={sheet}>
                {sheet}
              </option>
            ))}
          </select>
        </label>

        <label>
          Search
          <input
            value={props.query}
            onChange={(event) => props.onQueryChange(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === "Enter") {
                void props.onRunSearch();
              }
            }}
            placeholder="Filter rows..."
          />
        </label>

        <label>
          Page Size
          <select value={String(props.limit)} onChange={(event) => void props.onLimitChange(Number(event.target.value))}>
            {[25, 50, 100, 200].map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </select>
        </label>

        <label>
          Refresh
          <button className="btn" onClick={props.onRefresh} disabled={props.loading}>
            Refresh
          </button>
        </label>
      </div>

      <div className="meta">
        {props.sheet || "No sheet"} | {visibleColumns.length}/{props.columns.length} columns visible | right-click headers to show/hide
      </div>

      <div className="table-wrap" onClick={() => setHeaderMenu(null)}>
        <table>
          <thead>
            <tr>
              <th>#</th>
              {visibleColumns.map((column) => (
                <th
                  key={column}
                  onContextMenu={(event) => {
                    event.preventDefault();
                    setHeaderMenu({ x: event.clientX, y: event.clientY, column });
                  }}
                >
                  {column}
                </th>
              ))}
              <th className="row-actions-head">Actions</th>
            </tr>
          </thead>
          <tbody>
            {props.rows.map((row) => {
              const rowNumber = Number(row._sheet_row || 0);
              const rowTitle = pickItemName(row);
              return (
                <tr key={rowNumber || rowTitle || JSON.stringify(row)}>
                  <td>{rowNumber || ""}</td>
                  {visibleColumns.map((column) => {
                    const full = asText(row[column]);
                    const short = truncateText(full, props.cellCharLimit);
                    return (
                      <td key={`${rowNumber}-${column}`} title={short !== full ? full : undefined}>
                        {short}
                      </td>
                    );
                  })}
                  <td className="row-actions-cell">
                    <div className="row-actions">
                      <button className="btn row-action-btn" onClick={() => void props.onOpenContext(rowNumber, "details")}>Details</button>
                      <button className="btn row-action-btn" onClick={() => void props.onOpenContext(rowNumber, "intelligence")}>AI</button>
                      <button className="btn row-action-btn" onClick={() => void props.onOpenContext(rowNumber, "image")}>Image</button>

                      {integrationOptions.map((integration) => (
                        <details key={`${rowNumber}-${integration.key}`} className="row-action-menu">
                          <summary>{integration.label}</summary>
                          <div className="row-action-menu-list">
                            {integration.operations.map((operation) => (
                              <button
                                key={operation}
                                className="row-action-menu-btn"
                                onClick={() => void props.onIntegrationAction(rowNumber, integration.key, operation)}
                              >
                                {operation}
                              </button>
                            ))}
                          </div>
                        </details>
                      ))}
                    </div>
                  </td>
                </tr>
              );
            })}
            {!props.rows.length && (
              <tr>
                <td colSpan={visibleColumns.length + 2}>No rows.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="pager">
        <button className="btn" onClick={props.onPrevPage} disabled={props.loading || props.offset <= 0}>
          Prev
        </button>
        <span>
          Page {page} / {totalPages}
        </span>
        <button
          className="btn"
          onClick={props.onNextPage}
          disabled={props.loading || props.offset + props.limit >= props.totalRows}
        >
          Next
        </button>
      </div>

      {headerMenu && (
        <div className="column-menu" style={{ left: headerMenu.x, top: headerMenu.y }} onMouseLeave={() => setHeaderMenu(null)}>
          <div className="column-menu-title">Columns ({props.columns.length})</div>
          {props.columns.map((column) => (
            <label key={column} className="column-menu-item">
              <input type="checkbox" checked={visibleColumns.includes(column)} onChange={() => void toggleColumn(column)} />
              <span>{column}</span>
            </label>
          ))}
        </div>
      )}
    </section>
  );
}
