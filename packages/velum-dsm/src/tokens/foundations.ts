export const colorFamilies = {
  parchment: {
    50: "#fbf5eb",
    100: "#f5ead8",
    200: "#ede2cd",
    300: "#decfb4",
    400: "#cfb893",
  },
  ember: {
    400: "#c38c5b",
    500: "#a76537",
    600: "#8e4f28",
    700: "#6f3d1f",
  },
  moss: {
    300: "#8ea17a",
    500: "#647954",
    700: "#49593d",
  },
  slate: {
    100: "#c8c0b2",
    300: "#8c806e",
    500: "#5f5547",
    700: "#3a3027",
    900: "#231d16",
  },
  status: {
    ok: "#3a6e41",
    warn: "#8f6320",
    danger: "#9c463b",
    info: "#5d513f",
  },
} as const;

export const spacingScale = {
  0: "0",
  1: "4px",
  2: "8px",
  3: "12px",
  4: "16px",
  5: "20px",
  6: "24px",
  7: "32px",
  8: "40px",
  9: "48px",
} as const;

export const radiusScale = {
  sm: "8px",
  md: "12px",
  lg: "18px",
  xl: "24px",
  pill: "999px",
} as const;

export const typographyScale = {
  body: "\"IBM Plex Sans\", \"Trebuchet MS\", sans-serif",
  display: "\"Avenir Next Condensed\", \"Franklin Gothic Medium\", sans-serif",
  mono: "\"SFMono-Regular\", \"SF Mono\", Consolas, monospace",
  size: {
    xs: "0.78rem",
    sm: "0.85rem",
    md: "1rem",
    lg: "1.15rem",
    xl: "1.5rem",
    hero: "2rem",
  },
  tracking: {
    tight: "0.02em",
    normal: "0.04em",
    loud: "0.08em",
  },
} as const;

export const motionScale = {
  quick: "180ms",
  base: "240ms",
  slow: "320ms",
  easing: {
    standard: "ease",
    decelerate: "ease-out",
  },
} as const;

export const shadowScale = {
  soft: "0 18px 44px rgba(49, 34, 18, 0.12)",
  lift: "0 24px 60px rgba(49, 34, 18, 0.18)",
  insetAccent: "inset 0 -3px 0 rgba(195, 140, 91, 0.92)",
} as const;
