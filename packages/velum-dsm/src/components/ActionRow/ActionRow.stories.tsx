import type { Meta, StoryObj } from "@storybook/react";

import { ActionRow, Button } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Actions/ActionRow",
  component: ActionRow,
} satisfies Meta<typeof ActionRow>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <ActionRow>
        <Button $variant="primary">Save</Button>
        <Button>Reload</Button>
        <Button $variant="ghost">Reset</Button>
      </ActionRow>
    </StoryFrame>
  ),
};
