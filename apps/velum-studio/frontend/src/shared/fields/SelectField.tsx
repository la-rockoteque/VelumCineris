import { SelectInput } from "shared/library";

export interface SelectFieldProps {
  value: string;
  options: string[];
  onChange: (next: string) => void;
  className?: string;
}

export function SelectField(props: SelectFieldProps) {
  return (
    <SelectInput className={props.className} value={props.value} onChange={(event) => props.onChange(event.target.value)}>
      <option value="" />
      {props.options.map((option) => (
        <option key={option} value={option}>
          {option}
        </option>
      ))}
    </SelectInput>
  );
}
