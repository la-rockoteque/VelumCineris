import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { SegmentedControl } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/SegmentedControl",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

function Example(props: { initialValue: string; options: Array<{ value: string; label: string; disabled?: boolean }> }) {
  const [value, setValue] = useState(props.initialValue);
  return <SegmentedControl ariaLabel="Example choices" value={value} onChange={setValue} options={props.options} />;
}

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Binary Choice" description="Short high-signal decision set" minHeight="120px">
          <Example
            initialValue="dry_run"
            options={[
              { value: "dry_run", label: "Dry Run" },
              { value: "live", label: "Live Execute" },
            ]}
          />
        </StateCase>
        <StateCase label="Three Options" description="Small enum picker" minHeight="120px">
          <Example
            initialValue="balance"
            options={[
              { value: "balance", label: "Balance" },
              { value: "rewrite", label: "Rewrite" },
              { value: "qa", label: "QA" },
            ]}
          />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
