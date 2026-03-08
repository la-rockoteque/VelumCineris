import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { selectedRow } from "test/fixtures";

import { IntelligenceTab } from "./IntelligenceTab";

describe("IntelligenceTab", () => {
  it("submits intelligence request with selected row context", async () => {
    const user = userEvent.setup();
    const onRun = vi.fn().mockResolvedValue({ status: "ok" });

    render(<IntelligenceTab loading={false} selected={selectedRow()} output="out" onRun={onRun} />);

    await user.clear(screen.getByLabelText("Instruction"));
    await user.type(screen.getByLabelText("Instruction"), "Tune this spell.");
    await user.click(screen.getByRole("button", { name: "Run Intelligence" }));

    expect(onRun).toHaveBeenCalledTimes(1);
    expect(onRun.mock.calls[0][0]).toMatchObject({
      mode: "custom",
      instruction: expect.stringContaining("Tune this spell."),
      use_local_llm: true,
    });
  });
});
