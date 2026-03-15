import type { Meta, StoryObj } from "@storybook/react";

import { WorkspaceCard, WorkspaceLead, WorkspaceOutput, WorkspaceTitle } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Workspace/WorkspaceCard",
  component: WorkspaceCard,
} satisfies Meta<typeof WorkspaceCard>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <WorkspaceCard>
        <WorkspaceTitle>Translator</WorkspaceTitle>
        <WorkspaceLead>Primary shell for interactive tool screens.</WorkspaceLead>
        <WorkspaceOutput>{`status: ready\nsource: modern_lexicon`}</WorkspaceOutput>
      </WorkspaceCard>
    </StoryFrame>
  ),
};
