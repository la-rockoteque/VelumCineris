import { useEffect, useMemo, useState } from "react";

import type {
  TimelineCalendarMonth,
  TimelineCatalogResponse,
  TimelineEraEvent,
  TimelineHoliday,
  TimelineNamingGroup,
  TimelinePresentMonth,
} from "shared/types/api";
import { computeTimelineDayHeight, eraRowVisual, getHolidayNamesForDay } from "shared/utils/timeline";

interface TimelineTabProps {
  loading: boolean;
  timelineCatalog: TimelineCatalogResponse | null;
  onReload: () => Promise<void>;
  onSaveCatalog: (payload: Record<string, unknown>) => Promise<void>;
}

interface TimelineDraft {
  calendar_months: TimelineCalendarMonth[];
  naming_groups: TimelineNamingGroup[];
  weekdays: string[];
  holidays: TimelineHoliday[];
  era_events: TimelineEraEvent[];
  present_months: TimelinePresentMonth[];
  naming_template: string;
}

function cloneCatalog(catalog: TimelineCatalogResponse): TimelineDraft {
  return {
    calendar_months: structuredClone(catalog.calendar_months || []),
    naming_groups: structuredClone(catalog.naming_groups || []),
    weekdays: structuredClone(catalog.weekdays || []),
    holidays: structuredClone(catalog.holidays || []),
    era_events: structuredClone(catalog.era_events || []),
    present_months: structuredClone(catalog.present_months || []),
    naming_template: String(catalog.naming_template || ""),
  };
}

function normalizeHoliday(item: TimelineHoliday): TimelineHoliday | null {
  const name = String(item.name || "").trim();
  if (!name) {
    return null;
  }
  const day = Number(item.day);
  return {
    ...item,
    name,
    month_name: String(item.month_name || "").trim() || null,
    day: Number.isFinite(day) && day > 0 ? Math.floor(day) : null,
    recurrence: String(item.recurrence || "").trim() || null,
  };
}

function normalizeEvent(item: TimelineEraEvent): TimelineEraEvent | null {
  const event = String(item.event || "").trim();
  if (!event) {
    return null;
  }
  const year = Number(item.year);
  return {
    ...item,
    year: Number.isFinite(year) ? Math.floor(year) : null,
    event,
  };
}

export function TimelineTab(props: TimelineTabProps) {
  const [draft, setDraft] = useState<TimelineDraft | null>(null);
  const [status, setStatus] = useState("Timeline status and save output appear here.");

  useEffect(() => {
    if (!props.timelineCatalog) {
      setDraft(null);
      return;
    }
    setDraft(cloneCatalog(props.timelineCatalog));
  }, [props.timelineCatalog]);

  const monthNames = useMemo(
    () =>
      (draft?.calendar_months || [])
        .map((month) => String(month.month_name || "").trim())
        .filter(Boolean),
    [draft?.calendar_months],
  );

  const orderedEvents = useMemo(() => {
    const events = [...(draft?.era_events || [])]
      .map((item) => normalizeEvent(item))
      .filter(Boolean) as TimelineEraEvent[];

    return events.sort((a, b) => {
      const ay = Number.isFinite(Number(a.year)) ? Number(a.year) : Number.POSITIVE_INFINITY;
      const by = Number.isFinite(Number(b.year)) ? Number(b.year) : Number.POSITIVE_INFINITY;
      if (ay !== by) {
        return ay - by;
      }
      const ar = Number.isFinite(Number(a.row_number)) ? Number(a.row_number) : Number.POSITIVE_INFINITY;
      const br = Number.isFinite(Number(b.row_number)) ? Number(b.row_number) : Number.POSITIVE_INFINITY;
      if (ar !== br) {
        return ar - br;
      }
      const ac = Number.isFinite(Number(a.column)) ? Number(a.column) : Number.POSITIVE_INFINITY;
      const bc = Number.isFinite(Number(b.column)) ? Number(b.column) : Number.POSITIVE_INFINITY;
      return ac - bc;
    });
  }, [draft?.era_events]);

  if (!draft) {
    return (
      <section className="workspace-card">
        <h2>Timeline</h2>
        <p>Timeline data unavailable for current source.</p>
      </section>
    );
  }

  const updateDraft = (patch: Partial<TimelineDraft>) => {
    setDraft((current) => (current ? { ...current, ...patch } : current));
  };

  const saveNaming = async () => {
    await props.onSaveCatalog({
      calendar_months: draft.calendar_months,
      naming_groups: draft.naming_groups,
      weekdays: draft.weekdays,
    });
    setStatus("Timeline naming saved.");
  };

  const saveHolidays = async () => {
    await props.onSaveCatalog({
      holidays: draft.holidays.map((item) => normalizeHoliday(item)).filter(Boolean),
    });
    setStatus("Holidays saved.");
  };

  const saveEra = async () => {
    await props.onSaveCatalog({
      era_events: draft.era_events.map((item) => normalizeEvent(item)).filter(Boolean),
    });
    setStatus("Era events saved.");
  };

  return (
    <section className="workspace-card">
      <h2>Timeline</h2>
      <p>Explore Era events, Present calendar blocks, and naming/holiday structures.</p>

      <div className="toolbar">
        <button className="btn" disabled={props.loading} onClick={() => void props.onReload()}>
          Reload Timeline
        </button>
        <button className="btn" disabled={props.loading} onClick={() => void saveNaming()}>
          Save Naming
        </button>
        <button className="btn" disabled={props.loading} onClick={() => void saveHolidays()}>
          Save Holidays
        </button>
        <button className="btn" disabled={props.loading} onClick={() => void saveEra()}>
          Save Era Events
        </button>
      </div>

      <div className="workspace-grid" style={{ marginTop: 10 }}>
        <div className="workspace-controls">
          <div className="timeline-months">
            <article className="timeline-month-card">
              <h4>Month Naming</h4>
              {!draft.calendar_months.length && <div>No calendar months found.</div>}
              {draft.calendar_months.map((month, index) => (
                <div key={`${month.row_number}-${index}`} className="timeline-inline-input" style={{ marginTop: 6 }}>
                  <span>{month.month_order || `#${month.row_number}`}</span>
                  <input
                    value={String(month.month_name || "")}
                    onChange={(event) => {
                      const next = [...draft.calendar_months];
                      const base = next[index] || { row_number: month.row_number };
                      next[index] = { ...base, month_name: event.target.value };
                      updateDraft({ calendar_months: next });
                    }}
                  />
                </div>
              ))}
            </article>
          </div>

          <div className="timeline-weekdays">
            <article className="timeline-month-card">
              <h4>Weekday Naming</h4>
              {!draft.weekdays.length && <div>No weekday naming found.</div>}
              {draft.weekdays.map((weekday, index) => (
                <label key={`${weekday}-${index}`} className="timeline-inline-input">
                  <span>Day {index + 1}</span>
                  <input
                    value={weekday}
                    onChange={(event) => {
                      const next = [...draft.weekdays];
                      next[index] = event.target.value;
                      updateDraft({ weekdays: next });
                    }}
                  />
                </label>
              ))}
            </article>
          </div>

          <div className="timeline-naming">
            <article className="timeline-naming-group">
              <h4>Naming Sets</h4>
              <div style={{ marginBottom: 8 }}>Template: {draft.naming_template || "-"}</div>
              {!draft.naming_groups.length && <div>No naming groups found.</div>}
              {draft.naming_groups.map((group, index) => (
                <label key={`${group.key}-${index}`} style={{ marginTop: 8 }}>
                  {group.label || group.key}
                  <textarea
                    rows={3}
                    value={(group.values || []).join("\n")}
                    onChange={(event) => {
                      const nextGroups = [...draft.naming_groups];
                      const base = nextGroups[index] || { key: group.key, label: group.label, values: [] };
                      nextGroups[index] = {
                        ...base,
                        values: event.target.value
                          .split("\n")
                          .map((line) => line.trim())
                          .filter(Boolean),
                      };
                      updateDraft({ naming_groups: nextGroups });
                    }}
                  />
                </label>
              ))}
            </article>
          </div>

          <div className="timeline-holidays">
            <article className="timeline-month-card">
              <h4>Holidays</h4>
              {!draft.holidays.length && <div>No holidays yet.</div>}
              {draft.holidays.map((holiday, index) => (
                <div key={`${holiday.name}-${index}`} className="timeline-holiday-row">
                  <input
                    value={String(holiday.name || "")}
                    placeholder="Holiday name"
                    onChange={(event) => {
                      const next = [...draft.holidays];
                      const base = next[index] || { name: "", recurrence: "yearly" };
                      next[index] = { ...base, name: event.target.value, source: "holidays" };
                      updateDraft({ holidays: next });
                    }}
                  />

                  <select
                    value={String(holiday.month_name || "")}
                    onChange={(event) => {
                      const next = [...draft.holidays];
                      const base = next[index] || { name: holiday.name || "", recurrence: "yearly" };
                      next[index] = { ...base, month_name: event.target.value || null, source: "holidays" };
                      updateDraft({ holidays: next });
                    }}
                  >
                    <option value="">Month</option>
                    {monthNames.map((monthName) => (
                      <option key={monthName} value={monthName}>
                        {monthName}
                      </option>
                    ))}
                  </select>

                  <input
                    type="number"
                    min={1}
                    max={30}
                    value={holiday.day ?? ""}
                    placeholder="Day"
                    onChange={(event) => {
                      const parsed = Number(event.target.value);
                      const next = [...draft.holidays];
                      const base = next[index] || { name: holiday.name || "", recurrence: "yearly" };
                      next[index] = {
                        ...base,
                        day: Number.isFinite(parsed) && parsed > 0 ? Math.floor(parsed) : null,
                        source: "holidays",
                      };
                      updateDraft({ holidays: next });
                    }}
                  />

                  <select
                    value={String(holiday.recurrence || "yearly")}
                    onChange={(event) => {
                      const next = [...draft.holidays];
                      const base = next[index] || { name: holiday.name || "" };
                      next[index] = { ...base, recurrence: event.target.value, source: "holidays" };
                      updateDraft({ holidays: next });
                    }}
                  >
                    {[
                      ["yearly", "Yearly"],
                      ["monthly", "Monthly"],
                      ["once", "Once"],
                      ["custom", "Custom"],
                    ].map(([value, label]) => (
                      <option key={value} value={value}>
                        {label}
                      </option>
                    ))}
                  </select>

                  <button
                    type="button"
                    className="btn btn-inline"
                    onClick={() => {
                      const next = draft.holidays.filter((_, rowIndex) => rowIndex !== index);
                      updateDraft({ holidays: next });
                    }}
                  >
                    {holiday.source === "present" ? "Hide" : "Remove"}
                  </button>
                </div>
              ))}

              <button
                type="button"
                className="btn btn-inline"
                onClick={() => {
                  updateDraft({
                    holidays: [
                      ...draft.holidays,
                      {
                        name: "",
                        month_name: monthNames[0] || null,
                        day: 1,
                        recurrence: "yearly",
                        source: "holidays",
                      },
                    ],
                  });
                }}
              >
                Add Holiday
              </button>
            </article>
          </div>
        </div>

        <div className="workspace-results">
          <article className="timeline-present-month">
            <h4 style={{ margin: 0 }}>Present Calendar</h4>
            {!draft.present_months.length && <div style={{ marginTop: 8 }}>No Present calendar blocks found.</div>}
            {!!draft.present_months.length && (
              <div className="timeline-present" style={{ marginTop: 10 }}>
                {draft.present_months.map((month, monthIndex) => {
                  const dayHeight = computeTimelineDayHeight(month, draft.holidays);
                  return (
                    <article key={`${month.month_name}-${monthIndex}`} className="timeline-present-month">
                      <div className="timeline-present-header">
                        <h4>{month.month_name || "Month"}</h4>
                        <div className="timeline-present-year">
                          {month.year_name || "Year"}
                          {month.day_count ? ` · ${month.day_count} days` : ""}
                        </div>
                      </div>

                      <table className="timeline-present-table" style={{ ["--timeline-day-height" as string]: `${dayHeight}px` }}>
                        <thead>
                          <tr>
                            {(month.weekdays || []).slice(0, 5).map((weekday, index) => (
                              <th key={`${weekday}-${index}`}>{weekday || `Day ${index + 1}`}</th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {(month.weeks || []).map((week, weekIndex) => (
                            <tr key={`${month.month_name}-${weekIndex}`}>
                              {(week.days || []).slice(0, 5).map((day, dayIndex) => {
                                const dayValue = Number.isFinite(Number(day.day)) ? Number(day.day) : null;
                                const holidayNames = getHolidayNamesForDay(
                                  draft.holidays,
                                  String(month.month_name || ""),
                                  dayValue,
                                  String(month.year_name || ""),
                                );
                                return (
                                  <td key={`${weekIndex}-${dayIndex}`} className="timeline-present-cell">
                                    <div className="timeline-present-day">{day.day ?? ""}</div>
                                    {!!holidayNames.length && (
                                      <div className="timeline-present-event-list">
                                        {holidayNames.map((name) => (
                                          <div key={`${name}-${dayIndex}`} className="timeline-present-event">
                                            {name}
                                          </div>
                                        ))}
                                      </div>
                                    )}
                                  </td>
                                );
                              })}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </article>
                  );
                })}
              </div>
            )}
          </article>

          <article className="timeline-month-card" style={{ marginTop: 10 }}>
            <h4>Era Events</h4>
            {!orderedEvents.length && <div>No Era events found.</div>}
            <div className="timeline-era" style={{ marginTop: 8 }}>
              {orderedEvents.map((event, index) => {
                const yearNumber = Number.isFinite(Number(event.year)) ? Number(event.year) : null;
                const previousYearNumber = index > 0 && Number.isFinite(Number(orderedEvents[index - 1]?.year)) ? Number(orderedEvents[index - 1]?.year) : null;
                const visual = eraRowVisual(yearNumber, previousYearNumber);
                const century = yearNumber != null ? Math.floor(yearNumber / 100) * 100 : null;
                const decade = yearNumber != null ? Math.floor(yearNumber / 10) * 10 : null;
                const gap = yearNumber != null && previousYearNumber != null ? Math.abs(yearNumber - previousYearNumber) : 0;

                return (
                  <article
                    key={`${event.row_number}-${event.column}-${index}`}
                    className="timeline-era-row"
                    style={{
                      marginTop: `${visual.marginTop}px`,
                      background: visual.bg,
                      borderLeftColor: visual.borderLeftColor,
                    }}
                  >
                    <div>
                      <input
                        type="number"
                        className="timeline-era-year-input"
                        value={event.year ?? ""}
                        placeholder="Year"
                        onChange={(itemEvent) => {
                          const parsed = Number(itemEvent.target.value);
                          const next = [...draft.era_events];
                          const base = next[index] || { event: event.event || "" };
                          next[index] = {
                            ...base,
                            year: Number.isFinite(parsed) ? Math.floor(parsed) : null,
                          };
                          updateDraft({ era_events: next });
                        }}
                      />
                    </div>
                    <div className="timeline-era-content">
                      <div className="timeline-era-era">{event.era || "Era"}</div>
                      <div className="timeline-era-meta">
                        <span className="timeline-era-chip">{century != null ? `Century ${century}` : "Unknown century"}</span>
                        <span className="timeline-era-chip">{decade != null ? `Decade ${decade}` : "Unknown decade"}</span>
                        {gap > 1 && <span className="timeline-era-chip">Gap +{gap}</span>}
                      </div>
                      <textarea
                        className="timeline-era-text"
                        rows={2}
                        value={String(event.event || "")}
                        onChange={(itemEvent) => {
                          const next = [...draft.era_events];
                          const base = next[index] || { event: event.event || "" };
                          next[index] = {
                            ...base,
                            event: itemEvent.target.value,
                          };
                          updateDraft({ era_events: next });
                        }}
                      />
                    </div>
                    <div className="timeline-era-controls">
                      <button
                        type="button"
                        className="btn btn-inline"
                        onClick={() => {
                          const next = draft.era_events.filter((_, rowIndex) => rowIndex !== index);
                          updateDraft({ era_events: next });
                        }}
                      >
                        Remove
                      </button>
                    </div>
                  </article>
                );
              })}
            </div>

            <button
              type="button"
              className="btn btn-inline"
              style={{ marginTop: 8 }}
              onClick={() => {
                updateDraft({
                  era_events: [
                    ...draft.era_events,
                    {
                      year: orderedEvents.length ? Number(orderedEvents[orderedEvents.length - 1]?.year || 0) + 1 : 0,
                      era: "",
                      event: "",
                    },
                  ],
                });
              }}
            >
              Add Era Event
            </button>
          </article>

          <pre className="feature-output workspace-output">{status}</pre>
        </div>
      </div>
    </section>
  );
}
