import { styled } from "app/styletron";

export interface LongTextFieldProps {
  value: string;
  onChange: (next: string) => void;
  rows?: number;
  placeholder?: string;
  className?: string;
}

const Textarea = styled("textarea", {});

export function LongTextField(props: LongTextFieldProps) {
  return (
    <Textarea
      className={props.className}
      rows={props.rows ?? 5}
      value={props.value}
      placeholder={props.placeholder}
      onChange={(event) => props.onChange(event.target.value)}
    />
  );
}
