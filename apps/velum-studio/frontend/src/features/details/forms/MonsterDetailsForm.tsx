import { ManualDetailsForm } from "./ManualDetailsForm";
import type { ItemDetailsFormProps } from "./types";

export function MonsterDetailsForm(props: ItemDetailsFormProps) {
  return (
    <ManualDetailsForm
      {...props}
      schema={[
        {
          title: "Identifier",
          fields: [
            { field: "Source" },
            { field: "CR" },
            { field: "XP" },
            { field: "Size" },
            { field: "Type" },
            { field: "Subtype" },
            { field: "Alignment" },
          ],
        },
        {
          title: "Core Stats",
          fields: [
            { field: "Armor Class", span: 3 },
            { field: "Armor Type", span: 3 },
            { field: "Hit Points", span: 3 },
            { field: "Hit Dice", span: 3 },
            { field: "Proficiency Bonus", span: 3 },
            { field: "Passive Perception", span: 3 },
            { field: "Initiative", span: 3 },
            { field: "Skills", span: "full" },
          ],
        },
        {
          title: "Abilities",
          fields: [
            { field: "STR", span: 2 },
            { field: "DEX", span: 2 },
            { field: "CON", span: 2 },
            { field: "INT", span: 2 },
            { field: "WIS", span: 2 },
            { field: "CHA", span: 2 },
          ],
        },
        {
          title: "Defenses",
          fields: [
            { field: "Damage Vulnerabilities", span: 4 },
            { field: "Damage Resistances", span: 4 },
            { field: "Damage Immunities", span: 4 },
            { field: "Condition Immunities", span: 6 },
            { field: "Weaknesses", span: 6 },
          ],
        },
        {
          title: "Movement",
          fields: [
            { field: "Speed Walking", span: 4 },
            { field: "Speed Swimming", span: 4 },
            { field: "Speed Flying", span: 4 },
            { field: "Speed Burrowing", span: 4 },
            { field: "Speed Climbing", span: 4 },
            { field: "Teleport", span: 4 },
            { field: "Jump", span: 4 },
            { field: "Hover", span: 4 },
            { field: "Glide", span: 4 },
          ],
        },
        {
          title: "Traits",
          fields: [{ field: "Traits", span: "full" }],
        },
        {
          title: "Actions",
          fields: [
            { field: "Actions", span: "full" },
            { field: "Reactions", span: "full" },
            { field: "Bonus Actions", span: "full" },
            { field: "Legendary Actions", span: "full" },
            { field: "Mythic Actions", span: "full" },
          ],
        },
        {
          title: "Description",
          className: "details-section--description",
          fields: [
            { field: "Description", span: "full" },
            { field: "Sidebar", span: "full" },
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
