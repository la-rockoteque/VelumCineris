import { useMemo, useState } from "react";

import { styled } from "../../styletron";

import { Checkbox } from "../Checkbox/Checkbox";
import { useControllableState } from "../_internal/useControllableState";

function normalizeKey(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, "");
}

function parseDelimitedList(value: string): string[] {
  return value
    .split(/[,\n;]+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function dedupePreserveCase(values: string[]): string[] {
  const seen = new Set<string>();
  const out: string[] = [];

  for (const value of values) {
    const normalized = normalizeKey(value);
    if (seen.has(normalized)) {
      continue;
    }
    seen.add(normalized);
    out.push(value);
  }

  return out;
}

export interface MultiSelectProps {
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

const Trigger = styled("button", {
  width: "100%",
  minHeight: "42px",
  border: "1px solid var(--velum-color-border)",
  borderRadius: "var(--velum-radius-sm)",
  background: "rgba(255, 255, 255, 0.72)",
  color: "var(--velum-color-ink)",
  display: "grid",
  gridTemplateColumns: "minmax(0, 1fr) 44px",
  padding: 0,
  cursor: "pointer",
  textAlign: "left",
  overflow: "hidden",
  transition:
    "border-color var(--velum-motion-quick) var(--velum-motion-ease-standard), box-shadow var(--velum-motion-quick) var(--velum-motion-ease-standard)",
  ":focus-visible": {
    outline: "none",
    boxShadow: "var(--velum-focus-ring)",
  },
});

const TriggerContent = styled("span", {
  display: "flex",
  alignItems: "center",
  gap: "6px",
  flexWrap: "wrap",
  padding: "8px 10px",
  minWidth: 0,
});

const TriggerCaret = styled("span", {
  display: "grid",
  placeItems: "center",
  borderLeft: "1px solid var(--velum-color-border)",
  background: "rgba(241, 231, 214, 0.88)",
  color: "var(--velum-color-ink-soft)",
  fontSize: "var(--velum-font-size-sm)",
  fontWeight: 700,
});

const Pill = styled("span", {
  display: "inline-flex",
  alignItems: "center",
  maxWidth: "100%",
  padding: "2px 8px",
  borderRadius: "999px",
  border: "1px solid rgba(66, 48, 30, 0.12)",
  background: "rgba(241, 231, 214, 0.9)",
  color: "var(--velum-color-ink)",
  fontSize: "var(--velum-font-size-xs)",
  lineHeight: 1.3,
});

const Placeholder = styled("span", {
  color: "var(--velum-color-ink-soft)",
  fontSize: "var(--velum-font-size-sm)",
  lineHeight: 1.4,
});

const Dropdown = styled("div", {
  position: "absolute",
  zIndex: 40,
  left: 0,
  right: 0,
  top: "calc(100% + 4px)",
  border: "1px solid var(--velum-color-border)",
  borderRadius: "var(--velum-radius-sm)",
  background: "#fffaf1",
  boxShadow: "0 12px 24px rgba(0, 0, 0, 0.12)",
  maxHeight: "240px",
  overflow: "auto",
  padding: "8px",
  display: "grid",
  gap: "6px",
});

const OptionRow = styled("div", {
  padding: "6px 8px",
  borderRadius: "8px",
  ":hover": {
    background: "rgba(234, 220, 195, 0.5)",
  },
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
  const [rawValue, setRawValue] = useControllableState(value, value);

  const selected = parseDelimitedList(rawValue);
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
    setRawValue(next);
    onChange(next);
  };

  return (
    <Root className={className}>
      <Trigger
        type="button"
        aria-expanded={open}
        onClick={() => setOpen((current) => !current)}
        style={
          open
            ? {
                borderColor: "rgba(155, 77, 31, 0.5)",
                boxShadow: "var(--velum-focus-ring)",
              }
            : undefined
        }
      >
        <TriggerContent>
          {pills.length > 0 ? pills.map((pill) => <Pill key={pill}>{pill}</Pill>) : <Placeholder>{placeholder}</Placeholder>}
        </TriggerContent>
        <TriggerCaret>{open ? "▴" : "▾"}</TriggerCaret>
      </Trigger>
      {open ? (
        <Dropdown>
          {mergedOptions.map((option) => (
            <OptionRow key={option}>
              <Checkbox label={option} checked={selectedSet.has(normalizeKey(option))} onChange={() => toggle(option)} />
            </OptionRow>
          ))}
        </Dropdown>
      ) : null}
    </Root>
  );
}
