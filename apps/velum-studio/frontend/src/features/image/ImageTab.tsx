import { useEffect, useState } from "react";

import type { SelectedRow } from "shared/types/api";
import { pickItemName } from "shared/utils/fields";

interface ImageTabProps {
  loading: boolean;
  selected: SelectedRow | null;
  output: string;
  onRun: (payload: Record<string, unknown>) => Promise<Record<string, unknown> | null>;
}

export function ImageTab(props: ImageTabProps) {
  const [entityName, setEntityName] = useState("");
  const [entityType, setEntityType] = useState("spell");
  const [style, setStyle] = useState("cinematic concept art");
  const [description, setDescription] = useState("");

  useEffect(() => {
    if (!props.selected) {
      return;
    }
    if (!entityName.trim()) {
      setEntityName(pickItemName(props.selected.rowData));
    }
  }, [entityName, props.selected]);

  const run = async () => {
    const fromSelection = props.selected ? pickItemName(props.selected.rowData) : "";
    const resolved = entityName.trim() || fromSelection;
    if (!resolved) {
      return;
    }

    await props.onRun({
      entity_name: resolved,
      entity_type: entityType,
      style,
      description,
      provider: "chatgpt",
      dry_run: true,
    });
  };

  return (
    <section className="workspace-card">
      <h2>Image Generator</h2>
      <p>Generate provider-ready image prompt plans based on selected content.</p>

      <div className="toolbar">
        <label>
          Entity
          <input value={entityName} onChange={(event) => setEntityName(event.target.value)} disabled={props.loading || !props.selected} />
        </label>

        <label>
          Type
          <select value={entityType} onChange={(event) => setEntityType(event.target.value)} disabled={props.loading || !props.selected}>
            <option value="spell">Spell</option>
            <option value="species">Species</option>
            <option value="monster">Monster</option>
            <option value="item">Item</option>
            <option value="location">Location</option>
          </select>
        </label>

        <label>
          Style
          <input value={style} onChange={(event) => setStyle(event.target.value)} disabled={props.loading || !props.selected} />
        </label>
      </div>

      <label style={{ marginTop: 10 }}>
        Prompt Notes
        <textarea
          rows={8}
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          disabled={props.loading || !props.selected}
          placeholder="Extra visual details"
        />
      </label>

      <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 10 }}>
        <button className="btn" disabled={props.loading || !props.selected} onClick={() => void run()}>
          Generate Plan
        </button>
      </div>

      <pre className="feature-output workspace-output">{props.output}</pre>
    </section>
  );
}
