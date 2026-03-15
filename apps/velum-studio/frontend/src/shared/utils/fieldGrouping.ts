import { findRowKeyByNormalized } from "./fieldLookup";
import {
  isBackgroundSheet,
  isFeatSheet,
  isMonsterSheet,
  isSpeciesSheet,
  isSpellSheet,
} from "./fieldSheets";
import fieldGroupingRules from "./fieldGroupingRules.json";
import { createEmptyGroups, type FieldBucket, type GroupedFields } from "./fieldTypes";
import { normalizeKey } from "./text";

type DomainKey =
  | "generic"
  | "spell"
  | "monster"
  | "species"
  | "feat"
  | "background";

type BucketMatchType =
  | "anyTerm"
  | "exact"
  | "startsWith"
  | "anyTermOrRawLengthAtLeast";

interface BucketRuleConfig {
  bucket: FieldBucket;
  type: BucketMatchType;
  terms: string[];
  rawLengthAtLeast?: number;
}

interface ContainsAnySkipConfig {
  containsAny: string[];
  unlessContainsAny?: string[];
}

interface ConditionalSkipConfig {
  whenExact: string;
  requiresField: string;
  requiredValue: string;
}

interface SkipConfig {
  exact?: string[];
  startsWith?: string[];
  containsAny?: ContainsAnySkipConfig[];
  conditional?: ConditionalSkipConfig[];
}

interface PostFilterConfig {
  bucket: FieldBucket;
  excludeEndsWith?: string[];
}

interface DomainGroupingConfig {
  skip?: SkipConfig;
  buckets: BucketRuleConfig[];
  postFilters?: PostFilterConfig[];
}

interface SectionOrderEntry {
  bucket: FieldBucket;
  label: string;
}

interface FieldGroupingRulesConfig {
  groupingRules: Record<DomainKey, DomainGroupingConfig>;
  sectionOrder: {
    default: SectionOrderEntry[];
    species: SectionOrderEntry[];
    feat: SectionOrderEntry[];
    monster: SectionOrderEntry[];
    background: SectionOrderEntry[];
  };
}

const rules = fieldGroupingRules as FieldGroupingRulesConfig;

export function hasAnyTerm(text: string, terms: string[]): boolean {
  return terms.some((term) => text.includes(term));
}

function resolveDomain(sheetName: string): DomainKey {
  if (isMonsterSheet(sheetName)) {
    return "monster";
  }
  if (isSpellSheet(sheetName)) {
    return "spell";
  }
  if (isSpeciesSheet(sheetName)) {
    return "species";
  }
  if (isBackgroundSheet(sheetName)) {
    return "background";
  }
  if (isFeatSheet(sheetName)) {
    return "feat";
  }
  return "generic";
}

function matchesBucketRule(
  normalized: string,
  raw: string,
  rule: BucketRuleConfig,
): boolean {
  if (rule.type === "exact") {
    return rule.terms.includes(normalized);
  }
  if (rule.type === "startsWith") {
    return rule.terms.some((term) => normalized.startsWith(term));
  }
  if (rule.type === "anyTermOrRawLengthAtLeast") {
    return (
      hasAnyTerm(normalized, rule.terms) ||
      (typeof rule.rawLengthAtLeast === "number" && raw.length >= rule.rawLengthAtLeast)
    );
  }
  return hasAnyTerm(normalized, rule.terms);
}

function shouldSkip(
  rowData: Record<string, unknown>,
  normalized: string,
  skip: SkipConfig | undefined,
): boolean {
  if (!skip) {
    return false;
  }
  if (skip.exact?.includes(normalized)) {
    return true;
  }
  if (skip.startsWith?.some((prefix) => normalized.startsWith(prefix))) {
    return true;
  }

  for (const condition of skip.conditional || []) {
    if (normalized !== condition.whenExact) {
      continue;
    }
    const dependencyKey = findRowKeyByNormalized(rowData, [condition.requiresField]);
    const dependencyValue = dependencyKey ? rowData[dependencyKey] : null;
    const normalizedValue = String(dependencyValue ?? "").toLowerCase();
    if (normalizedValue !== condition.requiredValue.toLowerCase()) {
      return true;
    }
  }

  for (const rule of skip.containsAny || []) {
    if (!hasAnyTerm(normalized, rule.containsAny)) {
      continue;
    }
    if (rule.unlessContainsAny && hasAnyTerm(normalized, rule.unlessContainsAny)) {
      continue;
    }
    return true;
  }

  return false;
}

function resolveBucket(
  normalized: string,
  raw: string,
  bucketRules: BucketRuleConfig[],
): FieldBucket {
  for (const rule of bucketRules) {
    if (matchesBucketRule(normalized, raw, rule)) {
      return rule.bucket;
    }
  }
  return "additional";
}

function applyPostFilters(
  groups: GroupedFields,
  postFilters: PostFilterConfig[] | undefined,
): GroupedFields {
  if (!postFilters?.length) {
    return groups;
  }
  for (const filter of postFilters) {
    if (!filter.excludeEndsWith?.length) {
      continue;
    }
    groups[filter.bucket] = groups[filter.bucket].filter(
      (field) =>
        !filter.excludeEndsWith?.some((suffix) => field.normalized.endsWith(suffix)),
    );
  }
  return groups;
}

export function groupDetailFields(
  sheetName: string,
  rowData: Record<string, unknown>,
): GroupedFields {
  const domain = resolveDomain(sheetName);
  const domainRules = rules.groupingRules[domain];
  const groups = createEmptyGroups();

  for (const [key, value] of Object.entries(rowData)) {
    if (key === "_sheet_row") {
      continue;
    }

    const normalized = normalizeKey(key);
    if (shouldSkip(rowData, normalized, domainRules.skip)) {
      continue;
    }

    const raw = value == null ? "" : String(value);
    const bucket = resolveBucket(normalized, raw, domainRules.buckets);
    groups[bucket].push({ key, value, normalized, raw });
  }

  return applyPostFilters(groups, domainRules.postFilters);
}

export function getSectionOrder(sheetName: string): Array<[FieldBucket, string]> {
  const domain = resolveDomain(sheetName);
  const order =
    domain === "species" ||
    domain === "feat" ||
    domain === "monster" ||
    domain === "background"
      ? rules.sectionOrder[domain]
      : rules.sectionOrder.default;
  return order.map((item) => [item.bucket, item.label]);
}
