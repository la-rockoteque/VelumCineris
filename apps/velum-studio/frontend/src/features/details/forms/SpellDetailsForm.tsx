import { ManualDetailsForm } from "./ManualDetailsForm";
import type { ItemDetailsFormProps } from "./types";

export function SpellDetailsForm(props: ItemDetailsFormProps) {
  return (
    <ManualDetailsForm
      {...props}
      schema={[
        {
          title: "Identifier",
          fields: [
            { field: "Source" },
            { field: "Level" },
            { field: "School" },
            { field: "Class", span: 6 },
            { field: "New Class", span: 6 },
            { field: "Foundry Tag", span: 6 },
            { field: "Theme", span: 6 },
          ],
        },
        {
          title: "Mechanics",
          fields: [
            { field: "Casting Time", span: 4 },
            { field: "Range", span: 4 },
            { field: "Duration", span: 4 },
            { field: "Units Distance", span: 4 },
            { field: "Distance", span: 4 },
            { field: "Up To", span: 4 },
            { field: "Components", span: "full" },
            { field: "Ritual" },
            { field: "Concentration" },
            { field: "Saving Throw", span: 4 },
            { field: "Success", span: 4 },
            { field: "Fail", span: 4 },
            { field: "Skill Check", span: 4 },
            { field: "Ability Check Trigger", span: 8 },
            { field: "Blood Pact" },
            { field: "Blood Pact Effect", span: "full" },
          ],
        },
        {
          title: "Description",
          className: "details-section--description",
          fields: [
            { field: "Quotes", span: "full" },
            { field: "Description", span: "full" },
            { field: "Notes", span: "full" },
            { field: "Clarification", span: "full" },
          ],
        },
        {
          title: "Additional",
          fields: [],
          includeRemaining: true,
        },
      ]}
    />
  );
}
