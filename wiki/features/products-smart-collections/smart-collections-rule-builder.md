---
type: feature
nav_path: "Products → Smart Collections → Rule builder"
route_name: selections
route_path: /admin/products/smart-collections
aliases: ["Smart Collections rule builder", "Smart Collections criteria builder", "Smart Collections condition rows", "Selection criteria UI", "Collection criteria editor", "Metafield row", "Metafield condition"]
tags: [products, collections, selections, rule-builder, criteria, ui]
plan_gates: ["product_collections"]
created: 2026-06-10
updated: 2026-11-03
source_count: 2
---

> Part of [[products-smart-collections]]. See the hub for the other aspects (list view, editor, rule types, evaluation, storefront side-effects, rules and limits).

# Smart Collections — rule builder UI

## Purpose

The multi-row condition editor that lives inside the General card of the [[smart-collections-editor]]. Each row picks one field (Type), one operator, and one or more value records — and multiple rows combine with AND to define which products belong to the collection. This page documents the row layout, the per-type Records-selector endpoints, and the +Add criteria button. The full catalogue of rule types and per-type operators is on [[smart-collections-rule-types]].

## Where to find it

Sidebar → Products → **Smart Collections** → open any collection (or +Add collection) → inside the General settings card, below the Collection name input and a `<hr/>` divider.

The rule builder is introduced by a single header label *"Collection dropdowns label"*.

## What the merchant can do here

### Per-row layout

Each rule row is a horizontal flex group with this structure:

1. **Type dropdown** (1/4 width) — picks the field to match. The visible UI dropdown shows **10 options**, plus **Metafield** when a metafield can be used (see below). The backend also accepts `selection` and `featured`, which have no UI entry — see [[smart-collections-rule-types]].
2. **Operator dropdown** (1/4 width) — populated based on the chosen Type. Switches between `In / Not in` for multi-record types, the 7 numeric operators for `price`, and `Is / Is not` for booleans. Catalogue on [[smart-collections-rule-types]].
3. **Records selector** (~11/12 width on its own line) — only for `product / category / discount / vendor / tag / category_property_option` types. A tag-mode search-as-you-type select that hits a type-specific endpoint (table below).
4. **Value input(s)** — only for `price`, `new`, `digital`, `sale`:
   - `price` + simple operator → single currency input (~5/12 width).
   - `price` + `between` / `not_between` → two currency inputs (~2/12 width each) separated by the word *"to"*.
   - `new` / `digital` / `sale` → single dropdown with `Yes / No`.
5. **Remove-row icon** (×) — appears only when there is more than one row. Removes the row inline.
6. A horizontal divider between rows (when not the last row).

### + Add criteria button

At the bottom of the rule list, an **+ Add criteria** secondary button appends a fresh empty row. The default Type when adding a new row is `product` (verify) and the merchant changes it via the Type dropdown.

### What the merchant CANNOT do here

- **Reorder rows from the UI.** Order is the insertion order. The backend stores `sort_order` per row, but the UI does not expose drag-reorder. (Order has no effect on matching semantics — rows are AND-combined regardless of order; see [[smart-collections-rules-and-limits]].)
- **Group rows into nested OR clusters.** All rows AND together. Express OR by creating multiple collections.
- **Add more than 10 rows.** The platform enforces a hard cap of 10 rule rows per collection — see [[smart-collections-rules-and-limits]].

## Settings & fields

### Type dropdown options

| Type dropdown label | Internal value | Records source |
|---|---|---|
| **Products** | `product` | `/admin/api/core/items/search` |
| **Categories** | `category` | `/admin/api/core/product-categories/search` |
| **Discounts** | `discount` | `/admin/api/core/discounts/search` (filtered to `type IN (fixed, percent, flat)`, `only_customer=no`, `shipping=no`) |
| **Manufacturer** | `vendor` | `/admin/api/core/vendors/search` |
| **Tags** | `tag` | `/admin/api/core/product-tags/search` |
| **Price** | `price` | Currency input (no records lookup) |
| **Digital product** | `digital` | Yes / No dropdown |
| **Sale** | `sale` | Yes / No dropdown |
| **New** | `new` | Yes / No dropdown |
| **Category property** | `category_property_option` | `/admin/api/core/properties/value-autocomplete` |
| **Metafield** | `metafield` | The row below |

`selection` and `featured` are accepted by a save but not listed in the dropdown, so a row of either type shows a blank Type dropdown ([[smart-collections-rule-types]]).

### The metafield row

The Type dropdown offers **Metafield** when at least one product definition has its **Smart collections** switch on and its values prepared ([[metafields-capabilities]]), or when the row already is one. It has three cells:

- **Definition**, by name, searchable above 8. Choosing another resets the operator to its first and clears the value.
- **Operator**: *Equal*, *Greater than*, *Lower than*, as the type allows.
- **Value**, checked against the type, not the definition's validations:
  - True or false: a *Yes* / *No* select.
  - Integer, decimal, rating: typed as text. A rating shows its scale beside the input, which is shown, not enforced.
  - Single-line text: typed, matched exactly and case-sensitively.
  - Metaobject reference: a searchable select of the definition's entries, 25 a page, any status including drafts.

On a saved row, a definition no longer offered shows by name with its saved operator and the banner *"The metafield is not available for smart collections."* A deleted definition or entry shows *Deleted* until another is chosen.

Refusals: *"Field is required"*, *"The metafield is not available for smart collections."*, *"The value is not valid for the metafield's type."*, *"The entry does not exist."*, *"The value can be at most 191 characters long."*

Using the row needs Products or Products → Smart Collections. The same rows through the API are in [[smart-collections-admin-api]].

## Business rules

### Records selectors hit per-type search endpoints

The selector renders the matched records as removable chips. The merchant can pick multiple values per row — the operator (`In` / `Not in`) then governs whether the rule matches "any of" or "none of" those values. The Discounts list holds discounts that target products.

### Boolean rules use a Yes/No dropdown instead of records

`digital`, `sale`, and `new` (and the UI-hidden `featured`) are product-flag booleans. The row collapses to Type / Operator (`Is` / `Is not`) / Value (`Yes` / `No`) — no Records-selector endpoint. See [[smart-collections-rule-types]].

### Price uses a numeric input, with a special between layout

`price` is the only numeric platform type. Most operators (`equal`, `gt`, `gte`, `lt`, `lte`) render a single currency input. The `between` and `not_between` operators render two currency inputs separated by the word *"to"* — and the platform validates that the second value is strictly greater than the first. The numeric value is capped at 0 ≤ price ≤ 50,000 server-side. See [[smart-collections-rule-types]] for the full per-operator catalogue.

### Adding a category includes its descendants

A `category` rule with operator `In` matches products in the named category AND all its descendants (via the materialised path lookup on the category tree). The merchant doesn't need to list every leaf category — naming the parent covers them all. See [[products-categories]] for the category tree model.

## Related

- [[products-smart-collections]] — hub.
- [[smart-collections-editor]] — the modal that hosts this builder.
- [[smart-collections-rule-types]] — the catalogue of types and operators that this UI surfaces.
- [[smart-collections-rules-and-limits]] — the 10-row cap and AND-combination semantics.
- [[products-categories]] — categories used as a rule type; descendant matching via materialised path.
- [[products-vendors]] — vendors used as a rule type.
- [[products-property]] — category properties + options used as a rule type.
- [[products-products]] — products used as a rule type.
- [[metafields-capabilities]] — the switch behind the metafield row.

## Open questions

- (verify) Default Type on a freshly-added row — `product` or empty?
