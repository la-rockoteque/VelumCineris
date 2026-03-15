import type { Preview } from "@storybook/react";

import { VelumProvider } from "../src";
import "../src/reset.css";
import "./storybookPreview.css";
import { velumStorybookTheme } from "./velumStorybookTheme";

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
          ["BrandAssets", "Icons", "BrickAndMoss", "DiceLottie", "SigilMark", "RuneDivider", "CornerFlourish"],
          "Components",
          [
            "Badge",
            "Button",
            "InlineButton",
            "Checkbox",
            "RadioButton",
            "TextInput",
            "SelectInput",
            "TextArea",
            "SegmentedControl",
            "TabBar",
            "Table",
            "ComponentsField",
            "DiceField",
            "DelimitedListField",
            "MultiSelect",
            "NamedTableField",
            "StatWithModifierField",
            "Layout",
            ["Card", "Section", "Subsection", "Stack", "Cluster", "PanelGrid", "TableWrap"],
            "Actions",
            ["ActionRow", "ActionRowEnd", "Toolbar"],
            "Workspace",
            ["WorkspaceCard", "WorkbenchLayout", "InsetCard", "FeatureOutput", "MetaText"],
          ],
          "Patterns",
          ["Operational States", "Loading", "Scrolling", "Pagination", "Saving", "Disabled", "Error Management"],
        ],
      },
    },
    controls: {
      expanded: true,
    },
    backgrounds: {
      disable: true,
    },
    docs: {
      theme: velumStorybookTheme,
    },
  },
};

export default preview;
