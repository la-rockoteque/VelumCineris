import type { Meta, StoryObj } from "@storybook/react";

import { Card, diceLottieUrl } from "../../index";

const meta = {
  title: "Assets/DiceLottie",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <Card title="Dice Lottie" subtitle="Looping animation asset used by loading surfaces and tool feedback.">
      <div style={{ display: "grid", gap: "12px" }}>
        <div style={{ color: "var(--ink-soft)", fontSize: "0.9rem" }}>
          `.lottie` animation asset exported by the DSM for runtime loaders.
        </div>
        <code style={{ wordBreak: "break-all" }}>{diceLottieUrl}</code>
      </div>
    </Card>
  ),
};
