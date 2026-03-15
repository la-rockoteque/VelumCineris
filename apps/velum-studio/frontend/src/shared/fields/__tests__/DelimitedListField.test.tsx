import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { DelimitedListField } from "../DelimitedListField";

describe("DelimitedListField", () => {
  it("edits list values and emits joined result", () => {
    const onChange = vi.fn();

    render(<DelimitedListField value="Fire, Cold" onChange={onChange} />);

    fireEvent.change(screen.getByDisplayValue("Fire"), { target: { value: "Lightning" } });

    expect(onChange).toHaveBeenCalledWith("Lightning, Cold");
  });
});
