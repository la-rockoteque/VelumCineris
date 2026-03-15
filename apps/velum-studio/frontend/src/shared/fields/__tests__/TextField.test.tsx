import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { TextField } from "../TextField";

describe("TextField", () => {
  it("renders and emits updated text", () => {
    const onChange = vi.fn();
    render(<TextField value="Arc" onChange={onChange} placeholder="Name" className="text-field-shell" />);

    const input = screen.getByPlaceholderText("Name");
    expect(input).toHaveClass("text-field-shell");
    fireEvent.change(input, { target: { value: "Arc Flash" } });

    expect(onChange).toHaveBeenCalledWith("Arc Flash");
  });
});
