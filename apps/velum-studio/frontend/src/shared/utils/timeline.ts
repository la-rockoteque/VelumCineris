import { normalizeKey } from "./text";

import type { TimelineHoliday, TimelinePresentMonth } from "shared/types/api";

export function getHolidayNamesForDay(
  holidays: TimelineHoliday[],
  monthName: string,
  dayValue: number | null,
  yearName: string,
): string[] {
  if (!Number.isFinite(dayValue) || (dayValue ?? 0) <= 0) {
    return [];
  }

  const monthKey = normalizeKey(monthName || "");
  const yearKey = normalizeKey(yearName || "");
  const out: string[] = [];
  const seen = new Set<string>();

  for (const holiday of holidays || []) {
    const name = String(holiday?.name || "").trim();
    if (!name) {
      continue;
    }

    const targetDay = Number(holiday?.day);
    if (!Number.isFinite(targetDay) || targetDay !== dayValue) {
      continue;
    }

    const recurrence = normalizeKey(holiday?.recurrence || "yearly");
    const holidayMonth = normalizeKey(holiday?.month_name || "");
    const holidayYear = normalizeKey((holiday as { year?: string | null })?.year || "");

    const monthMatches = !holidayMonth || holidayMonth === monthKey;
    const yearMatches = !holidayYear || !yearKey || holidayYear === yearKey;
    const recurrenceAllows = recurrence === "monthly" || recurrence === "yearly" || recurrence === "once" || recurrence === "custom" || !recurrence;

    if (!monthMatches || !yearMatches || !recurrenceAllows) {
      continue;
    }

    const marker = normalizeKey(name);
    if (seen.has(marker)) {
      continue;
    }
    seen.add(marker);
    out.push(name);
  }

  return out;
}

export function computeTimelineDayHeight(month: TimelinePresentMonth, holidays: TimelineHoliday[]): number {
  const weeks = Array.isArray(month?.weeks) ? month.weeks : [];
  let maxLines = 1;

  for (const week of weeks) {
    const days = Array.isArray(week?.days) ? week.days : [];
    for (const day of days) {
      const dayValue = Number.isFinite(Number(day?.day)) ? Number(day?.day) : null;
      const holidayNames = getHolidayNamesForDay(holidays, String(month?.month_name || ""), dayValue, String(month?.year_name || ""));
      if (!holidayNames.length) {
        continue;
      }
      let lines = 0;
      for (const name of holidayNames) {
        lines += Math.max(1, Math.ceil(String(name).length / 28));
      }
      maxLines = Math.max(maxLines, lines);
    }
  }

  const multiplier = Math.max(1, Math.min(6, maxLines));
  return multiplier * 48;
}

export function eraRowVisual(year: number | null, previousYear: number | null): { marginTop: number; bg?: string; borderLeftColor?: string } {
  let marginTop = 2;
  if (previousYear != null && year != null) {
    const gap = Math.abs(year - previousYear);
    if (gap > 1) {
      const gapSpacing = Math.min(42, Math.round(Math.log2(gap + 1) * 6));
      marginTop = Math.max(2, gapSpacing);
    }
  }

  if (year == null) {
    return { marginTop };
  }

  const century = Math.floor(year / 100) * 100;
  const decade = Math.floor(year / 10) * 10;
  const hue = ((Math.abs(century) * 37) % 360 + 40) % 360;
  const decadeBand = Math.abs(Math.floor(decade / 10)) % 2;
  const lightness = decadeBand === 0 ? 92 : 86;

  return {
    marginTop,
    bg: `hsl(${hue} 56% ${lightness}%)`,
    borderLeftColor: `hsl(${hue} 62% 45%)`,
  };
}
