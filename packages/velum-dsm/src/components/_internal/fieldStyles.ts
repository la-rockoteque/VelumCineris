export const fieldStyles = {
  width: "100%",
  border: "1px solid var(--velum-color-border)",
  borderRadius: "var(--velum-radius-sm)",
  padding: "10px 12px",
  background: "rgba(255, 255, 255, 0.72)",
  color: "var(--velum-color-ink)",
  transition: `border-color var(--velum-motion-quick) var(--velum-motion-ease-standard), box-shadow var(--velum-motion-quick) var(--velum-motion-ease-standard), background var(--velum-motion-quick) var(--velum-motion-ease-standard), color var(--velum-motion-quick) var(--velum-motion-ease-standard)`,
  ":focus": {
    outline: "none",
    borderColor: "rgba(155, 77, 31, 0.5)",
    boxShadow: "var(--velum-focus-ring)",
  },
  ":disabled": {
    background: "rgba(214, 203, 184, 0.52)",
    color: "var(--velum-color-ink-soft)",
    cursor: "not-allowed",
  },
} as const;

export const selectCaretBackground =
  "url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'%3E%3Cpath fill='%236a5d4b' d='M4.22 5.97a.75.75 0 0 1 1.06 0L8 8.69l2.72-2.72a.75.75 0 1 1 1.06 1.06L8.53 10.28a.75.75 0 0 1-1.06 0L4.22 7.03a.75.75 0 0 1 0-1.06Z'/%3E%3C/svg%3E\")";
