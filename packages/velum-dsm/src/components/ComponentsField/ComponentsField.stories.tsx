import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { ComponentsField } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/ComponentsField",
  component: ComponentsField,
  args: {
    value: "",
    onChange: () => undefined,
  },
} satisfies Meta<typeof ComponentsField>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => {
    const [value, setValue] = useState("V, S, M (a silver bell)");

    return (
      <StoryFrame>
        <ComponentsField value={value} onChange={setValue} />
      </StoryFrame>
    );
  },
};
