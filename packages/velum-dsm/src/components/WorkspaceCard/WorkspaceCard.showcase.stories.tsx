import type { Meta, StoryObj } from "@storybook/react";

import { ActionRow, Button, MetaText, WorkspaceCard, WorkspaceLead, WorkspaceOutput, WorkspaceTitle } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Workspace/WorkspaceCard",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame>
      <StateMatrix>
        <StateCase label="Tool Shell" description="Title, lead, metadata, actions, and output" minHeight="320px">
          <WorkspaceCard>
            <WorkspaceTitle>Translator</WorkspaceTitle>
            <WorkspaceLead>Primary shell for interactive tool screens.</WorkspaceLead>
            <MetaText>Last synced 2 minutes ago</MetaText>
            <ActionRow>
              <Button $variant="primary">Run</Button>
              <Button>Reload</Button>
            </ActionRow>
            <WorkspaceOutput>{`status: ready\nsource: modern_lexicon\ntarget: translator`}</WorkspaceOutput>
          </WorkspaceCard>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
