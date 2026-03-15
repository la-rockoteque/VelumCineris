import { styled } from "app/styletron";

export const Button = styled("button", {
  border: "1px solid var(--border)",
  borderRadius: "9px",
  padding: "8px 10px",
  font: "inherit",
  color: "var(--ink)",
  background: "var(--surface-strong)",
  cursor: "pointer",
  fontWeight: 600,
  ":disabled": {
    opacity: 0.6,
    cursor: "not-allowed",
  },
  ":hover:not(:disabled)": {
    borderColor: "rgba(155, 77, 31, 0.5)",
  },
});

export const InlineButton = styled("button", {
  border: "1px solid var(--border)",
  borderRadius: "9px",
  padding: "4px 10px",
  font: "inherit",
  color: "var(--ink)",
  background: "var(--surface-strong)",
  cursor: "pointer",
  fontWeight: 600,
  fontSize: "0.78rem",
  whiteSpace: "nowrap",
  ":disabled": {
    opacity: 0.6,
    cursor: "not-allowed",
  },
  ":hover:not(:disabled)": {
    borderColor: "rgba(155, 77, 31, 0.5)",
  },
});

export const ActionRow = styled("div", {
  display: "flex",
  gap: "8px",
  marginTop: "10px",
});

export const ActionRowEnd = styled("div", {
  display: "flex",
  gap: "8px",
  marginTop: "10px",
  justifyContent: "flex-end",
});
