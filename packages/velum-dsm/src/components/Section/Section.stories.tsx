import type { Meta, StoryObj } from "@storybook/react";

import { Section } from "../../index";
import { DemoBlock, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Layout/Section",
  component: Section,
} satisfies Meta<typeof Section>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    title: "Section",
    subtitle: "Mid-level page grouping for related content.",
    children: "Sections are useful when the content belongs together but does not need a framed card.",
  },
  render: () => (
    <StoryFrame>
      <Section title="Section" subtitle="Mid-level page grouping for related content.">
        <DemoBlock>Sections are useful when the content belongs together but does not need a framed card.</DemoBlock>
      </Section>
    </StoryFrame>
  ),
};
