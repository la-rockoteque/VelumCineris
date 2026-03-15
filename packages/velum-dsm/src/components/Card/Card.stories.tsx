import type { Meta, StoryObj } from "@storybook/react";

import { Card } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Layout/Card",
  component: Card,
} satisfies Meta<typeof Card>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    title: "Editorial Card",
    subtitle: "Default framed content surface.",
    children: "Use cards for grouped content that needs emphasis and separation from the page canvas.",
  },
  render: () => (
    <StoryFrame>
      <Card title="Editorial Card" subtitle="Default framed content surface.">
        <p style={{ margin: 0 }}>Use cards for grouped content that needs emphasis and separation from the page canvas.</p>
      </Card>
    </StoryFrame>
  ),
};
