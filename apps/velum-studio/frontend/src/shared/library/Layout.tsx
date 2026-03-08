import type { ReactNode } from "react";

interface BlockProps {
  title?: string;
  subtitle?: string;
  className?: string;
  children: ReactNode;
}

export function Card(props: BlockProps) {
  return (
    <section className={`workspace-card ${props.className || ""}`.trim()}>
      {props.title ? <h2>{props.title}</h2> : null}
      {props.subtitle ? <p>{props.subtitle}</p> : null}
      {props.children}
    </section>
  );
}

export function Section(props: BlockProps) {
  return (
    <section className={props.className}>
      {props.title ? <h3>{props.title}</h3> : null}
      {props.subtitle ? <p>{props.subtitle}</p> : null}
      {props.children}
    </section>
  );
}

export function Subsection(props: BlockProps) {
  return (
    <section className={props.className}>
      {props.title ? <h4>{props.title}</h4> : null}
      {props.subtitle ? <p>{props.subtitle}</p> : null}
      {props.children}
    </section>
  );
}

