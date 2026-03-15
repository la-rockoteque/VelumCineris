import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { StatWithModifierField } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/StatWithModifierField",
  component: StatWithModifierField,
  args: {
    value: "",
    onChange: () => undefined,
  },
} satisfies Meta<typeof StatWithModifierField>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => {
    const [value, setValue] = useState("14");

    return (
      <StoryFrame>
        <StatWithModifierField value={value} onChange={setValue} />
      </StoryFrame>
    );
  },
};
