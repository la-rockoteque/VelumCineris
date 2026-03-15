import { StatWithModifierField as DsmStatWithModifierField } from "shared/library";

export interface StatWithModifierFieldProps {
  value: string;
  onChange: (next: string) => void;
  className?: string;
}

export function StatWithModifierField(props: StatWithModifierFieldProps) {
  return <DsmStatWithModifierField {...props} />;
}
