import type { ChangeEvent } from "react";
import { useMemo } from "react";

import { styled } from "../styletron";

import { TextInput } from "./Inputs";

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
  verbal: boolean;
  somatic: boolean;
  material: boolean;
  materialText: string;
  extras: string[];
}

function parseComponents(value: string): ParsedComponents {
  const tokens = parseDelimitedList(value);
  let verbal = false;
  let somatic = false;
  let material = false;
  let materialText = "";
  const extras: string[] = [];

  for (const token of tokens) {
    const normalized = normalizeKey(token);
    if (normalized === "v" || normalized === "verbal") {
      verbal = true;
      continue;
    }
    if (normalized === "s" || normalized === "somatic") {
      somatic = true;
      continue;
    }
    if (normalized === "m" || normalized === "material" || normalized.startsWith("m")) {
      material = true;
      const match = token.match(/m(?:aterial)?\s*(?:\((.*)\)|:\s*(.*)|-\s*(.*))?/i);
      materialText = (match?.[1] || match?.[2] || match?.[3] || materialText).trim();
      continue;
    }
    extras.push(token);
  }

  return {
    verbal,
    somatic,
    material,
    materialText,
    extras: dedupePreserveCase(extras),
  };
}

function serializeComponents(components: ParsedComponents): string {
  const parts: string[] = [];

  if (components.verbal) {
    parts.push("V");
  }
  if (components.somatic) {
    parts.push("S");
  }
  if (components.material) {
    const note = components.materialText.trim();
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
  display: "flex",
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
  display: "grid",
  gridTemplateColumns: "auto minmax(0, 1fr)",
  alignItems: "stretch",
});

function segmentEdge(index: number, total: number): "first" | "middle" | "last" | "single" {
  if (total === 1) {
    return "single";
  }
  if (index === 0) {
    return "first";
  }
  if (index === total - 1) {
    return "last";
  }
  return "middle";
}

export function ComponentsField(props: ComponentsFieldProps) {
  const parsed = useMemo(() => parseComponents(props.value || ""), [props.value]);

  const update = (patch: Partial<ParsedComponents>) => {
    props.onChange(serializeComponents({ ...parsed, ...patch }));
  };

  const onToggle = (field: "verbal" | "somatic" | "material") => (event: ChangeEvent<HTMLInputElement>) => {
    update({ [field]: event.target.checked });
  };

  return (
    <Root className={props.className}>
      <SegmentRow>
        {[
          { label: "V", checked: parsed.verbal, onChange: onToggle("verbal") },
          { label: "S", checked: parsed.somatic, onChange: onToggle("somatic") },
        ].map((item, index, items) => (
          <SegmentLabel key={item.label} $checked={item.checked} $edge={segmentEdge(index, items.length)}>
            {item.label}
            <HiddenCheckbox type="checkbox" checked={item.checked} onChange={item.onChange} />
          </SegmentLabel>
        ))}
      </SegmentRow>
      <MaterialRow>
        <SegmentLabel $checked={parsed.material} $edge="first">
          M
          <HiddenCheckbox type="checkbox" checked={parsed.material} onChange={onToggle("material")} />
        </SegmentLabel>
        <TextInput
          style={{
            marginLeft: "-1px",
            borderTopLeftRadius: 0,
            borderBottomLeftRadius: 0,
            background: !parsed.material ? "rgba(222, 212, 195, 0.55)" : undefined,
            color: !parsed.material ? "var(--velum-color-ink-soft)" : undefined,
          }}
          value={parsed.materialText}
          disabled={!parsed.material}
          placeholder="Material details"
          onChange={(event: ChangeEvent<HTMLInputElement>) => update({ materialText: event.target.value })}
        />
      </MaterialRow>
    </Root>
  );
}
