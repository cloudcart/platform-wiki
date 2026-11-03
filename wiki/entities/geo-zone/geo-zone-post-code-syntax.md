---
type: entity
nav_path: "Entity → Geo Zone → Post-code syntax"
aliases: ["Post-code patterns", "Operation 11", "OPERATION_POST_CODE", "Zip code wildcards", "Post-code ranges", "Four-dot range syntax", "Post-code matching"]
tags: [entity, geo, zones, post-codes, settings]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

# Geo Zone — Post-code syntax

> Part of [[geo-zone]]. See the hub for related aspects (fields, operations, relationships, lifecycle, matching rules).

## Identity

Operation 11 (OPERATION_POST_CODE) matches customer addresses by post-code within a country. The merchant types a **comma-separated list of patterns** into one field on the zone rule, and the platform checks each customer's post-code against that list at runtime. This page documents the pattern grammar — exact codes, wildcards, and four-dot ranges — plus the validation rules the platform enforces on save.

Post-code matching is the most flexible operation for zones that don't align with administrative regions (e.g., couriers that deliver to specific delivery zones identified by post code, or last-mile services with non-administrative coverage).

## Aliases

- "Post-code patterns" / "Zip code wildcards" — informal merchant references.
- "Operation 11" / "OPERATION_POST_CODE" — the operation ID and constant.
- "Four-dot range syntax" — describes the `1000....1999` range form, which uses FOUR dots, not two or three.
- "Post-code matching" — the runtime behaviour.

## Key Attributes

### The three pattern forms

Each entry in the comma-separated list is one of three forms:

| Form | Example | Matches |
|------|---------|---------|
| **Exact** | `1000` | Only the exact code `1000`. |
| **Wildcard** | `80*` | Any code starting with `80` (e.g., `8000`, `8045`, `80543`). |
| **Wildcard (suffix)** | `*ER` | Any code ending with `ER` (e.g., `SW1ER`, `M1ER`). |
| **Range** | `1000....1999` | Every numeric code from `1000` to `1999` inclusive. |

The `*` wildcard works anywhere — prefix (`80*`), suffix (`*ER`), or middle (`8*0`).

### Mixed lists

A single rule can mix all three forms in one field, separated by commas:

```
1000....1999,80*,90*,ER9875
```

This matches: every post code from 1000 to 1999, plus anything starting with `80`, plus anything starting with `90`, plus the exact code `ER9875`.

The merchant adds one rule with this whole list, NOT one rule per pattern — the list is itself OR-combined inside operation 11.

### Validation rules

The platform enforces these on save:

- **Range form requires NUMERIC bounds.** `A1000....A1999` is **rejected** — alphanumeric ranges are not supported.
- **Range lower bound must be less than upper bound.** `1999....1000` (inverted) is **rejected**.
- **Range uses exactly FOUR dots.** `1000..1999` (two dots) or `1000...1999` (three dots) are NOT recognised as ranges and are treated as exact-form entries that nothing will match.
- **Wildcards work with alphanumerics.** `M1*` is valid (UK-style post codes). `1*` is valid (numeric).
- **Country is required** alongside the post-code list — operation 11 always scopes to one country. Post-code matching ACROSS countries requires multiple rules (one per country) inside the same zone.

### Whitespace and case

- Whitespace around commas is tolerated (`1000, 2000` is equivalent to `1000,2000`).
- Letter case in alphanumeric post codes is normalised — `er9875` and `ER9875` match the same set.
- Leading zeros are preserved — `0050` and `50` are different patterns.

## Where it appears

- [[settings-geo-zones]] — the post-code field appears when the merchant picks operation 11 in the Add / Edit form.
- [[geo-targeting-post-codes]] — concept-page view of post-code matching inside [[geo-targeting]].

## Common merchant uses

Typical reasons merchants use post-code matching:

- **Courier delivers only to listed post codes.** Same-day delivery partners often restrict by post-code rather than administrative boundary.
- **Special pricing by post code.** A merchant offers cheaper shipping for nearby post codes that don't align with a city boundary.
- **Excluding remote islands.** A country with offshore islands (e.g., GR with the Aegean islands) sets a post-code rule excluding the island post codes from standard shipping; offshore gets a separate rule + zone with a surcharge.
- **Last-mile pickup-point networks.** Some pickup-point providers list their coverage as post-code ranges.

## Tips and pitfalls

- **Don't use range form for non-contiguous codes.** If the post codes the merchant wants are `1000, 1010, 1020, ..., 1090`, the range `1000....1099` will match unwanted in-between codes. Use a comma-separated list of exact codes or `10*0` if there's a consistent suffix pattern.
- **Post-code dataset coverage** depends on what the carrier or courier publishes. CloudCart doesn't ship a post-code-to-city lookup for matching — the platform simply pattern-matches the customer's typed post-code string against the rule. Garbage in (mis-typed post code) → no match.
- **Operation 11 is country-scoped.** A post-code rule with no country selected is rejected. Cross-country post-code overlaps (e.g., `1000` exists in both BG and US) are isolated by the country requirement.

## Related

- [[geo-zone]] — hub.
- [[geo-zone-fields]] — which input fields appear for each operation; post-code field shape.
- [[geo-zone-operations]] — operation 11 in context of the full 11-operation catalogue.
- [[geo-zone-matching-rules]] — how operation-11 rules combine with other rules in the same zone (OR-combined).
- [[geo-targeting-post-codes]] — concept-level treatment of post-code matching.

## Open Questions

- ⏸️ Whether the validation error message for a bad range pattern is shown inline on the field or as a form-level error.
- ⏸️ Whether wildcards can be combined with ranges inside a single pattern (e.g., `1*00....1*99`) — likely rejected as ranges require numeric bounds, but the boundary case isn't documented.
