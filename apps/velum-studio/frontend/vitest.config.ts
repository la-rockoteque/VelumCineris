import react from "@vitejs/plugin-react-swc";
import path from "node:path";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  resolve: {
    dedupe: ["react", "react-dom", "styletron-engine-atomic", "styletron-react"],
    alias: [
      { find: "@velum/dsm", replacement: path.resolve(__dirname, "../../../packages/velum-dsm/src/index.ts") },
      { find: /^@velum\/dsm\//, replacement: `${path.resolve(__dirname, "../../../packages/velum-dsm/src")}/` },
      { find: "react/jsx-dev-runtime", replacement: path.resolve(__dirname, "node_modules/react/jsx-dev-runtime.js") },
      { find: "react/jsx-runtime", replacement: path.resolve(__dirname, "node_modules/react/jsx-runtime.js") },
      { find: "styletron-engine-atomic", replacement: path.resolve(__dirname, "node_modules/styletron-engine-atomic/dist-node-cjs/index.js") },
      { find: "styletron-react", replacement: path.resolve(__dirname, "node_modules/styletron-react/dist-node-cjs/index.js") },
      { find: "react-dom/client", replacement: path.resolve(__dirname, "node_modules/react-dom/client.js") },
      { find: "react-dom", replacement: path.resolve(__dirname, "node_modules/react-dom/index.js") },
      { find: "react", replacement: path.resolve(__dirname, "node_modules/react/index.js") },
      { find: /^app\//, replacement: `${path.resolve(__dirname, "src/app")}/` },
      { find: /^components\//, replacement: `${path.resolve(__dirname, "src/components")}/` },
      { find: /^features\//, replacement: `${path.resolve(__dirname, "src/features")}/` },
      { find: /^shared\//, replacement: `${path.resolve(__dirname, "src/shared")}/` },
      { find: /^test\//, replacement: `${path.resolve(__dirname, "src/test")}/` },
      { find: /^src\//, replacement: `${path.resolve(__dirname, "src")}/` },
    ],
  },
  test: {
    environment: "happy-dom",
    setupFiles: ["./src/test/setup.ts"],
    css: false,
    pool: "threads",
    globals: true,
    include: ["src/**/__tests__/**/*.test.ts", "src/**/__tests__/**/*.test.tsx"],
  },
});
