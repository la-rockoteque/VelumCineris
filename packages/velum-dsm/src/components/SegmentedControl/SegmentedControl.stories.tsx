import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { SegmentedControl } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/SegmentedControl",
  component: SegmentedControl,
  args: {
    value: "",
    options: [],
    onChange: () => undefined,
    ariaLabel: "Choices",
  },
} satisfies Meta<typeof SegmentedControl>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => {
    const [value, setValue] = useState("dry_run");

    return (
      <StoryFrame>
        <SegmentedControl
          ariaLabel="Mode"
          value={value}
          onChange={setValue}
          options={[
            { value: "dry_run", label: "Dry Run" },
            { value: "live", label: "Live Execute" },
          ]}
        />
      </StoryFrame>
    );
  },
};
