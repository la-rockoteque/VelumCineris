import type { Meta, StoryObj } from "@storybook/react";

import { ActionRowEnd, Button } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/ActionRowEnd",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame>
      <StateMatrix>
        <StateCase label="Standard" description="Right-aligned terminal actions">
          <ActionRowEnd>
            <Button>Back</Button>
            <Button>Save Draft</Button>
            <Button $variant="primary">Continue</Button>
          </ActionRowEnd>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
