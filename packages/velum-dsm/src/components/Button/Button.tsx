import { styled } from "../../styletron";

type ButtonVariant = "primary" | "secondary" | "ghost";
type ButtonSize = "md" | "sm";

const baseButtonStyles = ({
  $variant = "secondary",
  $size = "md",
}: {
  $variant?: ButtonVariant;
  $size?: ButtonSize;
}) => ({
  border: "1px solid var(--velum-color-border)",
  borderRadius: "var(--velum-radius-sm)",
  padding: $size === "sm" ? "4px 10px" : "8px 10px",
  fontFamily: "inherit",
  fontSize: $size === "sm" ? "var(--velum-font-size-xs)" : "var(--velum-font-size-md)",
  color:
    $variant === "primary"
      ? "#fff8ef"
      : $variant === "ghost"
        ? "var(--velum-color-ink-soft)"
        : "var(--velum-color-ink)",
  background:
    $variant === "primary"
      ? "linear-gradient(180deg, var(--velum-color-accent-soft), var(--velum-color-accent))"
      : $variant === "ghost"
        ? "transparent"
        : "var(--velum-color-surface-strong)",
  cursor: "pointer",
  fontWeight: 700,
  whiteSpace: "nowrap" as const,
  transition: `border-color var(--velum-motion-quick) var(--velum-motion-ease-standard), box-shadow var(--velum-motion-quick) var(--velum-motion-ease-standard), transform var(--velum-motion-quick) var(--velum-motion-ease-standard)`,
  boxShadow: $variant === "primary" ? "var(--velum-shadow-inset-accent)" : "none",
  ":disabled": {
    opacity: 0.6,
    cursor: "not-allowed",
  },
  ":hover:not(:disabled)": {
    borderColor: "rgba(155, 77, 31, 0.5)",
    boxShadow:
      $variant === "primary"
        ? "var(--velum-shadow-inset-accent), var(--velum-shadow-soft)"
        : "var(--velum-shadow-soft)",
    transform: "translateY(-1px)",
  },
  ":focus-visible": {
    outline: "none",
    boxShadow: "var(--velum-focus-ring)",
  },
});

export const Button = styled("button", baseButtonStyles);

export type { ButtonSize, ButtonVariant };
