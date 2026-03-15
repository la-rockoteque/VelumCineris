import type { ReactNode } from "react";

import { styled } from "../styletron";

const BadgeRoot = styled(
  "span",
  ({ $tone = "info" }: { $tone?: "info" | "ok" | "warn" | "danger" }) => ({
    display: "inline-flex",
    alignItems: "center",
    border: "1px solid var(--velum-color-border)",
    borderRadius: "var(--velum-radius-pill)",
    padding: "6px 12px",
    fontSize: "var(--velum-font-size-sm)",
    fontWeight: 700,
    background: "var(--velum-color-surface-strong)",
    color:
      $tone === "ok"
        ? "var(--velum-color-ok)"
        : $tone === "warn"
          ? "var(--velum-color-warn)"
          : $tone === "danger"
            ? "var(--velum-color-danger)"
            : "var(--velum-color-info)",
  }),
);

export function Badge(props: {
  children: ReactNode;
  tone?: "info" | "ok" | "warn" | "danger";
}) {
  return <BadgeRoot $tone={props.tone}>{props.children}</BadgeRoot>;
}
