import type { Meta, StoryObj } from "@storybook/react";

import { shadowScale } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/ShadowScale",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <div style={{ display: "grid", gap: "16px" }}>
        {Object.entries(shadowScale).map(([token, value]) => (
          <div
            key={token}
            style={{
              border: "1px solid var(--border)",
              borderRadius: "12px",
              padding: "24px",
              background: "var(--surface-strong)",
              boxShadow: value,
            }}
          >
            <div style={{ fontWeight: 700 }}>{token}</div>
            <div style={{ marginTop: "8px", fontFamily: "var(--velum-font-mono)", fontSize: "0.82rem" }}>{value}</div>
          </div>
        ))}
      </div>
    </StoryFrame>
  ),
};
