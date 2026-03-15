import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { NamedTableField } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/NamedTableField",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

function Example(props: { initialValue: string }) {
  const [value, setValue] = useState(props.initialValue);
  return <NamedTableField value={value} keyLabel="Title" valueLabel="Text" onChange={setValue} />;
}

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="1240px">
      <StateMatrix columns="1fr">
        <StateCase label="Trait Rows" description="Compound row editor with glued cells" minHeight="280px">
          <Example initialValue="Trait:: Extra damage; Burst:: Pushes the target 10 feet" />
        </StateCase>
        <StateCase label="Single Blank Row" description="Starts with one editable row when there is no serialized data" minHeight="220px">
          <Example initialValue="" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
