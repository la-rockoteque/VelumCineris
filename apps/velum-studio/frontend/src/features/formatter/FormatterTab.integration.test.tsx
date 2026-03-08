import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { selectedRow } from "test/fixtures";

import { FormatterTab } from "./FormatterTab";

describe("FormatterTab", () => {
  it("loads templates and runs formatter preview for selected row", async () => {
    const user = userEvent.setup();
    const onSelectRow = vi.fn().mockResolvedValue(undefined);
    const onLoadRows = vi.fn().mockResolvedValue({
      source: "xlsx",
      sheet: "Spells",
      offset: 0,
      limit: 500,
      total_rows: 1,
      columns: ["Name"],
      rows: [{ _sheet_row: 2, Name: "Arc Flash" }],
    });
    const onRunPreview = vi.fn().mockResolvedValue({ status: "ok" });
    const onLoadTemplates = vi.fn().mockResolvedValue({
      templates: [{ name: "velum-default", label: "Velum Default" }],
    });
    const onLoadTemplate = vi.fn().mockResolvedValue({
      css: ":root { --accent: #9b4d1f; }",
      palette: [{ token: "--accent", value: "#9b4d1f" }],
    });
    const onSaveSettingsPatch = vi.fn().mockResolvedValue(undefined);

    render(
      <FormatterTab
        loading={false}
        source="xlsx"
        sheets={["Spells"]}
        selected={selectedRow({
          rowData: {
            _sheet_row: 2,
            Name: "Arc Flash",
            Homebrewery: "Arc Flash - Brew",
          },
        })}
        settings={{}}
        output="Formatter output"
        onSelectRow={onSelectRow}
        onLoadRows={onLoadRows}
        onRunPreview={onRunPreview}
        onLoadTemplates={onLoadTemplates}
        onLoadTemplate={onLoadTemplate}
        onSaveSettingsPatch={onSaveSettingsPatch}
      />,
    );

    await waitFor(() => {
      expect(onLoadRows).toHaveBeenCalledWith("Spells");
      expect(onLoadTemplates).toHaveBeenCalled();
      expect(onLoadTemplate).toHaveBeenCalledWith("velum-default");
    });

    expect(screen.getByText("homebrewery: Arc Flash - Brew (Homebrewery)")).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Run Formatter Preview" }));
    expect(onRunPreview).toHaveBeenCalledWith(
      expect.objectContaining({
        source: "xlsx",
        sheet: "Spells",
        row_number: 2,
        targets: ["homebrewery"],
        style_template: "velum-default",
      }),
    );

    await user.click(screen.getByRole("button", { name: "Save Style Settings" }));
    expect(onSaveSettingsPatch).toHaveBeenCalledWith(
      expect.objectContaining({
        formatter: expect.objectContaining({
          style_template: "velum-default",
        }),
      }),
    );
  });
});
