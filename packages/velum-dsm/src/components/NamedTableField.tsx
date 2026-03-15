import { useMemo } from "react";

import { styled } from "../styletron";

import { InlineButton } from "./Buttons";
import { TextArea, TextInput } from "./Inputs";

function parseNamedEntries(rawValue: string): Array<{ key: string; value: string }> {
  const parts = rawValue
    .split(/[;\n]+/)
    .map((item) => item.trim())
    .filter(Boolean);

  if (!parts.length) {
    return [{ key: "", value: "" }];
  }

  return parts.map((part) => {
    const idx = part.indexOf("::");
    if (idx === -1) {
      return { key: "", value: part };
    }

    return {
      key: part.slice(0, idx).trim(),
      value: part.slice(idx + 2).trim(),
    };
  });
}

function serializeNamedEntries(items: Array<{ key: string; value: string }>): string {
  return items
    .map((item) => ({ key: item.key.trim(), value: item.value.trim() }))
    .filter((item) => item.key || item.value)
    .map((item) => (item.key ? `${item.key}:: ${item.value}` : item.value))
    .join("; ");
}

export interface NamedTableFieldProps {
  value: string;
  keyLabel: string;
  valueLabel: string;
  onChange: (next: string) => void;
  className?: string;
}

const Root = styled("div", {
  display: "grid",
  gap: "var(--velum-space-2)",
});

const Header = styled("div", {
  display: "grid",
  gridTemplateColumns: "56px minmax(180px, 0.7fr) minmax(260px, 1fr) 92px",
  gap: 0,
});

const HeaderCell = styled("div", {
  padding: "6px 10px",
  border: "1px solid rgba(66, 48, 30, 0.12)",
  background: "rgba(241, 231, 214, 0.88)",
  color: "var(--velum-color-ink-soft)",
  fontSize: "var(--velum-font-size-xs)",
  fontWeight: 700,
  textTransform: "uppercase",
  letterSpacing: "0.04em",
});

const Rows = styled("div", {
  display: "grid",
  gap: "8px",
});

const Row = styled("div", {
  display: "grid",
  gridTemplateColumns: "56px minmax(180px, 0.7fr) minmax(260px, 1fr) 92px",
  gap: 0,
  alignItems: "stretch",
});

const IndexCell = styled("div", {
  display: "grid",
  placeItems: "center",
  border: "1px solid var(--velum-color-border)",
  borderTopLeftRadius: "var(--velum-radius-sm)",
  borderBottomLeftRadius: "var(--velum-radius-sm)",
  background: "rgba(241, 231, 214, 0.72)",
  color: "var(--velum-color-ink-soft)",
  fontSize: "var(--velum-font-size-sm)",
  fontWeight: 700,
});

const ActionCell = styled("div", {
  display: "grid",
  placeItems: "center",
  border: "1px solid var(--velum-color-border)",
  borderLeft: "none",
  borderTopRightRadius: "var(--velum-radius-sm)",
  borderBottomRightRadius: "var(--velum-radius-sm)",
  background: "rgba(255, 255, 255, 0.68)",
  padding: "6px",
});

export function NamedTableField(props: NamedTableFieldProps) {
  const entries = useMemo(() => parseNamedEntries(props.value), [props.value]);

  const updateEntry = (index: number, patch: Partial<{ key: string; value: string }>) => {
    const copy = [...entries];
    const base = copy[index] || { key: "", value: "" };
    copy[index] = { ...base, ...patch };
    props.onChange(serializeNamedEntries(copy));
  };

  const addRow = () => {
    props.onChange(serializeNamedEntries([...entries, { key: "", value: "" }]));
  };

  const removeRow = (index: number) => {
    const copy = entries.filter((_, idx) => idx !== index);
    props.onChange(serializeNamedEntries(copy.length ? copy : [{ key: "", value: "" }]));
  };

  return (
    <Root className={props.className}>
      <Header>
        <HeaderCell>#</HeaderCell>
        <HeaderCell style={{ borderLeft: "none" }}>{props.keyLabel}</HeaderCell>
        <HeaderCell style={{ borderLeft: "none" }}>{props.valueLabel}</HeaderCell>
        <HeaderCell style={{ borderLeft: "none" }}>Action</HeaderCell>
      </Header>
      <Rows>
        {entries.map((entry, index) => (
          <Row key={`${entry.key}-${index}`}>
            <IndexCell>{index + 1}</IndexCell>
            <TextInput
              value={entry.key}
              placeholder={props.keyLabel}
              style={{
                borderLeft: "none",
                borderRadius: 0,
              }}
              onChange={(event) => updateEntry(index, { key: event.target.value })}
            />
            <TextArea
              rows={2}
              value={entry.value}
              placeholder={props.valueLabel}
              style={{
                minHeight: "unset",
                resize: "vertical",
                borderLeft: "none",
                borderRadius: 0,
              }}
              onChange={(event) => updateEntry(index, { value: event.target.value })}
            />
            <ActionCell>
              <InlineButton type="button" onClick={() => removeRow(index)} disabled={entries.length <= 1}>
                Remove
              </InlineButton>
            </ActionCell>
          </Row>
        ))}
      </Rows>
      <InlineButton type="button" onClick={addRow}>
        Add Row
      </InlineButton>
    </Root>
  );
}
