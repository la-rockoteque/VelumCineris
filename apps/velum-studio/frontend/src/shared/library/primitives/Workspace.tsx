import { styled } from "app/styletron";

export const WorkspaceCard = styled("section", {
  border: "1px solid var(--border)",
  borderRadius: "12px",
  padding: "16px",
  background: "var(--surface-strong)",
});

export const WorkspaceTitle = styled("h2", {
  margin: 0,
  fontFamily: "\"Avenir Next Condensed\", \"Trebuchet MS\", sans-serif",
  textTransform: "uppercase",
  letterSpacing: "0.04em",
});

export const WorkspaceLead = styled("p", {
  margin: "6px 0 0",
  color: "var(--ink-soft)",
});

export const Toolbar = styled("div", {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))",
  gap: "10px",
  alignItems: "end",
});
