import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { ValidationsTab } from "../ValidationsTab";

describe("ValidationsTab", () => {
  it("loads and renders validation rows for selected sheet", async () => {
    const onLoadValidationRows = vi.fn().mockResolvedValue({
      source: "xlsx",
      sheet: "Spells:Validations",
      offset: 0,
      limit: 500,
      total_rows: 1,
      columns: ["School"],
      rows: [{ School: "Evocation" }],
    });

    render(
      <ValidationsTab
        loading={false}
        source="xlsx"
        validationSheets={["Spells:Validations"]}
        cellCharLimit={150}
        onLoadValidationRows={onLoadValidationRows}
      />,
    );

    await waitFor(() => {
      expect(onLoadValidationRows).toHaveBeenCalledWith("Spells:Validations");
    });

    expect(screen.getByText("Spells:Validations | 1 rows")).toBeInTheDocument();
    expect(screen.getByText("Evocation")).toBeInTheDocument();
  });
});
