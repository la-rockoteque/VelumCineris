import type { Key, ReactNode } from "react";

import { styled } from "../../styletron";

type TableAlign = "left" | "center" | "right";

export interface TableColumn<Row> {
  key: string;
  header: ReactNode;
  render?: (row: Row, index: number) => ReactNode;
  align?: TableAlign;
  width?: string;
  cellTitle?: (row: Row, index: number) => string | undefined;
}

export interface TableProps<Row extends Record<string, unknown>> {
  columns: Array<TableColumn<Row>>;
  rows: Row[];
  onRowClick: (row: Row, index: number) => void;
  getRowActions?: (
    row: Row,
    index: number,
  ) => Array<{
    key: string;
    label: string;
    icon: ReactNode;
    onClick: (row: Row, index: number) => void;
    disabled?: boolean;
  }>;
  getRowKey?: (row: Row, index: number) => Key;
  emptyMessage?: ReactNode;
  caption?: ReactNode;
  minWidth?: string;
  className?: string;
}

const Root = styled("table", {
  width: "100%",
  borderCollapse: "collapse",
  background: "rgba(255, 255, 255, 0.28)",
  color: "var(--velum-color-ink)",
});

const Caption = styled("caption", {
  captionSide: "top",
  padding: "0 0 var(--velum-space-2)",
  textAlign: "left",
  color: "var(--velum-color-ink-soft)",
  fontSize: "var(--velum-font-size-sm)",
});

const HeadCell = styled(
  "th",
  ({ $align = "left", $width }: { $align?: TableAlign; $width?: string }) => ({
    padding: "10px 12px",
    borderBottom: "1px solid rgba(66, 48, 30, 0.12)",
    background: "rgba(241, 231, 214, 0.85)",
    color: "var(--velum-color-ink-soft)",
    fontSize: "var(--velum-font-size-sm)",
    textAlign: $align,
    width: $width,
    whiteSpace: "nowrap",
  }),
);

const BodyRow = styled("tr", {
  cursor: "pointer",
  ":hover td": {
    background: "rgba(249, 240, 229, 0.92)",
  },
  ":hover [data-row-actions='true']": {
    opacity: 1,
    transform: "translateY(-50%) translateX(0)",
  },
});

const BodyCell = styled("td", ({ $align = "left" }: { $align?: TableAlign }) => ({
  padding: "10px 12px",
  borderBottom: "1px solid rgba(66, 48, 30, 0.1)",
  fontSize: "var(--velum-font-size-sm)",
  textAlign: $align,
  verticalAlign: "top",
  background: "transparent",
}));

const CellFrame = styled("div", ({ $withActions = false }: { $withActions?: boolean }) => ({
  position: "relative",
  minHeight: "1.2rem",
  paddingRight: $withActions ? "132px" : 0,
}));

const RowActions = styled("div", {
  position: "absolute",
  top: "50%",
  right: 0,
  display: "inline-flex",
  alignItems: "center",
  gap: "6px",
  transform: "translateY(-50%) translateX(8px)",
  opacity: 0,
  transition: "opacity 140ms ease, transform 140ms ease",
});

const RowActionButton = styled("button", ({ $disabled = false }: { $disabled?: boolean }) => ({
  width: "28px",
  height: "28px",
  display: "inline-flex",
  alignItems: "center",
  justifyContent: "center",
  border: "1px solid var(--velum-color-border)",
  borderRadius: "8px",
  background: "var(--velum-color-surface-strong)",
  color: "var(--velum-color-ink-soft)",
  cursor: $disabled ? "not-allowed" : "pointer",
  opacity: $disabled ? 0.55 : 1,
  ":hover:not(:disabled)": {
    borderColor: "rgba(155, 77, 31, 0.5)",
    color: "var(--velum-color-ink)",
  },
}));

function readCellValue<Row extends Record<string, unknown>>(row: Row, column: TableColumn<Row>, index: number): ReactNode {
  if (column.render) {
    return column.render(row, index);
  }

  return row[column.key] as ReactNode;
}

export function Table<Row extends Record<string, unknown>>(props: TableProps<Row>) {
  const columnCount = Math.max(1, props.columns.length);

  return (
    <Root className={props.className} style={{ minWidth: props.minWidth }}>
      {props.caption != null ? <Caption>{props.caption}</Caption> : null}
      <thead>
        <tr>
          {props.columns.map((column) => (
            <HeadCell key={column.key} $align={column.align} $width={column.width}>
              {column.header}
            </HeadCell>
          ))}
        </tr>
      </thead>
      <tbody>
        {props.rows.map((row, index) => (
          <BodyRow key={props.getRowKey ? props.getRowKey(row, index) : index} onClick={() => props.onRowClick(row, index)}>
            {props.columns.map((column, columnIndex, columns) => {
              const rowActions = columnIndex === columns.length - 1 ? props.getRowActions?.(row, index) ?? [] : [];
              return (
                <BodyCell key={column.key} $align={column.align} title={column.cellTitle?.(row, index)}>
                  <CellFrame $withActions={rowActions.length > 0}>
                    {readCellValue(row, column, index)}
                    {rowActions.length > 0 ? (
                      <RowActions data-row-actions="true">
                        {rowActions.map((action) => (
                          <RowActionButton
                            key={action.key}
                            type="button"
                            title={action.label}
                            aria-label={action.label}
                            $disabled={action.disabled}
                            disabled={action.disabled}
                            onClick={(event) => {
                              event.stopPropagation();
                              action.onClick(row, index);
                            }}
                          >
                            {action.icon}
                          </RowActionButton>
                        ))}
                      </RowActions>
                    ) : null}
                  </CellFrame>
                </BodyCell>
              );
            })}
          </BodyRow>
        ))}
        {!props.rows.length ? (
          <BodyRow>
            <BodyCell colSpan={columnCount}>{props.emptyMessage ?? "No rows."}</BodyCell>
          </BodyRow>
        ) : null}
      </tbody>
    </Root>
  );
}
