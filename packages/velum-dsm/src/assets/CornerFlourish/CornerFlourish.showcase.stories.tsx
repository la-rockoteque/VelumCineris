import type { Meta, StoryObj } from "@storybook/react";

import { Card, CornerFlourish } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Assets/CornerFlourish",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <Card title="Corner Flourish Showcase" subtitle="Orientation and framing examples for decorative corners.">
        <StateMatrix>
          <StateCase label="Top Left" description="Default orientation" minHeight="96px">
            <CornerFlourish style={{ width: "56px", color: "var(--accent-soft)" }} />
          </StateCase>
          <StateCase label="Top Right" description="Mirrored horizontally" minHeight="96px">
            <CornerFlourish style={{ width: "56px", color: "var(--accent-soft)", transform: "scaleX(-1)" }} />
          </StateCase>
          <StateCase label="Bottom Left" description="Mirrored vertically" minHeight="96px">
            <CornerFlourish style={{ width: "56px", color: "var(--accent)", transform: "scaleY(-1)" }} />
          </StateCase>
          <StateCase label="Framed Surface" description="Four-corner composition example" minHeight="180px">
            <div style={{ position: "relative", minHeight: "150px", border: "1px solid var(--border)", borderRadius: "16px", padding: "24px", background: "var(--surface)" }}>
              <CornerFlourish style={{ position: "absolute", top: "12px", left: "12px", width: "40px", color: "var(--accent-soft)" }} />
              <CornerFlourish style={{ position: "absolute", top: "12px", right: "12px", width: "40px", color: "var(--accent-soft)", transform: "scaleX(-1)" }} />
              <CornerFlourish style={{ position: "absolute", bottom: "12px", left: "12px", width: "40px", color: "var(--accent)", transform: "scaleY(-1)" }} />
              <CornerFlourish style={{ position: "absolute", bottom: "12px", right: "12px", width: "40px", color: "var(--accent)", transform: "scale(-1, -1)" }} />
            </div>
          </StateCase>
        </StateMatrix>
      </Card>
    </StoryFrame>
  ),
};
