import { useMemo, useState } from "react";
import { styled } from "app/styletron";

import { dedupePreserveCase, normalizeKey, parseDelimitedList } from "shared/utils/text";

interface MultiSelectProps {
  value: string;
  options: string[];
  delimiter?: string;
  onChange: (next: string) => void;
  placeholder?: string;
  className?: string;
}

const Root = styled("div", {
  position: "relative",
});

const DisplayButton = styled("button", {
  width: "100%",
  minHeight: "36px",
  border: "1px solid rgba(66, 48, 30, 0.18)",
  borderRadius: "8px",
  background: "#fffaf1",
  color: "#4e4335",
  display: "flex",
  alignItems: "flex-start",
  justifyContent: "space-between",
  gap: "8px",
  padding: "6px 8px",
  cursor: "pointer",
  textAlign: "left",
});

const Pills = styled("span", {
  display: "flex",
  flexWrap: "wrap",
  gap: "6px",
  flex: 1,
});

const Pill = styled("span", {
  display: "inline-flex",
  alignItems: "center",
  maxWidth: "100%",
  padding: "2px 8px",
  borderRadius: "999px",
  border: "1px solid rgba(66, 48, 30, 0.16)",
  background: "rgba(241, 231, 214, 0.9)",
  color: "#5d503f",
  fontSize: "0.72rem",
  lineHeight: 1.2,
});

const Placeholder = styled("span", {
  color: "#8c7f6b",
  fontSize: "0.76rem",
  lineHeight: 1.3,
});

const Caret = styled("span", {
  color: "#6f634f",
  fontSize: "0.8rem",
  lineHeight: 1.2,
  paddingTop: "3px",
});

const Dropdown = styled("div", {
  position: "absolute",
  zIndex: 40,
  left: 0,
  right: 0,
  top: "calc(100% + 4px)",
  border: "1px solid rgba(66, 48, 30, 0.2)",
  borderRadius: "8px",
  background: "#fffaf1",
  boxShadow: "0 12px 24px rgba(0, 0, 0, 0.12)",
  maxHeight: "220px",
  overflow: "auto",
  padding: "6px",
  display: "grid",
  gap: "3px",
});

const OptionLabel = styled("label", {
  display: "flex",
  alignItems: "center",
  gap: "8px",
  padding: "4px 6px",
  borderRadius: "6px",
  color: "#4f4436",
  fontSize: "0.8rem",
  ":hover": {
    background: "rgba(234, 220, 195, 0.65)",
  },
});

const Checkbox = styled("input", {
  width: "16px",
  height: "16px",
  margin: 0,
});

export function MultiSelect({
  value,
  options,
  delimiter = ", ",
  onChange,
  placeholder = "Select options",
  className,
}: MultiSelectProps) {
  const [open, setOpen] = useState(false);

  const selected = parseDelimitedList(value);
  const mergedOptions = useMemo(() => dedupePreserveCase([...options, ...selected]), [options, selected]);
  const selectedSet = new Set(selected.map((item) => normalizeKey(item)));

  const pills = mergedOptions.filter((option) => selectedSet.has(normalizeKey(option)));

  const toggle = (option: string) => {
    const key = normalizeKey(option);
    const current = new Set(pills.map((item) => normalizeKey(item)));
    if (current.has(key)) {
      current.delete(key);
    } else {
      current.add(key);
    }

    const next = mergedOptions.filter((candidate) => current.has(normalizeKey(candidate))).join(delimiter);
    onChange(next);
  };

  return (
    <Root className={className}>
      <DisplayButton
        type="button"
        onClick={() => setOpen((current) => !current)}
        style={
          open
            ? {
                borderColor: "rgba(160, 110, 54, 0.55)",
                boxShadow: "0 0 0 2px rgba(204, 165, 102, 0.2)",
              }
            : undefined
        }
      >
        <Pills>
          {pills.length > 0 ? pills.map((pill) => <Pill key={pill}>{pill}</Pill>) : <Placeholder>{placeholder}</Placeholder>}
        </Pills>
        <Caret>▾</Caret>
      </DisplayButton>
      {open && (
        <Dropdown>
          {mergedOptions.map((option) => (
            <OptionLabel key={option}>
              <Checkbox type="checkbox" checked={selectedSet.has(normalizeKey(option))} onChange={() => toggle(option)} />
              <span>{option}</span>
            </OptionLabel>
          ))}
        </Dropdown>
      )}
    </Root>
  );
}
