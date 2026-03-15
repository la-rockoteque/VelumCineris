import type { Meta, StoryObj } from "@storybook/react";

import { Badge } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Badge",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame>
      <StateMatrix>
        <StateCase label="Info" description="Neutral informative status">
          <Badge tone="info">Queued</Badge>
        </StateCase>
        <StateCase label="Ok" description="Positive system or workflow status">
          <Badge tone="ok">Healthy</Badge>
        </StateCase>
        <StateCase label="Warn" description="Needs attention but not blocked">
          <Badge tone="warn">Pending Review</Badge>
        </StateCase>
        <StateCase label="Danger" description="Blocked or failed state">
          <Badge tone="danger">Blocked</Badge>
        </StateCase>
        <StateCase label="Long Label" description="Badge handles longer summary content" minHeight="96px">
          <Badge tone="info">Sheet: Modern Lexicon</Badge>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
