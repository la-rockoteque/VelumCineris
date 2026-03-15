import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { NumberField } from "../NumberField";

describe("NumberField", () => {
  it("renders number input and emits value", () => {
    const onChange = vi.fn();
    render(<NumberField value="3" onChange={onChange} min={0} max={10} step="1" placeholder="Count" />);

    const input = screen.getByPlaceholderText("Count");
    expect(input).toHaveAttribute("type", "number");

    fireEvent.change(input, { target: { value: "4" } });
    expect(onChange).toHaveBeenCalledWith("4");
  });
});
