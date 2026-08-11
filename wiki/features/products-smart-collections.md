---
type: feature
nav_path: "Products → Smart Collections"
route_name: selections
route_path: /admin/products/smart-collections
aliases: ["Smart Collections", "Collections", "Selections", "Smart selections", "Smart groups", "Колекции", "Селекции", "Динамични колекции"]
tags: [products, collections, selections, smart-grouping]
plan_gates: ["product_collections"]
created: 2026-05-21
updated: 2026-06-10
source_count: 7
---

# Smart Collections

## Purpose

The screen where the merchant defines **rule-based product groupings** — collections that auto-populate with products matching the merchant's criteria, rather than manually-curated product lists. A Smart Collection is a named container with one or more rules (e.g., *"all products from Brand X"*, *"all products in the Electronics category that are on sale"*, *"all products under 100 BGN"*) and the platform continuously evaluates which products match. Customers see the collection as a landing page on the storefront; the merchant uses it for marketing, discount targeting, and storefront curation.

Smart Collections are **dynamic** — adding a new product that matches the rules automatically adds it to the collection; removing the product or changing its data removes it. The merchant doesn't maintain the list — they maintain the rules.

The feature is **plan-gated** — the merchant's plan caps how many Smart Collections they can create.

## Where to find it

Sidebar → Products → **Smart Collections**.

The page's breadcrumb reads "Products → Smart Collections". The route is `/admin/products/smart-collections`. The header icon is the layer-group icon.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages — each scoped to a single concern. The Assistant should drill into the aspect that matches the question rather than read every page.

- [[smart-collections-list-view]] — the paginated table, columns (ID, Name, Status, Discounts, Products, Criteria), sorting, filters (Status, Has products, Product), bulk-delete, and the per-plan usage chip on the Add button.
- [[smart-collections-editor]] — the right-side `xl` Add / Edit modal: General settings card (name + rule builder), Advanced settings card (SEO title, description, URL handle, canonical), header Close + Save buttons, no-footer mode, field-length caps.
- [[smart-collections-rule-builder]] — the criteria row UI: Type / Operator / Records-selector / Value-input column layout, per-type endpoints, +Add criteria button, the 10 visible vs 12 backend types gap, and what the merchant CANNOT do here.
- [[smart-collections-rule-types]] — the complete 12 rule-type catalogue (`product`, `category`, `discount`, `vendor`, `tag`, `category_property_option`, `selection`, `price`, `digital`, `sale`, `new`, `featured`) with per-type operators and the price 0–50,000 cap + strict-greater-than `between` rule.
- [[smart-collections-evaluation]] — async re-evaluation: the `executing` boolean driving the Pending / Finished badge, the three event sources that trigger regeneration, the cached `products` field, `last_generated_at`, and recovery from stuck Pending.
- [[smart-collections-storefront-side-effects]] — the `/selection/<slug>` storefront route (hardcoded prefix), AJAX endpoints (`ajax.selection`, `ajax.products.selection`, `ajax.filters-ts.selection`), time-series visit tracking, search re-index, storefront cache flush, and linked-discount re-evaluation on save.
- [[smart-collections-rules-and-limits]] — AND-combination semantics, the hard cap of 10 condition rows, the anti-circular safeguards (self-referential discount loop + collection-of-collections loop), the `product_collections` plan gate, and the permission section.

## What the merchant can do here

At a glance — the detail lives in the aspects above:

- **Browse and filter** all existing smart collections — see [[smart-collections-list-view]].
- **Create a new collection** by clicking + Add collection (subject to plan cap) and filling in the General + Advanced cards — see [[smart-collections-editor]].
- **Build the rule set** that defines which products belong to the collection — see [[smart-collections-rule-builder]] and [[smart-collections-rule-types]].
- **Wait for evaluation** — Status flips Pending → Finished when the background regeneration job completes — see [[smart-collections-evaluation]].
- **Use the collection on the storefront** — every collection auto-publishes at `/selection/<url-handle>` — see [[smart-collections-storefront-side-effects]].
- **Link discounts** to collections (managed from the Discounts feature, not here) — the Discounts column on the list page surfaces which collections drive which promotions.
- **Bulk-delete** unused collections from the list.

What the merchant CANNOT do here:

- Manually pick specific products into a collection — the manual cross-sell list lives on each product's editor under Linked Products in [[products-products]].
- Edit which discounts are linked to a collection — that's managed in the Discounts feature.
- Reorder products within a collection from this screen — that happens via product-field sort on the storefront layer.

## Settings & fields

The hub does not own field-level detail. The two aspects that catalogue every field and column are:

- [[smart-collections-list-view]] — list columns and filter chips.
- [[smart-collections-editor]] — every field on the Add / Edit modal (name, description, URL handle, SEO title, SEO description, canonical, plus the 11-field selection record shape).

The single plan-feature key for this feature is:

| Mapping | Shape | What it controls |
|---|---|---|
| `product_collections` | Numeric (max smart collections) | Per-plan cap on the total number of smart-collection records the merchant can own. Add collection button checks the cap before opening the create modal; when reached, opens the plan-upgrade prompt instead with the literal message *"You have reached the maximum number of collections allowed, you need to purchase more to continue."* Per-plan add-on packs available via [[plan-features]]. See [[smart-collections-rules-and-limits]] for the full plan-gate behaviour. |

## Business rules

At hub level, the four cross-aspect rules that every support agent should remember are:

1. **Rules are AND-combined within a collection.** All rules must match for a product to belong. Express OR by creating multiple collections — see [[smart-collections-rules-and-limits]].
2. **Re-evaluation is async.** The Status column tells the merchant whether a collection is still computing (Pending) or settled (Finished). Don't link a discount to a Pending collection — see [[smart-collections-evaluation]].
3. **The storefront URL is hardcoded at `/selection/<slug>`.** The slug comes from the URL handle field; the `/selection/` prefix is not merchant-configurable — see [[smart-collections-storefront-side-effects]].
4. **Anti-circular safeguards exist.** A collection rule cannot create a discount loop or a collection-of-collections loop — save fails with a verbatim error string — see [[smart-collections-rules-and-limits]].

Per-product membership is visible from [[products-products]]: the Smart Collections aside section on the product Edit page shows which collections the product currently belongs to. The merchant cannot manually add the product from there — they would need to modify the collection's rules to include the product.

## Plan gates

This feature is gated by `product_collections` (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]). See [[smart-collections-rules-and-limits]] for the cap-reached UX and the per-pack add-on flow.

## Related

- [[products]] — parent hub.
- [[products-products]] — products carry collection memberships; the Smart Collections aside section shows which collections each product belongs to.
- [[products-categories]] — categories are one of the criteria types.
- [[products-vendors]] — vendors are one of the criteria types.
- [[products-property]] — category properties + options are one of the criteria types.
- [[plan]] — the `product_collections` plan feature caps how many collections the merchant can create.
- [[plan-gates]] — concept page on plan-based feature gating.
- [[product]] — entity page.
- [[smart-collection]] — entity page.
- [[selection]] — storefront page rendered at `/selection/<slug>`.
- [[json-api-v2]] — JSON-API v2 surface for creating collections programmatically.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
