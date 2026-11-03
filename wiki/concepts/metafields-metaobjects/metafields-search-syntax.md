---
type: concept
nav_path: "Concept → Metafields and metaobjects → Search syntax"
aliases: ["Metafield search syntax", "Metaobject search query", "query argument", "metafields.namespace.key", "fields.key", "Search query language", "extensions.search", "Invalid search field for this query", "Range comparators are for numbers, measurements and dates", "free-text words", "AND OR NOT search", "Търсене по метаполе", "Синтаксис на търсене", "Филтриране на метаобекти"]
tags: [metafields, metaobjects, custom-data, filtering, search, admin-graphql, storefront-api, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 4
---

# Metafield and metaobject search syntax

> Part of [[metafields-metaobjects]]. Which fields can be searched is set by the *Filtering* switch ([[metafields-capabilities]]).

## Definition

Several lists on the Admin GraphQL and Storefront APIs take a `query:` argument, written in one query language. A query is a row of **terms**, such as `metafields.custom.material:cotton` or `fields.starts_at:>=2026-11-01`. This page gives the grammar, how each type matches, which fields each list takes, and how the answer reports what it could not use.

## Scope

### Grammar

| Part | Rule | Example |
|---|---|---|
| Joining terms | AND when nothing is written | `fields.a:1 fields.b:2` |
| `AND`, `OR`, `NOT` | Count only in capitals. **OR binds tighter than AND.** | `fields.a:1 fields.b:2 OR fields.b:3` |
| Negation | `-` right before a term, or `NOT ` | `-fields.archived:true` |
| Groups | Parentheses, up to 16 deep | `(fields.a:1 AND fields.b:2) OR fields.c:3` |
| Comparators | `:`, `:<`, `:>`, `:<=`, `:>=` | `fields.price:>=20` |
| Quotes | Single or double. A quoted value is literal, and a backslash escapes. | `fields.title:"Linen shirt"` |
| Prefix | An unquoted value ending in `*` | `fields.sku:AB*` |
| Has a value | A lone `*` | `fields.color:*` |
| Free text | A word or quoted phrase with no field | `linen "summer shirt"` |

`name:` followed by a space is read as the word `name`.

### A mistake does not fail the search

A malformed term answers a warning, and the rest of the query filters. That covers an unknown field, a field without Filtering on, a value the type cannot hold, an unclosed quote or a stray `)`.

A query is refused whole only in these cases:

- *"The search query is longer than 131072 bytes."*
- *"The search query has more than 250 terms."*
- *"The search query nests more than 16 groups."*
- *"The search query is not UTF-8 text."*
- *"The search query has more than 10 free-text words."*, on `products` only. A quoted phrase counts as one word.

### How each type matches

| Type | Term |
|---|---|
| Single-line and multi-line text, `url`, `color`, `id` | Exact and case-sensitive, or a `*` prefix |
| `link` | By its URL, the same way |
| `boolean` | `true` or `false` |
| `number_integer`, `number_decimal` | Exact or a range |
| `rating` | By its value, exact or a range |
| `money` | By its amount, exact or a range |
| A measurement | Exact or a range across units, the number right before its unit: `fields.weight:>=1kg`. The unit goes by name or symbol in any case: `kg`, `lb`, `cm`, `m2`, `mah`, `gb`, `min`. |
| `date` | Exact or a range |
| `date_time` | Exact or a range, read in UTC without a zone. **A date given for a `date_time` means that whole UTC day.** |
| A reference | Exact, by global ID: `gid://cloudcart/Product/123` ([[metafields-value-formats]]) |
| Any `list.` type | Matches when any item matches |

### Which fields each list takes

| List | Fields | Free text |
|---|---|---|
| Admin GraphQL `products(query:)` | `metafields.{namespace}.{key}:` | Name, description, SKU and barcode. Each word is a term, up to 10. |
| Admin GraphQL `metaobjects(type:, query:)` | `fields.{key}:`, `display_name` (any case), `handle`, `id`, `updated_at` (UTC) | A display name's start, or a handle |
| Admin GraphQL `metafieldDefinitions(query:)` | `key`, `namespace`, `type`, `owner_type`, `id`, `created_at`, `updated_at` (UTC) | Anywhere in the name, namespace or key, in any case |
| Storefront API `metaobjects(type:, query:)` | `fields.{key}:` | — |

`fields.` and `metafields.` terms work once the field's **Filtering** switch is on and its values are prepared.

On `products(query:)`, each `metafields.` term needs permission to read product metafields. Without it the term is left out, with the missing permission as its warning ([[metafields-permissions]]).

### Warnings

Warnings arrive in the response's `extensions.search`, and the key is absent when there are none:

```json
{"extensions": {"search": [{
  "path": ["metaobjects"],
  "query": "fields.topci:delivery",
  "warnings": [{"field": "fields.topci", "message": "Invalid search field for this query."}]
}]}}
```

- Messages include *"Invalid search field for this query."*, *"Range comparators are for numbers, measurements and dates."*, *"A `*` prefix is for text."* and *"Not a value of this field's type."*
- A repeat is folded. A query answers at most 25, the last being *"More warnings are left out."*
- A name is cut to 255 characters, and the echoed query to 1,024.
- The Storefront API reports them the same way. On a type the storefront does not show, it answers only the query's syntax warnings.

## Contrasts

- **`query:` vs the admin's list search**: the entries list in the admin takes plain text ([[metaobject-entries-admin]]). `query:` is for the APIs.
- **`query:` vs `productFilters`**: `metaobjects(query:)` filters entries by their fields. Storefront product listings filter through `productFilters`, by properties, options, vendor, price and tags ([[products-property]]).
- **Search vs smart-collection condition**: a condition compares one value with one operator, and matches the way a term does ([[smart-collections-rule-builder]]).

## Where it applies

- A Nitrogen storefront picking entries by content ([[metafields-nitrogen]]).
- Integrations finding products or entries by a metafield ([[metafields-admin-api]]).
- The bounds and the 10,000-match count are in [[metafields-limits]].

## Related

- [[metafields-metaobjects]]: hub.
- [[metafields-capabilities]]: the Filtering switch, its types and limits.
- [[metafields-value-formats]]: the values terms are compared with.

## Open Questions

- None known.
