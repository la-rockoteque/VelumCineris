import type { Meta, StoryObj } from "@storybook/react";

import { Badge, Table, TableWrap } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Table",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

const spellRows = [
  { name: "Magic Missile", level: 1, status: "Ready" },
  { name: "Fireball", level: 3, status: "Draft" },
  { name: "Teleport", level: 7, status: "Published" },
];

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="1080px">
      <StateMatrix>
        <StateCase label="Standard Rows" description="Default striped dataset" minHeight="260px">
          <TableWrap>
            <Table
              rows={spellRows}
              columns={[
                { key: "name", header: "Spell" },
                { key: "level", header: "Level", align: "center", width: "90px" },
                {
                  key: "status",
                  header: "Status",
                  width: "140px",
                  render: (row) => <Badge>{String(row.status)}</Badge>,
                },
              ]}
            />
          </TableWrap>
        </StateCase>
        <StateCase label="Empty State" description="No results available" minHeight="260px">
          <TableWrap>
            <Table
              rows={[]}
              emptyMessage="No matching entries."
              columns={[
                { key: "name", header: "Name" },
                { key: "type", header: "Type" },
              ]}
            />
          </TableWrap>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
