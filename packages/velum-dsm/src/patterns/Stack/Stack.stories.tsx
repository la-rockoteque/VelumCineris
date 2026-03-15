import type { Meta, StoryObj } from "@storybook/react";

import { Stack } from "../../index";
import { DemoBlock, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/Stack",
  component: Stack,
} satisfies Meta<typeof Stack>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <Stack $gap={4}>
        <DemoBlock>First item</DemoBlock>
        <DemoBlock>Second item</DemoBlock>
        <DemoBlock>Third item</DemoBlock>
      </Stack>
    </StoryFrame>
  ),
};
