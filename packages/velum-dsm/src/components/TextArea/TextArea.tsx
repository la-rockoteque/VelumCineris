import { forwardRef, type TextareaHTMLAttributes } from "react";

import { styled } from "../../styletron";

import { fieldStyles } from "../_internal/fieldStyles";
import { useControllableState } from "../_internal/useControllableState";

const Root = styled("textarea", {
  ...fieldStyles,
  minHeight: "120px",
  resize: "vertical",
});

export interface TextAreaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  className?: string;
}

function toStringValue(value: TextareaHTMLAttributes<HTMLTextAreaElement>["value"]) {
  if (Array.isArray(value)) {
    return value[0] ?? "";
  }
  if (value == null) {
    return "";
  }
  return String(value);
}

export const TextArea = forwardRef<HTMLTextAreaElement, TextAreaProps>(function TextArea(props, ref) {
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
