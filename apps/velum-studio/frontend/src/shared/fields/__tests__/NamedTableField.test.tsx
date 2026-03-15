import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { NamedTableField } from "../NamedTableField";

describe("NamedTableField", () => {
  it("updates key/value rows and emits serialized value", () => {
    const onChange = vi.fn();

    render(<NamedTableField value="Trait:: Extra damage" keyLabel="Title" valueLabel="Text" onChange={onChange} />);

    fireEvent.change(screen.getByDisplayValue("Trait"), { target: { value: "Burst" } });

    expect(onChange).toHaveBeenCalledWith("Burst:: Extra damage");
  });
});
