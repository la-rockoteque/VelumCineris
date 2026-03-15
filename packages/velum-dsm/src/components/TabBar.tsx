import type { ReactNode } from "react";

import { styled } from "../styletron";

export interface TabBarItem {
  key: string;
  label: ReactNode;
  disabled?: boolean;
}

export interface TabBarProps {
  items: readonly TabBarItem[];
  activeKey: string;
  onChange: (key: string) => void;
  ariaLabel: string;
  className?: string;
  layout?: "grid" | "wrap";
  size?: "md" | "sm";
}

const Root = styled("div", ({ $layout = "grid" }: { $layout?: "grid" | "wrap" }) => ({
  display: $layout === "grid" ? "grid" : "flex",
  gap: "var(--velum-space-2)",
  alignItems: "stretch",
  gridTemplateColumns: $layout === "grid" ? "repeat(auto-fit, minmax(140px, 1fr))" : undefined,
  flexWrap: $layout === "wrap" ? "wrap" : undefined,
}));

const TabButton = styled(
  "button",
  ({
    $active,
    $size = "md",
  }: {
    $active: boolean;
    $size?: "md" | "sm";
  }) => ({
    border: "1px solid var(--velum-color-border)",
    borderRadius: "var(--velum-radius-sm)",
    padding: $size === "sm" ? "8px 10px" : "10px 12px",
    background: $active ? "rgba(241, 225, 190, 0.95)" : "var(--velum-color-surface-strong)",
    color: $active ? "var(--velum-color-ink)" : "var(--velum-color-ink-soft)",
    font: "inherit",
    fontSize: $size === "sm" ? "var(--velum-font-size-sm)" : "var(--velum-font-size-md)",
    fontWeight: 700,
    whiteSpace: "nowrap",
    cursor: "pointer",
    transition:
      "border-color var(--velum-motion-quick) var(--velum-motion-ease-standard), box-shadow var(--velum-motion-quick) var(--velum-motion-ease-standard), transform var(--velum-motion-quick) var(--velum-motion-ease-standard)",
    borderColor: $active ? "rgba(155, 77, 31, 0.45)" : "var(--velum-color-border)",
    boxShadow: $active ? "inset 0 -3px 0 var(--velum-color-accent-soft)" : "none",
    ":hover:not(:disabled)": {
      color: "var(--velum-color-ink)",
      borderColor: "rgba(155, 77, 31, 0.45)",
      boxShadow: "inset 0 -3px 0 var(--velum-color-accent-soft)",
      transform: "translateY(-1px)",
    },
    ":focus-visible": {
      outline: "none",
      boxShadow: "var(--velum-focus-ring)",
    },
    ":disabled": {
      cursor: "default",
      opacity: $active ? 1 : 0.6,
    },
  }),
);

export function TabBar(props: TabBarProps) {
  const layout = props.layout ?? "grid";
  const size = props.size ?? "md";

  return (
    <Root className={props.className} $layout={layout} role="tablist" aria-label={props.ariaLabel}>
      {props.items.map((item) => {
        const active = item.key === props.activeKey;
        return (
          <TabButton
            key={item.key}
            type="button"
            role="tab"
            $active={active}
            $size={size}
            aria-selected={active}
            disabled={item.disabled}
            onClick={() => props.onChange(item.key)}
          >
            {item.label}
          </TabButton>
        );
      })}
    </Root>
  );
}
