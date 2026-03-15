import type { Meta, StoryObj } from "@storybook/react";

import { TableWrap } from "../../index";
import { StateCase, StateMatrix, StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Patterns/TableWrap",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Showcase: Story = {
  render: () => (
    <StoryFrame maxWidth="1100px">
      <StateMatrix columns="1fr">
        <StateCase label="Wide Data Table" description="Horizontal overflow preserved for larger tables" minHeight="260px">
          <TableWrap>
            <table style={{ width: "100%", minWidth: "760px", borderCollapse: "collapse" }}>
              <thead>
                <tr>
                  {["Source", "Sheet", "Rows", "Updated", "Owner", "Status"].map((heading) => (
                    <th key={heading} style={{ textAlign: "left", padding: "12px" }}>
                      {heading}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {[
                  ["Modern", "Lexicon", "312", "Today", "Rocko", "Healthy"],
                  ["Fantasy", "Bestiary", "128", "Yesterday", "Rocko", "Pending"],
                  ["Shared", "Timeline", "42", "Today", "Team", "Healthy"],
                ].map((row) => (
                  <tr key={row.join("-")}>
                    {row.map((cell) => (
                      <td key={cell} style={{ padding: "12px" }}>
                        {cell}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </TableWrap>
        </StateCase>
      </StateMatrix>
    </StoryFrame>
  ),
};
