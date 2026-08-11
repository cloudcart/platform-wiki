---
type: feature
nav_path: "Products → Smart Collections → Rule types"
route_name: selections
route_path: /admin/products/smart-collections
aliases: ["Smart Collections rule types", "Smart Collections value types", "Smart Collections operators", "Selection rule catalogue", "Selection conditions catalogue"]
tags: [products, collections, selections, rule-types, operators, validation]
plan_gates: ["product_collections"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[products-smart-collections]]. See the hub for the other aspects (list view, editor, rule builder, evaluation, storefront side-effects, rules and limits).

# Smart Collections — rule type catalogue

## Purpose

The complete catalogue of every `value_type` enum the backend accepts on a smart-collection rule row, with the operators valid per type, the validation rules applied server-side, and the gaps between the UI dropdown and the backend acceptance set. This is the canonical reference for support agents diagnosing *"why does my rule reject this value"* or *"why does this product not match the rule it should"* tickets.

The row-layout UI for picking a type lives on [[smart-collections-rule-builder]] — this page is the field reference.

## Where to find it

The rules live inside the Add / Edit modal's General settings card — see [[smart-collections-editor]] and [[smart-collections-rule-builder]].

## What the merchant can do here

The merchant picks one of the 10 visible types per row from the Type dropdown, then picks one of the operators valid for that type, then provides the value(s). The available types and their operators are catalogued below — and the row builder validates the combination on Save.

## Settings & fields

### Complete 12-type catalogue (10 visible + 2 backend-only)

| Type | Visible in UI? | Operators | Value shape | Notes |
|---|---|---|---|---|
| **`product`** | Yes (Products) | `In` / `Not in` | Multi-record (tag select) | Records from `/admin/api/core/items/search`. |
| **`category`** | Yes (Categories) | `In` / `Not in` | Multi-record | Records from `/admin/api/core/product-categories/search`. **Matches the named category AND all descendants** (materialised path). See [[products-categories]]. |
| **`discount`** | Yes (Discounts) | `In` / `Not in` | Multi-record | Records from `/admin/api/core/discounts/search`, server-filtered to `type IN (fixed, percent, flat)`, `only_customer=no`, `shipping=no`. Subject to anti-circular safeguard — see [[smart-collections-rules-and-limits]]. |
| **`vendor`** | Yes (Manufacturer) | `In` / `Not in` | Multi-record | Records from `/admin/api/core/vendors/search`. See [[products-vendors]]. |
| **`tag`** | Yes (Tags) | `In` / `Not in` | Multi-record | Records from `/admin/api/core/product-tags/search`. |
| **`category_property_option`** | Yes (Category property) | `In` / `Not in` | Multi-record | Records from `/admin/api/core/properties/value-autocomplete`. Matches by specific property value (e.g., Color = Red). See [[products-property]]. |
| **`selection`** | **No** (backend only) | `In` / `Not in` | Multi-record (other collections) | "Collection-of-collections" — references other smart collections by ID. Subject to anti-circular safeguard — see [[smart-collections-rules-and-limits]]. UI-hidden as a known gap. |
| **`price`** | Yes (Price) | `equal`, `not_equal`, `gt`, `gte`, `lt`, `lte`, `between`, `not_between` | Numeric currency input(s) | Integer **0 ≤ price ≤ 50,000** validated server-side. `between` / `not_between` use two inputs; the second must be **strictly greater than** the first. |
| **`digital`** | Yes (Digital product) | `is` / `is_not` | Yes / No dropdown | Product-flag boolean. |
| **`sale`** | Yes (Sale) | `is` / `is_not` | Yes / No dropdown | Product-flag boolean. |
| **`new`** | Yes (New) | `is` / `is_not` | Yes / No dropdown | Product-flag boolean. |
| **`featured`** | **No** (backend only) | `is` / `is_not` | Yes / No dropdown | "Is featured" product flag. UI-hidden as a known gap. |

### UI operator labels vs backend operator codes

The UI surfaces friendly labels for the price operators. The backend stores discrete codes:

| UI label | Backend code |
|---|---|
| Equal | `equal` |
| Not equal | `not_equal` |
| More than | `gt` |
| More than or equal | `gte` |
| Less than | `lt` |
| Less than or equal | `lte` |
| Between | `between` |
| Not between | `not_between` |

The earlier wiki text labelled price operators as "More than / Less than / Between" only — the backend in fact supports the strict (`gt`/`lt`) and inclusive (`gte`/`lte`) variants distinctly.

## Business rules

### Price has a hard cap of 50,000

Smart-collection price rules are validated server-side as integer **0 ≤ price ≤ 50,000**. Higher-priced products cannot be targeted directly by a Price rule — the merchant must use Category, Vendor, Tag, or another non-price type instead.

### `between` requires the second value to be strictly greater than the first

For Price rules with the `between` (or `not_between`) operator, the platform enforces `sub_value > value` — the upper bound must be strictly greater than the lower bound. Saving "between 200 and 100" fails with the verbatim error *"Field must be greater than 200"*. Equal values (e.g., between 100 and 100) are rejected for the same reason.

### Multi-record types accept multiple values per row, AND-combined across rows

Within one row, a multi-record selector (e.g., `category` with operator `In` and three categories picked) treats the three categories as OR among themselves — a product matches the row if it belongs to any of the three. Across rows, the AND combination from [[smart-collections-rules-and-limits]] still applies — every row must match for the product to be in the collection. To express "Category A OR Category B" as a top-level collection logic, the merchant creates two separate collections.

### `category` matches descendants via materialised path

A `category` rule on a parent category includes products in all descendant categories (materialised path lookup on the category tree). The merchant doesn't need to enumerate every leaf — naming the parent covers the whole subtree. See [[products-categories]] for the tree model.

### `discount` and `selection` types are subject to circular-reference guards

Because both `discount` (target products inside a specific discount) and `selection` (target products in another smart collection) reference other records that themselves reference collections, the platform validates against circular references on Save. The verbatim error strings and the `Not in` carve-out are catalogued on [[smart-collections-rules-and-limits]].

### UI-hidden types (`selection`, `featured`) are accepted from JSON-API v2

Even though the rule builder UI never lists `selection` or `featured`, both types are valid on the create / save POST and on JSON-API v2 writes. Collections imported via [[json-api-v2]] or created from legacy migrations may carry these types; opening such a collection in the rule builder renders the row with a blank Type dropdown (known UI gap). The merchant cannot reproduce the row by re-saving — the only path to add these rules is the API.

### Operator-type compatibility is validated on Save

The server rejects mismatches like "operator `gt` on type `vendor`" or "operator `In` on type `price`" with a generic validation error. The UI prevents most of these by populating the Operator dropdown based on the Type — but API-direct writes are validated independently.

## Related

- [[products-smart-collections]] — hub.
- [[smart-collections-rule-builder]] — UI for picking these types.
- [[smart-collections-rules-and-limits]] — anti-circular safeguards on `discount` / `selection` types, the AND-combination rule, and the 10-row cap.
- [[products-categories]] — descendant matching on `category` type.
- [[products-vendors]] — `vendor` type.
- [[products-property]] — `category_property_option` type.
- [[products-products]] — `product` type.
- [[json-api-v2]] — programmatic creation surface where `selection` and `featured` types are reachable.

## Open questions

None.
