import { styled } from "../../styletron";

export const Toolbar = styled("div", {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(170px, 1fr))",
  gap: "var(--velum-space-3)",
  alignItems: "end",
});
