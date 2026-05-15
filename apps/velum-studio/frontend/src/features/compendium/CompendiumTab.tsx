import { useMemo, useState, type ComponentProps } from "react";
import { styled } from "app/styletron";

import { Button, Checkbox, InlineButton, MetaText, iconAssets, SelectInput, TabBar, TableWrap, TextInput, Toolbar, WorkspaceCard, WorkspaceLead, WorkspaceTitle } from "shared/library";
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

const DataRow = styled("tr", {
  cursor: "pointer",
  ":hover td": {
    background: "#f9f0e5",
  },
  ":hover [data-row-actions='true']": {
    opacity: 1,
    transform: "translateY(-50%) translateX(0)",
  },
});

const RowActions = styled("div", {
  position: "absolute",
  top: "50%",
  right: "8px",
  display: "flex",
  gap: "6px",
  justifyContent: "flex-end",
  alignItems: "center",
  opacity: 0,
  transform: "translateY(-50%) translateX(8px)",
  transition: "opacity 140ms ease, transform 140ms ease",
});

const RowActionGlyph = styled("span", {
  fontSize: "0.9rem",
  lineHeight: 1,
});

const RowActionImage = styled("img", {
  width: "14px",
  height: "14px",
  objectFit: "contain",
});

const RowActionMenu = styled("details", {
  position: "relative",
});

const RowActionMenuSummary = styled("summary", {
  listStyle: "none",
  border: "1px solid var(--border)",
  borderRadius: "8px",
  width: "28px",
  height: "28px",
  background: "var(--surface-strong)",
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
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

function RowActionButton(props: ComponentProps<typeof InlineButton>) {
  return <InlineButton {...props} style={{ width: "28px", height: "28px", minWidth: "28px", padding: 0, ...props.style }} />;
}

function RowActionMenuButton(props: ComponentProps<typeof InlineButton>) {
  return (
    <InlineButton
      {...props}
      style={{
        width: "100%",
        justifyContent: "flex-start",
        borderColor: "transparent",
        background: "transparent",
        textAlign: "left",
        padding: "6px 8px",
        borderRadius: "6px",
        fontSize: "0.76rem",
        color: "#4f4537",
        ...props.style,
      }}
    />
  );
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
    <WorkspaceCard>
      <WorkspaceTitle>Compendium</WorkspaceTitle>
      <WorkspaceLead>Explore source sheets and trigger contextual actions from each row.</WorkspaceLead>

      <Toolbar>
        <label>
          Source
          <SelectInput value={props.source} onChange={(event) => void props.onSourceChange(event.target.value)} disabled={props.loading}>
            {props.sources.map((source) => (
              <option key={source.source} value={source.source}>
                {source.source}
                {source.available ? "" : " (unavailable)"}
              </option>
            ))}
          </SelectInput>
        </label>

        <label>
          Search
          <TextInput
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
          <SelectInput value={String(props.limit)} onChange={(event) => void props.onLimitChange(Number(event.target.value))}>
            {[25, 50, 100, 200].map((value) => (
              <option key={value} value={value}>
                {value}
              </option>
            ))}
          </SelectInput>
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
        <TabBar
          ariaLabel="Sheet"
          activeKey={props.sheet}
          onChange={(value) => void props.onSheetChange(value)}
          items={props.sheets.map((sheet) => ({
            key: sheet,
            label: sheet,
            disabled: props.loading || sheet === props.sheet,
          }))}
        />
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
            </tr>
          </thead>
          <tbody>
            {props.rows.map((row) => {
              const rowNumber = Number(row._sheet_row || 0);
              const rowTitle = pickItemName(row);
              return (
                <DataRow
                  key={rowNumber || rowTitle || JSON.stringify(row)}
                  onClick={() => void props.onOpenContext(rowNumber, "details")}
                >
                  <td>{rowNumber || ""}</td>
                  {visibleColumns.map((column, columnIndex) => {
                    const full = asText(row[column]);
                    const short = truncateText(full, props.cellCharLimit);
                    const isLastColumn = columnIndex === visibleColumns.length - 1;
                    return (
                      <td
                        key={`${rowNumber}-${column}`}
                        title={short !== full ? full : undefined}
                        style={isLastColumn ? { position: "relative", paddingRight: "210px" } : undefined}
                      >
                        {short}
                        {isLastColumn ? (
                          <RowActions data-row-actions="true">
                            <InlineButton
                              type="button"
                              onClick={(event) => {
                                event.stopPropagation();
                                void props.onOpenContext(rowNumber, "details");
                              }}
                            >
                              Details
                            </InlineButton>
                            <RowActionButton
                              type="button"
                              title="Open Intelligence"
                              aria-label="Open Intelligence"
                              onClick={(event) => {
                                event.stopPropagation();
                                void props.onOpenContext(rowNumber, "intelligence");
                              }}
                            >
                              <RowActionGlyph>✦</RowActionGlyph>
                            </RowActionButton>
                            <RowActionButton
                              type="button"
                              title="Open Image Generator"
                              aria-label="Open Image Generator"
                              onClick={(event) => {
                                event.stopPropagation();
                                void props.onOpenContext(rowNumber, "image");
                              }}
                            >
                              <RowActionGlyph>◫</RowActionGlyph>
                            </RowActionButton>

                            {integrationOptions.map((integration) => (
                              <RowActionMenu key={`${rowNumber}-${integration.key}`} onClick={(event) => event.stopPropagation()}>
                                <RowActionMenuSummary
                                  title={integration.label}
                                  aria-label={integration.label}
                                >
                                  {integration.key === "worldanvil" ? (
                                    <RowActionImage alt="" src={iconAssets.WA} />
                                  ) : integration.key === "dndbeyond" ? (
                                    <RowActionImage alt="" src={iconAssets.DNDBeyond} />
                                  ) : (
                                    <RowActionImage alt="" src={iconAssets.OP} />
                                  )}
                                </RowActionMenuSummary>
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
                        ) : null}
                      </td>
                    );
                  })}
                </DataRow>
              );
            })}
            {!props.rows.length && (
              <tr>
                <td colSpan={visibleColumns.length + 1}>No rows.</td>
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
            <Checkbox
              key={column}
              checked={visibleColumns.includes(column)}
              onChange={() => void toggleColumn(column)}
              label={column}
              style={{ padding: "4px 0" }}
            />
          ))}
        </ColumnMenu>
      )}
    </WorkspaceCard>
  );
}
