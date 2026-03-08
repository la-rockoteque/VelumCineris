import { normalizeKey } from "./text";

function parseCsv(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function isHttpUrl(value: string): boolean {
  return /^https?:\/\//i.test(value);
}

function rewriteGoogleDriveImageUrl(url: string): string {
  const directId = url.match(/\/d\/([a-zA-Z0-9_-]+)/);
  if (directId?.[1]) {
    return `https://drive.google.com/uc?export=view&id=${directId[1]}`;
  }

  const queryId = url.match(/[?&]id=([a-zA-Z0-9_-]+)/);
  if (queryId?.[1]) {
    return `https://drive.google.com/uc?export=view&id=${queryId[1]}`;
  }

  return url;
}

function rewriteLocalAssetPath(rawValue: string): string {
  let value = rawValue.trim();
  if (!value) {
    return "";
  }

  value = value.replace(/^file:\/\//i, "").replace(/\\/g, "/");

  if (value.startsWith("/assets/")) {
    return value;
  }
  if (value.startsWith("assets/")) {
    return `/${value}`;
  }
  if (value.startsWith("./assets/")) {
    return `/${value.slice(2)}`;
  }
  if (value.startsWith("../assets/")) {
    return `/assets/${value.slice("../assets/".length)}`;
  }

  const marker = "/assets/";
  const index = value.toLowerCase().indexOf(marker);
  if (index >= 0) {
    return value.slice(index);
  }

  return "";
}

function normalizeImageUrl(value: unknown): string {
  if (value == null) {
    return "";
  }

  let raw = String(value).trim();
  if (!raw) {
    return "";
  }

  const markdownMatch = raw.match(/!\[[^\]]*\]\(([^)]+)\)/);
  if (markdownMatch?.[1]) {
    raw = markdownMatch[1].trim();
  }

  if (raw.startsWith("data:image/")) {
    return raw;
  }

  const firstCsv = parseCsv(raw)[0] || raw;
  raw = firstCsv.trim().replace(/^"+|"+$/g, "").replace(/^'+|'+$/g, "");

  if (!raw) {
    return "";
  }

  if (raw.startsWith("www.")) {
    return `https://${raw}`;
  }

  if (isHttpUrl(raw)) {
    return rewriteGoogleDriveImageUrl(raw);
  }

  const local = rewriteLocalAssetPath(raw);
  if (local) {
    return local;
  }

  if (raw.startsWith("/") || raw.startsWith("./") || raw.startsWith("../")) {
    return raw;
  }

  if (/\.(png|jpe?g|gif|webp|svg)(\?.*)?$/i.test(raw)) {
    if (raw.includes("/")) {
      const mapped = rewriteLocalAssetPath(raw);
      return mapped || raw;
    }
    return `/assets/${raw}`;
  }

  return "";
}

export function resolveRowImage(rowData: Record<string, unknown>): { field: string; url: string } | null {
  const exactPriority = [
    "image",
    "imageurl",
    "art",
    "artwork",
    "portrait",
    "thumbnail",
    "cover",
    "icon",
    "token",
    "avatar",
    "illustration",
  ];
  const keyTerms = ["image", "img", "art", "portrait", "thumbnail", "cover", "icon", "token", "avatar", "illustration"];

  const candidates: Array<{ field: string; url: string; score: number }> = [];
  for (const [field, value] of Object.entries(rowData)) {
    const normalized = normalizeKey(field);
    if (!keyTerms.some((term) => normalized.includes(term))) {
      continue;
    }

    const resolved = normalizeImageUrl(value);
    if (!resolved) {
      continue;
    }

    const exactIndex = exactPriority.indexOf(normalized);
    const score = exactIndex >= 0 ? 100 - exactIndex : 10;
    candidates.push({ field, url: resolved, score });
  }

  if (!candidates.length) {
    return null;
  }

  candidates.sort((a, b) => b.score - a.score);
  return { field: candidates[0]!.field, url: candidates[0]!.url };
}

export function isRemoteImage(url: string): boolean {
  return isHttpUrl(url);
}
