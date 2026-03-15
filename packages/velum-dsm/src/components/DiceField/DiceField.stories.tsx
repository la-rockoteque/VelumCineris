import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { DiceField } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/DiceField",
  component: DiceField,
  args: {
    value: "",
    onChange: () => undefined,
  },
} satisfies Meta<typeof DiceField>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => {
    const [value, setValue] = useState("3d8+2");

    return (
      <StoryFrame>
        <DiceField value={value} onChange={setValue} />
      </StoryFrame>
    );
  },
};
