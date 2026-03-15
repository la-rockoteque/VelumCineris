import type { Meta, StoryObj } from "@storybook/react";

import { Table, TableWrap } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Table",
  component: Table,
  args: {
    columns: [],
    rows: [],
    onRowClick: () => undefined,
  },
} satisfies Meta<typeof Table<Record<string, unknown>>>;

export default meta;

type Story = StoryObj<typeof meta>;

const rows = [
  { name: "Magic Missile", level: "1", school: "Evocation" },
  { name: "Shield", level: "1", school: "Abjuration" },
  { name: "Counterspell", level: "3", school: "Abjuration" },
];

export const Default: Story = {
  render: () => (
    <StoryFrame maxWidth="980px">
      <TableWrap>
        <Table
          rows={rows}
          onRowClick={() => undefined}
          columns={[
            { key: "name", header: "Name" },
            { key: "level", header: "Level", width: "90px" },
            { key: "school", header: "School" },
          ]}
        />
      </TableWrap>
    </StoryFrame>
  ),
};
