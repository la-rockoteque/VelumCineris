import type { Meta, StoryObj } from "@storybook/react";

import { InsetCard, InsetLead, InsetTitle } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/InsetCard",
  component: InsetCard,
} satisfies Meta<typeof InsetCard>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <InsetCard>
        <InsetTitle>Language Context</InsetTitle>
        <InsetLead>Inset surfaces are intended for nested summaries, editors, and previews.</InsetLead>
      </InsetCard>
    </StoryFrame>
  ),
};
