import { TextInput } from "shared/library";

export interface NumberFieldProps {
  value: string;
  onChange: (next: string) => void;
  min?: number;
  max?: number;
  step?: string;
  placeholder?: string;
  className?: string;
}

export function NumberField(props: NumberFieldProps) {
  return (
    <TextInput
      className={props.className}
      type="number"
      value={props.value}
      min={props.min}
      max={props.max}
      step={props.step ?? "any"}
      placeholder={props.placeholder}
      onChange={(event) => props.onChange(event.target.value)}
    />
  );
}
