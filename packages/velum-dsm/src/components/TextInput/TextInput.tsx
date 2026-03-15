import { forwardRef, type InputHTMLAttributes } from "react";

import { styled } from "../../styletron";

import { fieldStyles } from "../_internal/fieldStyles";
import { useControllableState } from "../_internal/useControllableState";

const Root = styled("input", fieldStyles);

export interface TextInputProps extends InputHTMLAttributes<HTMLInputElement> {
  className?: string;
}

function toStringValue(value: InputHTMLAttributes<HTMLInputElement>["value"]) {
  if (Array.isArray(value)) {
    return value[0] ?? "";
  }
  if (value == null) {
    return "";
  }
  return String(value);
}

export const TextInput = forwardRef<HTMLInputElement, TextInputProps>(function TextInput(props, ref) {
  const { className, defaultValue, value, onChange, ...inputProps } = props;
  const [internalValue, setInternalValue] = useControllableState(
    value !== undefined ? toStringValue(value) : undefined,
    toStringValue(defaultValue),
  );

  return (
    <Root
      {...inputProps}
      ref={ref}
      className={className}
      value={internalValue}
      onChange={(event) => {
        setInternalValue(event.target.value);
        onChange?.(event);
      }}
    />
  );
});
