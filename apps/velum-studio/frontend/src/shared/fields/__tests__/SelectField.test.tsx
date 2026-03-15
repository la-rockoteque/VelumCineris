import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { SelectField } from "../SelectField";

describe("SelectField", () => {
  it("emits selected option", () => {
    const onChange = vi.fn();
    render(<SelectField value="" options={["Wizard", "Cleric"]} onChange={onChange} />);

    const select = screen.getByRole("combobox");
    fireEvent.change(select, { target: { value: "Wizard" } });

    expect(onChange).toHaveBeenCalledWith("Wizard");
  });
});
