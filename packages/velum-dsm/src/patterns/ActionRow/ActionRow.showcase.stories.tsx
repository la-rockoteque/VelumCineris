import type { Meta, StoryObj } from "@storybook/react";

import { ActionRow, Button } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/ActionRow",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame>
      <StateMatrix>
        <StateCase label="Standard" description="Common multi-action row">
          <ActionRow>
            <Button $variant="primary">Save</Button>
            <Button>Reload</Button>
            <Button>Validate</Button>
            <Button $variant="ghost">Reset</Button>
          </ActionRow>
        </StateCase>
        <StateCase label="Wrapping" description="Long labels still wrap cleanly" minHeight="96px">
          <ActionRow>
            <Button $variant="primary">Publish to Google Docs</Button>
            <Button>Generate Homebrewery Preview</Button>
          </ActionRow>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
