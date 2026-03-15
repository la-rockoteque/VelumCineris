import { styled } from "app/styletron";

import type { BlockProps } from "./types";

const SectionRoot = styled("section", {});
const SectionTitle = styled("h3", {});
const SectionSubtitle = styled("p", {});

export function Section(props: BlockProps) {
  return (
    <SectionRoot className={props.className}>
      {props.title ? <SectionTitle>{props.title}</SectionTitle> : null}
      {props.subtitle ? <SectionSubtitle>{props.subtitle}</SectionSubtitle> : null}
      {props.children}
    </SectionRoot>
  );
}
