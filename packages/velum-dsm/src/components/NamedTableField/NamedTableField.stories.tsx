import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { NamedTableField } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/NamedTableField",
  component: NamedTableField,
  args: {
    value: "",
    keyLabel: "Title",
    valueLabel: "Text",
    onChange: () => undefined,
  },
} satisfies Meta<typeof NamedTableField>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => {
    const [value, setValue] = useState("Trait:: Extra damage; Burst:: Pushes the target 10 feet");

    return (
      <StoryFrame maxWidth="1080px">
        <NamedTableField value={value} keyLabel="Title" valueLabel="Text" onChange={setValue} />
      </StoryFrame>
    );
  },
};
