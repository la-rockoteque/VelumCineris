import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { selectedRow } from "test/fixtures";

import { ImageTab } from "../ImageTab";

describe("ImageTab", () => {
  it("submits a generation plan for the selected row", async () => {
    const user = userEvent.setup();
    const onRun = vi.fn().mockResolvedValue({ status: "ok" });

    render(<ImageTab loading={false} selected={selectedRow()} output="Image output" onRun={onRun} />);

    await user.selectOptions(screen.getByLabelText("Type"), "monster");
    await user.clear(screen.getByLabelText("Style"));
    await user.type(screen.getByLabelText("Style"), "inked bestiary");
    await user.type(screen.getByLabelText("Prompt Notes"), " glowing sigils");
    await user.click(screen.getByRole("button", { name: "Generate Plan" }));

    expect(onRun).toHaveBeenCalledWith(
      expect.objectContaining({
        entity_name: "Arc Flash",
        entity_type: "monster",
        style: "inked bestiary",
        description: " glowing sigils",
        provider: "chatgpt",
        dry_run: true,
      }),
    );
  });
});
