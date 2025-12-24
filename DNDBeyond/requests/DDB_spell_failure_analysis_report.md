
# D&D Beyond Spell Creation Failure Analysis Report

This report analyzes why certain spells failed to be created on D&D Beyond and provides concrete, mechanical fixes.
It is designed to be fed directly to an LLM (Claude) to implement automated corrections.

---

## Executive Summary

D&D Beyond does **not** return explicit API errors when homebrew spell creation fails.
Instead, it returns HTTP 200 with a silently re-rendered HTML form.
Failures must be inferred from data patterns.

Across 401 attempted spells:
- 60 created successfully
- 4 skipped (already existed)
- **337 failed due to validation issues**

These failures are deterministic and correctable.

---

## Root Causes (In Order of Impact)

### 1. Invalid Duration Configuration (CRITICAL)

**Observed pattern**
```
duration_id = 2
duration_interval = ""
duration_unit = ""
```

**Why it fails**
- duration_id = 2 means a *timed duration*
- Timed durations REQUIRE:
  - duration_interval (number)
  - duration_unit (round, minute, hour, etc.)

**Fix rule**
```
IF duration_id == 2:
  duration_interval MUST be set
  duration_unit MUST be set
```

**Common valid mappings**
| Effect | duration_id | interval | unit |
|------|------------|----------|------|
| Instant | 1 | — | — |
| Until next turn | 2 | 1 | round |
| 1 minute | 2 | 1 | minute |
| Concentration 1 min | 2 | 1 | minute |

---

### 2. Range / Origin Mismatch (CRITICAL)

**Observed invalid combinations**
```
range = 0 AND origin_id = Distance
range > 0 AND origin_id = Self
```

**Valid logic**
| Range | origin_id | Valid |
|-----|----------|------|
| 0 | Self or Touch | Yes |
| >0 | Distance | Yes |
| 0 | Distance | No |
| >0 | Self | No |

**Fix rule**
```
IF range == 0:
  origin_id = Self or Touch
ELSE:
  origin_id = Distance
```

---

### 3. Invalid or Truncated HTML Descriptions (CRITICAL)

**Observed pattern**
- HTML cut mid-sentence
- Missing closing tags
- Unescaped characters

**Why it fails**
- DDB sanitizes HTML strictly
- Invalid markup silently fails validation

**Fix rule**
```
- Wrap content in <p> blocks
- Ensure all tags are closed
- Enforce max-length safety cap
```

---

### 4. Higher-Level Scaling Flag Mismatch (HIGH)

**Observed invalid state**
```
can_cast_at_higher_level = false
higher_level_scale = 3
```

**Fix rule**
```
IF can_cast_at_higher_level == false:
  higher_level_scale MUST be null or 0
```

---

### 5. Cantrip Rule Violations (MEDIUM)

Some cantrips fail despite valid structure due to DDB design constraints:
- Auto-stabilizing creatures
- Altering death saves
- Non-damage effects without saves

**Fix strategy**
- Flag such spells as "DDB-incompatible"
- Exclude or up-level them before submission

---

## Recommended Preflight Validation Pipeline

### Mandatory Checks
1. Normalize duration
2. Normalize range + origin
3. Sanitize HTML
4. Normalize higher-level scaling
5. Reject unsafe cantrip mechanics

### Suggested Architecture
- Canonical CSV / JSON source of truth
- DDB compatibility transformer
- Separate DDB-safe vs canon-only spells

---

## Outcome

All observed failures are:
- Deterministic
- Preventable
- Fixable via preprocessing

D&D Beyond is not unreliable.
It is **strict, undocumented, and silent**.

This report can be used to implement a fully automated fix pipeline.

---
