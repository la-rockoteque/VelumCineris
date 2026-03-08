import { useMemo } from "react";

import { MultiSelect } from "components/MultiSelect";
import { dedupePreserveCase, normalizeKey, parseDelimitedList, safeNumber, toBoolean } from "shared/utils/text";

function textValue(value: unknown): string {
  if (value == null) {
    return "";
  }
  return String(value);
}

export interface TextFieldProps {
  value: string;
  onChange: (next: string) => void;
  placeholder?: string;
  readOnly?: boolean;
  disabled?: boolean;
}

export function TextField(props: TextFieldProps) {
  return (
    <input
      value={props.value}
      onChange={(event) => props.onChange(event.target.value)}
      placeholder={props.placeholder}
      readOnly={props.readOnly}
      disabled={props.disabled}
    />
  );
}

export interface NumberFieldProps {
  value: string;
  onChange: (next: string) => void;
  min?: number;
  max?: number;
  step?: string;
  placeholder?: string;
}

export function NumberField(props: NumberFieldProps) {
  return (
    <input
      type="number"
      value={props.value}
      min={props.min}
      max={props.max}
      step={props.step ?? "any"}
      placeholder={props.placeholder}
      onChange={(event) => props.onChange(event.target.value)}
    />
  );
}

export interface LongTextFieldProps {
  value: string;
  onChange: (next: string) => void;
  rows?: number;
  placeholder?: string;
}

export function LongTextField(props: LongTextFieldProps) {
  return <textarea rows={props.rows ?? 5} value={props.value} placeholder={props.placeholder} onChange={(event) => props.onChange(event.target.value)} />;
}

export interface SelectFieldProps {
  value: string;
  options: string[];
  onChange: (next: string) => void;
}

export function SelectField(props: SelectFieldProps) {
  return (
    <select value={props.value} onChange={(event) => props.onChange(event.target.value)}>
      <option value="" />
      {props.options.map((option) => (
        <option key={option} value={option}>
          {option}
        </option>
      ))}
    </select>
  );
}

export interface MultiSelectFieldProps {
  value: string;
  options: string[];
  onChange: (next: string) => void;
  placeholder?: string;
}

export function MultiSelectField(props: MultiSelectFieldProps) {
  return <MultiSelect value={props.value} options={props.options} onChange={props.onChange} placeholder={props.placeholder} />;
}

export interface BooleanFieldProps {
  value: unknown;
  onChange: (next: string) => void;
  trueLabel?: string;
  falseLabel?: string;
}

export function BooleanField(props: BooleanFieldProps) {
  const checked = toBoolean(props.value);
  const trueLabel = props.trueLabel ?? "True";
  const falseLabel = props.falseLabel ?? "False";

  return (
    <label className="check-wrap">
      <input type="checkbox" checked={checked} onChange={(event) => props.onChange(event.target.checked ? "True" : "False")} />
      <span>{checked ? trueLabel : falseLabel}</span>
    </label>
  );
}

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
}

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
    <div className="list-table-editor">
      <table className="list-table">
        <thead>
          <tr>
            <th>#</th>
            <th>{props.keyLabel}</th>
            <th>{props.valueLabel}</th>
            <th />
          </tr>
        </thead>
        <tbody>
          {entries.map((entry, index) => (
            <tr key={`${entry.key}-${index}`}>
              <td>{index + 1}</td>
              <td>
                <input value={entry.key} onChange={(event) => updateEntry(index, { key: event.target.value })} />
              </td>
              <td>
                <textarea rows={2} value={entry.value} onChange={(event) => updateEntry(index, { value: event.target.value })} />
              </td>
              <td>
                <button type="button" className="btn btn-inline" onClick={() => removeRow(index)} disabled={entries.length <= 1}>
                  Remove
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button type="button" className="btn btn-inline" onClick={addRow}>
        Add Row
      </button>
    </div>
  );
}

export interface DelimitedListFieldProps {
  value: string;
  onChange: (next: string) => void;
  options?: string[];
  delimiter?: string;
}

export function DelimitedListField(props: DelimitedListFieldProps) {
  const delimiter = props.delimiter ?? ", ";
  const lines = parseDelimitedList(props.value);
  const editableLines = lines.length ? lines : [""];
  const datalistId = useMemo(() => `list-${Math.random().toString(36).slice(2)}`, []);

  return (
    <div className="pipe-entry-editor">
      {editableLines.map((line, index) => (
        <div key={`${line}-${index}`} className="line-item">
          <input
            value={line}
            onChange={(event) => {
              const copy = [...editableLines];
              copy[index] = event.target.value;
              props.onChange(copy.filter(Boolean).join(delimiter));
            }}
            list={props.options?.length ? datalistId : undefined}
          />
          <button
            type="button"
            className="btn btn-inline"
            onClick={() => {
              const copy = editableLines.filter((_, idx) => idx !== index);
              props.onChange(copy.join(delimiter));
            }}
            disabled={editableLines.length <= 1}
          >
            Remove
          </button>
        </div>
      ))}
      {!!props.options?.length && (
        <datalist id={datalistId}>
          {props.options.map((option) => (
            <option key={option} value={option} />
          ))}
        </datalist>
      )}
      <button type="button" className="btn btn-inline" onClick={() => props.onChange([...editableLines, ""].join(delimiter))}>
        Add Row
      </button>
    </div>
  );
}

interface ParsedHitDice {
  count: number;
  diceType: number;
  bonus: number;
}

function parseHitDice(rawValue: string): ParsedHitDice {
  const match = rawValue.match(/(\d+)\s*d\s*(\d+)\s*([+-]\s*\d+)?/i);
  if (!match) {
    return { count: 0, diceType: 0, bonus: 0 };
  }
  return {
    count: Number(match[1] || 0),
    diceType: Number(match[2] || 0),
    bonus: Number(String(match[3] || "0").replace(/\s+/g, "")) || 0,
  };
}

function stringifyHitDice(input: ParsedHitDice): string {
  if (!Number.isFinite(input.count) || input.count <= 0 || !Number.isFinite(input.diceType) || input.diceType <= 0) {
    return "";
  }
  const plus = Number.isFinite(input.bonus) && input.bonus !== 0 ? (input.bonus > 0 ? `+${input.bonus}` : `${input.bonus}`) : "";
  return `${Math.floor(input.count)}d${Math.floor(input.diceType)}${plus}`;
}

export interface HitDiceFieldProps {
  value: string;
  onChange: (next: string) => void;
}

export function HitDiceField(props: HitDiceFieldProps) {
  const parsed = useMemo(() => parseHitDice(props.value), [props.value]);

  return (
    <div className="spell-measure-inline">
      <NumberField
        value={parsed.count ? String(parsed.count) : ""}
        placeholder="Count"
        min={0}
        step="1"
        onChange={(next) => props.onChange(stringifyHitDice({ ...parsed, count: safeNumber(next, 0) }))}
      />
      <NumberField
        value={parsed.diceType ? String(parsed.diceType) : ""}
        placeholder="Dice type"
        min={0}
        step="1"
        onChange={(next) => props.onChange(stringifyHitDice({ ...parsed, diceType: safeNumber(next, 0) }))}
      />
      <NumberField
        value={parsed.bonus ? String(parsed.bonus) : ""}
        placeholder="Bonus"
        step="1"
        onChange={(next) => props.onChange(stringifyHitDice({ ...parsed, bonus: safeNumber(next, 0) }))}
      />
    </div>
  );
}

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
}

export function StatWithModifierField(props: StatWithModifierFieldProps) {
  return (
    <div className="monster-ability-editor">
      <NumberField value={props.value} step="1" onChange={props.onChange} />
      <span className="monster-ability-mod">{formatModifier(props.value)}</span>
    </div>
  );
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
    const trimmed = token.trim();
    const normalized = normalizeKey(trimmed);
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
      const match = trimmed.match(/m(?:aterial)?\s*(?:\((.*)\)|:\s*(.*)|-\s*(.*))?/i);
      materialText = (match?.[1] || match?.[2] || match?.[3] || materialText).trim();
      continue;
    }
    extras.push(trimmed);
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
}

export function ComponentsField(props: ComponentsFieldProps) {
  const parsed = useMemo(() => parseComponents(textValue(props.value)), [props.value]);

  const update = (patch: Partial<ParsedComponents>) => {
    props.onChange(serializeComponents({ ...parsed, ...patch }));
  };

  return (
    <div className="spell-components-editor components-field">
      <label className="components-option">
        <input type="checkbox" checked={parsed.verbal} onChange={(event) => update({ verbal: event.target.checked })} />
        <span>V</span>
      </label>
      <label className="components-option">
        <input type="checkbox" checked={parsed.somatic} onChange={(event) => update({ somatic: event.target.checked })} />
        <span>S</span>
      </label>
      <div className="components-option-row">
        <label className="components-option">
          <input type="checkbox" checked={parsed.material} onChange={(event) => update({ material: event.target.checked })} />
          <span>M</span>
        </label>
        <input
          className={`components-note ${!parsed.material ? "is-disabled" : ""}`.trim()}
          placeholder="Material details"
          value={parsed.materialText}
          disabled={!parsed.material}
          onChange={(event) => update({ materialText: event.target.value })}
        />
      </div>
    </div>
  );
}
