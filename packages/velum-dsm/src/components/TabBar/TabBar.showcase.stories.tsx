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
        { key: "spells", label: "Spells" },
        { key: "monsters", label: "Monsters" },
        { key: "feats", label: "Feats" },
        { key: "species", label: "Species", disabled: true },
      ]}
    />
  );
}

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="1080px">
      <StateMatrix>
        <StateCase label="Sheet Selector" description="Default stepped sheet tabs" minHeight="120px">
          <ExampleTabs activeKey="spells" layout="grid" />
        </StateCase>
        <StateCase label="Compact Tabs" description="Smaller tab treatment for dense spaces" minHeight="120px">
          <ExampleTabs activeKey="monsters" layout="wrap" size="sm" />
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
