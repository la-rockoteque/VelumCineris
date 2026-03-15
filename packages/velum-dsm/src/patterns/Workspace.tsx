import { styled } from "../styletron";

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

export const Toolbar = styled("div", {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))",
  gap: "var(--velum-space-3)",
  alignItems: "end",
});

export const MetaText = styled("div", {
  color: "var(--velum-color-ink-soft)",
  fontSize: "var(--velum-font-size-sm)",
});

export const TableWrap = styled("div", {
  overflowX: "auto",
  border: "1px solid var(--velum-color-border)",
  borderRadius: "var(--velum-radius-md)",
  background: "rgba(255, 255, 255, 0.28)",
});

export const FeatureOutput = styled("div", {
  border: "1px solid var(--velum-color-border)",
  borderRadius: "var(--velum-radius-md)",
  padding: "var(--velum-space-4)",
  background: "rgba(255, 255, 255, 0.34)",
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

export const WorkbenchLayout = styled(
  "div",
  ({
    $sidebar = "minmax(260px, 360px)",
    $gap = "14px",
    $collapseAt = "1100px",
  }: {
    $sidebar?: string;
    $gap?: string;
    $collapseAt?: string;
  }) => ({
    marginTop: "var(--velum-space-3)",
    display: "grid",
    gap: $gap,
    gridTemplateColumns: `${$sidebar} minmax(0, 1fr)`,
    alignItems: "start",
    [`@media (max-width: ${$collapseAt})`]: {
      gridTemplateColumns: "1fr",
    },
  }),
);

export const WorkbenchSidebar = styled("div", {
  display: "grid",
  gap: "var(--velum-space-3)",
  alignContent: "start",
});

export const WorkbenchMain = styled("div", {
  minWidth: 0,
});

export const InsetCard = styled("div", {
  display: "grid",
  gap: "var(--velum-space-2)",
  padding: "10px",
  borderRadius: "10px",
  border: "1px solid var(--velum-color-border)",
  background: "#fbf5e8",
});

export const InsetTitle = styled("h3", {
  margin: 0,
  fontSize: "0.82rem",
  textTransform: "uppercase",
  letterSpacing: "var(--velum-font-tracking-normal)",
  color: "#6a5d4b",
});

export const InsetLead = styled("p", {
  margin: 0,
  fontSize: "0.8rem",
  color: "var(--velum-color-ink-soft)",
});
