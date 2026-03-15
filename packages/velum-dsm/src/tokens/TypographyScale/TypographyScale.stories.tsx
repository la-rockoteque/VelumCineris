import type { Meta, StoryObj } from "@storybook/react";

import { typographyScale } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/TypographyScale",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame>
      <div style={{ display: "grid", gap: "16px" }}>
        <div style={{ border: "1px solid var(--border)", borderRadius: "12px", padding: "16px", background: "var(--surface-strong)" }}>
          <div style={{ fontFamily: typographyScale.display, fontSize: typographyScale.size.hero, textTransform: "uppercase", letterSpacing: typographyScale.tracking.loud }}>
            The cinders remember
          </div>
          <div style={{ marginTop: "12px", fontFamily: typographyScale.body }}>
            Body typography is tuned for application workflows and readable content blocks.
          </div>
          <div style={{ marginTop: "12px", fontFamily: typographyScale.mono, fontSize: "0.84rem" }}>
            Mono is reserved for diagnostics, output, and system-facing text.
          </div>
        </div>
        <div style={{ border: "1px solid var(--border)", borderRadius: "12px", padding: "16px", background: "var(--surface-strong)", fontFamily: "var(--velum-font-mono)" }}>
          <div>body: {typographyScale.body}</div>
          <div>display: {typographyScale.display}</div>
          <div>mono: {typographyScale.mono}</div>
        </div>
      </div>
    </StoryFrame>
  ),
};
