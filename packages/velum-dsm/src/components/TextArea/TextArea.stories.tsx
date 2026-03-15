import type { Meta, StoryObj } from "@storybook/react";

import { TextArea } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/TextArea",
  component: TextArea,
} satisfies Meta<typeof TextArea>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <label style={{ display: "grid", gap: "8px" }}>
        Prompt Notes
        <TextArea defaultValue="The citadel remembers every translation ever attempted within its walls." />
      </label>
    </StoryFrame>
  ),
};
