import { styled } from "app/styletron";

import type { BlockProps } from "./types";

const SubsectionRoot = styled("section", {});
const SubsectionTitle = styled("h4", {});
const SubsectionSubtitle = styled("p", {});

export function Subsection(props: BlockProps) {
  return (
    <SubsectionRoot className={props.className}>
      {props.title ? <SubsectionTitle>{props.title}</SubsectionTitle> : null}
      {props.subtitle ? <SubsectionSubtitle>{props.subtitle}</SubsectionSubtitle> : null}
      {props.children}
    </SubsectionRoot>
  );
}
