import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { selectedRow, validationCatalog } from "test/fixtures";

import { DetailsTab } from "../DetailsTab";

describe("DetailsTab", () => {
  it("supports title editing and item actions", async () => {
    const user = userEvent.setup();
    const onActionModeChange = vi.fn();
    const onRowDataChange = vi.fn();
    const onItemAction = vi.fn().mockResolvedValue(undefined);

    render(
      <DetailsTab
        loading={false}
        selected={selectedRow()}
        validationCatalog={validationCatalog()}
        cellCharLimit={150}
        actionMode="dry_run"
        onActionModeChange={onActionModeChange}
        onRowDataChange={onRowDataChange}
        onItemAction={onItemAction}
        lookupFieldOptions={() => []}
      />,
    );

    expect(screen.getByText("Details Editor")).toBeInTheDocument();
    expect(screen.getByRole("heading", { name: "Arc Flash" })).toBeInTheDocument();

    onRowDataChange.mockClear();
    await user.click(screen.getByRole("heading", { name: "Arc Flash" }));
    const titleInput = screen.getByDisplayValue("Arc Flash");
    await user.clear(titleInput);
    await user.type(titleInput, "Arc Burst{enter}");
    expect(onRowDataChange).toHaveBeenCalledWith(expect.objectContaining({ Name: "Arc Burst" }));

    await user.click(screen.getByRole("button", { name: "WA Publish" }));
    expect(onItemAction).toHaveBeenCalledWith("worldanvil", "publish", true);

    await user.selectOptions(screen.getByLabelText("Mode"), "live");
    expect(onActionModeChange).toHaveBeenCalledWith("live");
  });

  it("shows empty state when no row is selected", () => {
    render(
      <DetailsTab
        loading={false}
        selected={null}
        validationCatalog={validationCatalog()}
        cellCharLimit={150}
        actionMode="dry_run"
        onActionModeChange={vi.fn()}
        onRowDataChange={vi.fn()}
        onItemAction={vi.fn().mockResolvedValue(undefined)}
        lookupFieldOptions={() => []}
      />,
    );

    expect(screen.getByText("Select a row from Compendium to view contextual details and actions.")).toBeInTheDocument();
  });
});
