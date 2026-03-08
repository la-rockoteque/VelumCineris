import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "node:path";

const backendPort = Number(process.env.VELUM_PORT || 8765);
const backendHost = process.env.VELUM_HOST || "127.0.0.1";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: [
      { find: /^app\//, replacement: `${path.resolve(__dirname, "src/app")}/` },
      { find: /^components\//, replacement: `${path.resolve(__dirname, "src/components")}/` },
      { find: /^features\//, replacement: `${path.resolve(__dirname, "src/features")}/` },
      { find: /^shared\//, replacement: `${path.resolve(__dirname, "src/shared")}/` },
    ],
  },
  base: "/app/",
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
  server: {
    host: "127.0.0.1",
    port: 5173,
    proxy: {
      "/api": `http://${backendHost}:${backendPort}`,
      "/health": `http://${backendHost}:${backendPort}`,
      "/assets": `http://${backendHost}:${backendPort}`,
    },
  },
});
