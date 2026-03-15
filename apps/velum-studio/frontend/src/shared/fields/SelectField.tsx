import { styled } from "app/styletron";

export interface SelectFieldProps {
  value: string;
  options: string[];
  onChange: (next: string) => void;
  className?: string;
}

const Select = styled("select", {});
const Option = styled("option", {});

export function SelectField(props: SelectFieldProps) {
  return (
    <Select className={props.className} value={props.value} onChange={(event) => props.onChange(event.target.value)}>
      <Option value="" />
      {props.options.map((option) => (
        <Option key={option} value={option}>
          {option}
        </Option>
      ))}
    </Select>
  );
}
