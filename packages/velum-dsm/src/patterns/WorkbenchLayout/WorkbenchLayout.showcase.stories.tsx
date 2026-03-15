import type { Meta, StoryObj } from "@storybook/react";

import { Button, InsetCard, InsetLead, InsetTitle, MetaText, WorkbenchLayout, WorkbenchMain, WorkbenchSidebar, WorkspaceOutput } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/WorkbenchLayout",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="1100px">
      <StateMatrix columns="1fr" gap="20px">
        <StateCase label="Balanced Layout" description="Standard sidebar + result surface" minHeight="380px">
          <WorkbenchLayout>
            <WorkbenchSidebar>
              <InsetCard>
                <InsetTitle>Controls</InsetTitle>
                <InsetLead>Sidebar area for filters, forms, and quick actions.</InsetLead>
                <Button $variant="primary">Run</Button>
                <Button>Reload</Button>
              </InsetCard>
              <InsetCard>
                <InsetTitle>Summary</InsetTitle>
                <MetaText>2 pending changes</MetaText>
              </InsetCard>
            </WorkbenchSidebar>
            <WorkbenchMain>
              <InsetCard>
                <InsetTitle>Results</InsetTitle>
                <WorkspaceOutput>{`romanized: ashmar\nsymbolized: ASH-MR`}</WorkspaceOutput>
              </InsetCard>
            </WorkbenchMain>
          </WorkbenchLayout>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
