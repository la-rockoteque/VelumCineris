import type { ReactNode } from "react";

import { styled } from "../../styletron";

import { useControllableState } from "../_internal/useControllableState";

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
  overflowX: $layout === "wrap" ? "visible" : "auto",
  overflowY: "hidden",
  borderBottom: "1px solid rgba(118, 87, 42, 0.35)",
  scrollbarWidth: "thin",
}));

const List = styled("div", ({ $layout = "grid" }: { $layout?: "grid" | "wrap" }) => ({
  display: "inline-flex",
  flexWrap: $layout === "wrap" ? "wrap" : "nowrap",
  alignItems: "flex-end",
  minWidth: "100%",
  width: $layout === "wrap" ? "100%" : "max-content",
  padding: "0 4px",
  minHeight: "40px",
}));

const TabButton = styled(
  "button",
  ({
    $active,
    $disabled,
    $size = "md",
  }: {
    $active: boolean;
    $disabled: boolean;
    $size?: "md" | "sm";
  }) => ({
    flex: "0 0 auto",
    border: "1px solid rgba(118, 87, 42, 0.35)",
    borderBottom: "none",
    borderRadius: "10px 10px 0 0",
    marginRight: "-1px",
    padding: $size === "sm" ? "6px 12px 6px" : "8px 14px 7px",
    background: $active
      ? "linear-gradient(180deg, #f6eab9 0%, #f0d88b 100%)"
      : "linear-gradient(180deg, #efd99f 0%, #e7c874 100%)",
    color: $active ? "#30220f" : "#5c4827",
    font: "inherit",
    fontSize: $size === "sm" ? "0.76rem" : "0.8rem",
    fontWeight: 700,
    letterSpacing: "0.01em",
    whiteSpace: "nowrap",
    cursor: $disabled ? "default" : "pointer",
    boxShadow: $active
      ? "inset 0 1px 0 rgba(255, 255, 236, 0.8)"
      : "inset 0 1px 0 rgba(255, 250, 225, 0.65)",
    position: "relative",
    top: "1px",
    transform: $active ? "translateY(0)" : $size === "sm" ? "translateY(9px)" : "translateY(12px)",
    transition: "border-color 160ms ease, background 160ms ease, color 160ms ease, filter 160ms ease, transform 180ms ease",
    borderColor: $active ? "rgba(112, 78, 34, 0.5)" : "rgba(118, 87, 42, 0.35)",
    zIndex: $active ? 2 : 1,
    ":hover:not(:disabled)": {
      filter: "brightness(1.04)",
      color: "#3f2f18",
      transform: "translateY(0)",
      zIndex: 2,
    },
    ":focus-visible": {
      outline: "none",
      boxShadow: "var(--velum-focus-ring)",
      transform: "translateY(0)",
      zIndex: 2,
    },
    ":disabled": {
      opacity: $active ? 1 : 0.6,
    },
  }),
);

export function TabBar(props: TabBarProps) {
  const layout = props.layout ?? "grid";
  const size = props.size ?? "md";
  const [activeKey, setActiveKey] = useControllableState(props.activeKey, props.activeKey);

  return (
    <Root className={props.className} $layout={layout}>
      <List $layout={layout} role="tablist" aria-label={props.ariaLabel}>
      {props.items.map((item) => {
        const active = item.key === activeKey;
        return (
          <TabButton
            key={item.key}
            type="button"
            role="tab"
            $active={active}
            $disabled={Boolean(item.disabled || active)}
            $size={size}
            aria-selected={active}
            disabled={item.disabled || active}
            onClick={() => {
              setActiveKey(item.key);
              props.onChange(item.key);
            }}
          >
            {item.label}
          </TabButton>
        );
      })}
      </List>
    </Root>
  );
}
