import react from "@vitejs/plugin-react-swc";
import path from "node:path";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [
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
    include: ["src/**/*.test.ts", "src/**/*.test.tsx"],
  },
});
