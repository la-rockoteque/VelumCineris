import { styled } from "app/styletron";

export interface TextFieldProps {
  value: string;
  onChange: (next: string) => void;
  placeholder?: string;
  readOnly?: boolean;
  disabled?: boolean;
  className?: string;
}

const Input = styled("input", {});

export function TextField(props: TextFieldProps) {
  return (
    <Input
      className={props.className}
      value={props.value}
      onChange={(event) => props.onChange(event.target.value)}
      placeholder={props.placeholder}
      readOnly={props.readOnly}
      disabled={props.disabled}
    />
  );
}
