import type { Meta, StoryObj } from "@storybook/react";

import { Stack } from "../../index";
import { DemoBlock, StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/Stack",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Compact" description="Tight vertical rhythm" minHeight="240px">
          <Stack $gap={2}>
            <DemoBlock>Gap 2</DemoBlock>
            <DemoBlock>Compact</DemoBlock>
            <DemoBlock>Stack</DemoBlock>
          </Stack>
        </StateCase>
        <StateCase label="Relaxed" description="Looser vertical spacing" minHeight="240px">
          <Stack $gap={5}>
            <DemoBlock>Gap 5</DemoBlock>
            <DemoBlock>More air</DemoBlock>
            <DemoBlock>For larger surfaces</DemoBlock>
          </Stack>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
