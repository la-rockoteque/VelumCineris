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

const Root = styled("section", {
  display: "grid",
  gap: "var(--velum-space-3)",
});

const Title = styled("h3", {
  ...headingStyles,
  fontSize: "var(--velum-font-size-lg)",
});

const Subtitle = styled("p", subtitleStyles);

export function Section(props: BlockProps) {
  return (
    <Root className={props.className}>
      {props.title ? <Title>{props.title}</Title> : null}
      {props.subtitle ? <Subtitle>{props.subtitle}</Subtitle> : null}
      {props.children}
    </Root>
  );
}
