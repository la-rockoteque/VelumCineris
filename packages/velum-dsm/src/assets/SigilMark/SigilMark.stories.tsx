import type { Meta, StoryObj } from "@storybook/react";

import { Card, SigilMark } from "../../index";

const meta = {
  title: "Assets/SigilMark",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Card title="Sigil Mark" subtitle="Primary emblematic mark for the DSM.">
      <div style={{ display: "grid", placeItems: "center", padding: "16px" }}>
        <SigilMark style={{ width: "88px", color: "var(--accent)" }} />
      </div>
    </Card>
  ),
};
