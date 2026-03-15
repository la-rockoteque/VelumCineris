import { styled } from "../../styletron";
import type { BlockProps } from "../../types";

const headingStyles = {
  margin: "0",
  fontFamily: "var(--velum-font-display)",
  textTransform: "uppercase" as const,
  letterSpacing: "var(--velum-font-tracking-normal)",
};

const subtitleStyles = {
  margin: "0",
  color: "var(--velum-color-ink-soft)",
};

const CardRoot = styled("section", {
  display: "grid",
  gap: "var(--velum-space-3)",
  border: "1px solid var(--velum-color-border)",
  borderRadius: "var(--velum-radius-md)",
  padding: "var(--velum-space-4)",
  background: "var(--velum-color-surface-strong)",
  boxShadow: "var(--velum-shadow-soft)",
});

const CardTitle = styled("h2", {
  ...headingStyles,
  fontSize: "var(--velum-font-size-xl)",
});

const CardSubtitle = styled("p", subtitleStyles);

export function Card(props: BlockProps) {
  return (
    <CardRoot className={props.className}>
      {props.title ? <CardTitle>{props.title}</CardTitle> : null}
      {props.subtitle ? <CardSubtitle>{props.subtitle}</CardSubtitle> : null}
      {props.children}
    </CardRoot>
  );
}
