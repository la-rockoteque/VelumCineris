import { styled } from "../../styletron";

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
