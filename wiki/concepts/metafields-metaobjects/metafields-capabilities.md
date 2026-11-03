---
type: concept
nav_path: "Settings → Metaobjects → a definition → Capabilities"
aliases: ["Metafield capabilities", "Filtering", "Filtering switch", "Smart collections switch", "Options card", "Preparing values…", "Checking values…", "Not switched on", "METAFIELD_DEFINITION_IN_USE", "CAPABILITY_CANNOT_BE_DISABLED", "Admin filter metafield", "adminFilterable", "Filterable metafield", "Smart collection condition metafield", "smartCollectionCondition", "Unique values", "uniqueValues", "metafields.custom.key:value", "fields.key:value", "Филтър по метаполе", "Умна колекция по метаполе", "Уникални стойности"]
tags: [metafields, metaobjects, custom-data, filtering, smart-collections, concepts]
plan_gates: []
created: 2026-10-20
updated: 2026-11-03
source_count: 6
---

# Metafield capabilities: admin filter, smart-collection condition, unique values

> Part of [[metafields-metaobjects]]. See the hub for definitions, types, limits and permissions.

## Definition

A **capability** is a switch on a definition that makes its values do more than be stored and read. There are three, in the definition page's **Options** card. Each switch appears only where its capability is offered.

| On screen | On the API | Offered on | What it does |
|---|---|---|---|
| **Filtering**: *"Lets the Admin API filter products by this value."*; on a metaobject field, *"Lets the APIs filter the entries by this field."* | Admin filter, `adminFilterable` | Product metafield definitions; metaobject fields | Values can be searched and filtered by. |
| **Smart collections**: *"Lets a smart collection take the products by this value."* | Smart-collection condition, `smartCollectionCondition` | Product metafield definitions of six types | A smart collection can include products by the value. |
| **Unique values**: *"No two products can have the same value."* (customers and categories likewise) | `uniqueValues` | Single-line text, URL and integer definitions of any owner type; always on for `id` | No two owners hold the same value. |

## Scope

### Switching on runs in the background

Turning on **Filtering** or **Smart collections** prepares the values that already exist. Meanwhile the switch carries the badge **Preparing values…**. Only when that has finished does it filter or appear among collection conditions.

It is enabled at once when nothing needs preparing:

- a definition with no values;
- **Smart collections** on a metaobject reference, or while Filtering is enabled;
- **Filtering** while Smart collections is enabled.

On the Admin GraphQL API the filter's status is `NOT_FILTERABLE`, `IN_PROGRESS`, `FILTERABLE` or `FAILED`. `FAILED` carries no badge on the page, and saving the definition with the switch on prepares the values again.

### Switching off

- **Filtering** and **Unique values** switch off at once.
- An `id` definition's unique values stay on: `CAPABILITY_CANNOT_BE_DISABLED`.
- **Smart collections** switches off at once while no smart collection's condition names the definition. While one does, the switch-off is refused with the same refusal as deleting the definition, `METAFIELD_DEFINITION_IN_USE`: *"Action cannot proceed. Definition is currently in use by the smart collections {collections}."* It names the collections and shows under the switch. A condition is edited in the collection's editor ([[smart-collections-rule-builder]]).

### Admin filter

- **Types**: every type except `json` and `rich_text_field`, lists included (a list matches when any item matches).
- **Product definitions**: products can be searched by `metafields.{namespace}.{key}:{value}`, e.g. `metafields.custom.material:cotton`, on the Admin GraphQL API's product list.
- **Metaobject fields**: entries can be filtered by `fields.{key}:{value}`, on the Admin GraphQL API and on the Storefront API's `metaobjects(type:, query:)` list. This is a Nitrogen storefront's main way to pick entries by content ([[metafields-nitrogen]]).
- **Matching**: the query language, how each type matches and the warnings are in [[metafields-search-syntax]].
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
- A definition that a smart collection uses **cannot be deleted or have this switch turned off** while the collection uses it. A metaobject definition whose deletion would delete such a metafield definition cannot be deleted either.
- When a product's value changes, the collections that depend on it are recalculated, as for any other condition ([[products-smart-collections]]).
- The editor's row is in [[smart-collections-rule-builder]]. The same conditions through the API are in [[smart-collections-admin-api]].

This is how a metafield shapes what a storefront lists: the smart collection is a normal collection on the Storefront API ([[headless-product-listing-order]]) and on classic themes. Example: `custom.eco_certified = true` gives an "Eco" collection that maintains itself.

### Unique values

- No two products (customers, categories) hold the same value of the definition. A save that would repeat a value is refused with `TAKEN`: *"The input value is already taken."*
- **`id`** is always unique and cannot be switched off. On a metaobject, a field of type `id` is unique by its type.
- Switching on is refused while values already repeat: *"Unique values need every value to differ; these repeat: {values}."* It lists up to 20 of them, each cut to 100 characters.
- While existing values are checked the switch carries the badge **Checking values…**, and a value another owner holds is refused meanwhile.
- If a value repeats during that check, the switch shows off with the badge **Not switched on**: *"A value repeated while the values were checked. Switch unique values on again to see which values repeat."*

## Contrasts

- **Admin filter vs storefront product filters**: the admin filter does **not** add a filter to storefront product listings. Listing filters on the Storefront API (`productFilters`) work by category properties, variant options, vendor, price and tags ([[products-property]]). To let shoppers filter by a characteristic, keep it a property. To give shoppers a fixed set of products by a metafield, use a smart collection.
- **Unique values vs `id` type**: use `id` for identifiers (an ERP code, a supplier SKU) where uniqueness is the point. Use unique values on a single-line text, URL or integer when the value has another meaning but must still not repeat.

## Where it applies

- The **Options** card on a metafield definition's page, and **Filtering** per field on a metaobject definition's page.
- **Products → Smart Collections → condition → Metafield** ([[products-smart-collections]]): lists the enabled product definitions, with their operations, and an entry picker for references.
- The Admin GraphQL `products(query:)` and `metaobjects(type:, query:)`, and the Storefront API's `metaobjects(type:, query:)`.

## Related

- [[metafields-metaobjects]]: hub.
- [[metafields-types]]: which types each capability accepts.
- [[metafields-limits]]: the 50 and 128 limits in context.
- [[metafields-search-syntax]]: the query language the filter answers.
- [[products-smart-collections]]: the collection editor where the condition is used.

## Open Questions

- None known.
