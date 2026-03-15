import type { Meta, StoryObj } from "@storybook/react";

import { SelectInput } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/SelectInput",
  component: SelectInput,
} satisfies Meta<typeof SelectInput>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <label style={{ display: "grid", gap: "8px" }}>
        Target
        <SelectInput defaultValue="translator">
          <option value="translator">Translator</option>
          <option value="formatter">Formatter</option>
          <option value="timeline">Timeline</option>
        </SelectInput>
      </label>
    </StoryFrame>
  ),
};
