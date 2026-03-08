const { spawn } = require("node:child_process");

const POLL_MS = 350;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForUrl(url, timeoutMs = 30000) {
  const started = Date.now();
  while (Date.now() - started < timeoutMs) {
    try {
      const response = await fetch(url);
      if (response.ok) {
        return;
      }
    } catch (_err) {
      // Target may still be starting.
    }
    await sleep(POLL_MS);
  }
  throw new Error(`Service did not become available at ${url} within ${timeoutMs}ms`);
}

function startManagedProcess({ command, args, cwd, label }) {
  const processRef = spawn(command, args, {
    cwd,
    stdio: ["ignore", "pipe", "pipe"],
  });

  processRef.stdout.on("data", (chunk) => {
    process.stdout.write(`[${label}] ${chunk}`);
  });

  processRef.stderr.on("data", (chunk) => {
    process.stderr.write(`[${label}] ${chunk}`);
  });

  processRef.on("exit", (code, signal) => {
    process.stdout.write(`[${label}] exited code=${code} signal=${signal}\n`);
  });

  return processRef;
}

function stopManagedProcess(processRef) {
  if (!processRef) {
    return;
  }
  processRef.kill("SIGTERM");
}

module.exports = {
  waitForUrl,
  startManagedProcess,
  stopManagedProcess,
};
