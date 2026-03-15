import type { Meta, StoryObj } from "@storybook/react";

import { studioTheme } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/StudioTheme",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame maxWidth="900px">
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(220px, 1fr))", gap: "12px" }}>
        {Object.entries(studioTheme).map(([token, value]) => (
          <div
            key={token}
            style={{
              border: "1px solid var(--border)",
              borderRadius: "12px",
              padding: "16px",
              background: "var(--surface-strong)",
            }}
          >
            <div style={{ fontWeight: 700, marginBottom: "8px" }}>{token}</div>
            <div style={{ fontFamily: "var(--velum-font-mono)", fontSize: "0.82rem", wordBreak: "break-word" }}>{value}</div>
          </div>
        ))}
      </div>
    </StoryFrame>
  ),
};
