import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { CompendiumTab } from "../CompendiumTab";

describe("CompendiumTab", () => {
  it("renders rows and triggers core row actions", async () => {
    const user = userEvent.setup();
    const onSourceChange = vi.fn().mockResolvedValue(undefined);
    const onSheetChange = vi.fn().mockResolvedValue(undefined);
    const onQueryChange = vi.fn();
    const onRunSearch = vi.fn().mockResolvedValue(undefined);
    const onLimitChange = vi.fn().mockResolvedValue(undefined);
    const onPrevPage = vi.fn().mockResolvedValue(undefined);
    const onNextPage = vi.fn().mockResolvedValue(undefined);
    const onRefresh = vi.fn().mockResolvedValue(undefined);
    const onVisibleColumnsChange = vi.fn().mockResolvedValue(undefined);
    const onOpenContext = vi.fn().mockResolvedValue(undefined);
    const onIntegrationAction = vi.fn().mockResolvedValue(undefined);

    render(
      <CompendiumTab
        loading={false}
        sources={[{ source: "xlsx", available: true }, { source: "google", available: false }]}
        source="xlsx"
        sheets={["Spells", "Monsters"]}
        sheet="Spells"
        query=""
        limit={50}
        offset={0}
        totalRows={1}
        columns={["Name", "Description"]}
        visibleColumns={["Name", "Description"]}
        rows={[{ _sheet_row: 2, Name: "Arc Flash", Description: "A bright flash" }]}
        cellCharLimit={150}
        onSourceChange={onSourceChange}
        onSheetChange={onSheetChange}
        onQueryChange={onQueryChange}
        onRunSearch={onRunSearch}
        onLimitChange={onLimitChange}
        onPrevPage={onPrevPage}
        onNextPage={onNextPage}
        onRefresh={onRefresh}
        onVisibleColumnsChange={onVisibleColumnsChange}
        onOpenContext={onOpenContext}
        onIntegrationAction={onIntegrationAction}
      />,
    );

    expect(screen.getByText("Compendium")).toBeInTheDocument();
    expect(screen.getByText("Arc Flash")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Details" }));
    expect(onOpenContext).toHaveBeenCalledWith(2, "details");

    await user.selectOptions(screen.getByLabelText("Source"), "google");
    expect(onSourceChange).toHaveBeenCalledWith("google");

    await user.click(screen.getByRole("tab", { name: "Monsters" }));
    expect(onSheetChange).toHaveBeenCalledWith("Monsters");

    fireEvent.contextMenu(screen.getByText("Description"));
    await user.click(screen.getByLabelText("Description"));
    expect(onVisibleColumnsChange).toHaveBeenCalledWith(["Name"]);
  });
});
