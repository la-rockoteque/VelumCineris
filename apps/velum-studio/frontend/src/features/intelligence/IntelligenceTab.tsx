import { useEffect, useState } from "react";
import { styled } from "app/styletron";

import {
  ActionRowEnd,
  Button,
  SegmentedControl,
  SelectInput,
  TextArea,
  TextInput,
  Toolbar,
  WorkspaceCard,
  WorkspaceLead,
  WorkspaceOutput,
  WorkspaceTitle,
} from "shared/library";
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
          <SegmentedControl
            ariaLabel="Intelligence mode"
            value={mode}
            onChange={setMode}
            options={[
              { value: "custom", label: "Custom", disabled: props.loading || !props.selected },
              { value: "balance", label: "Balance", disabled: props.loading || !props.selected },
              { value: "rewrite", label: "Rewrite", disabled: props.loading || !props.selected },
              { value: "qa", label: "QA", disabled: props.loading || !props.selected },
            ]}
          />
        </label>

        <label>
          Model
          <TextInput value={model} onChange={(event) => setModel(event.target.value)} disabled={props.loading || !props.selected} />
        </label>

        <label>
          Provider
          <SegmentedControl
            ariaLabel="Provider"
            value={useLocal ? "true" : "false"}
            onChange={(value) => setUseLocal(value === "true")}
            options={[
              { value: "true", label: "Local LLM", disabled: props.loading || !props.selected },
              { value: "false", label: "Remote", disabled: props.loading || !props.selected },
            ]}
          />
        </label>
      </Toolbar>

      <InstructionLabel>
        Instruction
        <TextArea
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
