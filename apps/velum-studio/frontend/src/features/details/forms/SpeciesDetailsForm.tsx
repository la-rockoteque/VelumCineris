import { ManualDetailsForm } from "./ManualDetailsForm";
import type { ItemDetailsFormProps } from "./types";
import { styled } from "app/styletron";

export function SpeciesDetailsForm(props: ItemDetailsFormProps) {
  return (
    <ManualDetailsForm
      {...props}
      schema={[
        {
          title: "Identifier",
          fields: [
            { field: "Source" },
            { field: "Size" },
            { field: "Demonym" },
            { field: "Tag" },
            { field: "Alias", span: 6 },
            { field: "Slogan", span: 6 },
          ],
        },
        {
          title: "Stats",
          fields: [
            { field: "Ability", span: 4 },
            { field: "Score", span: 4 },
            { field: "Walk Speed", span: 4 },
            { field: "Fly Speed", span: 4 },
            { field: "Speed", span: 4 },
            { field: "Vision", span: 4 },
            { field: "Age", span: 4 },
          ],
        },
        {
          title: "Languages",
          fields: [{ field: "Languages", span: "full" }],
        },
        {
          title: "Traits",
          fields: [{ field: "Traits", span: "full" }],
        },
        {
          title: "Lore",
          className: "details-section--description",
          fields: [
            { field: "Intro", span: "full" },
            { field: "Origin", span: "full" },
            { field: "Appearance", span: "full" },
            { field: "Culture Identity", span: "full" },
            { field: "Societal Roles", span: "full" },
            { field: "Naming Conventions", span: "full" },
            { field: "Life in Orimond", span: "full" },
            { field: "Playstyle Roleplaying", span: "full" },
          ],
        },
        {
          title: "Media",
          fields: [
            { field: "Image", span: "full" },
            { field: "Preview", span: "full" },
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
