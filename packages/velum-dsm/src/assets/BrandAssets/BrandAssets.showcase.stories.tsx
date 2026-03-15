import type { Meta, StoryObj } from "@storybook/react";

import { CornerFlourish, RuneDivider, SigilMark, brandAssets } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Assets/BrandAssets",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Brand Tone" description={brandAssets.tone}>
          <div style={{ display: "grid", gap: "6px" }}>
            <div>Marks: {brandAssets.marks.join(", ")}</div>
            <div>Icons: {brandAssets.icons.join(", ")}</div>
            <div>Surfaces: {brandAssets.surfaces.join(", ")}</div>
            <div>Motion: {brandAssets.motion.join(", ")}</div>
          </div>
        </StateCase>
        <StateCase label="Primary Mark" description="SigilMark">
          <SigilMark style={{ width: "72px" }} />
        </StateCase>
        <StateCase label="Divider" description="RuneDivider">
          <RuneDivider style={{ width: "100%" }} />
        </StateCase>
        <StateCase label="Flourish" description="CornerFlourish">
          <CornerFlourish style={{ width: "48px" }} />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
