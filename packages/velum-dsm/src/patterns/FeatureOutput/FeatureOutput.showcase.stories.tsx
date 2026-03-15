import type { Meta, StoryObj } from "@storybook/react";

import { FeatureOutput } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/FeatureOutput",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Short" description="Brief summary output">
          <FeatureOutput>Short summary output.</FeatureOutput>
        </StateCase>
        <StateCase label="Long" description="Longer generated content" minHeight="140px">
          <FeatureOutput>Longer generated output surfaces can hold paragraphs, summaries, or rich result content.</FeatureOutput>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
