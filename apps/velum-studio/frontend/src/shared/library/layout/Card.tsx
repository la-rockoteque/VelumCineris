import { styled } from "app/styletron";

import type { BlockProps } from "./types";

const CardRoot = styled("section", {
  border: "1px solid var(--border)",
  borderRadius: "12px",
  padding: "16px",
  background: "var(--surface-strong)",
});

const CardTitle = styled("h2", {
  margin: 0,
  fontFamily: "\"Avenir Next Condensed\", \"Trebuchet MS\", sans-serif",
  textTransform: "uppercase",
  letterSpacing: "0.04em",
});

const CardSubtitle = styled("p", {
  margin: "6px 0 0",
  color: "var(--ink-soft)",
});

export function Card(props: BlockProps) {
  return (
    <CardRoot className={props.className}>
      {props.title ? <CardTitle>{props.title}</CardTitle> : null}
      {props.subtitle ? <CardSubtitle>{props.subtitle}</CardSubtitle> : null}
      {props.children}
    </CardRoot>
  );
}
