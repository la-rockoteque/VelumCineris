import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { StatWithModifierField } from "../StatWithModifierField";

describe("StatWithModifierField", () => {
  it("shows computed modifier and emits stat edits", () => {
    const onChange = vi.fn();

    render(<StatWithModifierField value="14" onChange={onChange} />);

    expect(screen.getByText("+2")).toBeInTheDocument();

    fireEvent.change(screen.getByRole("spinbutton"), { target: { value: "16" } });
    expect(onChange).toHaveBeenCalledWith("16");
  });
});
