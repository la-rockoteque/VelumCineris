import { useEffect, useMemo, useState } from "react";

import type { SelectedRow, SpreadsheetRowsResponse } from "shared/types/api";
import { pickItemName } from "shared/utils/fields";
import { normalizeKey } from "shared/utils/text";

interface StyleTemplateInfo {
  name: string;
  label: string;
}

interface StylePaletteToken {
  token: string;
  value: string;
}

interface FormatterTabProps {
  loading: boolean;
  source: string;
  sheets: string[];
  selected: SelectedRow | null;
  settings: Record<string, unknown>;
  output: string;
  onSelectRow: (rowNumber: number, sheet: string) => Promise<void>;
  onLoadRows: (sheet: string) => Promise<SpreadsheetRowsResponse | null>;
  onRunPreview: (payload: Record<string, unknown>) => Promise<Record<string, unknown> | null>;
  onLoadTemplates: () => Promise<{ templates?: StyleTemplateInfo[] } | null>;
  onLoadTemplate: (name: string) => Promise<{ css?: string; palette?: StylePaletteToken[] } | null>;
  onSaveSettingsPatch: (patch: Record<string, unknown>) => Promise<void>;
}

interface LibraryEntry {
  provider: string;
  title: string;
  source: string;
}

function dedupeFormatterLibrary(entries: LibraryEntry[]): LibraryEntry[] {
  const seen = new Set<string>();
  const out: LibraryEntry[] = [];
  for (const entry of entries) {
    const marker = `${entry.provider}::${entry.title}`;
    if (seen.has(marker)) {
      continue;
    }
    seen.add(marker);
    out.push(entry);
  }
  return out;
}

function toHexColor(value: string): string {
  const candidate = value.trim();
  if (/^#[0-9a-fA-F]{6}$/.test(candidate)) {
    return candidate;
  }
  return "#c68a5e";
}

function parseFormatterSettings(settings: Record<string, unknown>): { style_template: string; style_css: string } {
  const formatter = (settings.formatter as Record<string, unknown> | undefined) || {};
  return {
    style_template: String(formatter.style_template || ""),
    style_css: String(formatter.style_css || ""),
  };
}

function applyPaletteTokenChange(css: string, token: string, nextColor: string): string {
  const escaped = token.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const pattern = new RegExp(`(${escaped}\\s*:\\s*)([^;]+)(;)`, "g");
  const replaced = css.replace(pattern, `$1${nextColor}$3`);
  if (replaced !== css) {
    return replaced;
  }
  return `${css}\n:root { ${token}: ${nextColor}; }\n`;
}

export function FormatterTab(props: FormatterTabProps) {
  const [target, setTarget] = useState("homebrewery");
  const [itemType, setItemType] = useState("");
  const [itemRow, setItemRow] = useState(0);
  const [folderHint, setFolderHint] = useState("");
  const [rowsBySheet, setRowsBySheet] = useState<Record<string, Record<string, unknown>[]>>({});
  const [templates, setTemplates] = useState<StyleTemplateInfo[]>([]);
  const [template, setTemplate] = useState("");
  const [css, setCss] = useState("");
  const [palette, setPalette] = useState<StylePaletteToken[]>([]);
  const [message, setMessage] = useState("Select an item and run formatter preview.");

  useEffect(() => {
    if (!props.sheets.length) {
      setItemType("");
      return;
    }
    setItemType((current) => (current && props.sheets.includes(current) ? current : props.selected?.sheet || props.sheets[0] || ""));
  }, [props.selected?.sheet, props.sheets]);

  useEffect(() => {
    if (!itemType) {
      return;
    }
    if (rowsBySheet[itemType]?.length) {
      return;
    }
    void (async () => {
      const payload = await props.onLoadRows(itemType);
      if (!payload) {
        return;
      }
      setRowsBySheet((current) => ({ ...current, [itemType]: payload.rows || [] }));
    })();
  }, [itemType, props.onLoadRows, rowsBySheet]);

  useEffect(() => {
    void (async () => {
      const payload = await props.onLoadTemplates();
      const nextTemplates = payload?.templates || [];
      setTemplates(nextTemplates);
      const fromSettings = parseFormatterSettings(props.settings).style_template;
      const names = nextTemplates.map((item) => item.name);
      const nextTemplate = names.includes(fromSettings) ? fromSettings : nextTemplates[0]?.name || "";
      setTemplate(nextTemplate);
      if (nextTemplate) {
        const detail = await props.onLoadTemplate(nextTemplate);
        setCss(parseFormatterSettings(props.settings).style_css || String(detail?.css || ""));
        setPalette(detail?.palette || []);
      } else {
        setCss(parseFormatterSettings(props.settings).style_css || "");
        setPalette([]);
      }
    })();
  }, [props.onLoadTemplate, props.onLoadTemplates, props.settings]);

  useEffect(() => {
    if (!props.selected) {
      return;
    }
    setItemType(props.selected.sheet);
    setItemRow(props.selected.rowNumber);
  }, [props.selected]);

  const currentRows = rowsBySheet[itemType] || [];

  const visibleLibrary = useMemo(() => {
    const entries: LibraryEntry[] = [];
    if (props.selected?.rowData) {
      for (const [key, value] of Object.entries(props.selected.rowData)) {
        const text = String(value || "").trim();
        if (!text) {
          continue;
        }
        const normalized = normalizeKey(key);
        if (normalized.includes("homebrewery")) {
          entries.push({ provider: "homebrewery", title: text, source: key });
        }
        if (normalized.includes("googledoc") || normalized.includes("gdoc")) {
          entries.push({ provider: "google_docs", title: text, source: key });
        }
      }
    }

    if (folderHint.trim()) {
      entries.push({ provider: "drive", title: `Folder: ${folderHint.trim()}`, source: "folder_hint" });
    }

    const deduped = dedupeFormatterLibrary(entries);
    return deduped.filter((entry) => {
      if (target === "fivetools") {
        return entry.provider === "drive";
      }
      return entry.provider === target || entry.provider === "drive";
    });
  }, [folderHint, props.selected, target]);

  const paletteSummary = useMemo(
    () => `${palette.length} tokens | ${css.length} CSS chars`,
    [css.length, palette.length],
  );

  const runPreview = async () => {
    if (!props.selected) {
      setMessage("Select a row first.");
      return;
    }

    const payload = await props.onRunPreview({
      source: props.selected.source,
      sheet: props.selected.sheet,
      row_number: props.selected.rowNumber,
      targets: [target],
      style_template: template || null,
      style_css: css.trim() || null,
    });

    if (!payload) {
      return;
    }

    setMessage("Formatter preview generated.");
  };

  const loadTemplate = async (name: string) => {
    if (!name) {
      return;
    }
    const payload = await props.onLoadTemplate(name);
    if (!payload) {
      return;
    }
    setPalette(payload.palette || []);
    setCss(String(payload.css || ""));
  };

  const applyPreset = (kind: "warm" | "cool" | "contrast") => {
    const presets: Record<string, Record<string, string>> = {
      warm: {
        "--accent": "#9b4d1f",
        "--accent-soft": "#d88d5f",
        "--ink": "#2c2119",
        "--bg": "#fbf1df",
      },
      cool: {
        "--accent": "#2f6070",
        "--accent-soft": "#6fa7b8",
        "--ink": "#1d2a33",
        "--bg": "#eaf3f6",
      },
      contrast: {
        "--accent": "#2b2b2b",
        "--accent-soft": "#cf8f20",
        "--ink": "#121212",
        "--bg": "#fff7e8",
      },
    };

    const paletteChanges = presets[kind];
    if (!paletteChanges) {
      return;
    }
    let nextCss = css;
    for (const [token, color] of Object.entries(paletteChanges)) {
      nextCss = applyPaletteTokenChange(nextCss, token, color);
    }

    setCss(nextCss);
    setPalette((current) => {
      const copy = [...current];
      for (const [token, color] of Object.entries(paletteChanges)) {
        const found = copy.find((item) => item.token === token);
        if (found) {
          found.value = color;
        } else {
          copy.push({ token, value: color });
        }
      }
      return copy;
    });
  };

  const saveStyleSettings = async () => {
    await props.onSaveSettingsPatch({
      formatter: {
        style_template: template,
        style_css: css,
      },
    });
    setMessage("Formatter style settings saved.");
  };

  const currentRowOptions = useMemo(
    () =>
      currentRows
        .map((row) => {
          const rowNumber = Number(row._sheet_row || 0);
          if (!rowNumber) {
            return null;
          }
          return {
            rowNumber,
            label: `${pickItemName(row) || `Row ${rowNumber}`} (#${rowNumber})`,
          };
        })
        .filter(Boolean) as Array<{ rowNumber: number; label: string }>,
    [currentRows],
  );

  return (
    <section className="workspace-card">
      <h2>Formatters</h2>
      <p>Generate target-specific previews and manage Homebrewery style templates.</p>

      <div className="workspace-grid">
        <div className="workspace-controls">
          <div className="toolbar">
            <label>
              Target
              <select value={target} onChange={(event) => setTarget(event.target.value)} disabled={props.loading}>
                <option value="homebrewery">Homebrewery</option>
                <option value="google_docs">Google Docs</option>
                <option value="fivetools">5eTools</option>
              </select>
            </label>

            <label>
              Item Type
              <select value={itemType} onChange={(event) => setItemType(event.target.value)} disabled={props.loading}>
                {props.sheets.map((sheet) => (
                  <option key={sheet} value={sheet}>
                    {sheet}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Item
              <select
                value={itemRow ? String(itemRow) : ""}
                onChange={(event) => {
                  const rowNumber = Number(event.target.value || 0);
                  setItemRow(rowNumber);
                  if (rowNumber > 0 && itemType) {
                    void props.onSelectRow(rowNumber, itemType);
                  }
                }}
                disabled={props.loading}
              >
                <option value="">Select item</option>
                {currentRowOptions.map((option) => (
                  <option key={option.rowNumber} value={option.rowNumber}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Drive Folder Hint
              <input value={folderHint} onChange={(event) => setFolderHint(event.target.value)} placeholder="Google Drive folder name" />
            </label>
          </div>

          <div className="formatter-library-card">
            <h3>Loaded Drafts</h3>
            <p>
              {visibleLibrary.length
                ? `${visibleLibrary.length} candidate document(s) found.`
                : "No document found for this target in selected row."}
            </p>
            <div className="formatter-library-list">
              {visibleLibrary.map((entry) => (
                <div key={`${entry.provider}-${entry.title}-${entry.source}`} className="formatter-library-item">
                  {entry.provider}: {entry.title} ({entry.source})
                </div>
              ))}
            </div>
          </div>

          <div className="formatter-library-card">
            <h3>Style Editor</h3>
            <div className="toolbar">
              <label>
                Template
                <select
                  value={template}
                  onChange={(event) => {
                    const next = event.target.value;
                    setTemplate(next);
                    void loadTemplate(next);
                  }}
                  disabled={props.loading}
                >
                  {templates.map((item) => (
                    <option key={item.name} value={item.name}>
                      {item.label}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            <div className="formatter-style-presets" style={{ marginTop: 8 }}>
              <button className="btn btn-inline" disabled={props.loading} onClick={() => applyPreset("warm")}>Warm</button>
              <button className="btn btn-inline" disabled={props.loading} onClick={() => applyPreset("cool")}>Cool</button>
              <button className="btn btn-inline" disabled={props.loading} onClick={() => applyPreset("contrast")}>Contrast</button>
            </div>

            <div className="meta">{paletteSummary}</div>
            <div className="formatter-style-palette">
              {palette.map((token) => (
                <label key={token.token} className="style-palette-item">
                  <span>{token.token}</span>
                  <input
                    type="color"
                    value={toHexColor(token.value)}
                    onInput={(event) => {
                      const next = (event.target as HTMLInputElement).value;
                      setCss((current) => applyPaletteTokenChange(current, token.token, next));
                      setPalette((current) =>
                        current.map((item) => (item.token === token.token ? { ...item, value: next } : item)),
                      );
                    }}
                  />
                  <input
                    value={token.value}
                    onChange={(event) => {
                      const next = event.target.value.trim();
                      if (!next) {
                        return;
                      }
                      setCss((current) => applyPaletteTokenChange(current, token.token, next));
                      setPalette((current) =>
                        current.map((item) => (item.token === token.token ? { ...item, value: next } : item)),
                      );
                    }}
                  />
                </label>
              ))}
            </div>

            <label style={{ marginTop: 8 }}>
              CSS
              <textarea rows={14} value={css} onChange={(event) => setCss(event.target.value)} />
            </label>

            <button className="btn" style={{ marginTop: 8 }} disabled={props.loading} onClick={() => void saveStyleSettings()}>
              Save Style Settings
            </button>
          </div>
        </div>

        <div className="workspace-results">
          <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: 8 }}>
            <button className="btn" disabled={props.loading || !props.selected} onClick={() => void runPreview()}>
              Run Formatter Preview
            </button>
          </div>

          <div className="meta">{message}</div>
          <pre className="feature-output workspace-output">{props.output}</pre>
        </div>
      </div>
    </section>
  );
}
