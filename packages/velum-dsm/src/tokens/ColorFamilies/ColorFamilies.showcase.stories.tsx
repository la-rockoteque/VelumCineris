import type { Meta, StoryObj } from "@storybook/react";

import { colorFamilies } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/ColorFamilies",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="1100px">
      <StateMatrix columns="1fr">
        {Object.entries(colorFamilies).map(([family, values]) => (
          <StateCase key={family} label={family} description="All tones in the family" minHeight="160px">
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(150px, 1fr))", gap: "10px" }}>
              {Object.entries(values).map(([tone, swatch]) => (
                <div key={tone} style={{ borderRadius: "10px", overflow: "hidden", border: "1px solid var(--border)" }}>
                  <div style={{ height: "52px", background: swatch }} />
                  <div style={{ padding: "10px", fontFamily: "var(--velum-font-mono)", fontSize: "0.78rem" }}>
                    {family}.{tone}
                  </div>
                </div>
              ))}
            </div>
          </StateCase>
        ))}
      </StateMatrix>
    </StoryFrame>
  ),
};
