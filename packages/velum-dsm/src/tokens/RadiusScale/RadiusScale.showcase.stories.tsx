import type { Meta, StoryObj } from "@storybook/react";

import { radiusScale } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/RadiusScale",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        {Object.entries(radiusScale).map(([token, value]) => (
          <StateCase key={token} label={token} description={value} minHeight="140px">
            <div style={{ height: "72px", borderRadius: value, background: "linear-gradient(135deg, var(--accent-soft), var(--accent))" }} />
          </StateCase>
        ))}
      </StateMatrix>
    </StoryFrame>
  ),
};
