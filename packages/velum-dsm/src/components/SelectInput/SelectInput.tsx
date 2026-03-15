import { forwardRef, type SelectHTMLAttributes } from "react";

import { styled } from "../../styletron";

import { fieldStyles, selectCaretBackground } from "../_internal/fieldStyles";
import { useControllableState } from "../_internal/useControllableState";

const Root = styled("select", {
  ...fieldStyles,
  appearance: "none",
  backgroundImage: selectCaretBackground,
  backgroundPosition: "right 12px center",
  backgroundRepeat: "no-repeat",
  backgroundSize: "16px 16px",
  paddingRight: "36px",
});

export interface SelectInputProps extends SelectHTMLAttributes<HTMLSelectElement> {
  className?: string;
}

function toStringValue(value: SelectHTMLAttributes<HTMLSelectElement>["value"]) {
  if (Array.isArray(value)) {
    return value[0] ?? "";
  }
  if (value == null) {
    return "";
  }
  return String(value);
}

export const SelectInput = forwardRef<HTMLSelectElement, SelectInputProps>(function SelectInput(props, ref) {
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
