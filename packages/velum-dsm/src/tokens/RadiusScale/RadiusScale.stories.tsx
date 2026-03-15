import type { Meta, StoryObj } from "@storybook/react";

import { radiusScale } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/RadiusScale",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <div style={{ display: "grid", gap: "12px" }}>
        {Object.entries(radiusScale).map(([token, value]) => (
          <div
            key={token}
            style={{
              display: "grid",
              gridTemplateColumns: "120px 1fr 100px",
              gap: "16px",
              alignItems: "center",
              border: "1px solid var(--border)",
              borderRadius: "12px",
              padding: "16px",
              background: "var(--surface-strong)",
            }}
          >
            <div style={{ fontWeight: 700 }}>{token}</div>
            <div style={{ height: "44px", background: "var(--accent-soft)", borderRadius: value }} />
            <div style={{ fontFamily: "var(--velum-font-mono)" }}>{value}</div>
          </div>
        ))}
      </div>
    </StoryFrame>
  ),
};
