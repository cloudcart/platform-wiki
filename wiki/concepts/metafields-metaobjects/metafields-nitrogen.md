---
type: concept
nav_path: "Concept → Metafields and metaobjects → On a Nitrogen storefront"
aliases: ["Metafields on Nitrogen", "Metafields Storefront API", "metafield(namespace key)", "metafields(identifiers)", "metaobject(handle)", "metaobjects(type)", "HasMetafieldsIdentifier", "MetaobjectHandleInput", "Metafields on classic theme", "Метаполета в Nitrogen", "Метаполета в темата"]
tags: [metafields, metaobjects, custom-data, nitrogen, headless, storefront-api, concepts]
plan_gates: []
created: 2026-10-20
updated: 2026-10-20
source_count: 4
---

# Metafields and metaobjects on a Nitrogen storefront

> Part of [[metafields-metaobjects]]. See the hub for definitions, types, limits and permissions.

## Definition

At the time of writing, metafields and metaobjects are **mainly for headless stores built with Nitrogen**. The store's own themes do not display them. A Nitrogen storefront reads them through the **Storefront API** (`/api/sf`, [[headless-storefront-api]]) and decides itself where and how each value appears.

## Scope

### Reading metafields

`Product`, `Collection` (a category) and `Customer` have:

- `metafield(namespace:, key:)`: one value, or null.
- `metafields(identifiers: [{namespace, key}, …])`: up to **250** at once, answered in the same order, null where there is none.

```graphql
product(handle: "linen-shirt") {
  care: metafield(namespace: "custom", key: "care_instructions") { value }
  chart: metafield(namespace: "custom", key: "size_chart") {
    reference { ... on Metaobject { handle field(key: "table") { value } } }
  }
}
```

- **The namespace is required.** Without it nothing is found, since there is no app-reserved default. Definitions made in the admin are in `custom`.
- A **`Metafield`** returns:
  - `namespace`, `key`, `type`, `value`, `list` and `description`;
  - `createdAt` and `updatedAt`;
  - `parentResource`, plus `reference` (single references) or `references` (lists, paginated, in the stored order).
- **`value` is always a string.** Lists and object types (rating, money, measurement, link, rich text, JSON) arrive as JSON text for the storefront to parse.
- A **customer's** metafields come only to that customer, signed in, and only for `READ` definitions ([[metafields-permissions]], [[headless-customer-accounts]]).

### Reading metaobjects

- `metaobject(handle: {type: "designer", handle: "ana-petrova"})`, or `metaobject(id:)`: one entry, or null.
- `metaobjects(type: "faq", first: 20, after:, sortKey: "id" | "updated_at", reverse:, query:)`: a type's entries, page by page.
- `query` filters by fields that have the admin filter on: `fields.topic:delivery`, `fields.starts_at:>=2026-11-01`, `-fields.archived:true` ([[metafields-capabilities]]).
- An entry gives `id`, `handle`, `type`, `updatedAt`, `field(key:)` and `fields`. Only filled fields appear. Each field gives `key`, `type`, `value`, `reference` and `references`.
- Only entries of `PUBLIC_READ` definitions are returned, and only **Active** ones when the definition has the active/draft status.

### What references resolve to

`Product`, `ProductVariant`, `Collection`, `Page`, `Metaobject`, and files as `MediaImage`, `Video` (the uploaded file itself, as its only source) or `GenericFile` (URL, MIME type, size). A referenced record the storefront does not show is left out. A customer reference never resolves. Entries referencing entries can be followed level by level in one query.

## Contrasts

- **Owners**: products, categories and customers, plus metaobject entries. Variants and pages are reached through references.
- **Languages**: a store serves one language, and each field holds one value. A multi-language business runs sister sites ([[apps-multilang]]), each defining and filling its own metafields; the Multilang sync does not copy them. One Nitrogen storefront serving two languages from one store keeps one field per language (`title_bg`, `title_en`). See [[metafields-use-case-multilanguage]].
- **Entry pages**: the Nitrogen storefront builds routes from `type` + `handle` and sets each entry page's SEO itself.
- **Listing filters**: product-listing filters on the Storefront API work by category properties ([[products-property]]). A metafield shapes a listing through a smart collection.
- **Entry order**: entries sort by `id` or `updated_at`. The storefront filters with `query`, then orders by any field itself.
- **Customer values** are read-only from the storefront: `READ_WRITE` reads as `READ`.
- **Namespaces**: any valid namespace except those beginning `app--`, which are reserved. Every definition is the store's own.

**Classic themes**: no CloudCart theme reads metafields or metaobjects yet. On a classic-theme store they can already be filled in, searched through the Admin GraphQL API, and drive smart collections. The storefront shows only what those collections produce.

## Where it applies

- The Nitrogen storefront's own code: product, category and account pages, plus any content route built from metaobject types ([[metafields-use-cases]]).
- Storefront tokens of every Nitrogen storefront of the store ([[nitrogen-storefront-overview]]): all of them see the same `PUBLIC_READ` data.

## Related

- [[metafields-metaobjects]]: hub.
- [[headless-storefront]]: Nitrogen and headless storefronts.
- [[headless-storefront-api]]: endpoint, tokens and scopes.
- [[headless-legacy-vs-nitrogen]]: other things that differ between classic themes and Nitrogen.
- [[metafields-use-cases]]: what to build with these queries.

## Open Questions

- None known.
