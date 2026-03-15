import type { Meta, StoryObj } from "@storybook/react";

import { SelectInput, TextInput, Toolbar } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/Toolbar",
  component: Toolbar,
} satisfies Meta<typeof Toolbar>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame maxWidth="960px">
      <Toolbar>
        <label style={{ display: "grid", gap: "8px" }}>
          Source
          <SelectInput defaultValue="translator">
            <option value="translator">Translator</option>
            <option value="formatter">Formatter</option>
          </SelectInput>
        </label>
        <label style={{ display: "grid", gap: "8px" }}>
          Filter
          <TextInput defaultValue="Archive" />
        </label>
      </Toolbar>
    </StoryFrame>
  ),
};
