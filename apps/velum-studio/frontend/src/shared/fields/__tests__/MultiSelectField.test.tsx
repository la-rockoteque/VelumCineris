import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { MultiSelectField } from "../MultiSelectField";

describe("MultiSelectField", () => {
  it("opens dropdown and emits selected values", async () => {
    const user = userEvent.setup();
    const onChange = vi.fn();

    render(<MultiSelectField value="" options={["Fire", "Cold"]} onChange={onChange} placeholder="Pick tags" className="multi-shell" />);

    const trigger = screen.getByRole("button", { name: /pick tags/i });
    expect(trigger.closest("div")).toHaveClass("multi-shell");
    await user.click(trigger);
    await user.click(screen.getByLabelText("Fire"));

    expect(onChange).toHaveBeenCalledWith("Fire");
  });
});
