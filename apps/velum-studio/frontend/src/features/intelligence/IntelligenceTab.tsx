import { useEffect, useState } from "react";
import { styled } from "app/styletron";

import { ActionRowEnd, Button, Toolbar, WorkspaceCard, WorkspaceLead, WorkspaceOutput, WorkspaceTitle } from "shared/library";
import type { SelectedRow } from "shared/types/api";

interface IntelligenceTabProps {
  loading: boolean;
  selected: SelectedRow | null;
  output: string;
  onRun: (payload: Record<string, unknown>) => Promise<Record<string, unknown> | null>;
}

const InstructionLabel = styled("label", {
  marginTop: "10px",
});

export function IntelligenceTab(props: IntelligenceTabProps) {
  const [mode, setMode] = useState("custom");
  const [model, setModel] = useState("llama3.1:8b");
  const [useLocal, setUseLocal] = useState(true);
  const [instruction, setInstruction] = useState("Balance this entry for D&D 5e while preserving flavor and intent.");

  useEffect(() => {
    if (!props.selected) {
      return;
    }
    if (!instruction.trim()) {
      setInstruction("Balance this entry for D&D 5e while preserving flavor and intent.");
    }
  }, [instruction, props.selected]);

  const run = async () => {
    if (!props.selected) {
      return;
    }

    await props.onRun({
      mode,
      instruction: instruction.trim(),
      row_data: props.selected.rowData,
      use_local_llm: useLocal,
      model: model.trim() || "llama3.1:8b",
    });
  };

  return (
    <WorkspaceCard>
      <WorkspaceTitle>Intelligence</WorkspaceTitle>
      <WorkspaceLead>Run local or remote suggestion workflows on the currently selected item.</WorkspaceLead>

      <Toolbar>
        <label>
          Mode
          <select value={mode} onChange={(event) => setMode(event.target.value)} disabled={props.loading || !props.selected}>
            <option value="custom">Custom</option>
            <option value="balance">Balance</option>
            <option value="rewrite">Rewrite</option>
            <option value="qa">QA</option>
          </select>
        </label>

        <label>
          Model
          <input value={model} onChange={(event) => setModel(event.target.value)} disabled={props.loading || !props.selected} />
        </label>

        <label>
          Provider
          <select
            value={useLocal ? "true" : "false"}
            onChange={(event) => setUseLocal(event.target.value === "true")}
            disabled={props.loading || !props.selected}
          >
            <option value="true">Local LLM</option>
            <option value="false">Remote</option>
          </select>
        </label>
      </Toolbar>

      <InstructionLabel>
        Instruction
        <textarea
          rows={6}
          value={instruction}
          onChange={(event) => setInstruction(event.target.value)}
          disabled={props.loading || !props.selected}
        />
      </InstructionLabel>

      <ActionRowEnd>
        <Button disabled={props.loading || !props.selected} onClick={() => void run()}>
          Run Intelligence
        </Button>
      </ActionRowEnd>

      <WorkspaceOutput>{props.output}</WorkspaceOutput>
    </WorkspaceCard>
  );
}
