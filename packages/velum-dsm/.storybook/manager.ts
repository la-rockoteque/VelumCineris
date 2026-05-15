import { addons } from "storybook/manager-api";

import "./storybookManager.css";
import { velumStorybookTheme } from "./velumStorybookTheme";

addons.setConfig({
  theme: velumStorybookTheme,
});
