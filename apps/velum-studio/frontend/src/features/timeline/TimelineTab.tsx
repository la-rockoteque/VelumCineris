import { useEffect, useMemo, useState, type CSSProperties, type ReactNode } from "react";
import { styled } from "app/styletron";

import {
  Button,
  InsetCard,
  InsetTitle,
  InlineButton,
  SelectInput,
  TextArea,
  TextInput,
  Toolbar,
  WorkbenchLayout,
  WorkbenchMain,
  WorkbenchSidebar,
  WorkspaceCard,
  WorkspaceLead,
  WorkspaceOutput,
  WorkspaceTitle,
} from "shared/library";
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

const TimelineGroup = styled("div", {
  display: "grid",
  gap: "8px",
});

const InlineInputRow = styled("div", {
  display: "grid",
  gridTemplateColumns: "72px minmax(0, 1fr)",
  alignItems: "center",
  gap: "8px",
});

const InlineInputLabel = styled("label", {
  display: "grid",
  gridTemplateColumns: "72px minmax(0, 1fr)",
  alignItems: "center",
  gap: "8px",
});

const InlineHint = styled("span", {
  fontSize: "0.76rem",
  color: "#6a5f4d",
});

const HolidayRow = styled("div", {
  display: "grid",
  gridTemplateColumns: "minmax(180px, 2fr) minmax(120px, 1fr) 84px 120px auto",
  gap: "8px",
  alignItems: "center",
  "@media (max-width: 860px)": {
    gridTemplateColumns: "1fr 1fr",
  },
  "@media (max-width: 560px)": {
    gridTemplateColumns: "1fr",
  },
});

const PresentWrapper = styled("div", {
  display: "grid",
  gap: "8px",
});

const PresentHeader = styled("div", {
  display: "grid",
  gap: "2px",
  marginBottom: "6px",
});

const PresentTitle = styled("h4", {
  margin: 0,
  fontSize: "0.82rem",
  textTransform: "uppercase",
  letterSpacing: "0.03em",
  color: "#5f523f",
});

const PresentYear = styled("div", {
  fontSize: "0.74rem",
  color: "#7a6b57",
});

const PresentTable = styled("table", {
  width: "100%",
  borderCollapse: "collapse",
  fontSize: "0.72rem",
  tableLayout: "fixed",
});

const PresentHeadCell = styled("th", {
  border: "1px solid rgba(66, 48, 30, 0.14)",
  padding: "4px",
  verticalAlign: "top",
  width: "20%",
  maxWidth: "none",
  background: "rgba(244, 230, 207, 0.55)",
  color: "#625543",
  fontWeight: 700,
  position: "static",
});

const PresentCell = styled("td", {
  border: "1px solid rgba(66, 48, 30, 0.14)",
  padding: "4px",
  verticalAlign: "top",
  width: "20%",
  maxWidth: "none",
  height: "var(--timeline-day-height, 96px)",
});

const PresentDay = styled("div", {
  fontWeight: 700,
  color: "#5a4d3b",
});

const PresentEventList = styled("div", {
  display: "grid",
  gap: "4px",
  marginTop: "4px",
});

const PresentEvent = styled("div", {
  marginTop: 0,
  color: "#6d5d48",
  whiteSpace: "pre-wrap",
  border: "1px solid rgba(66, 48, 30, 0.14)",
  borderRadius: "7px",
  background: "rgba(244, 230, 207, 0.55)",
  padding: "2px 5px",
});

const EraList = styled("div", {
  display: "grid",
  gap: "8px",
  marginTop: "8px",
});

const EraRow = styled("article", ({ $marginTop, $background, $borderLeftColor }: { $marginTop: number; $background: string; $borderLeftColor: string }) => ({
  border: "1px solid rgba(66, 48, 30, 0.14)",
  borderRadius: "9px",
  padding: "8px",
  overflow: "hidden",
  display: "grid",
  gridTemplateColumns: "88px minmax(0, 1fr) auto",
  gap: "8px",
  alignItems: "start",
  borderLeft: `4px solid ${$borderLeftColor}`,
  background: $background,
  marginTop: `${$marginTop}px`,
  "@media (max-width: 860px)": {
    gridTemplateColumns: "1fr",
  },
}));

const EraLabel = styled("div", {
  fontSize: "0.76rem",
  color: "#786b58",
  textTransform: "uppercase",
  letterSpacing: "0.03em",
});

const EraMeta = styled("div", {
  display: "flex",
  flexWrap: "wrap",
  gap: "6px",
});

const EraChip = styled("span", {
  fontSize: "0.68rem",
  border: "1px solid rgba(66, 48, 30, 0.22)",
  borderRadius: "999px",
  padding: "1px 7px",
  color: "#5f543f",
  background: "rgba(255, 248, 236, 0.72)",
});

const EraControls = styled("div", {
  display: "grid",
  gap: "6px",
  justifyItems: "end",
  "@media (max-width: 860px)": {
    justifyItems: "start",
  },
});

const TemplateRow = styled("div", {
  marginBottom: "8px",
});

const NoDataRow = styled("div", {
  marginTop: "8px",
});

function TimelineCard(props: { title: string; children: ReactNode; style?: CSSProperties }) {
  return (
    <InsetCard style={{ overflow: "hidden", ...props.style }}>
      <InsetTitle>{props.title}</InsetTitle>
      {props.children}
    </InsetCard>
  );
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
      <WorkspaceCard>
        <WorkspaceTitle>Timeline</WorkspaceTitle>
        <WorkspaceLead>Timeline data unavailable for current source.</WorkspaceLead>
      </WorkspaceCard>
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
    <WorkspaceCard>
      <WorkspaceTitle>Timeline</WorkspaceTitle>
      <WorkspaceLead>Explore Era events, Present calendar blocks, and naming/holiday structures.</WorkspaceLead>

      <Toolbar>
        <Button disabled={props.loading} onClick={() => void props.onReload()}>
          Reload Timeline
        </Button>
        <Button disabled={props.loading} onClick={() => void saveNaming()}>
          Save Naming
        </Button>
        <Button disabled={props.loading} onClick={() => void saveHolidays()}>
          Save Holidays
        </Button>
        <Button disabled={props.loading} onClick={() => void saveEra()}>
          Save Era Events
        </Button>
      </Toolbar>

        <WorkbenchLayout>
        <WorkbenchSidebar>
          <TimelineGroup>
            <TimelineCard title="Month Naming">
              {!draft.calendar_months.length && <div>No calendar months found.</div>}
              {draft.calendar_months.map((month, index) => (
                <InlineInputRow key={`${month.row_number}-${index}`} style={{ marginTop: "6px" }}>
                  <InlineHint>{month.month_order || `#${month.row_number}`}</InlineHint>
                  <TextInput
                    value={String(month.month_name || "")}
                    onChange={(event) => {
                      const next = [...draft.calendar_months];
                      const base = next[index] || { row_number: month.row_number };
                      next[index] = { ...base, month_name: event.target.value };
                      updateDraft({ calendar_months: next });
                    }}
                  />
                </InlineInputRow>
              ))}
            </TimelineCard>
          </TimelineGroup>

          <TimelineGroup>
            <TimelineCard title="Weekday Naming">
              {!draft.weekdays.length && <div>No weekday naming found.</div>}
              {draft.weekdays.map((weekday, index) => (
                <InlineInputLabel key={`${weekday}-${index}`}>
                  <InlineHint>Day {index + 1}</InlineHint>
                  <TextInput
                    value={weekday}
                    onChange={(event) => {
                      const next = [...draft.weekdays];
                      next[index] = event.target.value;
                      updateDraft({ weekdays: next });
                    }}
                  />
                </InlineInputLabel>
              ))}
            </TimelineCard>
          </TimelineGroup>

          <TimelineGroup>
            <TimelineCard title="Naming Sets">
              <TemplateRow>Template: {draft.naming_template || "-"}</TemplateRow>
              {!draft.naming_groups.length && <div>No naming groups found.</div>}
              {draft.naming_groups.map((group, index) => (
                <label key={`${group.key}-${index}`} style={{ marginTop: "8px" }}>
                  {group.label || group.key}
                  <TextArea
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
            </TimelineCard>
          </TimelineGroup>

          <TimelineGroup>
            <TimelineCard title="Holidays">
              {!draft.holidays.length && <div>No holidays yet.</div>}
              {draft.holidays.map((holiday, index) => (
                <HolidayRow key={`${holiday.name}-${index}`}>
                  <TextInput
                    value={String(holiday.name || "")}
                    placeholder="Holiday name"
                    onChange={(event) => {
                      const next = [...draft.holidays];
                      const base = next[index] || { name: "", recurrence: "yearly" };
                      next[index] = { ...base, name: event.target.value, source: "holidays" };
                      updateDraft({ holidays: next });
                    }}
                  />

                  <SelectInput
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
                  </SelectInput>

                  <TextInput
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

                  <SelectInput
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
                  </SelectInput>

                  <InlineButton
                    type="button"
                    onClick={() => {
                      const next = draft.holidays.filter((_, rowIndex) => rowIndex !== index);
                      updateDraft({ holidays: next });
                    }}
                  >
                    {holiday.source === "present" ? "Hide" : "Remove"}
                  </InlineButton>
                </HolidayRow>
              ))}

              <InlineButton
                type="button"
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
              </InlineButton>
            </TimelineCard>
          </TimelineGroup>
        </WorkbenchSidebar>

        <WorkbenchMain>
          <TimelineCard title="Present Calendar">
            {!draft.present_months.length && <NoDataRow>No Present calendar blocks found.</NoDataRow>}
            {!!draft.present_months.length && (
              <PresentWrapper style={{ marginTop: "10px" }}>
                {draft.present_months.map((month, monthIndex) => {
                  const dayHeight = computeTimelineDayHeight(month, draft.holidays);
                  return (
                    <TimelineCard key={`${month.month_name}-${monthIndex}`} title={String(month.month_name || "Month")}>
                      <PresentHeader>
                        <PresentYear>
                          {month.year_name || "Year"}
                          {month.day_count ? ` · ${month.day_count} days` : ""}
                        </PresentYear>
                      </PresentHeader>

                      <PresentTable style={{ ["--timeline-day-height" as string]: `${dayHeight}px` }}>
                        <thead>
                          <tr>
                            {(month.weekdays || []).slice(0, 5).map((weekday, index) => (
                              <PresentHeadCell key={`${weekday}-${index}`}>{weekday || `Day ${index + 1}`}</PresentHeadCell>
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
                                  <PresentCell key={`${weekIndex}-${dayIndex}`}>
                                    <PresentDay>{day.day ?? ""}</PresentDay>
                                    {!!holidayNames.length && (
                                      <PresentEventList>
                                        {holidayNames.map((name) => (
                                          <PresentEvent key={`${name}-${dayIndex}`}>{name}</PresentEvent>
                                        ))}
                                      </PresentEventList>
                                    )}
                                  </PresentCell>
                                );
                              })}
                            </tr>
                          ))}
                        </tbody>
                      </PresentTable>
                    </TimelineCard>
                  );
                })}
              </PresentWrapper>
            )}
          </TimelineCard>

          <TimelineCard title="Era Events" style={{ marginTop: "10px" }}>
            {!orderedEvents.length && <div>No Era events found.</div>}
            <EraList>
              {orderedEvents.map((event, index) => {
                const yearNumber = Number.isFinite(Number(event.year)) ? Number(event.year) : null;
                const previousYearNumber = index > 0 && Number.isFinite(Number(orderedEvents[index - 1]?.year)) ? Number(orderedEvents[index - 1]?.year) : null;
                const visual = eraRowVisual(yearNumber, previousYearNumber);
                const century = yearNumber != null ? Math.floor(yearNumber / 100) * 100 : null;
                const decade = yearNumber != null ? Math.floor(yearNumber / 10) * 10 : null;
                const gap = yearNumber != null && previousYearNumber != null ? Math.abs(yearNumber - previousYearNumber) : 0;

                return (
                  <EraRow
                    key={`${event.row_number}-${event.column}-${index}`}
                    $marginTop={visual.marginTop}
                    $background={visual.bg}
                    $borderLeftColor={visual.borderLeftColor}
                  >
                    <div>
                      <TextInput
                        type="number"
                        value={event.year ?? ""}
                        placeholder="Year"
                        style={{ width: "100%" }}
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
                    <div>
                      <EraLabel>{event.era || "Era"}</EraLabel>
                      <EraMeta>
                        <EraChip>{century != null ? `Century ${century}` : "Unknown century"}</EraChip>
                        <EraChip>{decade != null ? `Decade ${decade}` : "Unknown decade"}</EraChip>
                        {gap > 1 && <EraChip>Gap +{gap}</EraChip>}
                      </EraMeta>
                      <TextArea
                        rows={2}
                        value={String(event.event || "")}
                        style={{ minHeight: "56px", width: "100%" }}
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
                    <EraControls>
                      <InlineButton
                        type="button"
                        onClick={() => {
                          const next = draft.era_events.filter((_, rowIndex) => rowIndex !== index);
                          updateDraft({ era_events: next });
                        }}
                      >
                        Remove
                      </InlineButton>
                    </EraControls>
                  </EraRow>
                );
              })}
            </EraList>

            <InlineButton
              type="button"
              style={{ marginTop: "8px" }}
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
            </InlineButton>
          </TimelineCard>

          <WorkspaceOutput>{status}</WorkspaceOutput>
        </WorkbenchMain>
      </WorkbenchLayout>
    </WorkspaceCard>
  );
}
