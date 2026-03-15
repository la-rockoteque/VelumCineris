import { MultiSelect } from "shared/library";

export interface MultiSelectFieldProps {
  value: string;
  options: string[];
  onChange: (next: string) => void;
  placeholder?: string;
  className?: string;
}

export function MultiSelectField(props: MultiSelectFieldProps) {
  return (
    <MultiSelect
      className={props.className}
      value={props.value}
      options={props.options}
      onChange={props.onChange}
      placeholder={props.placeholder}
    />
  );
}
