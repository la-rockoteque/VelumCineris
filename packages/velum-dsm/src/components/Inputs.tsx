import { styled } from "../styletron";

const fieldStyles = {
  width: "100%",
  border: "1px solid var(--velum-color-border)",
  borderRadius: "var(--velum-radius-sm)",
  padding: "10px 12px",
  background: "rgba(255, 255, 255, 0.72)",
  color: "var(--velum-color-ink)",
  transition: `border-color var(--velum-motion-quick) var(--velum-motion-ease-standard), box-shadow var(--velum-motion-quick) var(--velum-motion-ease-standard)`,
  ":focus": {
    outline: "none",
    borderColor: "rgba(155, 77, 31, 0.5)",
    boxShadow: "var(--velum-focus-ring)",
  },
};

export const TextInput = styled("input", fieldStyles);

export const TextArea = styled("textarea", {
  ...fieldStyles,
  minHeight: "120px",
  resize: "vertical",
});

export const SelectInput = styled("select", {
  ...fieldStyles,
  appearance: "none",
});
