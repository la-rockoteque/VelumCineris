import type { Meta, StoryObj } from "@storybook/react";

import { Card, brickAndMossUrl } from "../../index";

const meta = {
  title: "Assets/BrickAndMoss",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Card title="Brick And Moss" subtitle="Primary atmospheric background texture for Velum Studio.">
      <div
        style={{
          minHeight: "220px",
          borderRadius: "14px",
          border: "1px solid var(--border)",
          background: `url("${brickAndMossUrl}") center / cover no-repeat`,
        }}
      />
    </Card>
  ),
};
