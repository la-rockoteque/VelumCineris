import { styled } from "../../styletron";

export const PanelGrid = styled(
  "div",
  ({ $min = "280px" }: { $min?: string }) => ({
    display: "grid",
    gap: "var(--velum-space-4)",
    gridTemplateColumns: `repeat(auto-fit, minmax(${$min}, 1fr))`,
  }),
);
