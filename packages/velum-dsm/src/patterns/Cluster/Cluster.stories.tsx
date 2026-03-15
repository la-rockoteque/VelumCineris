import type { Meta, StoryObj } from "@storybook/react";

import { Button, Cluster } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/Cluster",
  component: Cluster,
} satisfies Meta<typeof Cluster>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <Cluster $gap={2}>
        <Button $variant="primary">Publish</Button>
        <Button>Preview</Button>
        <Button $variant="ghost">Cancel</Button>
      </Cluster>
    </StoryFrame>
  ),
};
