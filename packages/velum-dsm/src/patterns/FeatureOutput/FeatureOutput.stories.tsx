import type { Meta, StoryObj } from "@storybook/react";

import { FeatureOutput } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/FeatureOutput",
  component: FeatureOutput,
} satisfies Meta<typeof FeatureOutput>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <FeatureOutput>Feature output surfaces are useful for summaries, previews, and generated responses.</FeatureOutput>
    </StoryFrame>
  ),
};
