import type { Meta, StoryObj } from "@storybook/react";

import { PanelGrid } from "../../index";
import { DemoBlock, StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Layout/PanelGrid",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="1100px">
      <StateMatrix>
        <StateCase label="Four Panels" description="Balanced grid with equal cards" minHeight="260px">
          <PanelGrid $min="200px">
            <DemoBlock>Panel 1</DemoBlock>
            <DemoBlock>Panel 2</DemoBlock>
            <DemoBlock>Panel 3</DemoBlock>
            <DemoBlock>Panel 4</DemoBlock>
          </PanelGrid>
        </StateCase>
        <StateCase label="Narrow Min Width" description="More aggressive auto-fit layout" minHeight="260px">
          <PanelGrid $min="140px">
            <DemoBlock>A</DemoBlock>
            <DemoBlock>B</DemoBlock>
            <DemoBlock>C</DemoBlock>
            <DemoBlock>D</DemoBlock>
            <DemoBlock>E</DemoBlock>
          </PanelGrid>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
