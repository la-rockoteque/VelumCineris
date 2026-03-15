import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { MultiSelect } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/MultiSelect",
  component: MultiSelect,
  args: {
    value: "",
    options: [],
    onChange: () => undefined,
  },
} satisfies Meta<typeof MultiSelect>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => {
    const [value, setValue] = useState("Fire, Cold");

    return (
      <StoryFrame>
        <MultiSelect value={value} options={["Fire", "Cold", "Force", "Necrotic"]} onChange={setValue} placeholder="Pick tags" />
      </StoryFrame>
    );
  },
};
