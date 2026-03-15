import type { ChangeEvent } from "react";
import { useMemo } from "react";

import { styled } from "../../styletron";

import { TextInput } from "../TextInput/TextInput";
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

interface ParsedComponents {
  verbal: { active: boolean; note: string };
  somatic: { active: boolean; note: string };
  material: { active: boolean; note: string };
  extras: string[];
}

function parseComponents(value: string): ParsedComponents {
  const tokens = parseDelimitedList(value);
  let verbal = { active: false, note: "" };
  let somatic = { active: false, note: "" };
  let material = { active: false, note: "" };
  const extras: string[] = [];

  for (const token of tokens) {
    const normalized = normalizeKey(token);
    const match = token.match(/^(v(?:erbal)?|s(?:omatic)?|m(?:aterial)?)\s*(?:\((.*)\)|:\s*(.*)|-\s*(.*))?$/i);
    const note = (match?.[2] || match?.[3] || match?.[4] || "").trim();

    if (normalized === "v" || normalized === "verbal" || match?.[1]?.toLowerCase().startsWith("v")) {
      verbal = { active: true, note };
      continue;
    }
    if (normalized === "s" || normalized === "somatic" || match?.[1]?.toLowerCase().startsWith("s")) {
      somatic = { active: true, note };
      continue;
    }
    if (normalized === "m" || normalized === "material" || normalized.startsWith("m")) {
      material = { active: true, note };
      continue;
    }
    extras.push(token);
  }

  return {
    verbal,
    somatic,
    material,
    extras: dedupePreserveCase(extras),
  };
}

function serializeComponents(components: ParsedComponents): string {
  const parts: string[] = [];

  if (components.verbal.active) {
    parts.push(components.verbal.note.trim() ? `V (${components.verbal.note.trim()})` : "V");
  }
  if (components.somatic.active) {
    parts.push(components.somatic.note.trim() ? `S (${components.somatic.note.trim()})` : "S");
  }
  if (components.material.active) {
    const note = components.material.note.trim();
    parts.push(note ? `M (${note})` : "M");
  }

  return [...parts, ...components.extras].join(", ");
}

export interface ComponentsFieldProps {
  value: string;
  onChange: (next: string) => void;
  className?: string;
}

const Root = styled("div", {
  display: "grid",
  gap: "var(--velum-space-2)",
});

const SegmentRow = styled("div", {
  display: "grid",
  gridTemplateColumns: "54px minmax(0, 1fr)",
  alignItems: "stretch",
});

const SegmentLabel = styled(
  "label",
  ({
    $checked,
    $edge,
  }: {
    $checked: boolean;
    $edge: "first" | "middle" | "last" | "single";
  }) => ({
    position: "relative",
    display: "inline-flex",
    alignItems: "center",
    justifyContent: "center",
    minWidth: "54px",
    padding: "10px 14px",
    border: "1px solid var(--velum-color-border)",
    marginLeft: $edge === "first" || $edge === "single" ? 0 : "-1px",
    borderTopLeftRadius: $edge === "first" || $edge === "single" ? "var(--velum-radius-sm)" : "0",
    borderBottomLeftRadius: $edge === "first" || $edge === "single" ? "var(--velum-radius-sm)" : "0",
    borderTopRightRadius: $edge === "last" || $edge === "single" ? "var(--velum-radius-sm)" : "0",
    borderBottomRightRadius: $edge === "last" || $edge === "single" ? "var(--velum-radius-sm)" : "0",
    background: $checked ? "rgba(241, 225, 190, 0.95)" : "rgba(255, 255, 255, 0.72)",
    color: $checked ? "var(--velum-color-ink)" : "var(--velum-color-ink-soft)",
    fontSize: "var(--velum-font-size-sm)",
    fontWeight: 700,
    cursor: "pointer",
    transition:
      "border-color var(--velum-motion-quick) var(--velum-motion-ease-standard), background var(--velum-motion-quick) var(--velum-motion-ease-standard), color var(--velum-motion-quick) var(--velum-motion-ease-standard), box-shadow var(--velum-motion-quick) var(--velum-motion-ease-standard)",
    ":hover": {
      borderColor: "rgba(155, 77, 31, 0.5)",
      color: "var(--velum-color-ink)",
    },
    ":focus-within": {
      zIndex: 1,
      boxShadow: "var(--velum-focus-ring)",
    },
  }),
);

const HiddenCheckbox = styled("input", {
  position: "absolute",
  inset: 0,
  opacity: 0,
  cursor: "pointer",
});

const MaterialRow = styled("div", {
  display: "contents",
});

export function ComponentsField(props: ComponentsFieldProps) {
  const [rawValue, setRawValue] = useControllableState(props.value, props.value);
  const parsed = useMemo(() => parseComponents(rawValue || ""), [rawValue]);

  const update = (patch: Partial<ParsedComponents>) => {
    const next = serializeComponents({ ...parsed, ...patch });
    setRawValue(next);
    props.onChange(next);
  };

  const onToggle = (field: "verbal" | "somatic" | "material") => (event: ChangeEvent<HTMLInputElement>) => {
    update({
      [field]: {
        ...parsed[field],
        active: event.target.checked,
      },
    });
  };

  const rows: Array<{ key: "verbal" | "somatic" | "material"; label: "V" | "S" | "M"; placeholder: string }> = [
    { key: "verbal", label: "V", placeholder: "Verbal details" },
    { key: "somatic", label: "S", placeholder: "Somatic details" },
    { key: "material", label: "M", placeholder: "Material details" },
  ];

  return (
    <Root className={props.className}>
      {rows.map((row) => (
        <SegmentRow key={row.key}>
          <SegmentLabel $checked={parsed[row.key].active} $edge="single">
            {row.label}
            <HiddenCheckbox
              aria-label={row.label}
              type="checkbox"
              checked={parsed[row.key].active}
              onChange={onToggle(row.key)}
            />
          </SegmentLabel>
          <MaterialRow>
            <TextInput
              style={{
                marginLeft: "-1px",
                borderTopLeftRadius: 0,
                borderBottomLeftRadius: 0,
              }}
              value={parsed[row.key].note}
              disabled={!parsed[row.key].active}
              placeholder={row.placeholder}
              onChange={(event: ChangeEvent<HTMLInputElement>) =>
                update({
                  [row.key]: {
                    ...parsed[row.key],
                    note: event.target.value,
                  },
                })
              }
            />
          </MaterialRow>
        </SegmentRow>
      ))}
    </Root>
  );
}
