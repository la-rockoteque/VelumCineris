import type { InputHTMLAttributes, ReactNode } from "react";

import { styled } from "../../styletron";

import { useControllableState } from "../_internal/useControllableState";

export interface CheckboxProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "type"> {
  label?: ReactNode;
  description?: ReactNode;
  className?: string;
}

const Root = styled("label", ({ $disabled }: { $disabled?: boolean }) => ({
  display: "inline-grid",
  gridTemplateColumns: "16px minmax(0, 1fr)",
  gap: "10px",
  alignItems: "start",
  color: $disabled ? "var(--velum-color-ink-soft)" : "var(--velum-color-ink)",
  cursor: $disabled ? "not-allowed" : "pointer",
}));

const Input = styled("input", {
  width: "16px",
  height: "16px",
  margin: "2px 0 0",
  accentColor: "var(--velum-color-accent)",
});

const Body = styled("span", {
  display: "grid",
  gap: "2px",
  minWidth: 0,
});

const Label = styled("span", {
  fontSize: "var(--velum-font-size-md)",
  lineHeight: 1.35,
});

const Description = styled("span", {
  fontSize: "var(--velum-font-size-sm)",
  color: "var(--velum-color-ink-soft)",
  lineHeight: 1.45,
});

export function Checkbox(props: CheckboxProps) {
  const { label, description, className, disabled, checked, defaultChecked, onChange, ...inputProps } = props;
  const [internalChecked, setInternalChecked] = useControllableState(checked, Boolean(defaultChecked));

  return (
    <Root className={className} $disabled={disabled}>
      <Input
        type="checkbox"
        disabled={disabled}
        checked={internalChecked}
        onChange={(event) => {
          setInternalChecked(event.target.checked);
          onChange?.(event);
        }}
        {...inputProps}
      />
      <Body>
        {label != null ? <Label>{label}</Label> : null}
        {description != null ? <Description>{description}</Description> : null}
      </Body>
    </Root>
  );
}
