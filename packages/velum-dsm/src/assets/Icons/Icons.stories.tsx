import type { Meta, StoryObj } from "@storybook/react";

import { Card, iconAssets } from "../../index";

const meta = {
  title: "Assets/Icons",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Card title="Icons" subtitle="DSM icon asset set rendered as a reference grid.">
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(140px, 1fr))",
          gap: "16px",
        }}
      >
        {Object.entries(iconAssets).map(([name, url]) => (
          <div
            key={name}
            style={{
              display: "grid",
              gap: "10px",
              padding: "16px",
              borderRadius: "12px",
              border: "1px solid var(--border)",
              background: "var(--surface-strong)",
              justifyItems: "center",
            }}
          >
            <img src={url} alt={name} style={{ width: "56px", height: "56px", objectFit: "contain" }} />
            <div style={{ fontWeight: 700 }}>{name}</div>
          </div>
        ))}
      </div>
    </Card>
  ),
};
