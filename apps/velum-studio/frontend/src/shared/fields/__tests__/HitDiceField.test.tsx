import React from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";
import { styled } from "app/styletron";

import { HitDiceField } from "../HitDiceField";

describe("HitDiceField", () => {
  it("renders and updates a compound XDY value", async () => {
    const user = userEvent.setup();
    const onChangeSpy = vi.fn();

    function Harness() {
      const [value, setValue] = React.useState("3d8+2");
      return (
        <HitDiceField
          className="hit-dice-shell"
          value={value}
          onChange={(next) => {
            onChangeSpy(next);
            setValue(next);
          }}
        />
      );
    }

    render(<Harness />);

    expect(screen.getByPlaceholderText("Count")).toHaveValue(3);
    expect(screen.getByLabelText("Dice type")).toHaveValue("8");
    expect(screen.getByPlaceholderText("Bonus")).toHaveValue(2);
    expect(screen.getByPlaceholderText("Count").closest("div")).toHaveClass("hit-dice-shell");

    const count = screen.getByPlaceholderText("Count");
    await user.click(count);
    await user.keyboard("{Control>}a{/Control}4");
    expect(onChangeSpy).toHaveBeenLastCalledWith("4d8+2");

    const diceType = screen.getByLabelText("Dice type");
    await user.selectOptions(diceType, "10");
    expect(onChangeSpy).toHaveBeenLastCalledWith("4d10+2");

    const bonus = screen.getByPlaceholderText("Bonus");
    await user.click(bonus);
    await user.keyboard("{Control>}a{/Control}5");
    expect(onChangeSpy).toHaveBeenLastCalledWith("4d10+5");
  });

  it("can be wrapped by Styletron styled()", () => {
    const StyledHitDiceField = styled(HitDiceField, {});
    render(<StyledHitDiceField value="2d6+1" onChange={() => undefined} />);
    expect(screen.getByPlaceholderText("Count")).toHaveValue(2);
    expect(screen.getByLabelText("Dice type")).toHaveValue("6");
  });
});
