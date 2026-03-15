import type { Meta, StoryObj } from "@storybook/react";

import { InlineButton } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/InlineButton",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame>
      <StateMatrix>
        <StateCase label="Secondary" description="Default inline action">
          <InlineButton>Quick Edit</InlineButton>
        </StateCase>
        <StateCase label="Primary" description="High-emphasis inline action">
          <InlineButton $variant="primary">Apply</InlineButton>
        </StateCase>
        <StateCase label="Ghost" description="Muted inline action">
          <InlineButton $variant="ghost">Dismiss</InlineButton>
        </StateCase>
        <StateCase label="Disabled" description="Unavailable inline action">
          <InlineButton disabled>Disabled</InlineButton>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
