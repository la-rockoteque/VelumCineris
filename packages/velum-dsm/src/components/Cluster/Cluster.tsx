import { styled } from "../../styletron";

type GapScale = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;

export const Cluster = styled(
  "div",
  ({
    $gap = 3,
    $align = "center",
    $justify = "flex-start",
  }: {
    $gap?: GapScale;
    $align?: "stretch" | "flex-start" | "center" | "flex-end";
    $justify?: "flex-start" | "center" | "flex-end" | "space-between";
  }) => ({
    display: "flex",
    flexWrap: "wrap",
    gap: `var(--velum-space-${$gap})`,
    alignItems: $align,
    justifyContent: $justify,
  }),
);
