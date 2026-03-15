import type { Meta, StoryObj } from "@storybook/react";

import { MetaText } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/MetaText",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame>
      <StateMatrix>
        <StateCase label="Metrics" description="Counts and compact metadata">
          <MetaText>5 palette tokens | 164 CSS chars</MetaText>
        </StateCase>
        <StateCase label="Timestamp" description="Status timestamp or sync indicator">
          <MetaText>Last saved 2 minutes ago</MetaText>
        </StateCase>
        <StateCase label="Context" description="Source and sheet summaries">
          <MetaText>Source: modern_lexicon · Sheet: translator</MetaText>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
