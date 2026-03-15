import { ManualDetailsForm } from "./ManualDetailsForm";
import type { ItemDetailsFormProps } from "./types";
import { styled } from "app/styletron";

export function BackgroundDetailsForm(props: ItemDetailsFormProps) {
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
            { field: "Type" },
          ],
        },
        {
          title: "Feature",
          fields: [
            { field: "Feature Name", span: 6 },
            { field: "Feature Type", span: 6 },
            { field: "Feature", span: "full" },
          ],
        },
        {
          title: "Languages",
          fields: [
            { field: "Language Choice", span: 6 },
            { field: "Language Count", span: 6 },
            { field: "Languages", span: "full" },
          ],
        },
        {
          title: "Proficiencies",
          fields: [
            { field: "Skills Proficiency", span: "full" },
            { field: "Tool Proficiency", span: "full" },
          ],
        },
        {
          title: "Roleplay Tables",
          fields: [
            { field: "Personality Traits", span: "full" },
            { field: "Ideals", span: "full" },
            { field: "Bonds", span: "full" },
            { field: "Flaws", span: "full" },
          ],
        },
        {
          title: "Description",
          className: "details-section--description",
          fields: [
            { field: "Description", span: "full" },
            { field: "Equipment Text", span: "full" },
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
