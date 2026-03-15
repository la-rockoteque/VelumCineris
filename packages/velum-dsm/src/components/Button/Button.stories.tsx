import type { Meta, StoryObj } from "@storybook/react";

import { Button } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Button",
  component: Button,
} satisfies Meta<typeof Button>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
        <Button $variant="primary">Publish</Button>
        <Button>Save Draft</Button>
        <Button $variant="ghost">Cancel</Button>
        <Button disabled>Disabled</Button>
      </div>
    </StoryFrame>
  ),
};
