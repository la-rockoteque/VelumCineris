import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { DelimitedListField } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/DelimitedListField",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

function Example(props: { initialValue: string; options?: string[] }) {
  const [value, setValue] = useState(props.initialValue);
  return <DelimitedListField value={value} onChange={setValue} options={props.options} />;
}

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="1080px">
      <StateMatrix columns="1fr">
        <StateCase label="Suggested Values" description="Editable rows with datalist suggestions" minHeight="220px">
          <Example initialValue="Fire, Cold" options={["Fire", "Cold", "Lightning", "Poison"]} />
        </StateCase>
        <StateCase label="Blank List" description="Begins with a single empty editable row" minHeight="180px">
          <Example initialValue="" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
