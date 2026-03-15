import { DiceField } from "shared/library";

export interface HitDiceFieldProps {
  value: string;
  onChange: (next: string) => void;
  className?: string;
}

export function HitDiceField(props: HitDiceFieldProps) {
  return <DiceField {...props} />;
}
