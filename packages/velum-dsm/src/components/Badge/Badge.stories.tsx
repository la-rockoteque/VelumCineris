import type { Meta, StoryObj } from "@storybook/react";

import { Badge } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Badge",
  component: Badge,
} satisfies Meta<typeof Badge>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: "Queued",
  },
  render: () => (
    <StoryFrame>
      <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
        <Badge tone="info">Queued</Badge>
        <Badge tone="ok">Healthy</Badge>
        <Badge tone="warn">Pending Review</Badge>
        <Badge tone="danger">Blocked</Badge>
      </div>
    </StoryFrame>
  ),
};
