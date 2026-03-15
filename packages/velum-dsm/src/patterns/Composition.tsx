import { styled } from "../styletron";

type GapScale = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9;

export const Stack = styled(
  "div",
  ({ $gap = 4, $align = "stretch" }: { $gap?: GapScale; $align?: "stretch" | "flex-start" | "center" | "flex-end" }) => ({
    display: "flex",
    flexDirection: "column",
    gap: `var(--velum-space-${$gap})`,
    alignItems: $align,
  }),
);

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

export const PanelGrid = styled(
  "div",
  ({ $min = "280px" }: { $min?: string }) => ({
    display: "grid",
    gap: "var(--velum-space-4)",
    gridTemplateColumns: `repeat(auto-fit, minmax(${$min}, 1fr))`,
  }),
);

export const ActionRow = styled("div", {
  display: "flex",
  flexWrap: "wrap",
  gap: "var(--velum-space-2)",
  marginTop: "var(--velum-space-3)",
});

export const ActionRowEnd = styled("div", {
  display: "flex",
  flexWrap: "wrap",
  gap: "var(--velum-space-2)",
  marginTop: "var(--velum-space-3)",
  justifyContent: "flex-end",
});
