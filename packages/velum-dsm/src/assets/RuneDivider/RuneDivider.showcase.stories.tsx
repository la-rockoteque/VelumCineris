import type { Meta, StoryObj } from "@storybook/react";

import { Card, RuneDivider } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Assets/RuneDivider",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <Card title="Rune Divider Showcase" subtitle="Different widths and color emphasis for editorial breaks.">
        <StateMatrix>
          <StateCase label="Compact" description="Short inline divider" minHeight="80px">
            <RuneDivider style={{ width: "220px", color: "var(--accent-soft)" }} />
          </StateCase>
          <StateCase label="Standard" description="Default section break" minHeight="80px">
            <RuneDivider style={{ width: "100%", maxWidth: "420px", color: "var(--accent)" }} />
          </StateCase>
          <StateCase label="Emphatic" description="High emphasis editorial divider" minHeight="80px">
            <RuneDivider style={{ width: "100%", maxWidth: "560px", color: "var(--ink)" }} />
          </StateCase>
        </StateMatrix>
      </Card>
    </StoryFrame>
  ),
};
