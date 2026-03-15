const path = require("node:path");

const HOST = process.env.VELUM_HOST || "127.0.0.1";
const BACKEND_PORT = Number(process.env.VELUM_PORT || 8765);
const FRONTEND_HOST = process.env.VELUM_FRONTEND_HOST || "127.0.0.1";
const FRONTEND_PORT = Number(process.env.VELUM_FRONTEND_PORT || 5173);
const FRONTEND_URL = process.env.VELUM_FRONTEND_URL || `http://${FRONTEND_HOST}:${FRONTEND_PORT}/app/`;
const ROOT_DIR = path.resolve(__dirname, "../../../..");
const BACKEND_DIR = path.resolve(__dirname, "../../backend");
const FRONTEND_DIR = path.resolve(__dirname, "../../frontend");
const START_FRONTEND = process.env.VELUM_START_FRONTEND !== "0";

module.exports = {
  HOST,
  BACKEND_PORT,
  FRONTEND_HOST,
  FRONTEND_PORT,
  FRONTEND_URL,
  ROOT_DIR,
  BACKEND_DIR,
  FRONTEND_DIR,
  START_FRONTEND,
};
