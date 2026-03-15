import type { Meta, StoryObj } from "@storybook/react";

import { MetaText } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/MetaText",
  component: MetaText,
} satisfies Meta<typeof MetaText>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <MetaText>5 palette tokens | 164 CSS chars</MetaText>
    </StoryFrame>
  ),
};
