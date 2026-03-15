import type { Meta, StoryObj } from "@storybook/react";

import { ActionRowEnd, Button } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/ActionRowEnd",
  component: ActionRowEnd,
} satisfies Meta<typeof ActionRowEnd>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <ActionRowEnd>
        <Button>Back</Button>
        <Button $variant="primary">Continue</Button>
      </ActionRowEnd>
    </StoryFrame>
  ),
};
