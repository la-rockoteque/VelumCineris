import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { DelimitedListField } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/DelimitedListField",
  component: DelimitedListField,
  args: {
    value: "",
    onChange: () => undefined,
  },
} satisfies Meta<typeof DelimitedListField>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => {
    const [value, setValue] = useState("Fire, Cold");

    return (
      <StoryFrame maxWidth="980px">
        <DelimitedListField value={value} options={["Fire", "Cold", "Lightning", "Poison"]} onChange={setValue} />
      </StoryFrame>
    );
  },
};
