import type { Meta, StoryObj } from "@storybook/react";

import { TextInput } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/TextInput",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Default" description="Standard populated text input">
          <TextInput defaultValue="Ashmarked Archive" />
        </StateCase>
        <StateCase label="Placeholder" description="Empty input with hint text">
          <TextInput placeholder="Search by title or row number" />
        </StateCase>
        <StateCase label="Disabled" description="Read-only unavailable state">
          <TextInput defaultValue="Locked field" disabled />
        </StateCase>
        <StateCase label="Numeric" description="Text input also covers numeric entry">
          <TextInput type="number" defaultValue="12" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
