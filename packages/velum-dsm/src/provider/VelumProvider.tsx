import type { PropsWithChildren } from "react";

import { designTokenVars } from "../tokens";
import { StyletronProvider, styletron, styled } from "../styletron";

const ThemeRoot = styled("div", {
  ...designTokenVars,
  minHeight: "100%",
  color: "var(--velum-color-ink)",
  fontFamily: "var(--velum-font-body)",
});

export function VelumProvider(props: PropsWithChildren) {
  return (
    <StyletronProvider value={styletron}>
      <ThemeRoot>{props.children}</ThemeRoot>
    </StyletronProvider>
  );
}
