import type { Meta, StoryObj } from "@storybook/react";

import { TableWrap } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Components/Layout/TableWrap",
  component: TableWrap,
} satisfies Meta<typeof TableWrap>;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame maxWidth="960px">
      <TableWrap>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={{ textAlign: "left", padding: "12px" }}>Column</th>
              <th style={{ textAlign: "left", padding: "12px" }}>Value</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={{ padding: "12px" }}>Source</td>
              <td style={{ padding: "12px" }}>Modern Lexicon</td>
            </tr>
            <tr>
              <td style={{ padding: "12px" }}>Rows</td>
              <td style={{ padding: "12px" }}>5</td>
            </tr>
          </tbody>
        </table>
      </TableWrap>
    </StoryFrame>
  ),
};
