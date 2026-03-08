import type { ValidationCatalogResponse } from "shared/types/api";
import type { GroupedFields } from "shared/utils/fields";

export interface ItemDetailsFormProps {
  sheet: string;
  grouped: GroupedFields;
  rowData: Record<string, unknown>;
  validationCatalog: ValidationCatalogResponse | null;
  lookupFieldOptions: (fieldName: string) => string[];
  onFieldChange: (fieldName: string, value: unknown) => void;
  onRowDataPatch: (patch: Record<string, unknown>) => void;
}

export interface ManualFieldConfig {
  field: string;
  span?: number | "full";
}

export interface ManualSectionConfig {
  title: string;
  className?: string;
  fields: ManualFieldConfig[];
  includeRemaining?: boolean;
}
