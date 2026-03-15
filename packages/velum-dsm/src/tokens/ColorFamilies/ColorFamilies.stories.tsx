import type { Meta, StoryObj } from "@storybook/react";

import { colorFamilies } from "../../index";
import { StoryFrame } from "../../stories/_helpers";

const meta = {
  title: "Tokens/ColorFamilies",
} satisfies Meta;

export default meta;

type Story = StoryObj<typeof meta>;

export const Default: Story = {
  render: () => (
    <StoryFrame maxWidth="1100px">
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: "16px" }}>
        {Object.entries(colorFamilies).map(([family, values]) => (
          <div
            key={family}
            style={{
              border: "1px solid var(--border)",
              borderRadius: "12px",
              padding: "16px",
              background: "var(--surface-strong)",
            }}
          >
            <div style={{ fontWeight: 700, marginBottom: "12px", textTransform: "capitalize" }}>{family}</div>
            <div style={{ display: "grid", gap: "8px" }}>
              {Object.entries(values).map(([tone, swatch]) => (
                <div
                  key={tone}
                  style={{
                    display: "grid",
                    gridTemplateColumns: "64px 1fr",
                    gap: "12px",
                    alignItems: "center",
                  }}
                >
                  <div style={{ height: "32px", borderRadius: "8px", background: swatch, border: "1px solid var(--border)" }} />
                  <div style={{ fontFamily: "var(--velum-font-mono)", fontSize: "0.82rem" }}>
                    {tone}: {swatch}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </StoryFrame>
  ),
};
