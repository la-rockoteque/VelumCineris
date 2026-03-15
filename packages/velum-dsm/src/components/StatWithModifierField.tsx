import { styled } from "../styletron";

import { TextInput } from "./Inputs";

function formatModifier(score: string): string {
  const value = Number(score);
  if (!Number.isFinite(value)) {
    return "—";
  }
  const modifier = Math.floor((value - 10) / 2);
  return modifier >= 0 ? `+${modifier}` : String(modifier);
}

export interface StatWithModifierFieldProps {
  value: string;
  onChange: (next: string) => void;
  className?: string;
}

const Root = styled("div", {
  display: "inline-grid",
  gridTemplateColumns: "minmax(70px, 110px) auto",
  alignItems: "stretch",
  gap: 0,
});

const Modifier = styled("span", {
  display: "grid",
  placeItems: "center",
  minWidth: "58px",
  marginLeft: "-1px",
  border: "1px solid var(--velum-color-border)",
  borderTopRightRadius: "var(--velum-radius-sm)",
  borderBottomRightRadius: "var(--velum-radius-sm)",
  background: "rgba(241, 231, 214, 0.88)",
  color: "var(--velum-color-ink-soft)",
  fontSize: "var(--velum-font-size-sm)",
  fontWeight: 700,
  padding: "0 10px",
});

export function StatWithModifierField(props: StatWithModifierFieldProps) {
  return (
    <Root className={props.className}>
      <TextInput
        type="number"
        value={props.value}
        step={1}
        style={{
          borderTopRightRadius: 0,
          borderBottomRightRadius: 0,
        }}
        onChange={(event) => props.onChange(event.target.value)}
      />
      <Modifier>{formatModifier(props.value)}</Modifier>
    </Root>
  );
}
