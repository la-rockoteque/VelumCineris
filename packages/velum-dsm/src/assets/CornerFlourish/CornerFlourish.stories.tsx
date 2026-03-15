import type { Meta, StoryObj } from "@storybook/react";

import { Card, CornerFlourish } from "../../index";

const meta = {
  title: "Assets/CornerFlourish",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Card title="Corner Flourish" subtitle="Decorative corner motif for framing surfaces and compositions.">
      <div style={{ display: "flex", justifyContent: "space-between", padding: "16px" }}>
        <CornerFlourish style={{ width: "56px", color: "var(--accent-soft)" }} />
        <CornerFlourish style={{ width: "56px", color: "var(--accent-soft)", transform: "scaleX(-1)" }} />
      </div>
    </Card>
  ),
};
