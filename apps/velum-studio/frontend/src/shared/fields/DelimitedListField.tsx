import { DelimitedListField as DsmDelimitedListField } from "shared/library";

export interface DelimitedListFieldProps {
  value: string;
  onChange: (next: string) => void;
  options?: string[];
  delimiter?: string;
  className?: string;
}

export function DelimitedListField(props: DelimitedListFieldProps) {
  return <DsmDelimitedListField {...props} />;
}
