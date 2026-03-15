import type { ReactNode } from "react";

import { styled } from "../../styletron";
import { useControllableState } from "../_internal/useControllableState";

export interface SegmentedControlOption {
  value: string;
  label: ReactNode;
  disabled?: boolean;
}

export interface SegmentedControlProps {
  value: string;
  options: readonly SegmentedControlOption[];
  onChange: (value: string) => void;
  ariaLabel: string;
  className?: string;
}

const Root = styled("div", {
  display: "inline-flex",
  alignItems: "stretch",
});

const Segment = styled(
  "label",
  ({
    $selected,
    $edge,
    $disabled,
  }: {
    $selected: boolean;
    $edge: "first" | "middle" | "last" | "single";
    $disabled: boolean;
  }) => ({
    position: "relative",
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    minWidth: "88px",
    padding: "10px 14px",
    border: "1px solid var(--velum-color-border)",
    marginLeft: $edge === "first" || $edge === "single" ? 0 : "-1px",
    borderTopLeftRadius: $edge === "first" || $edge === "single" ? "var(--velum-radius-sm)" : "0",
    borderBottomLeftRadius: $edge === "first" || $edge === "single" ? "var(--velum-radius-sm)" : "0",
    borderTopRightRadius: $edge === "last" || $edge === "single" ? "var(--velum-radius-sm)" : "0",
    borderBottomRightRadius: $edge === "last" || $edge === "single" ? "var(--velum-radius-sm)" : "0",
    background: $selected ? "rgba(241, 225, 190, 0.95)" : "rgba(255, 255, 255, 0.72)",
    color: $selected ? "var(--velum-color-ink)" : "var(--velum-color-ink-soft)",
    fontSize: "var(--velum-font-size-sm)",
    fontWeight: 700,
    cursor: $disabled ? "not-allowed" : "pointer",
    opacity: $disabled ? 0.6 : 1,
    transition:
      "border-color var(--velum-motion-quick) var(--velum-motion-ease-standard), background var(--velum-motion-quick) var(--velum-motion-ease-standard), color var(--velum-motion-quick) var(--velum-motion-ease-standard), box-shadow var(--velum-motion-quick) var(--velum-motion-ease-standard)",
    ":hover": $disabled
      ? undefined
      : {
          borderColor: "rgba(155, 77, 31, 0.5)",
          color: "var(--velum-color-ink)",
        },
    ":focus-within": {
      zIndex: 1,
      boxShadow: "var(--velum-focus-ring)",
    },
  }),
);

const HiddenRadio = styled("input", {
  position: "absolute",
  inset: 0,
  opacity: 0,
  cursor: "pointer",
});

function edge(index: number, total: number): "first" | "middle" | "last" | "single" {
  if (total === 1) {
    return "single";
  }
  if (index === 0) {
    return "first";
  }
  if (index === total - 1) {
    return "last";
  }
  return "middle";
}

export function SegmentedControl(props: SegmentedControlProps) {
  const [value, setValue] = useControllableState(props.value, props.value);

  return (
    <Root className={props.className} role="radiogroup" aria-label={props.ariaLabel}>
      {props.options.map((option, index, options) => {
        const selected = option.value === value;
        return (
          <Segment
            key={option.value}
            $selected={selected}
            $edge={edge(index, options.length)}
            $disabled={Boolean(option.disabled)}
            onClick={() => {
              if (!option.disabled) {
                setValue(option.value);
                props.onChange(option.value);
              }
            }}
          >
            {option.label}
            <HiddenRadio
              type="radio"
              name={props.ariaLabel}
              checked={selected}
              disabled={option.disabled}
              onChange={() => {
                setValue(option.value);
                props.onChange(option.value);
              }}
            />
          </Segment>
        );
      })}
    </Root>
  );
}
