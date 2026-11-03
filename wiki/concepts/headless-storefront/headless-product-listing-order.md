---
type: concept
nav_path: "Concept → Headless storefronts → Product listing order"
aliases: ["Storefront API default sort", "Nitrogen listing order", "products sortKey", "ProductSortKeys", "Default product order Nitrogen", "Best sellers first", "collections kind", "CollectionKind", "SMART_COLLECTION", "List smart collections Storefront API", "Подредба на продукти Nitrogen", "Подредба по подразбиране", "Умни колекции в Nitrogen"]
tags: [nitrogen, headless, storefront-api, listing, sorting, smart-collections, concepts]
plan_gates: []
created: 2026-11-03
updated: 2026-11-03
source_count: 3
---

> Part of [[headless-storefront]]. See the hub for the other aspects (Nitrogen overview, deployment methods, Nova platform, Storefront API, customer accounts, environment variables, legacy-vs-Nitrogen surfaces).

# Headless — product listing order and smart collections

## Definition

A Nitrogen storefront asks the Storefront API (`/api/sf`) for products with or without a `sortKey`. This page gives the order it gets when it sends none, what each `sortKey` does, and how a storefront lists smart collections next to categories.

## Scope

### Asked without a `sortKey`

| Asked for | Order |
|---|---|
| `products` with `query` | By relevance |
| `products` without `query` | The store's order |
| A smart collection's `products` | Its own default sort, else the store's order |
| A category's, a brand's or a tag's `products` | The store's order |

**The store's order** is the store's `list.product` listing setting ([[design-module-product-listing]]), and **best sellers first** when the store set none.

The Storefront API schema's description of the `products` field reads "`ID`, oldest product first". The order applied is the one above, as the description of its `sortKey` argument says.

When the merchant lists products that cannot be bought last, they come after the others in every order.

### Asked with a `sortKey`

| `sortKey` | Order | With `reverse: true` |
|---|---|---|
| `TITLE` | A to Z | Z to A |
| `PRICE` | Lowest first | Dearest first |
| `BEST_SELLING` | Best sellers first | Least sold first |
| `CREATED_AT`, `ID` | Oldest first | Newest first |
| `UPDATED_AT` | Sorts as `CREATED_AT` | Newest first |
| `RELEVANCE` | In a search by relevance; in a listing, the merchant's own arrangement | No effect |
| `PRODUCT_TYPE`, `VENDOR` | Keep the default order above | No effect |

`reverse` has no effect without a key.

### Listing smart collections

`collections` lists one kind at a time, through `kind` (`CollectionKind`):

| `kind` | Lists |
|---|---|
| Omitted, or `CATEGORY` | The categories |
| `SMART_COLLECTION` | The smart collections |

For both, ask twice under two aliases. For smart collections:

- `topLevel` makes no difference, as a smart collection has no parent.
- `withProducts` keeps those with products of their own.
- `sortKey: MANUAL` orders by id, since the merchant arranges only categories.

### Finding one collection

`collection(handle:)` without `kind` looks for a category first, then a smart collection. A category and a smart collection may share a handle, so a smart collection in that position is reached with `kind: SMART_COLLECTION`. With a `kind`, the other kind answers null.

## Contrasts

- **Nitrogen vs a classic theme**: when the store set no listing order, a Nitrogen storefront lists best sellers first, and the platform's own storefront lists newest first.
- **`RELEVANCE` in a listing vs in a search**: the same key means the merchant's arrangement in a listing and the search's ranking in a search.
- **Category vs smart collection pages**: a smart collection can carry its own default sort; a category follows the store's order.

## Where it applies

- A Nitrogen storefront's category, smart collection, brand and tag pages, and any list it asks for with `products`.
- Any headless client of the Storefront API ([[headless-storefront-api]]).

## Related

- [[headless-storefront]] — hub.
- [[headless-storefront-api]] — endpoint, tokens and scopes.
- [[products-smart-collections]] — smart collections in the admin.
- [[smart-collections-admin-api]] — the same collections through the Admin GraphQL API.
- [[design-module-product-listing]] — the store's listing setting.

## Open Questions

- None known.
