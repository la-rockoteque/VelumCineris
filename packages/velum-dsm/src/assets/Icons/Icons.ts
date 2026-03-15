const iconModules = import.meta.glob("./*.{svg,png,jpg,jpeg,webp}", {
  eager: true,
  import: "default",
  query: "?url",
}) as Record<string, string>;

const sortedIconEntries = Object.entries(iconModules)
  .map(([path, url]) => {
    const fileName = path.split("/").pop() ?? path;
    const name = fileName.replace(/\.[^.]+$/, "");
    return [name, url] as const;
  })
  .sort(([left], [right]) => left.localeCompare(right));

export const iconAssets = Object.fromEntries(sortedIconEntries) as Record<string, string>;

export const d20IconUrl = iconAssets.D20;
