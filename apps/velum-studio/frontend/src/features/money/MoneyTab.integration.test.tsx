import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { moneyCatalog } from "test/fixtures";

import { MoneyTab } from "./MoneyTab";

describe("MoneyTab", () => {
  it("converts money and refreshes the matrix", async () => {
    const user = userEvent.setup();
    const onRefresh = vi.fn().mockResolvedValue(undefined);

    render(<MoneyTab loading={false} moneyCatalog={moneyCatalog()} onRefresh={onRefresh} />);

    expect(screen.getByText(/1\.00 gp = 10\.00 sp/)).toBeInTheDocument();

    await user.clear(screen.getByLabelText("Amount"));
    await user.type(screen.getByLabelText("Amount"), "2");
    expect(screen.getByText(/2\.00 gp = 20\.00 sp/)).toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Refresh" }));
    expect(onRefresh).toHaveBeenCalledTimes(1);
  });
});
