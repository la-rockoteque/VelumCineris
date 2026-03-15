import type { Meta, StoryObj } from "@storybook/react";

import { SelectInput } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/SelectInput",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <StateMatrix>
        <StateCase label="Default" description="Standard select with short options">
          <SelectInput defaultValue="translator">
            <option value="translator">Translator</option>
            <option value="formatter">Formatter</option>
            <option value="timeline">Timeline</option>
          </SelectInput>
        </StateCase>
        <StateCase label="Long Options" description="Long labels remain readable">
          <SelectInput defaultValue="modern">
            <option value="modern">Modern Lexicon and Reference Materials</option>
            <option value="fantasy">Fantasy Bestiary and Spell Catalog</option>
          </SelectInput>
        </StateCase>
        <StateCase label="Disabled" description="Unavailable select state">
          <SelectInput defaultValue="locked" disabled>
            <option value="locked">Selection locked</option>
          </SelectInput>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
