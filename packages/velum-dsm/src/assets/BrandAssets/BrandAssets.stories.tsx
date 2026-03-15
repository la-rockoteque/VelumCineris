import type { Meta, StoryObj } from "@storybook/react";

import { brandAssets } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Assets/BrandAssets",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <pre style={{ margin: 0 }}>{JSON.stringify(brandAssets, null, 2)}</pre>
    </StoryFrame>
  ),
};
