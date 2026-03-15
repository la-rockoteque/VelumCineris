import type { Meta, StoryObj } from "@storybook/react";

import { PanelGrid } from "../../index";
import { DemoBlock, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Layout/PanelGrid",
  component: PanelGrid,
} satisfies Meta<typeof PanelGrid>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame maxWidth="960px">
      <PanelGrid $min="180px">
        <DemoBlock>Adaptive</DemoBlock>
        <DemoBlock>Auto-fit</DemoBlock>
        <DemoBlock>Panels</DemoBlock>
      </PanelGrid>
    </StoryFrame>
  ),
};
