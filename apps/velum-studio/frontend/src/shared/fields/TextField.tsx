import { TextInput } from "shared/library";

export interface TextFieldProps {
  value: string;
  onChange: (next: string) => void;
  placeholder?: string;
  readOnly?: boolean;
  disabled?: boolean;
  className?: string;
}

export function TextField(props: TextFieldProps) {
  return (
    <TextInput
      className={props.className}
      value={props.value}
      onChange={(event) => props.onChange(event.target.value)}
      placeholder={props.placeholder}
      readOnly={props.readOnly}
      disabled={props.disabled}
    />
  );
}
