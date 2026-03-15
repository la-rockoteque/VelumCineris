import type { Meta, StoryObj } from "@storybook/react";

import { InlineButton } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/InlineButton",
  component: InlineButton,
} satisfies Meta<typeof InlineButton>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
        <InlineButton>Quick Edit</InlineButton>
        <InlineButton $variant="primary">Apply</InlineButton>
        <InlineButton $variant="ghost">Dismiss</InlineButton>
      </div>
    </StoryFrame>
  ),
};
