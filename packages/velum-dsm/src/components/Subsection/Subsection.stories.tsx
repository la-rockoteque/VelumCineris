import type { Meta, StoryObj } from "@storybook/react";

import { Subsection } from "../../index";
import { DemoBlock, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Layout/Subsection",
  component: Subsection,
} satisfies Meta<typeof Subsection>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    title: "Subsection",
    subtitle: "Local grouping inside a larger section or card.",
    children: "Subsections tighten hierarchy without introducing a full new surface.",
  },
  render: () => (
    <StoryFrame>
      <Subsection title="Subsection" subtitle="Local grouping inside a larger section or card.">
        <DemoBlock>Subsections tighten hierarchy without introducing a full new surface.</DemoBlock>
      </Subsection>
    </StoryFrame>
  ),
};
