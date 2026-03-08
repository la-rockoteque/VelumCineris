import { useMemo, useState } from "react";

import { dedupePreserveCase, normalizeKey, parseDelimitedList } from "shared/utils/text";

interface MultiSelectProps {
  value: string;
  options: string[];
  delimiter?: string;
  onChange: (next: string) => void;
  placeholder?: string;
}

export function MultiSelect({
  value,
  options,
  delimiter = ", ",
  onChange,
  placeholder = "Select options",
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
    <div className={`multi-select ${open ? "is-open" : ""}`}>
      <button type="button" className="multi-select-display" onClick={() => setOpen((current) => !current)}>
        <span className="multi-select-pills">
          {pills.length > 0 ? pills.map((pill) => <span key={pill} className="multi-select-pill">{pill}</span>) : <span className="multi-select-placeholder">{placeholder}</span>}
        </span>
        <span className="multi-select-caret">▾</span>
      </button>
      {open && (
        <div className="multi-select-dropdown">
          {mergedOptions.map((option) => (
            <label key={option} className="multi-select-option">
              <input type="checkbox" checked={selectedSet.has(normalizeKey(option))} onChange={() => toggle(option)} />
              <span>{option}</span>
            </label>
          ))}
        </div>
      )}
    </div>
  );
}
