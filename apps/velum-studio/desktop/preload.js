const { contextBridge } = require("electron");

contextBridge.exposeInMainWorld("velum", {
  version: "0.1.0",
});
