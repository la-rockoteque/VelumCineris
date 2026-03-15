import type { Meta, StoryObj } from "@storybook/react";

import { Button } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Button",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Primary" description="High-emphasis action">
          <Button $variant="primary">Primary</Button>
        </StateCase>
        <StateCase label="Secondary" description="Default action style">
          <Button>Secondary</Button>
        </StateCase>
        <StateCase label="Ghost" description="Low-emphasis action">
          <Button $variant="ghost">Ghost</Button>
        </StateCase>
        <StateCase label="Disabled" description="Disabled primary state">
          <Button $variant="primary" disabled>
            Primary Disabled
          </Button>
        </StateCase>
        <StateCase label="Long Label" description="Handles longer action labels" minHeight="96px">
          <Button $variant="primary">Publish to Google Docs</Button>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
