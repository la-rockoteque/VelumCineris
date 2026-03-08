import { useEffect, useState } from "react";

interface SettingsTabProps {
  loading: boolean;
  source: string;
  settings: Record<string, unknown>;
  onSavePatch: (patch: Record<string, unknown>) => Promise<void>;
  onResetColumns: () => Promise<void>;
}

function readCompendiumSettings(settings: Record<string, unknown>) {
  const compendium = (settings.compendium as Record<string, unknown> | undefined) || {};
  return {
    defaultSource: String(settings.default_source || "auto"),
    minimalEnabled: Boolean(compendium.minimal_columns_default ?? true),
    minimalCount: Number(compendium.minimal_column_count ?? 8),
    cellLimit: Number(compendium.cell_char_limit ?? 150),
  };
}

export function SettingsTab(props: SettingsTabProps) {
  const [defaultSource, setDefaultSource] = useState("auto");
  const [minimalEnabled, setMinimalEnabled] = useState(true);
  const [minimalCount, setMinimalCount] = useState("8");
  const [cellLimit, setCellLimit] = useState("150");
  const [status, setStatus] = useState("Settings output appears here.");

  useEffect(() => {
    const parsed = readCompendiumSettings(props.settings);
    setDefaultSource(parsed.defaultSource);
    setMinimalEnabled(parsed.minimalEnabled);
    setMinimalCount(String(parsed.minimalCount));
    setCellLimit(String(parsed.cellLimit));
  }, [props.settings]);

  const save = async () => {
    const patch = {
      default_source: defaultSource,
      compendium: {
        minimal_columns_default: minimalEnabled,
        minimal_column_count: Math.min(30, Math.max(1, Number(minimalCount || 8) || 8)),
        cell_char_limit: Math.min(1000, Math.max(40, Number(cellLimit || 150) || 150)),
      },
    };

    await props.onSavePatch(patch);
    setStatus("Settings saved.");
  };

  const resetColumns = async () => {
    await props.onResetColumns();
    setStatus(`Column visibility reset for ${props.source}.`);
  };

  return (
    <section className="workspace-card">
      <h2>Settings</h2>
      <p>Preferences are persisted in your home profile (`~/.velum`).</p>

      <div className="toolbar">
        <label>
          Default Source
          <select value={defaultSource} onChange={(event) => setDefaultSource(event.target.value)} disabled={props.loading}>
            <option value="auto">auto</option>
            <option value="xlsx">xlsx</option>
            <option value="google">google</option>
          </select>
        </label>

        <label>
          Minimal Columns by Default
          <select
            value={minimalEnabled ? "true" : "false"}
            onChange={(event) => setMinimalEnabled(event.target.value === "true")}
            disabled={props.loading}
          >
            <option value="true">Enabled</option>
            <option value="false">Disabled</option>
          </select>
        </label>

        <label>
          Minimal Column Count
          <input type="number" min={1} max={30} value={minimalCount} onChange={(event) => setMinimalCount(event.target.value)} disabled={props.loading} />
        </label>

        <label>
          Cell Char Limit
          <input type="number" min={40} max={1000} value={cellLimit} onChange={(event) => setCellLimit(event.target.value)} disabled={props.loading} />
        </label>
      </div>

      <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
        <button className="btn" disabled={props.loading} onClick={() => void save()}>
          Save Settings
        </button>
        <button className="btn" disabled={props.loading} onClick={() => void resetColumns()}>
          Reset Sheet Columns
        </button>
      </div>

      <pre className="feature-output workspace-output">{status}</pre>
    </section>
  );
}
