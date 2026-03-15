import type { Meta, StoryObj } from "@storybook/react";

import { TextArea } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/TextArea",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix columns="repeat(auto-fit, minmax(280px, 1fr))">
        <StateCase label="Short Note" description="Compact authored content" minHeight="170px">
          <TextArea defaultValue="This item needs a stronger visual motif." />
        </StateCase>
        <StateCase label="Long Draft" description="Longer multi-line content" minHeight="170px">
          <TextArea defaultValue="The citadel remembers every translation ever attempted within its walls. Each inscription leaves a trace in the ash-lined vaults below the archive." />
        </StateCase>
        <StateCase label="Disabled" description="Unavailable textarea state" minHeight="170px">
          <TextArea defaultValue="Locked textarea content" disabled />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
