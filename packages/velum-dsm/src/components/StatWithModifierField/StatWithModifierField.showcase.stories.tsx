import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { StatWithModifierField } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/StatWithModifierField",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

function Example(props: { initialValue: string }) {
  const [value, setValue] = useState(props.initialValue);
  return <StatWithModifierField value={value} onChange={setValue} />;
}

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Positive Modifier" description="Standard ability score compound field" minHeight="120px">
          <Example initialValue="14" />
        </StateCase>
        <StateCase label="Zero Modifier" description="Centerline score" minHeight="120px">
          <Example initialValue="10" />
        </StateCase>
        <StateCase label="Negative Modifier" description="Low-score presentation" minHeight="120px">
          <Example initialValue="7" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
