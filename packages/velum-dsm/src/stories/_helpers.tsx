import type { ReactNode } from "react";

export function StoryFrame(props: { children: ReactNode; maxWidth?: string }) {
  return (
    <div
      style={{
        width: "100%",
        maxWidth: props.maxWidth ?? "720px",
        display: "grid",
        gap: "16px",
      }}
    >
      {props.children}
    </div>
  );
}

export function DemoBlock(props: { children: ReactNode; minHeight?: string }) {
  return (
    <div
      style={{
        minHeight: props.minHeight ?? "56px",
        padding: "16px",
        borderRadius: "12px",
        border: "1px solid var(--border)",
        background: "var(--surface-strong)",
      }}
    >
      {props.children}
    </div>
  );
}

export function ShowcaseGrid(props: { children: ReactNode; columns?: string; gap?: string }) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: props.columns ?? "repeat(auto-fit, minmax(220px, 1fr))",
        gap: props.gap ?? "16px",
        alignItems: "start",
      }}
    >
      {props.children}
    </div>
  );
}

export function StateMatrix(props: { children: ReactNode; columns?: string; gap?: string }) {
  return (
    <div
      style={{
        display: "grid",
        gridTemplateColumns: props.columns ?? "repeat(auto-fit, minmax(220px, 1fr))",
        gap: props.gap ?? "16px",
        alignItems: "stretch",
      }}
    >
      {props.children}
    </div>
  );
}

export function StateCase(props: {
  label: string;
  description?: string;
  children: ReactNode;
  minHeight?: string;
}) {
  return (
    <div
      style={{
        display: "grid",
        gap: "12px",
        alignContent: "start",
        border: "1px solid var(--border)",
        borderRadius: "12px",
        padding: "16px",
        background: "var(--surface-strong)",
      }}
    >
      <div style={{ display: "grid", gap: "4px" }}>
        <div style={{ fontWeight: 700 }}>{props.label}</div>
        {props.description ? (
          <div style={{ color: "var(--ink-soft)", fontSize: "0.82rem", lineHeight: 1.4 }}>
            {props.description}
          </div>
        ) : null}
      </div>
      <div style={{ minHeight: props.minHeight ?? "72px", display: "grid", alignContent: "center" }}>
        {props.children}
      </div>
    </div>
  );
}
