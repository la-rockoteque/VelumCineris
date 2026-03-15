import type { Meta, StoryObj } from "@storybook/react";

import { Subsection } from "../../index";
import { DemoBlock, StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Layout/Subsection",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Minimal" description="Title only subsection" minHeight="180px">
          <Subsection title="General">
            <DemoBlock>Lightweight nested grouping.</DemoBlock>
          </Subsection>
        </StateCase>
        <StateCase label="With Subtitle" description="Optional subtitle support" minHeight="180px">
          <Subsection title="Relations" subtitle="Optional subtitle support.">
            <DemoBlock>Use subsections to split content without adding a card shell.</DemoBlock>
          </Subsection>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
