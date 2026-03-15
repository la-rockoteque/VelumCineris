import type { Meta, StoryObj } from "@storybook/react";

import { DemoBlock, StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";
import { Section, Subsection } from "../../index";

const meta = {
  title: "Components/Layout/Section",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame>
      <StateMatrix>
        <StateCase label="Nested" description="Section containing multiple subsections" minHeight="260px">
          <Section title="Compendium Section" subtitle="Top-level grouping for related content blocks.">
            <Subsection title="Primary Fields">
              <DemoBlock>Fields, summaries, and nested components can all live inside a section.</DemoBlock>
            </Subsection>
            <Subsection title="Secondary Fields">
              <DemoBlock>Sections are useful when the grouping matters more than a framed surface.</DemoBlock>
            </Subsection>
          </Section>
        </StateCase>
        <StateCase label="Simple" description="Section without nested hierarchy" minHeight="180px">
          <Section title="Simple Section">
            <DemoBlock>Use a section when structure matters more than chrome.</DemoBlock>
          </Section>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
