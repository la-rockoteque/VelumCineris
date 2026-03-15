import { create } from "@storybook/theming/create";

import d20IconUrl from "../src/assets/Icons/D20.svg";
import { colorFamilies } from "../src/tokens/ColorFamilies/ColorFamilies";
import { radiusScale } from "../src/tokens/RadiusScale/RadiusScale";
import { shadowScale } from "../src/tokens/ShadowScale/ShadowScale";
import { studioTheme } from "../src/tokens/StudioTheme/StudioTheme";
import { typographyScale } from "../src/tokens/TypographyScale/TypographyScale";

export const velumStorybookTheme = create({
  base: "light",
  colorPrimary: studioTheme.accent,
  colorSecondary: colorFamilies.moss[500],
  appBg: studioTheme.background,
  appContentBg: studioTheme.surface,
  appPreviewBg: studioTheme.backgroundAlt,
  appBorderColor: "rgba(74, 56, 39, 0.18)",
  appBorderRadius: Number.parseInt(radiusScale.lg, 10),
  barBg: "rgba(249, 238, 221, 0.92)",
  barSelectedColor: studioTheme.accent,
  barTextColor: studioTheme.inkSoft,
  barHoverColor: studioTheme.ink,
  buttonBg: "rgba(255, 251, 244, 0.9)",
  buttonBorder: "rgba(74, 56, 39, 0.16)",
  booleanBg: colorFamilies.parchment[100],
  booleanSelectedBg: colorFamilies.moss[500],
  inputBg: "rgba(255, 251, 244, 0.92)",
  inputBorder: "rgba(74, 56, 39, 0.2)",
  inputTextColor: studioTheme.ink,
  textColor: studioTheme.ink,
  textInverseColor: colorFamilies.parchment[50],
  textMutedColor: studioTheme.inkSoft,
  fontBase: typographyScale.body,
  fontCode: typographyScale.mono,
  brandTitle: "Velum DSM",
  brandImage: d20IconUrl,
  brandTarget: "_self",
});

export const velumStorybookShadow = shadowScale.soft;
