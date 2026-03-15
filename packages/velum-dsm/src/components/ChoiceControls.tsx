import type { InputHTMLAttributes, ReactNode } from "react";

import { styled } from "../styletron";

interface BaseChoiceProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: ReactNode;
  description?: ReactNode;
  className?: string;
}

export interface CheckboxProps extends BaseChoiceProps {}

export interface RadioButtonProps extends BaseChoiceProps {}

const ChoiceRoot = styled("label", ({ $disabled }: { $disabled?: boolean }) => ({
  display: "inline-grid",
  gridTemplateColumns: "16px minmax(0, 1fr)",
  gap: "10px",
  alignItems: "start",
  color: $disabled ? "var(--velum-color-ink-soft)" : "var(--velum-color-ink)",
  cursor: $disabled ? "not-allowed" : "pointer",
}));

const ChoiceInput = styled("input", {
  width: "16px",
  height: "16px",
  margin: "2px 0 0",
  accentColor: "var(--velum-color-accent)",
});

const ChoiceBody = styled("span", {
  display: "grid",
  gap: "2px",
  minWidth: 0,
});

const ChoiceLabel = styled("span", {
  fontSize: "var(--velum-font-size-md)",
  lineHeight: 1.35,
});

const ChoiceDescription = styled("span", {
  fontSize: "var(--velum-font-size-sm)",
  color: "var(--velum-color-ink-soft)",
  lineHeight: 1.45,
});

function ChoiceControl(props: BaseChoiceProps & { type: "checkbox" | "radio" }) {
  const { label, description, className, disabled, type, ...inputProps } = props;

  return (
    <ChoiceRoot className={className} $disabled={disabled}>
      <ChoiceInput type={type} disabled={disabled} {...inputProps} />
      <ChoiceBody>
        {label != null ? <ChoiceLabel>{label}</ChoiceLabel> : null}
        {description != null ? <ChoiceDescription>{description}</ChoiceDescription> : null}
      </ChoiceBody>
    </ChoiceRoot>
  );
}

export function Checkbox(props: CheckboxProps) {
  return <ChoiceControl type="checkbox" {...props} />;
}

export function RadioButton(props: RadioButtonProps) {
  return <ChoiceControl type="radio" {...props} />;
}
