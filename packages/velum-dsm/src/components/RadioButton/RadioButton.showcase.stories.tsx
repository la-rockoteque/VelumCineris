import type { Meta, StoryObj } from "@storybook/react";

import { RadioButton } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/RadioButton",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Unchecked" description="Available radio option">
          <RadioButton name="publish-mode-a" label="Dry Run" />
        </StateCase>
        <StateCase label="Checked" description="Selected radio option">
          <RadioButton name="publish-mode-b" label="Live Execute" checked readOnly />
        </StateCase>
        <StateCase label="With Description" description="Additional context">
          <RadioButton name="publish-mode-c" label="Publish and Sync" description="Use when all linked destinations should receive updates." />
        </StateCase>
        <StateCase label="Disabled" description="Unavailable option">
          <RadioButton name="publish-mode-d" label="Locked" disabled />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
