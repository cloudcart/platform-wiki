---
type: concept
nav_path: "Settings → Metaobjects → a definition → Capabilities"
aliases: ["Metafield capabilities", "Admin filter metafield", "adminFilterable", "Filterable metafield", "Smart collection condition metafield", "smartCollectionCondition", "Unique values", "uniqueValues", "metafields.custom.key:value", "fields.key:value", "Филтър по метаполе", "Умна колекция по метаполе", "Уникални стойности"]
tags: [metafields, metaobjects, custom-data, filtering, smart-collections, concepts]
plan_gates: []
created: 2026-10-20
updated: 2026-10-21
source_count: 5
---

# Metafield capabilities: admin filter, smart-collection condition, unique values

> Part of [[metafields-metaobjects]]. See the hub for definitions, types, limits and permissions.

## Definition

A **capability** is a switch on a definition that makes its values do more than be stored and read. There are three:

| Capability | Offered on | What it does |
|---|---|---|
| **Admin filter** (`adminFilterable`) | Product metafield definitions; metaobject fields | Values can be searched and filtered by. |
| **Smart-collection condition** (`smartCollectionCondition`) | Product metafield definitions of six types | A smart collection can include products by the value. |
| **Unique values** (`uniqueValues`) | Single-line text, URL and integer definitions of any owner type; always on for `id` | No two owners hold the same value. |

## Scope

### Switching on runs in the background

Turning on the admin filter or the smart-collection condition indexes the values that already exist. Meanwhile the capability shows **In progress**, and only once it is **Enabled** does it filter or appear among collection conditions. If indexing fails for good it shows **Failed**, and switching it on again retries. Switching off always works at once.

### Admin filter

- **Types**: every type except `json` and `rich_text_field`, lists included (a list matches when any item matches).
- **Product definitions**: products can be searched by `metafields.{namespace}.{key}:{value}`, e.g. `metafields.custom.material:cotton`, on the Admin GraphQL API's product list. Category and customer definitions cannot have it.
- **Metaobject fields**: entries can be filtered by `fields.{key}:{value}`, on the Admin GraphQL API and on the Storefront API's `metaobjects(type:, query:)` list. This is a Nitrogen storefront's main way to pick entries by content ([[metafields-nitrogen]]).
- **Matching**:
  - Text matches exactly and case-sensitively, or by prefix with `*`.
  - Numbers, measurements and dates take `>`, `>=`, `<` and `<=`; measurements compare in a common unit.
  - A reference matches by the target's global ID, `gid://cloudcart/Product/123` ([[metafields-value-formats]]).
  - `fields.{key}:*` means "has a value", and `-` or `NOT` negates.
  - A term the list cannot use (an unknown field, a field without the filter, a value the type cannot hold) is ignored with a warning rather than failing the search.
- **Text length**: text is indexed by its first 255 characters; longer exact matches are still confirmed in full.
- **Limit**: 50 filterable definitions per owner type, and 50 filterable fields per metaobject definition.

### Smart-collection condition

| Type | Operations |
|---|---|
| `boolean` | equals |
| `number_integer`, `number_decimal`, `rating` | equals, greater than, less than |
| `single_line_text_field` | equals |
| `metaobject_reference` | equals (pick an entry) |

- Only **product** definitions, since a smart collection holds products. Up to **128** definitions can have it.
- A condition's value is at most 191 characters.
- A definition that a smart collection uses **cannot be deleted** while the collection uses it. The same applies to a metaobject definition whose deletion would delete such a metafield definition.
- When a product's value changes, the collections that depend on it are recalculated, as for any other condition ([[products-smart-collections]]).

This is how a metafield shapes what a storefront lists: the smart collection is a normal collection on the Storefront API and on classic themes. Example: `custom.eco_certified = true` gives an "Eco" collection that maintains itself.

### Unique values

- No two products (customers, categories) hold the same value of the definition, and no two entries of one metaobject hold the same value of a field. A save that would repeat a value is refused: the value is already taken.
- **`id`** is always unique and cannot be switched off. A metaobject field of type `id` is unique by its type.
- Switching on is refused while values already repeat. The refusal lists up to 20 of the repeated values.

## Contrasts

- **Admin filter vs storefront product filters**: the admin filter does **not** add a filter to storefront product listings. Listing filters on the Storefront API (`productFilters`) work by category properties, variant options, vendor, price and tags ([[products-property]]). To let shoppers filter by a characteristic, keep it a property. To give shoppers a fixed set of products by a metafield, use a smart collection.
- **Unique values vs `id` type**: use `id` for identifiers (an ERP code, a supplier SKU) where uniqueness is the point. Use unique values on a single-line text, URL or integer when the value has another meaning but must still not repeat.

## Where it applies

- The capability switches on a metafield definition's page, and per field on a metaobject definition's page.
- **Products → Smart Collections → condition → Metafield** ([[products-smart-collections]]): lists the enabled product definitions, with their operations, and an entry picker for references.
- The Admin GraphQL `products(query:)` and `metaobjects(type:, query:)`, and the Storefront API's `metaobjects(type:, query:)`.

## Related

- [[metafields-metaobjects]]: hub.
- [[metafields-types]]: which types each capability accepts.
- [[metafields-limits]]: the 50 and 128 limits in context.
- [[products-smart-collections]]: the collection editor where the condition is used.

## Open Questions

- None known.
