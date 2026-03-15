import type { Key, ReactNode } from "react";

import { styled } from "../styletron";

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
  ":hover td": {
    background: "rgba(249, 240, 229, 0.92)",
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
          <BodyRow key={props.getRowKey ? props.getRowKey(row, index) : index}>
            {props.columns.map((column) => (
              <BodyCell key={column.key} $align={column.align} title={column.cellTitle?.(row, index)}>
                {readCellValue(row, column, index)}
              </BodyCell>
            ))}
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
