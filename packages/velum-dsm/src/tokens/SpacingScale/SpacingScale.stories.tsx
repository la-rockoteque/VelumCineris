import type { Meta, StoryObj } from "@storybook/react";

import { spacingScale } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/SpacingScale",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <div style={{ border: "1px solid var(--border)", borderRadius: "12px", padding: "16px", background: "var(--surface-strong)" }}>
        {Object.entries(spacingScale).map(([step, value]) => (
          <div key={step} style={{ display: "grid", gridTemplateColumns: "64px 1fr", gap: "12px", alignItems: "center", marginBottom: "10px" }}>
            <div style={{ fontFamily: "var(--velum-font-mono)" }}>{step}</div>
            <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
              <div style={{ width: value, height: "10px", borderRadius: "999px", background: "var(--accent)" }} />
              <span style={{ fontFamily: "var(--velum-font-mono)" }}>{value}</span>
            </div>
          </div>
        ))}
      </div>
    </StoryFrame>
  ),
};
