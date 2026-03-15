import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { ComponentsField } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/ComponentsField",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

function ExampleField(props: { initialValue: string }) {
  const [value, setValue] = useState(props.initialValue);
  return <ComponentsField value={value} onChange={setValue} />;
}

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Empty" description="No components selected" minHeight="150px">
          <ExampleField initialValue="" />
        </StateCase>
        <StateCase label="Verbal and Somatic" description="Common spell setup" minHeight="150px">
          <ExampleField initialValue="V, S" />
        </StateCase>
        <StateCase label="Material Note" description="Supports material details" minHeight="150px">
          <ExampleField initialValue="V, M (a pearl worth 100 gp)" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
