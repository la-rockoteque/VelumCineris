import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { DiceField } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/DiceField",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

function ExampleField(props: { initialValue: string; diceTypes?: number[] }) {
  const [value, setValue] = useState(props.initialValue);
  return <DiceField value={value} onChange={setValue} diceTypes={props.diceTypes} />;
}

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Standard" description="Classic hit dice expression" minHeight="120px">
          <ExampleField initialValue="5d10+10" />
        </StateCase>
        <StateCase label="Blank" description="Starts empty until the user composes a value" minHeight="120px">
          <ExampleField initialValue="" />
        </StateCase>
        <StateCase label="Custom Dice Set" description="Allows non-default dice sizes" minHeight="120px">
          <ExampleField initialValue="2d3+1" diceTypes={[3, 4, 6, 8, 10, 12]} />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
