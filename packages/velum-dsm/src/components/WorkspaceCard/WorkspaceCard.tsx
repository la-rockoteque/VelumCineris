import { styled } from "../../styletron";

export const WorkspaceCard = styled("section", {
  display: "grid",
  gap: "var(--velum-space-3)",
  border: "1px solid var(--velum-color-border)",
  borderRadius: "var(--velum-radius-md)",
  padding: "var(--velum-space-4)",
  background: "var(--velum-color-surface-strong)",
  boxShadow: "var(--velum-shadow-soft)",
});

export const WorkspaceTitle = styled("h2", {
  margin: 0,
  fontFamily: "var(--velum-font-display)",
  fontSize: "var(--velum-font-size-xl)",
  textTransform: "uppercase",
  letterSpacing: "var(--velum-font-tracking-normal)",
});

export const WorkspaceLead = styled("p", {
  margin: 0,
  color: "var(--velum-color-ink-soft)",
});

export const WorkspaceOutput = styled("pre", {
  margin: 0,
  padding: "var(--velum-space-4)",
  border: "1px solid var(--velum-color-border)",
  borderRadius: "var(--velum-radius-md)",
  background: "rgba(35, 29, 22, 0.92)",
  color: "#f7eedf",
  fontFamily: "var(--velum-font-mono)",
  fontSize: "0.88rem",
  overflowX: "auto",
  whiteSpace: "pre-wrap",
  wordBreak: "break-word",
});
