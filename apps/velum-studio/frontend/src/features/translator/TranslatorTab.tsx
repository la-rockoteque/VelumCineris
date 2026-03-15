import { useEffect, useMemo, useState } from "react";
import { styled } from "app/styletron";

import {
  ActionRow,
  Button,
  InsetCard,
  InsetTitle,
  SelectInput,
  TableWrap,
  TextArea,
  Toolbar,
  WorkbenchLayout,
  WorkbenchMain,
  WorkbenchSidebar,
  WorkspaceCard,
  WorkspaceLead,
  WorkspaceOutput,
  WorkspaceTitle,
} from "shared/library";
import type { SelectedRow, TranslatorContextResponse } from "shared/types/api";
import { pickItemName } from "shared/utils/fields";
import { truncateText } from "shared/utils/text";

interface TranslatorTabProps {
  loading: boolean;
  source: string;
  selected: SelectedRow | null;
  output: string;
  romanized: string;
  symbolized: string;
  context: TranslatorContextResponse | null;
  onLoadTargets: () => Promise<{ source: string; targets: string[] } | null>;
  onLoadContext: (target: string) => Promise<TranslatorContextResponse | null>;
  onTranslate: (target: string, text: string) => Promise<void>;
}

const ResultText = styled("p", {
  margin: 0,
  fontSize: "0.94rem",
  color: "#3f3529",
});

const ContextSummary = styled("div", {
  color: "#5d513f",
  fontSize: "0.8rem",
});

const ContextContainer = styled("div", {
  marginTop: "8px",
  display: "grid",
  gap: "8px",
});

const ContextBlock = styled("article", {
  display: "grid",
  gap: "6px",
});

const ContextEmpty = styled("div", {
  fontSize: "0.78rem",
  color: "#736854",
});

export function TranslatorTab(props: TranslatorTabProps) {
  const [targets, setTargets] = useState<string[]>([]);
  const [target, setTarget] = useState("");
  const [input, setInput] = useState("");

  useEffect(() => {
    void (async () => {
      const payload = await props.onLoadTargets();
      if (!payload) {
        return;
      }
      setTargets(payload.targets || []);
      setTarget((current) => {
        if (current && payload.targets.includes(current)) {
          return current;
        }
        return payload.targets[0] || "";
      });
    })();
  }, [props.source]);

  useEffect(() => {
    if (!props.selected) {
      return;
    }
    if (!input.trim()) {
      setInput(pickItemName(props.selected.rowData));
    }
  }, [input, props.selected]);

  useEffect(() => {
    if (!target) {
      return;
    }
    void props.onLoadContext(target);
  }, [props.onLoadContext, target]);

  const contextSummary = useMemo(() => {
    const context = props.context;
    if (!context) {
      return "No language context loaded.";
    }
    return `Dictionary: ${context.dictionary_sheet || "n/a"} | Phonetics: ${context.phonetics_sheet || "n/a"} | Script: ${context.script_sheet || "n/a"} | Grammar: ${context.grammar_sheet || "n/a"}`;
  }, [props.context]);

  const playAudio = () => {
    const audioText = props.romanized || input;
    if (!audioText.trim()) {
      return;
    }
    if (!window.speechSynthesis) {
      return;
    }
    const utterance = new SpeechSynthesisUtterance(audioText);
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  };

  return (
    <WorkspaceCard>
      <WorkspaceTitle>Translator</WorkspaceTitle>
      <WorkspaceLead>Translate text into your target language with romanized and symbolized outputs.</WorkspaceLead>

      <WorkbenchLayout>
        <WorkbenchSidebar>
          <Toolbar>
            <label>
              Target
              <SelectInput
                value={target}
                onChange={(event) => setTarget(event.target.value)}
                disabled={props.loading || !targets.length}
              >
                {targets.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </SelectInput>
            </label>
          </Toolbar>

          <label>
            English Input
            <TextArea
              rows={6}
              value={input}
              onChange={(event) => setInput(event.target.value)}
              disabled={props.loading || !target}
              placeholder="Enter English source text"
            />
          </label>

          <ActionRow>
            <Button disabled={props.loading || !target || !input.trim()} onClick={() => void props.onTranslate(target, input)}>
              Translate
            </Button>
            <Button disabled={props.loading || !target} onClick={() => void props.onLoadContext(target)}>
              Reload Context
            </Button>
            <Button disabled={props.loading || !props.romanized} onClick={playAudio}>
              Pronunciation
            </Button>
          </ActionRow>

          <InsetCard>
            <InsetTitle>Romanized</InsetTitle>
            <ResultText>{props.romanized || "-"}</ResultText>
          </InsetCard>

          <InsetCard>
            <InsetTitle>Symbolized</InsetTitle>
            <ResultText>{props.symbolized || "-"}</ResultText>
          </InsetCard>
        </WorkbenchSidebar>

        <WorkbenchMain>
          <InsetCard>
            <InsetTitle>Language Context</InsetTitle>
            <ContextSummary>{contextSummary}</ContextSummary>
            <ContextContainer>
              {(props.context?.sheets || []).map((section) => {
                const rows = section.rows || [];
                const preview = rows.slice(0, 5);
                const columns = Object.keys(preview[0] || {});
                return (
                  <ContextBlock key={section.sheet}>
                    <h4>{section.sheet}</h4>
                    {!rows.length && <ContextEmpty>No rows.</ContextEmpty>}
                    {!!rows.length && (
                      <TableWrap>
                        <table>
                          <thead>
                            <tr>
                              {columns.map((column) => (
                                <th key={column}>{column}</th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {preview.map((row, index) => (
                              <tr key={`${section.sheet}-${index}`}>
                                {columns.map((column) => (
                                  <td key={`${index}-${column}`}>{truncateText(String(row[column] ?? ""), 80)}</td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </TableWrap>
                    )}
                  </ContextBlock>
                );
              })}
            </ContextContainer>
          </InsetCard>
          <WorkspaceOutput>{props.output}</WorkspaceOutput>
        </WorkbenchMain>
      </WorkbenchLayout>
    </WorkspaceCard>
  );
}
