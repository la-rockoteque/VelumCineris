import type { Meta, StoryObj } from "@storybook/react";

import { Card, iconAssets } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Assets/Icons",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <Card title="Icons Showcase" subtitle="Full icon set rendered across common sizing treatments.">
        <StateMatrix columns="repeat(auto-fit, minmax(240px, 1fr))">
          {Object.entries(iconAssets).map(([name, url]) => (
            <StateCase key={name} label={name} description="16px, 32px, 64px" minHeight="120px">
              <div style={{ display: "flex", alignItems: "center", gap: "16px", flexWrap: "wrap" }}>
                <img src={url} alt={`${name} 16`} style={{ width: "16px", height: "16px" }} />
                <img src={url} alt={`${name} 32`} style={{ width: "32px", height: "32px" }} />
                <img src={url} alt={`${name} 64`} style={{ width: "64px", height: "64px" }} />
              </div>
            </StateCase>
          ))}
        </StateMatrix>
      </Card>
    </StoryFrame>
  ),
};
