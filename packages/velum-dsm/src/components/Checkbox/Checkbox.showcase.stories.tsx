import type { Meta, StoryObj } from "@storybook/react";

import { Checkbox } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Checkbox",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Unchecked" description="Default checkbox state">
          <Checkbox label="Verbal component" />
        </StateCase>
        <StateCase label="Checked" description="Selected state">
          <Checkbox label="Somatic component" checked readOnly />
        </StateCase>
        <StateCase label="With Description" description="Supports helper copy">
          <Checkbox label="Material component" description="Enable when a spell consumes or references a material requirement." />
        </StateCase>
        <StateCase label="Disabled" description="Unavailable control">
          <Checkbox label="Published" checked disabled />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
