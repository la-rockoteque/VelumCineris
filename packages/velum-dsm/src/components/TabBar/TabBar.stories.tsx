import { useState } from "react";
import type { Meta, StoryObj } from "@storybook/react";

import { TabBar } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/TabBar",
  component: TabBar,
  args: {
    items: [],
    activeKey: "",
    onChange: () => undefined,
    ariaLabel: "Tabs",
  },
} satisfies Meta<typeof TabBar>;

export default meta;

type Story = StoryObj<typeof meta>;

const items = [
  { key: "compendium", label: "Compendium" },
  { key: "details", label: "Details" },
  { key: "translator", label: "Translator" },
  { key: "image", label: "Image" },
];

export const Default: Story = {
  render: () => {
    const [active, setActive] = useState("compendium");

    return (
      <StoryFrame maxWidth="980px">
        <TabBar ariaLabel="Sheet selector" items={items} activeKey={active} onChange={setActive} />
      </StoryFrame>
    );
  },
};
