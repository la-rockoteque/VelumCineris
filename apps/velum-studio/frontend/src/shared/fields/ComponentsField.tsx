import { ComponentsField as DsmComponentsField } from "shared/library";

export interface ComponentsFieldProps {
  value: string;
  onChange: (next: string) => void;
  className?: string;
}

export function ComponentsField(props: ComponentsFieldProps) {
  return <DsmComponentsField {...props} />;
}
