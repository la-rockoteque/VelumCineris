import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { RadioButton } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/RadioButton",
  component: RadioButton,
} satisfies Meta<typeof RadioButton>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => {
    const [value, setValue] = useState("dry_run");

    return (
      <StoryFrame>
        <div style={{ display: "grid", gap: "12px" }}>
          <RadioButton
            name="mode"
            label="Dry Run"
            description="Preview the outbound payload without sending it."
            checked={value === "dry_run"}
            onChange={() => setValue("dry_run")}
          />
          <RadioButton
            name="mode"
            label="Live Execute"
            description="Send changes to the integration target."
            checked={value === "live"}
            onChange={() => setValue("live")}
          />
        </div>
      </StoryFrame>
    );
  },
};
