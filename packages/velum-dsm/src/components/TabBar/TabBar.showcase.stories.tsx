import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { TabBar } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/TabBar",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

function ExampleTabs(props: { activeKey: string; layout?: "grid" | "wrap"; size?: "md" | "sm" }) {
  const [active, setActive] = useState(props.activeKey);

  return (
    <TabBar
      ariaLabel="Example tabs"
      activeKey={active}
      onChange={setActive}
      layout={props.layout}
      size={props.size}
      items={[
        { key: "overview", label: "Overview" },
        { key: "spellbook", label: "Spellbook" },
        { key: "integrations", label: "Integrations" },
        { key: "history", label: "History", disabled: true },
      ]}
    />
  );
}

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="1080px">
      <StateMatrix>
        <StateCase label="Grid Layout" description="Primary top-level navigation" minHeight="120px">
          <ExampleTabs activeKey="overview" layout="grid" />
        </StateCase>
        <StateCase label="Wrapped Layout" description="Compact sheet or subsection tabs" minHeight="120px">
          <ExampleTabs activeKey="spellbook" layout="wrap" size="sm" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
