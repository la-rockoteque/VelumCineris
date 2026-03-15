import { styled } from "../../styletron";

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
