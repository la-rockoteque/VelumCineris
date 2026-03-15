import { styled } from "app/styletron";

export const MetaText = styled("div", {
  marginTop: "8px",
  color: "var(--ink-soft)",
  minHeight: "20px",
});

export const TableWrap = styled("div", {
  marginTop: "12px",
  border: "1px solid var(--border)",
  borderRadius: "14px",
  overflow: "auto",
  maxHeight: "60vh",
  background: "var(--surface-strong)",
});

export const FeatureOutput = styled("div", {
  marginTop: "12px",
  border: "1px solid var(--border)",
  borderRadius: "10px",
  background: "var(--surface-muted)",
  padding: "10px",
  maxHeight: "42vh",
  overflow: "auto",
  fontSize: "0.8rem",
  whiteSpace: "pre-wrap",
});

export const WorkspaceOutput = styled("pre", {
  marginTop: "12px",
  border: "1px solid var(--border)",
  borderRadius: "10px",
  background: "var(--surface-muted)",
  padding: "10px",
  maxHeight: "42vh",
  overflow: "auto",
  fontSize: "0.8rem",
  whiteSpace: "pre-wrap",
  minHeight: "320px",
});
