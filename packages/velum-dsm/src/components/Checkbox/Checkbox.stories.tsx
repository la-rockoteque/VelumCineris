import type { Meta, StoryObj } from "@storybook/react";

import { Checkbox } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Checkbox",
  component: Checkbox,
} satisfies Meta<typeof Checkbox>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <Checkbox label="Include somatic component" description="Writes the standard boolean state with a readable label." />
    </StoryFrame>
  ),
};
