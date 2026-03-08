const { BrowserWindow } = require("electron");
const path = require("node:path");

function createMainWindow(url) {
  const windowRef = new BrowserWindow({
    width: 1500,
    height: 980,
    minWidth: 980,
    minHeight: 680,
    webPreferences: {
      preload: path.join(__dirname, "../preload.js"),
      contextIsolation: true,
      nodeIntegration: false,
    },
  });

  void windowRef.loadURL(url);
  return windowRef;
}

module.exports = {
  createMainWindow,
};
