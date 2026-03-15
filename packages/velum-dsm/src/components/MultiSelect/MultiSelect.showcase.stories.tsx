import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { MultiSelect } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/MultiSelect",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

function Example(props: { initialValue: string }) {
  const [value, setValue] = useState(props.initialValue);

  return (
    <MultiSelect
      value={value}
      onChange={setValue}
      options={["Fire", "Cold", "Force", "Necrotic", "Radiant"]}
      placeholder="Pick tags"
    />
  );
}

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Empty" description="Prompt-first enum picker" minHeight="120px">
          <Example initialValue="" />
        </StateCase>
        <StateCase label="Selected Tags" description="Shows selected items as pills" minHeight="120px">
          <Example initialValue="Fire, Force" />
        </StateCase>
        <StateCase label="Many Values" description="Wraps pills inside the same control shell" minHeight="120px">
          <Example initialValue="Fire, Cold, Force, Necrotic" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
