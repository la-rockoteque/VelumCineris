import type { Meta, StoryObj } from "@storybook/react";

import { InsetCard, InsetTitle, WorkbenchLayout, WorkbenchMain, WorkbenchSidebar } from "../../index";
import { DemoBlock, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/WorkbenchLayout",
  component: WorkbenchLayout,
} satisfies Meta<typeof WorkbenchLayout>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame maxWidth="1100px">
      <WorkbenchLayout>
        <WorkbenchSidebar>
          <InsetCard>
            <InsetTitle>Controls</InsetTitle>
            <DemoBlock minHeight="96px">Sidebar area for filters, forms, and actions.</DemoBlock>
          </InsetCard>
        </WorkbenchSidebar>
        <WorkbenchMain>
          <InsetCard>
            <InsetTitle>Results</InsetTitle>
            <DemoBlock minHeight="180px">Main area for previews, tables, or structured output.</DemoBlock>
          </InsetCard>
        </WorkbenchMain>
      </WorkbenchLayout>
    </StoryFrame>
  ),
};
