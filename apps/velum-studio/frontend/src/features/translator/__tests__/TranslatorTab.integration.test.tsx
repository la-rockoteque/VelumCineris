import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { selectedRow, translatorContext } from "test/fixtures";

import { TranslatorTab } from "../TranslatorTab";

describe("TranslatorTab", () => {
  it("loads language targets and submits translation requests", async () => {
    const user = userEvent.setup();
    const onLoadTargets = vi.fn().mockResolvedValue({ source: "xlsx", targets: ["Elvish", "Dwarvish"] });
    const onLoadContext = vi.fn().mockResolvedValue(translatorContext());
    const onTranslate = vi.fn().mockResolvedValue(undefined);

    render(
      <TranslatorTab
        loading={false}
        source="xlsx"
        selected={selectedRow()}
        output="Translation output"
        romanized="arku"
        symbolized="ᚨᚱᚲᚢ"
        context={translatorContext()}
        onLoadTargets={onLoadTargets}
        onLoadContext={onLoadContext}
        onTranslate={onTranslate}
      />,
    );

    await waitFor(() => {
      expect(onLoadTargets).toHaveBeenCalledTimes(1);
      expect(onLoadContext).toHaveBeenCalledWith("Elvish");
    });

    await waitFor(() => {
      expect((screen.getByLabelText("English Input") as HTMLTextAreaElement).value).toContain("Arc Flash");
    });

    await user.click(screen.getByRole("button", { name: "Translate" }));
    expect(onTranslate).toHaveBeenCalledWith("Elvish", "Arc Flash");

    await user.click(screen.getByRole("button", { name: "Reload Context" }));
    expect(onLoadContext).toHaveBeenCalledTimes(2);
  });
});
