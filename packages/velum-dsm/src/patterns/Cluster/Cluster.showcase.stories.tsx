import type { Meta, StoryObj } from "@storybook/react";

import { Button, Cluster } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/Cluster",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame>
      <StateMatrix>
        <StateCase label="Wrapped Actions" description="Cluster handles mixed-width actions">
          <Cluster $gap={2}>
            <Button $variant="primary">Translate</Button>
            <Button>Reload Context</Button>
            <Button $variant="ghost">Pronunciation</Button>
            <Button disabled>Disabled</Button>
          </Cluster>
        </StateCase>
        <StateCase label="Spaced Between" description="Can distribute content across a row">
          <Cluster $gap={2} $justify="space-between">
            <Button>Back</Button>
            <Button $variant="primary">Continue</Button>
          </Cluster>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
