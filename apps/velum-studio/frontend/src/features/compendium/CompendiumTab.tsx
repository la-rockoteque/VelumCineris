import { useMemo, useState } from "react";
import { styled } from "app/styletron";

import { Button, InlineButton, MetaText, TableWrap, Toolbar, WorkspaceCard, WorkspaceLead, WorkspaceTitle } from "shared/library";
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

const SheetTabsRow = styled("div", {
  marginTop: "10px",
  display: "grid",
  gap: "6px",
});

const SheetTabsLabel = styled("div", {
  fontSize: "0.78rem",
  fontWeight: 700,
  letterSpacing: "0.04em",
  textTransform: "uppercase",
  color: "#6c604f",
});

const SheetTabbarWrap = styled("div", {
  overflowX: "auto",
  overflowY: "hidden",
  borderBottom: "1px solid rgba(118, 87, 42, 0.35)",
  scrollbarWidth: "thin",
});

const SheetTabbar = styled("div", {
  display: "inline-flex",
  alignItems: "flex-end",
  minWidth: "100%",
  width: "max-content",
  padding: "0 4px",
  minHeight: "40px",
});

const SheetTab = styled("button", ({ $active }: { $active: boolean }) => ({
  flex: "0 0 auto",
  border: "1px solid rgba(118, 87, 42, 0.35)",
  borderBottom: "none",
  borderRadius: "10px 10px 0 0",
  marginRight: "-1px",
  padding: "8px 14px 7px",
  font: "inherit",
  fontSize: "0.8rem",
  fontWeight: 700,
  letterSpacing: "0.01em",
  whiteSpace: "nowrap",
  background: $active
    ? "linear-gradient(180deg, #f6eab9 0%, #f0d88b 100%)"
    : "linear-gradient(180deg, #efd99f 0%, #e7c874 100%)",
  color: $active ? "#30220f" : "#5c4827",
  cursor: "pointer",
  boxShadow: $active
    ? "inset 0 1px 0 rgba(255, 255, 236, 0.8)"
    : "inset 0 1px 0 rgba(255, 250, 225, 0.65)",
  position: "relative",
  top: "1px",
  transform: $active ? "translateY(0)" : "translateY(12px)",
  transition: "border-color 160ms ease, background 160ms ease, color 160ms ease, filter 160ms ease, transform 180ms ease",
  borderColor: $active ? "rgba(112, 78, 34, 0.5)" : "rgba(118, 87, 42, 0.35)",
  zIndex: $active ? 2 : 1,
  ":hover:not(:disabled)": {
    filter: "brightness(1.04)",
    color: "#3f2f18",
    transform: "translateY(0)",
    zIndex: 2,
  },
  ":focus-visible": {
    transform: "translateY(0)",
    zIndex: 2,
  },
  ":disabled": {
    opacity: 1,
    cursor: "default",
  },
}));

const ActionHeadCell = styled("th", {
  width: "280px",
  minWidth: "280px",
});

const ActionCell = styled("td", {
  width: "280px",
  minWidth: "280px",
});

const DataRow = styled("tr", {
  ":hover td": {
    background: "#f9f0e5",
  },
  ":hover [data-row-actions='true']": {
    opacity: 1,
    transform: "translateX(0)",
  },
});

const RowActions = styled("div", {
  display: "flex",
  gap: "6px",
  justifyContent: "flex-end",
  alignItems: "center",
  opacity: 0,
  transform: "translateX(8px)",
  transition: "opacity 140ms ease, transform 140ms ease",
});

const RowActionButton = styled("button", {
  border: "1px solid var(--border)",
  borderRadius: "8px",
  padding: "4px 8px",
  font: "inherit",
  fontSize: "0.72rem",
  fontWeight: 600,
  minWidth: "56px",
  background: "var(--surface-strong)",
  cursor: "pointer",
  ":disabled": {
    opacity: 0.6,
    cursor: "not-allowed",
  },
  ":hover:not(:disabled)": {
    borderColor: "rgba(155, 77, 31, 0.5)",
  },
});

const RowActionMenu = styled("details", {
  position: "relative",
});

const RowActionMenuSummary = styled("summary", {
  listStyle: "none",
  border: "1px solid var(--border)",
  borderRadius: "8px",
  padding: "4px 8px",
  fontSize: "0.72rem",
  fontWeight: 700,
  background: "var(--surface-strong)",
  cursor: "pointer",
});

const RowActionMenuList = styled("div", {
  position: "absolute",
  right: 0,
  top: "calc(100% + 5px)",
  zIndex: 15,
  minWidth: "110px",
  border: "1px solid var(--border)",
  borderRadius: "8px",
  background: "#fff9ef",
  boxShadow: "0 10px 20px rgba(0, 0, 0, 0.12)",
  padding: "4px",
  display: "grid",
  gap: "4px",
});

const RowActionMenuButton = styled("button", {
  border: "1px solid transparent",
  background: "transparent",
  textAlign: "left",
  padding: "6px 8px",
  borderRadius: "6px",
  fontSize: "0.76rem",
  cursor: "pointer",
  color: "#4f4537",
  ":hover": {
    borderColor: "rgba(155, 77, 31, 0.35)",
    background: "#f6ecdd",
  },
});

const Pager = styled("div", {
  marginTop: "10px",
  display: "flex",
  justifyContent: "flex-end",
  alignItems: "center",
  gap: "10px",
});

const ColumnMenu = styled("div", {
  position: "fixed",
  zIndex: 99,
  minWidth: "220px",
  maxHeight: "60vh",
  overflow: "auto",
  border: "1px solid var(--border)",
  borderRadius: "10px",
  background: "var(--surface-strong)",
  boxShadow: "0 12px 24px rgba(0, 0, 0, 0.12)",
  padding: "8px",
});

const ColumnMenuTitle = styled("div", {
  fontSize: "0.8rem",
  fontWeight: 700,
  color: "var(--ink-soft)",
  marginBottom: "6px",
  paddingBottom: "6px",
  borderBottom: "1px solid rgba(66, 48, 30, 0.14)",
});

const ColumnMenuItem = styled("label", {
  display: "flex",
  alignItems: "center",
  gap: "8px",
  padding: "4px 0",
  color: "var(--ink)",
  fontSize: "0.84rem",
});

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
    <WorkspaceCard>
      <WorkspaceTitle>Compendium</WorkspaceTitle>
      <WorkspaceLead>Explore source sheets and trigger contextual actions from each row.</WorkspaceLead>

      <Toolbar>
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
          <Button onClick={props.onRefresh} disabled={props.loading}>
            Refresh
          </Button>
        </label>
      </Toolbar>

      <SheetTabsRow>
        <SheetTabsLabel>Sheet</SheetTabsLabel>
        <SheetTabbarWrap>
          <SheetTabbar role="tablist" aria-label="Sheet">
            {props.sheets.map((sheet) => {
              const isActive = sheet === props.sheet;
              return (
                <SheetTab
                  key={sheet}
                  type="button"
                  role="tab"
                  $active={isActive}
                  aria-selected={isActive}
                  onClick={() => void props.onSheetChange(sheet)}
                  disabled={props.loading || isActive}
                >
                  {sheet}
                </SheetTab>
              );
            })}
          </SheetTabbar>
        </SheetTabbarWrap>
      </SheetTabsRow>

      <MetaText>
        {props.sheet || "No sheet"} | {visibleColumns.length}/{props.columns.length} columns visible | right-click headers to show/hide
      </MetaText>

      <TableWrap onClick={() => setHeaderMenu(null)}>
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
              <ActionHeadCell>Actions</ActionHeadCell>
            </tr>
          </thead>
          <tbody>
            {props.rows.map((row) => {
              const rowNumber = Number(row._sheet_row || 0);
              const rowTitle = pickItemName(row);
              return (
                <DataRow key={rowNumber || rowTitle || JSON.stringify(row)}>
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
                  <ActionCell>
                    <RowActions data-row-actions="true">
                      <RowActionButton onClick={() => void props.onOpenContext(rowNumber, "details")}>Details</RowActionButton>
                      <RowActionButton onClick={() => void props.onOpenContext(rowNumber, "intelligence")}>AI</RowActionButton>
                      <RowActionButton onClick={() => void props.onOpenContext(rowNumber, "image")}>Image</RowActionButton>

                      {integrationOptions.map((integration) => (
                        <RowActionMenu key={`${rowNumber}-${integration.key}`}>
                          <RowActionMenuSummary>{integration.label}</RowActionMenuSummary>
                          <RowActionMenuList>
                            {integration.operations.map((operation) => (
                              <RowActionMenuButton
                                key={operation}
                                onClick={() => void props.onIntegrationAction(rowNumber, integration.key, operation)}
                              >
                                {operation}
                              </RowActionMenuButton>
                            ))}
                          </RowActionMenuList>
                        </RowActionMenu>
                      ))}
                    </RowActions>
                  </ActionCell>
                </DataRow>
              );
            })}
            {!props.rows.length && (
              <tr>
                <td colSpan={visibleColumns.length + 2}>No rows.</td>
              </tr>
            )}
          </tbody>
        </table>
      </TableWrap>

      <Pager>
        <Button onClick={props.onPrevPage} disabled={props.loading || props.offset <= 0}>
          Prev
        </Button>
        <span>
          Page {page} / {totalPages}
        </span>
        <Button onClick={props.onNextPage} disabled={props.loading || props.offset + props.limit >= props.totalRows}>
          Next
        </Button>
      </Pager>

      {headerMenu && (
        <ColumnMenu style={{ left: headerMenu.x, top: headerMenu.y }} onMouseLeave={() => setHeaderMenu(null)}>
          <ColumnMenuTitle>Columns ({props.columns.length})</ColumnMenuTitle>
          {props.columns.map((column) => (
            <ColumnMenuItem key={column}>
              <input type="checkbox" checked={visibleColumns.includes(column)} onChange={() => void toggleColumn(column)} />
              <span>{column}</span>
            </ColumnMenuItem>
          ))}
        </ColumnMenu>
      )}
    </WorkspaceCard>
  );
}
