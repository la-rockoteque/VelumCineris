import type { Preview } from "@storybook/react";

import { VelumProvider } from "../src";
import "../src/reset.css";

const preview: Preview = {
  decorators: [
    (Story) => (
      <VelumProvider>
        <div
          style={{
            minHeight: "100vh",
            padding: "24px",
            background:
              "radial-gradient(circle at top right, rgba(195, 140, 91, 0.2), transparent 28%), radial-gradient(circle at bottom left, rgba(100, 121, 84, 0.18), transparent 24%), var(--bg)",
            color: "var(--ink)",
            fontFamily: "var(--velum-font-body)",
          }}
        >
          <Story />
        </div>
      </VelumProvider>
    ),
  ],
  parameters: {
    layout: "fullscreen",
    options: {
      storySort: {
        order: [
          "Tokens",
          [
            "ColorFamilies",
            "SpacingScale",
            "RadiusScale",
            "TypographyScale",
            "MotionScale",
            "ShadowScale",
            "StudioTheme",
          ],
          "Assets",
          ["SigilMark", "RuneDivider", "CornerFlourish"],
          "Components",
          ["Badge", "Button", "InlineButton", "TextInput", "SelectInput", "TextArea"],
          "Patterns",
          [
            "Card",
            "Section",
            "Subsection",
            "Stack",
            "Cluster",
            "PanelGrid",
            "ActionRow",
            "ActionRowEnd",
            "Toolbar",
            "WorkspaceCard",
            "WorkbenchLayout",
            "InsetCard",
            "TableWrap",
            "FeatureOutput",
            "MetaText",
          ],
        ],
      },
    },
    controls: {
      expanded: true,
    },
    backgrounds: {
      disable: true,
    },
  },
};

export default preview;
