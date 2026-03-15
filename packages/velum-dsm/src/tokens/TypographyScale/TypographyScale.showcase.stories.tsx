import type { Meta, StoryObj } from "@storybook/react";

import { typographyScale } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/TypographyScale",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix columns="1fr">
        {Object.entries(typographyScale.size).map(([token, value]) => (
          <StateCase key={token} label={token} description={`font-size ${value}`} minHeight="140px">
            <div style={{ fontFamily: typographyScale.display, fontSize: value, letterSpacing: typographyScale.tracking.normal, textTransform: "uppercase" }}>
              {token} heading sample
            </div>
          </StateCase>
        ))}
      </StateMatrix>
    </StoryFrame>
  ),
};
