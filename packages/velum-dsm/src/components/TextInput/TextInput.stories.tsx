import type { Meta, StoryObj } from "@storybook/react";

import { TextInput } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/TextInput",
  component: TextInput,
} satisfies Meta<typeof TextInput>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <label style={{ display: "grid", gap: "8px" }}>
        Archive Name
        <TextInput defaultValue="Ashmarked Archive" />
      </label>
    </StoryFrame>
  ),
};
