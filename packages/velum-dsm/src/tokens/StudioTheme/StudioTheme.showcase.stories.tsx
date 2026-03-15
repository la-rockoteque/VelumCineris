import type { Meta, StoryObj } from "@storybook/react";

import { Badge, Button, Card, MetaText, studioTheme } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/StudioTheme",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Surface Composition" description="Theme tokens applied as a composed fragment" minHeight="260px">
          <Card title="Studio Theme Showcase" subtitle="Theme tokens applied as a composed interface fragment.">
            <div style={{ display: "grid", gap: "16px" }}>
              <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
                <Badge tone="ok">Healthy</Badge>
                <Badge tone="warn">Pending</Badge>
                <Badge tone="danger">Blocked</Badge>
              </div>
              <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
                <Button $variant="primary">Primary</Button>
                <Button>Secondary</Button>
                <Button $variant="ghost">Ghost</Button>
              </div>
              <MetaText>{Object.entries(studioTheme).map(([key, value]) => `${key}: ${value}`).slice(0, 4).join(" · ")}</MetaText>
            </div>
          </Card>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
