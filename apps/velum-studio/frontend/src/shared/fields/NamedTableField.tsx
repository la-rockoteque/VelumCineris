import { NamedTableField as DsmNamedTableField } from "shared/library";

export interface NamedTableFieldProps {
  value: string;
  keyLabel: string;
  valueLabel: string;
  onChange: (next: string) => void;
  className?: string;
}

export function NamedTableField(props: NamedTableFieldProps) {
  return <DsmNamedTableField {...props} />;
}
