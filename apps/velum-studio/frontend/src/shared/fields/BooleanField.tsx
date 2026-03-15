import { toBoolean } from "shared/utils/text";
import { styled } from "app/styletron";
import { Checkbox } from "shared/library";

export interface BooleanFieldProps {
  value: unknown;
  onChange: (next: string) => void;
  trueLabel?: string;
  falseLabel?: string;
  className?: string;
}

const CheckWrap = styled("div", {
  display: "inline-flex",
  alignItems: "center",
  gap: "8px",
  minHeight: "36px",
  fontSize: "0.8rem",
  color: "#5b4f3f",
});

export function BooleanField(props: BooleanFieldProps) {
  const checked = toBoolean(props.value);
  const trueLabel = props.trueLabel ?? "True";
  const falseLabel = props.falseLabel ?? "False";

  return (
    <CheckWrap className={props.className}>
      <Checkbox checked={checked} onChange={(event) => props.onChange(event.target.checked ? "True" : "False")} label={checked ? trueLabel : falseLabel} />
    </CheckWrap>
  );
}
