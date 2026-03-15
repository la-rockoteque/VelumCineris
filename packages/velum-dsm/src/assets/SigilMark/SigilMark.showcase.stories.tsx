import type { Meta, StoryObj } from "@storybook/react";

import { Card, SigilMark } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Assets/SigilMark",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

const cases = [
  { label: "Small", width: "48px", color: "var(--accent-soft)" },
  { label: "Default", width: "88px", color: "var(--accent)" },
  { label: "Large", width: "132px", color: "var(--ink)" },
];

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <Card title="Sigil Mark Showcase" subtitle="Scale and tone variations for the primary emblem.">
        <StateMatrix>
          {cases.map((item) => (
            <StateCase
              key={item.label}
              label={item.label}
              description={`${item.width} · ${item.color.replace("var(", "").replace(")", "")}`}
              minHeight="120px"
            >
              <SigilMark style={{ width: item.width, color: item.color }} />
            </StateCase>
          ))}
        </StateMatrix>
      </Card>
    </StoryFrame>
  ),
};
