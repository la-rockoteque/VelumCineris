import type { Meta, StoryObj } from "@storybook/react";

import { Card, brickAndMossUrl } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Assets/BrickAndMoss",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="1100px">
      <Card title="Brick And Moss Showcase" subtitle="Background usage across shell, crop, and overlay treatments.">
        <StateMatrix columns="repeat(auto-fit, minmax(260px, 1fr))">
          <StateCase label="Full Bleed" description="App-shell background treatment" minHeight="180px">
            <div
              style={{
                minHeight: "180px",
                borderRadius: "14px",
                border: "1px solid var(--border)",
                background: `url("${brickAndMossUrl}") center / cover no-repeat`,
              }}
            />
          </StateCase>
          <StateCase label="Inset Crop" description="Card or hero fragment" minHeight="180px">
            <div
              style={{
                minHeight: "180px",
                borderRadius: "14px",
                border: "1px solid var(--border)",
                background: `url("${brickAndMossUrl}") 34% center / 145% auto no-repeat`,
              }}
            />
          </StateCase>
          <StateCase label="Veiled Surface" description="Texture beneath UI glass or blur" minHeight="180px">
            <div
              style={{
                minHeight: "180px",
                borderRadius: "14px",
                border: "1px solid var(--border)",
                background: `linear-gradient(rgba(247, 241, 231, 0.68), rgba(247, 241, 231, 0.78)), url("${brickAndMossUrl}") center / cover no-repeat`,
              }}
            />
          </StateCase>
        </StateMatrix>
      </Card>
    </StoryFrame>
  ),
};
