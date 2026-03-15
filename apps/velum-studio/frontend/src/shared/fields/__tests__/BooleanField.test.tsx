import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { BooleanField } from "../BooleanField";

describe("BooleanField", () => {
  it("toggles boolean string values", async () => {
    const user = userEvent.setup();
    const onChange = vi.fn();

    render(<BooleanField value="False" onChange={onChange} />);
    await user.click(screen.getByRole("checkbox"));

    expect(onChange).toHaveBeenCalledWith("True");
  });
});
