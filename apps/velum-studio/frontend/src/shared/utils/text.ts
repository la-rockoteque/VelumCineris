export function normalizeKey(value: unknown): string {
  return String(value ?? "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "");
}

export function asText(value: unknown): string {
  if (value == null) {
    return "";
  }
  return String(value).trim();
}

export function truncateText(value: string, limit: number): string {
  if (value.length <= limit) {
    return value;
  }
  if (limit <= 1) {
    return "…";
  }
  return `${value.slice(0, limit - 1)}…`;
}

export function parseDelimitedList(value: unknown): string[] {
  return String(value ?? "")
    .split(/[\n,;|]+/)
    .map((item) => item.trim())
    .filter(Boolean);
}

export function dedupePreserveCase(values: string[]): string[] {
  const out: string[] = [];
  const seen = new Set<string>();
  for (const value of values) {
    const text = value.trim();
    if (!text) {
      continue;
    }
    const key = text.toLowerCase();
    if (seen.has(key)) {
      continue;
    }
    seen.add(key);
    out.push(text);
  }
  return out;
}

export function toBoolean(value: unknown): boolean {
  const lowered = asText(value).toLowerCase();
  return lowered === "true" || lowered === "1" || lowered === "yes" || lowered === "y";
}

export function safeNumber(value: unknown, fallback = 0): number {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}
