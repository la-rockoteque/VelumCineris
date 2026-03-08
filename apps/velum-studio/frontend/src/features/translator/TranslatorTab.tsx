import { useEffect, useMemo, useState } from "react";

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
    <section className="workspace-card">
      <h2>Translator</h2>
      <p>Translate text into your target language with romanized and symbolized outputs.</p>

      <div className="workspace-grid">
        <div className="workspace-controls">
          <div className="toolbar">
            <label>
              Target
              <select value={target} onChange={(event) => setTarget(event.target.value)} disabled={props.loading || !targets.length}>
                {targets.map((item) => (
                  <option key={item} value={item}>
                    {item}
                  </option>
                ))}
              </select>
            </label>
          </div>

          <label>
            English Input
            <textarea
              rows={6}
              value={input}
              onChange={(event) => setInput(event.target.value)}
              disabled={props.loading || !target}
              placeholder="Enter English source text"
            />
          </label>

          <div style={{ display: "flex", gap: 8 }}>
            <button className="btn" disabled={props.loading || !target || !input.trim()} onClick={() => void props.onTranslate(target, input)}>
              Translate
            </button>
            <button className="btn" disabled={props.loading || !target} onClick={() => void props.onLoadContext(target)}>
              Reload Context
            </button>
            <button className="btn" disabled={props.loading || !props.romanized} onClick={playAudio}>
              Pronunciation
            </button>
          </div>

          <div className="translator-card" style={{ marginTop: 10 }}>
            <h3>Romanized</h3>
            <p className="translator-result">{props.romanized || "-"}</p>
          </div>

          <div className="translator-card">
            <h3>Symbolized</h3>
            <p className="translator-result">{props.symbolized || "-"}</p>
          </div>
        </div>

        <div className="workspace-results">
          <div className="translator-context-card">
            <h3>Language Context</h3>
            <div className="translator-context-summary">{contextSummary}</div>
            <div className="translator-context" style={{ marginTop: 8 }}>
              {(props.context?.sheets || []).map((section) => {
                const rows = section.rows || [];
                const preview = rows.slice(0, 5);
                const columns = Object.keys(preview[0] || {});
                return (
                  <article key={section.sheet} className="translator-context-block">
                    <h4>{section.sheet}</h4>
                    {!rows.length && <div className="translator-context-empty">No rows.</div>}
                    {!!rows.length && (
                      <div className="table-wrap">
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
                      </div>
                    )}
                  </article>
                );
              })}
            </div>
          </div>

          <pre className="feature-output workspace-output">{props.output}</pre>
        </div>
      </div>
    </section>
  );
}
