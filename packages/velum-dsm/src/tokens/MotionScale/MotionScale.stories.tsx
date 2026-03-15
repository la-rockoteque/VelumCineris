import type { Meta, StoryObj } from "@storybook/react";

import { motionScale } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/MotionScale",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <div style={{ border: "1px solid var(--border)", borderRadius: "12px", padding: "16px", background: "var(--surface-strong)" }}>
        {Object.entries(motionScale).map(([key, value]) => (
          <div key={key} style={{ marginBottom: "10px", fontFamily: "var(--velum-font-mono)" }}>
            {key}: {typeof value === "string" ? value : JSON.stringify(value)}
          </div>
        ))}
      </div>
    </StoryFrame>
  ),
};
