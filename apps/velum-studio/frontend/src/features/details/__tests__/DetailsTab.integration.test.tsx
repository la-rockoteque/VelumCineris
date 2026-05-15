import { render, screen, waitFor } from "@testing-library/react";
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
    const onSuggestField = vi.fn().mockResolvedValue({
      provider: "chatgpt",
      model: "gpt-5-mini",
      status: "ok",
      field_name: "Description",
      current_value: "A bright arc of energy.",
      suggested_value: "A lash of controlled lightning leaps to one creature you can see within range.",
      rationale: "Tighter 5e wording keeps the field concise and mechanically legible.",
    });

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
        onSuggestField={onSuggestField}
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

    await user.click(screen.getByLabelText("Live Execute"));
    expect(onActionModeChange).toHaveBeenCalledWith("live");
  });

  it("requests and accepts a field suggestion", async () => {
    const user = userEvent.setup();
    const onRowDataChange = vi.fn();
    const onSuggestField = vi.fn().mockResolvedValue({
      provider: "chatgpt",
      model: "gpt-5-mini",
      status: "ok",
      field_name: "Description",
      current_value: "A bright arc of energy.",
      suggested_value: "A lash of controlled lightning leaps to one creature you can see within range.",
      rationale: "Tighter 5e wording keeps the field concise and mechanically legible.",
    });

    render(
      <DetailsTab
        loading={false}
        selected={selectedRow()}
        validationCatalog={validationCatalog()}
        cellCharLimit={150}
        actionMode="dry_run"
        onActionModeChange={vi.fn()}
        onRowDataChange={onRowDataChange}
        onItemAction={vi.fn().mockResolvedValue(undefined)}
        lookupFieldOptions={() => []}
        onSuggestField={onSuggestField}
      />,
    );

    await user.click(screen.getByRole("button", { name: "Suggest balanced value for Description" }));
    expect(onSuggestField).toHaveBeenCalledWith("Description", []);

    expect(await screen.findByText("ChatGPT Suggestion")).toBeInTheDocument();
    expect(screen.getByText("A lash of controlled lightning leaps to one creature you can see within range.")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Accept suggestion for Description" }));
    expect(onRowDataChange).toHaveBeenCalledWith(
      expect.objectContaining({
        Description: "A lash of controlled lightning leaps to one creature you can see within range.",
      }),
    );
  });

  it("can reject a field suggestion", async () => {
    const user = userEvent.setup();
    const onRowDataChange = vi.fn();

    render(
      <DetailsTab
        loading={false}
        selected={selectedRow()}
        validationCatalog={validationCatalog()}
        cellCharLimit={150}
        actionMode="dry_run"
        onActionModeChange={vi.fn()}
        onRowDataChange={onRowDataChange}
        onItemAction={vi.fn().mockResolvedValue(undefined)}
        lookupFieldOptions={() => []}
        onSuggestField={vi.fn().mockResolvedValue({
          provider: "chatgpt",
          model: "gpt-5-mini",
          status: "ok",
          field_name: "Description",
          current_value: "A bright arc of energy.",
          suggested_value: "A steadier arc of force courses toward a creature within range.",
          rationale: "The phrasing is cleaner and easier to adjudicate.",
        })}
      />,
    );

    await user.click(screen.getByRole("button", { name: "Suggest balanced value for Description" }));
    expect(await screen.findByText("ChatGPT Suggestion")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Reject suggestion for Description" }));
    await waitFor(() => {
      expect(screen.queryByText("ChatGPT Suggestion")).not.toBeInTheDocument();
    });
    expect(onRowDataChange).not.toHaveBeenCalled();
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
        onSuggestField={vi.fn()}
      />,
    );

    expect(screen.getByText("Select a row from Compendium to view contextual details and actions.")).toBeInTheDocument();
  });
});
