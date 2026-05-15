import { TextArea } from "shared/library";

export interface LongTextFieldProps {
  value: string;
  onChange: (next: string) => void;
  rows?: number;
  placeholder?: string;
  className?: string;
}

export function LongTextField(props: LongTextFieldProps) {
  return (
    <TextArea
      className={props.className}
      rows={props.rows ?? 5}
      value={props.value}
      placeholder={props.placeholder}
      onChange={(event) => props.onChange(event.target.value)}
    />
  );
}
