import type { Meta, StoryObj } from "@storybook/react";

import { shadowScale } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/ShadowScale",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <div style={{ padding: "24px", background: "radial-gradient(circle at top, rgba(195, 140, 91, 0.2), transparent 35%), var(--bg)" }}>
        <StateMatrix>
          {Object.entries(shadowScale).map(([token, value]) => (
            <StateCase key={token} label={token} description={value} minHeight="140px">
              <div style={{ padding: "24px", borderRadius: "16px", background: "var(--surface-strong)", boxShadow: value }} />
            </StateCase>
          ))}
        </StateMatrix>
      </div>
    </StoryFrame>
  ),
};
