import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { LongTextField } from "../LongTextField";

describe("LongTextField", () => {
  it("renders textarea and emits changes", () => {
    const onChange = vi.fn();
    render(<LongTextField value="Old" rows={4} onChange={onChange} placeholder="Description" />);

    const textarea = screen.getByPlaceholderText("Description");
    fireEvent.change(textarea, { target: { value: "New description" } });

    expect(onChange).toHaveBeenCalledWith("New description");
  });
});
