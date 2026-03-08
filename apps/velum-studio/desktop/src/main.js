const { app, BrowserWindow, dialog } = require("electron");

const {
  HOST,
  BACKEND_PORT,
  FRONTEND_HOST,
  FRONTEND_PORT,
  FRONTEND_URL,
  ROOT_DIR,
  FRONTEND_DIR,
  START_FRONTEND,
} = require("./config");
const { createMainWindow } = require("./window");
const { startManagedProcess, stopManagedProcess, waitForUrl } = require("./processes");

let backendProcess = null;
let frontendProcess = null;

function startBackend() {
  if (backendProcess) {
    return;
  }
  backendProcess = startManagedProcess({
    command: "poetry",
    args: [
      "run",
      "uvicorn",
      "app.main:app",
      "--host",
      HOST,
      "--port",
      String(BACKEND_PORT),
      "--app-dir",
      "apps/velum-studio/backend",
    ],
    cwd: ROOT_DIR,
    label: "backend",
  });
}

function startFrontend() {
  if (!START_FRONTEND || frontendProcess) {
    return;
  }

  frontendProcess = startManagedProcess({
    command: "npm",
    args: ["run", "dev", "--", "--host", FRONTEND_HOST, "--port", String(FRONTEND_PORT)],
    cwd: FRONTEND_DIR,
    label: "frontend",
  });
}

function stopAllProcesses() {
  stopManagedProcess(frontendProcess);
  stopManagedProcess(backendProcess);
  frontendProcess = null;
  backendProcess = null;
}

async function boot() {
  startBackend();
  startFrontend();

  await waitForUrl(`http://${HOST}:${BACKEND_PORT}/health`, 30000);
  await waitForUrl(FRONTEND_URL, 45000);

  createMainWindow(FRONTEND_URL);
}

app.whenReady().then(async () => {
  try {
    await boot();
    app.on("activate", () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        createMainWindow(FRONTEND_URL);
      }
    });
  } catch (error) {
    dialog.showErrorBox("Velum Studio Startup Failed", String(error));
    stopAllProcesses();
    app.quit();
  }
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit();
  }
});

app.on("before-quit", () => {
  stopAllProcesses();
});
