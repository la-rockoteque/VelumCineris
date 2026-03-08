import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { SettingsTab } from "./SettingsTab";

describe("SettingsTab", () => {
  it("saves and resets compendium settings", async () => {
    const user = userEvent.setup();
    const onSavePatch = vi.fn().mockResolvedValue(undefined);
    const onResetColumns = vi.fn().mockResolvedValue(undefined);

    render(
      <SettingsTab
        loading={false}
        source="xlsx"
        settings={{
          default_source: "auto",
          compendium: {
            minimal_columns_default: true,
            minimal_column_count: 8,
            cell_char_limit: 150,
          },
        }}
        onSavePatch={onSavePatch}
        onResetColumns={onResetColumns}
      />,
    );

    await user.selectOptions(screen.getByLabelText("Default Source"), "google");
    await user.selectOptions(screen.getByLabelText("Minimal Columns by Default"), "false");
    await user.clear(screen.getByLabelText("Minimal Column Count"));
    await user.type(screen.getByLabelText("Minimal Column Count"), "40");
    await user.clear(screen.getByLabelText("Cell Char Limit"));
    await user.type(screen.getByLabelText("Cell Char Limit"), "10");
    await user.click(screen.getByRole("button", { name: "Save Settings" }));

    expect(onSavePatch).toHaveBeenCalledWith({
      default_source: "google",
      compendium: {
        minimal_columns_default: false,
        minimal_column_count: 30,
        cell_char_limit: 40,
      },
    });

    await user.click(screen.getByRole("button", { name: "Reset Sheet Columns" }));
    expect(onResetColumns).toHaveBeenCalledTimes(1);
  });
});
