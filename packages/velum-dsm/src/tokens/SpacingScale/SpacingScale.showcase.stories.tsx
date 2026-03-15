import type { Meta, StoryObj } from "@storybook/react";

import { spacingScale } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/SpacingScale",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Compact" description="Steps 0-3" minHeight="180px">
          <div style={{ display: "grid", gap: "8px" }}>
            {Object.entries(spacingScale)
              .filter(([step]) => Number(step) <= 3)
              .map(([step, value]) => (
                <div key={step} style={{ border: "1px solid var(--border)", borderRadius: "12px", padding: value, background: "var(--surface)" }}>
                  <div style={{ border: "1px dashed var(--accent)", borderRadius: "8px", padding: "8px", fontFamily: "var(--velum-font-mono)" }}>
                    {step} = {value}
                  </div>
                </div>
              ))}
          </div>
        </StateCase>
        <StateCase label="Standard" description="Steps 4-6" minHeight="220px">
          <div style={{ display: "grid", gap: "8px" }}>
            {Object.entries(spacingScale)
              .filter(([step]) => Number(step) >= 4 && Number(step) <= 6)
              .map(([step, value]) => (
                <div key={step} style={{ border: "1px solid var(--border)", borderRadius: "12px", padding: value, background: "var(--surface)" }}>
                  <div style={{ border: "1px dashed var(--accent)", borderRadius: "8px", padding: "8px", fontFamily: "var(--velum-font-mono)" }}>
                    {step} = {value}
                  </div>
                </div>
              ))}
          </div>
        </StateCase>
        <StateCase label="Large" description="Steps 7-9" minHeight="260px">
          <div style={{ display: "grid", gap: "8px" }}>
            {Object.entries(spacingScale)
              .filter(([step]) => Number(step) >= 7)
              .map(([step, value]) => (
                <div key={step} style={{ border: "1px solid var(--border)", borderRadius: "12px", padding: value, background: "var(--surface)" }}>
                  <div style={{ border: "1px dashed var(--accent)", borderRadius: "8px", padding: "8px", fontFamily: "var(--velum-font-mono)" }}>
                    {step} = {value}
                  </div>
                </div>
              ))}
          </div>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
