import React from "react";
import { fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { ComponentsField } from "../ComponentsField";

describe("ComponentsField", () => {
  it("builds component string from toggles and material note", async () => {
    const user = userEvent.setup();
    const onChangeSpy = vi.fn();

    function Harness() {
      const [value, setValue] = React.useState("");
      return (
        <ComponentsField
          value={value}
          onChange={(next) => {
            onChangeSpy(next);
            setValue(next);
          }}
        />
      );
    }

    render(<Harness />);

    await user.click(screen.getByLabelText("V"));
    expect(onChangeSpy).toHaveBeenLastCalledWith("V");

    await user.click(screen.getByLabelText("M"));
    const materialInput = screen.getByPlaceholderText("Material details");
    fireEvent.change(materialInput, { target: { value: "a pearl" } });

    expect(onChangeSpy).toHaveBeenLastCalledWith("V, M (a pearl)");
  });
});
