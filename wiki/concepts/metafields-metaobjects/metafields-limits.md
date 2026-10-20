---
type: concept
nav_path: "Concept → Metafields and metaobjects → Limits"
aliases: ["Metafield limits", "Metaobject limits", "How many metafields", "How many metaobjects", "Max fields per metaobject", "Max metaobject entries", "metafield value size", "LIMIT_EXCEEDED", "MAX_DEFINITIONS_EXCEEDED", "MAX_OBJECTS_EXCEEDED", "PINNED_LIMIT_REACHED", "Лимити на метаполета", "Колко метаобекта"]
tags: [metafields, metaobjects, custom-data, limits, concepts]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 3
---

# Metafields and metaobjects: limits

> Part of [[metafields-metaobjects]]. See the hub for definitions, types and permissions.

## Definition

Every limit on metafields and metaobjects, in one place. At the time of writing the limits are the same on every plan. A refusal names the limit reached, e.g. *"The limit of 128 metaobject definitions is reached."*, with an error code on the APIs.

## Scope

### Definitions

| What | Limit | Error code |
|---|---|---|
| Metafield definitions per owner type (products / categories / customers) | 256 | `LIMIT_EXCEEDED` |
| Pinned definitions per owner type | 50 | `PINNED_LIMIT_REACHED` |
| Metaobject definitions per store | 128 | `MAX_DEFINITIONS_EXCEEDED` |
| Fields per metaobject definition | 40 | `INVALID` |
| Entries per metaobject definition | 1,000,000 | `MAX_OBJECTS_EXCEEDED` |
| Definitions with the admin filter, per owner type or per metaobject definition | 50 | `OWNER_TYPE_LIMIT_EXCEEDED_FOR_USE_AS_ADMIN_FILTERS` |
| Product definitions usable as a smart-collection condition | 128 | `OWNER_TYPE_LIMIT_EXCEEDED_FOR_AUTOMATED_COLLECTIONS` |

### Identifiers

| What | Limit |
|---|---|
| Namespace; metaobject type | 3–255 characters: letters, digits, `-`, `_` |
| Key; metaobject field key | 2–64 characters, same characters |
| Entry handle | up to 255 characters: letters, digits, `-` |
| Definition name / description | 255 characters each |

### Values

| What | Limit |
|---|---|
| A value | 64 KB |
| A `json` value | 128 KB |
| A `url` or `id` value | 2 KB |
| Items in a list | 128 |
| Items in a list of metaobject or mixed references | 1,024 |
| A whole list's stored value | 8 MB |
| Choices of a single-line text | 128, together at most 300,000 characters |
| Allowed domains of a `url` / `link` | 128 |
| A `regex` validation | 1,000 characters |
| A `number_decimal` | 13 digits before and 9 after the point |
| A smart-collection condition's value | 191 characters |

### Calls

| What | Limit |
|---|---|
| Values set in one `metafieldsSet` | 25 |
| Values deleted in one `metafieldsDelete` | 250 |
| Identifiers in one Storefront API `metafields(identifiers:)` | 250 |
| Keys in one Admin GraphQL `metafields(keys:)` | 250 |
| Entries in one batch deletion | 250 |

### Search queries

The admin filter and the Storefront API's `metaobjects(query:)` use one search syntax ([[metafields-capabilities]]), within these bounds: 128 KB per query, 250 terms, 16 nested groups. Free text in a products search is at most 10 words. A filtered list's total is counted up to 10,000 matches. Beyond that the count shows as "at least".

## Contrasts

- **Limits vs page sizes**: lists of definitions and entries are read page by page. A page size is not a cap on how many exist.
- **Owner-type limits are separate**: products, categories and customers each have their own 256 definitions and 50 pinned. The 128 metaobject definitions are per store, each with its own 1,000,000 entries.

## Where it applies

- Every create in Settings → Metaobjects and in the Admin GraphQL API checks the definition limits before saving.
- Every value write (Metafields card, entry form, `metafieldsSet`, metaobject mutations) checks the value limits.
- Nitrogen storefronts meet the Storefront API's 250-identifier limit when they read many metafields of one product in one request ([[metafields-nitrogen]]).

## Related

- [[metafields-metaobjects]]: hub.
- [[metafields-types]]: value formats behind the size limits.
- [[metafields-capabilities]]: the admin-filter and smart-collection limits in context.

## Open Questions

- None known.
