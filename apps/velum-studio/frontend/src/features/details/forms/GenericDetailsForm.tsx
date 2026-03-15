import { ManualDetailsForm } from "./ManualDetailsForm";
import type { ItemDetailsFormProps } from "./types";
import { styled } from "app/styletron";

export function GenericDetailsForm(props: ItemDetailsFormProps) {
  return (
    <ManualDetailsForm
      {...props}
      schema={[
        { title: "Primary", fields: [] },
        { title: "Additional", fields: [], includeRemaining: true },
      ]}
    />
  );
}
