import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { timelineCatalog } from "test/fixtures";

import { TimelineTab } from "./TimelineTab";

describe("TimelineTab", () => {
  it("supports holiday and era saves from timeline draft state", async () => {
    const user = userEvent.setup();
    const onReload = vi.fn().mockResolvedValue(undefined);
    const onSaveCatalog = vi.fn().mockResolvedValue(undefined);

    render(<TimelineTab loading={false} timelineCatalog={timelineCatalog()} onReload={onReload} onSaveCatalog={onSaveCatalog} />);

    expect(screen.getByText("First Light")).toBeInTheDocument();
    expect(screen.getByText("The world awakens.")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Add Holiday" }));
    const holidayNameInputs = screen.getAllByPlaceholderText("Holiday name");
    const lastHolidayName = holidayNameInputs[holidayNameInputs.length - 1];
    await user.type(lastHolidayName, "Sunrise Feast");

    await user.click(screen.getByRole("button", { name: "Save Holidays" }));
    expect(onSaveCatalog).toHaveBeenNthCalledWith(
      1,
      expect.objectContaining({
        holidays: expect.arrayContaining([
          expect.objectContaining({ name: "First Light" }),
          expect.objectContaining({ name: expect.stringMatching(/^S/) }),
        ]),
      }),
    );

    await user.click(screen.getByRole("button", { name: "Save Era Events" }));
    expect(onSaveCatalog).toHaveBeenNthCalledWith(
      2,
      expect.objectContaining({
        era_events: expect.arrayContaining([expect.objectContaining({ event: "The world awakens." })]),
      }),
    );

    await user.click(screen.getByRole("button", { name: "Reload Timeline" }));
    expect(onReload).toHaveBeenCalledTimes(1);
  });
});
