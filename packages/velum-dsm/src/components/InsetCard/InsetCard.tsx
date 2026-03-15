import { styled } from "../../styletron";

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
