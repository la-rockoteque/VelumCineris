import type { Meta, StoryObj } from "@storybook/react";

import { ActionRow, Button, Card, MetaText } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Layout/Card",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Standard" description="Title, subtitle, metadata, and actions" minHeight="220px">
          <Card title="Editorial Card" subtitle="Standard framed content.">
            <MetaText>Cards can host summary text, metadata, and nested actions.</MetaText>
            <ActionRow>
              <Button $variant="primary">Publish</Button>
              <Button>Preview</Button>
            </ActionRow>
          </Card>
        </StateCase>
        <StateCase label="Title Only" description="Subtitle is optional" minHeight="220px">
          <Card title="No Subtitle">
            <p style={{ margin: 0 }}>The subtitle is optional, and cards still keep a stable internal rhythm.</p>
          </Card>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
