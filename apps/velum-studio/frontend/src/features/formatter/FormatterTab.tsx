import { useEffect, useMemo, useState, type ComponentProps } from "react";
import { styled } from "app/styletron";

import {
  Button,
  InlineButton,
  InsetCard,
  InsetLead,
  InsetTitle,
  MetaText,
  SelectInput,
  TextArea,
  TextInput,
  Toolbar,
  WorkbenchLayout,
  WorkbenchMain,
  WorkbenchSidebar,
  WorkspaceCard,
  WorkspaceLead,
  WorkspaceOutput,
  WorkspaceTitle,
} from "shared/library";
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

const LibraryList = styled("div", {
  display: "grid",
  gap: "6px",
});

const LibraryItem = styled("div", {
  border: "1px solid rgba(66, 48, 30, 0.15)",
  borderRadius: "7px",
  background: "#fff8ec",
  padding: "6px 8px",
  fontSize: "0.78rem",
});

const Presets = styled("div", {
  display: "flex",
  flexWrap: "wrap",
  gap: "6px",
  marginTop: "8px",
});

const PaletteList = styled("div", {
  display: "grid",
  gap: "8px",
});

const PaletteItem = styled("label", {
  display: "grid",
  gridTemplateColumns: "minmax(120px, 1fr) 46px minmax(120px, 1fr)",
  alignItems: "center",
  gap: "8px",
});

const PaletteToken = styled("span", {
  fontSize: "0.76rem",
  color: "#615543",
  fontWeight: 700,
});

const CssLabel = styled("label", {
  marginTop: "8px",
});

const PreviewActionRow = styled("div", {
  display: "flex",
  justifyContent: "flex-end",
  marginBottom: "8px",
});

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

function ColorInput(props: ComponentProps<typeof TextInput>) {
  return <TextInput {...props} type="color" style={{ width: "100%", minHeight: "34px", padding: "3px", ...props.style }} />;
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

  const paletteSummary = useMemo(() => `${palette.length} tokens | ${css.length} CSS chars`, [css.length, palette.length]);

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
    <WorkspaceCard>
      <WorkspaceTitle>Formatters</WorkspaceTitle>
      <WorkspaceLead>Generate target-specific previews and manage Homebrewery style templates.</WorkspaceLead>

      <WorkbenchLayout>
        <WorkbenchSidebar>
          <Toolbar>
            <label>
              Target
              <SelectInput value={target} onChange={(event) => setTarget(event.target.value)} disabled={props.loading}>
                <option value="homebrewery">Homebrewery</option>
                <option value="google_docs">Google Docs</option>
                <option value="fivetools">5eTools</option>
              </SelectInput>
            </label>

            <label>
              Item Type
              <SelectInput value={itemType} onChange={(event) => setItemType(event.target.value)} disabled={props.loading}>
                {props.sheets.map((sheet) => (
                  <option key={sheet} value={sheet}>
                    {sheet}
                  </option>
                ))}
              </SelectInput>
            </label>

            <label>
              Item
              <SelectInput
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
              </SelectInput>
            </label>

            <label>
              Drive Folder Hint
              <TextInput value={folderHint} onChange={(event) => setFolderHint(event.target.value)} placeholder="Google Drive folder name" />
            </label>
          </Toolbar>

          <InsetCard>
            <InsetTitle>Loaded Drafts</InsetTitle>
            <InsetLead>
              {visibleLibrary.length
                ? `${visibleLibrary.length} candidate document(s) found.`
                : "No document found for this target in selected row."}
            </InsetLead>
            <LibraryList>
              {visibleLibrary.map((entry) => (
                <LibraryItem key={`${entry.provider}-${entry.title}-${entry.source}`}>
                  {entry.provider}: {entry.title} ({entry.source})
                </LibraryItem>
              ))}
            </LibraryList>
          </InsetCard>

          <InsetCard>
            <InsetTitle>Style Editor</InsetTitle>
            <Toolbar>
              <label>
                Template
                <SelectInput
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
                </SelectInput>
              </label>
            </Toolbar>

            <Presets>
              <InlineButton disabled={props.loading} onClick={() => applyPreset("warm")}>
                Warm
              </InlineButton>
              <InlineButton disabled={props.loading} onClick={() => applyPreset("cool")}>
                Cool
              </InlineButton>
              <InlineButton disabled={props.loading} onClick={() => applyPreset("contrast")}>
                Contrast
              </InlineButton>
            </Presets>

            <MetaText>{paletteSummary}</MetaText>
            <PaletteList>
              {palette.map((token) => (
                <PaletteItem key={token.token}>
                  <PaletteToken>{token.token}</PaletteToken>
                  <ColorInput
                    type="color"
                    value={toHexColor(token.value)}
                    onInput={(event) => {
                      const next = (event.target as HTMLInputElement).value;
                      setCss((current) => applyPaletteTokenChange(current, token.token, next));
                      setPalette((current) => current.map((item) => (item.token === token.token ? { ...item, value: next } : item)));
                    }}
                  />
                  <TextInput
                    value={token.value}
                    onChange={(event) => {
                      const next = event.target.value.trim();
                      if (!next) {
                        return;
                      }
                      setCss((current) => applyPaletteTokenChange(current, token.token, next));
                      setPalette((current) => current.map((item) => (item.token === token.token ? { ...item, value: next } : item)));
                    }}
                  />
                </PaletteItem>
              ))}
            </PaletteList>

            <CssLabel>
              CSS
              <TextArea rows={14} value={css} onChange={(event) => setCss(event.target.value)} />
            </CssLabel>

            <Button style={{ marginTop: "8px" }} disabled={props.loading} onClick={() => void saveStyleSettings()}>
              Save Style Settings
            </Button>
          </InsetCard>
        </WorkbenchSidebar>

        <WorkbenchMain>
          <PreviewActionRow>
            <Button disabled={props.loading || !props.selected} onClick={() => void runPreview()}>
              Run Formatter Preview
            </Button>
          </PreviewActionRow>

          <MetaText>{message}</MetaText>
          <WorkspaceOutput>{props.output}</WorkspaceOutput>
        </WorkbenchMain>
      </WorkbenchLayout>
    </WorkspaceCard>
  );
}
