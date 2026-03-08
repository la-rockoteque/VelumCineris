import { ManualDetailsForm } from "./ManualDetailsForm";
import type { ItemDetailsFormProps } from "./types";

export function FeatDetailsForm(props: ItemDetailsFormProps) {
  return (
    <ManualDetailsForm
      {...props}
      schema={[
        {
          title: "Identifier",
          fields: [
            { field: "Source" },
            { field: "Category" },
            { field: "Tag" },
            { field: "Feat Type" },
          ],
        },
        {
          title: "Prerequisites",
          fields: [
            { field: "Prerequisite", span: "full" },
            { field: "Prerequisite Text", span: "full" },
          ],
        },
        {
          title: "Benefits",
          fields: [
            { field: "ASI", span: 4 },
            { field: "Action Type", span: 4 },
            { field: "Usage Type", span: 4 },
            { field: "Usage Amount", span: 4 },
            { field: "Usage Reset", span: 4 },
            { field: "Scaling Type", span: 4 },
          ],
        },
        {
          title: "Effects",
          fields: [
            { field: "Granted Spells", span: "full" },
            { field: "Conditions Applied", span: "full" },
            { field: "Modifiers Granted", span: "full" },
            { field: "Proficiencies Granted", span: "full" },
          ],
        },
        {
          title: "Rules",
          className: "details-section--description",
          fields: [
            { field: "Rules Text", span: "full" },
            { field: "Rules Bullets", span: "full" },
            { field: "Designer Notes", span: "full" },
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
