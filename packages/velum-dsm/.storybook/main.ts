import type { StorybookConfig } from "@storybook/react-vite";

const config: StorybookConfig = {
  stories: ["../src/**/*.stories.@(ts|tsx)", "../src/**/*.mdx"],
  addons: ["@storybook/addon-a11y", "@storybook/addon-docs"],
  framework: {
    name: "@storybook/react-vite",
    options: {},
  },
  async viteFinal(config) {
    config.resolve ??= {};
    config.resolve.dedupe = ["react", "react-dom", "styletron-engine-atomic", "styletron-react"];
    config.assetsInclude = ["**/*.lottie"];
    return config;
  },
};

export default config;
