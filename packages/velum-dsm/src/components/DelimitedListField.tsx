import { useMemo } from "react";

import { styled } from "../styletron";

import { InlineButton } from "./Buttons";
import { TextInput } from "./Inputs";

function parseDelimitedList(value: string): string[] {
  return value
    .split(/[,\n;]+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

export interface DelimitedListFieldProps {
  value: string;
  onChange: (next: string) => void;
  options?: string[];
  delimiter?: string;
  className?: string;
}

const Root = styled("div", {
  display: "grid",
  gap: "var(--velum-space-2)",
});

const Row = styled("div", {
  display: "grid",
  gridTemplateColumns: "minmax(0, 1fr) auto",
  gap: 0,
  alignItems: "stretch",
});

const ActionCell = styled("div", {
  display: "grid",
  placeItems: "center",
  minWidth: "92px",
  marginLeft: "-1px",
  border: "1px solid var(--velum-color-border)",
  borderTopRightRadius: "var(--velum-radius-sm)",
  borderBottomRightRadius: "var(--velum-radius-sm)",
  background: "rgba(255, 255, 255, 0.68)",
  padding: "6px",
});

export function DelimitedListField(props: DelimitedListFieldProps) {
  const delimiter = props.delimiter ?? ", ";
  const lines = parseDelimitedList(props.value);
  const editableLines = lines.length ? lines : [""];
  const datalistId = useMemo(() => `velum-list-${Math.random().toString(36).slice(2)}`, []);

  return (
    <Root className={props.className}>
      {editableLines.map((line, index) => (
        <Row key={`${line}-${index}`}>
          <TextInput
            value={line}
            list={props.options?.length ? datalistId : undefined}
            style={{
              borderTopRightRadius: 0,
              borderBottomRightRadius: 0,
            }}
            onChange={(event) => {
              const copy = [...editableLines];
              copy[index] = event.target.value;
              props.onChange(copy.filter(Boolean).join(delimiter));
            }}
          />
          <ActionCell>
            <InlineButton
              type="button"
              onClick={() => {
                const copy = editableLines.filter((_, idx) => idx !== index);
                props.onChange(copy.join(delimiter));
              }}
              disabled={editableLines.length <= 1}
            >
              Remove
            </InlineButton>
          </ActionCell>
        </Row>
      ))}
      {props.options?.length ? (
        <datalist id={datalistId}>
          {props.options.map((option) => (
            <option key={option} value={option} />
          ))}
        </datalist>
      ) : null}
      <InlineButton type="button" onClick={() => props.onChange([...editableLines, ""].join(delimiter))}>
        Add Row
      </InlineButton>
    </Root>
  );
}
