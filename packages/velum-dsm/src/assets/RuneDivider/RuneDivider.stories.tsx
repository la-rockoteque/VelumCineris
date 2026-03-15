import type { Meta, StoryObj } from "@storybook/react";

import { Card, RuneDivider } from "../../index";

const meta = {
  title: "Assets/RuneDivider",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Card title="Rune Divider" subtitle="Horizontal ornamental divider for section transitions.">
      <div style={{ display: "grid", placeItems: "center", padding: "16px" }}>
        <RuneDivider style={{ width: "100%", maxWidth: "360px", color: "var(--accent)" }} />
      </div>
    </Card>
  ),
};
