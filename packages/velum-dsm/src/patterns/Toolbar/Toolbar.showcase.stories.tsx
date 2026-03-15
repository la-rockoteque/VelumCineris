import type { Meta, StoryObj } from "@storybook/react";

import { SelectInput, TextArea, TextInput, Toolbar } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/Toolbar",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="1100px">
      <StateMatrix>
        <StateCase label="Mixed Controls" description="Toolbar with select, input, and textarea" minHeight="260px">
          <Toolbar>
            <label style={{ display: "grid", gap: "8px" }}>
              Source
              <SelectInput defaultValue="translator">
                <option value="translator">Translator</option>
                <option value="formatter">Formatter</option>
              </SelectInput>
            </label>
            <label style={{ display: "grid", gap: "8px" }}>
              Sheet
              <SelectInput defaultValue="modern">
                <option value="modern">Modern Lexicon</option>
                <option value="fantasy">Fantasy Bestiary</option>
              </SelectInput>
            </label>
            <label style={{ display: "grid", gap: "8px" }}>
              Search
              <TextInput defaultValue="Ashmarked" />
            </label>
            <label style={{ display: "grid", gap: "8px" }}>
              Notes
              <TextArea defaultValue="Toolbar children can be any form controls." rows={4} />
            </label>
          </Toolbar>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
