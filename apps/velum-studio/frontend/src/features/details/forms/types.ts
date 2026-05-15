import type { FieldSuggestionResponse, ValidationCatalogResponse } from "shared/types/api";
import type { GroupedFields } from "shared/utils/fields";

export interface ItemDetailsFormProps {
  sheet: string;
  grouped: GroupedFields;
  rowData: Record<string, unknown>;
  validationCatalog: ValidationCatalogResponse | null;
  lookupFieldOptions: (fieldName: string) => string[];
  onFieldChange: (fieldName: string, value: unknown) => void;
  onRowDataPatch: (patch: Record<string, unknown>) => void;
  onSuggestField: (fieldName: string, validationOptions: string[]) => Promise<FieldSuggestionResponse>;
}

export interface ManualFieldConfig {
  field: string | string[];
  aliases?: string[];
  label?: string;
  span?: number | "full";
}

export interface ManualSubsectionConfig {
  title: string;
  fields: ManualFieldConfig[];
}

export interface ManualSectionConfig {
  title: string;
  className?: string;
  fields?: ManualFieldConfig[];
  subsections?: ManualSubsectionConfig[];
  includeRemaining?: boolean;
}
