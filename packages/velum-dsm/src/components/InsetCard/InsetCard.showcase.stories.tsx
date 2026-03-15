import type { Meta, StoryObj } from "@storybook/react";

import { InsetCard, InsetLead, InsetTitle, MetaText } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Workspace/InsetCard",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Summary" description="Title + lead composition" minHeight="180px">
          <InsetCard>
            <InsetTitle>Context</InsetTitle>
            <InsetLead>Nested summary surface.</InsetLead>
          </InsetCard>
        </StateCase>
        <StateCase label="Metrics" description="Title + metadata composition" minHeight="180px">
          <InsetCard>
            <InsetTitle>Metrics</InsetTitle>
            <MetaText>12 rows loaded</MetaText>
            <MetaText>4 tokens customized</MetaText>
          </InsetCard>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
