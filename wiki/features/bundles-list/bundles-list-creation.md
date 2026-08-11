---
type: feature
nav_path: "Products → Bundles → Add / Edit bundle"
route_name: bundles-add.new
route_path: /admin/products/bundles-new/add
aliases: ["Add bundle", "Edit bundle", "Bundle editor", "Bundle item rows", "Bundle creation"]
tags: [apps, administration, products, bundles]
plan_gates: ["bundles"]
created: 2026-06-10
updated: 2026-06-10
source_count: 5
---
# Bundles — creation, item rows & list actions

> Part of [[bundles-list]]. See the hub for the other aspects (pricing, stock, plan gates).

## Purpose

This aspect covers the **mechanics of building and managing a bundle**: the list table, the Add/Edit form, the rich per-item override fields on each constituent row, time-window scheduling, the bulk actions on the list, and the server-side validation that runs on save. Pricing rules live on [[bundles-list-pricing]]; stock derivation lives on [[bundles-list-stock]].

## Where to find it

- **List**: Sidebar → Products → **Bundles** (route `bundles-list.new`, path `/admin/products/bundles-new`).
- **Add**: **+ Add bundle** button (route `bundles-add.new`, path `/admin/products/bundles-new/add`).
- **Edit**: row → Edit (route `bundles-edit.new`, path `/admin/products/bundles-new/edit/:id`).

## What the merchant can do here

### Bundle-level fields

- **Bundle name** — what the customer sees on the storefront.
- **Bundle image** — the main visual.
- **Bundle description** — explanatory text.
- **Included products** — multi-select from the catalogue, with a quantity per product.
- **SEO settings** — title, description, URL handle.
- **Active period** — `publish_date` (start) + `active_to` (end), plus two timer switches (see below).

### Per-item overrides (the bundle item rows)

Each item in a bundle is more than "product + quantity". On each constituent row the merchant can set:

- **`qty`** — how many of this product the bundle contains. Per-item `qty` requires toggling **`individual_qty_enabled`** ON for that row, then entering a value (min 1). If the toggle is OFF, qty resets to 1 regardless of what was entered.
- **`optional`** — whether the customer can opt out of this constituent at checkout.
- **`individual_price`** + **`individual_price_enabled`** — override this item's price inside the bundle (different from its standalone price). The pricing knock-on of enabling this is on [[bundles-list-pricing]].
- **`discount`** — a per-item discount inside the bundle.
- **`override_title`** / **`title`** — override the displayed name for this item in the bundle context.
- **`override_short_description`** / **`short_description`** — override the displayed description.
- **`hide_thumb`** — hide this item's thumbnail in the bundle layout.
- **Three independent visibility toggles** — `visible_product_details` (show on the product page), `visible_cart` (show in the cart), `visible_order_details` (show on the order detail). A parallel set of `price_visible_*` toggles hide the per-item price separately from the item itself.

These overrides make bundles flexible. The merchant can build "buy one, get one hidden free gift" by hiding the gift item in the cart and order details.

## Settings & fields

### Time-window scheduling

The editor's "Active period" section accepts a publish date (`publish_date` / start) and an end date (`active_to`). Two extra switches control storefront timer visibility:

- **Show timer in products listing** — shows a countdown badge on the bundle's listing card. Only enabled when `active_to` is set.
- **Show timer in product details page** — shows a countdown on the bundle's product page. Only enabled when `active_to` is set.

After `active_to` passes, the bundle remains visible until it is manually deactivated (there is no auto-disable like banners — only the timer disappears). To auto-hide after expiry, the merchant must also set `active = 0` manually.

### Bulk actions on the list

The list table supports multi-select with: **Publish** (set `active = 1`), **Unpublish** (set `active = 0`), **Duplicate** (clone the bundle with all items but a new ID/URL), and **Delete**. Each multi-select action is confirmed.

## Business rules

### Server-side validation rules

The bundle save runs a small set of rules on top of the standard product-save validation (since a bundle is also a product, the heavy product-side rules also apply — see [[products-products]] § "Server-side validation"):

| Field | Rules | Wording on failure |
|---|---|---|
| `name` | **required**, max **191** chars | *"Product name is required"* / *"The maximum allowed characters for 'name' are 191"* |
| `description` | max **250,000** chars (LONGTEXT column) | *"The maximum allowed characters for 'description' are 250000"* |
| `bundle` | **required** array, min 1 entry (a bundle must contain at least one constituent — note the merchant-facing wording says *"at least two products"*, but the rule actually allows a single-item bundle through) | *"You have to choose products to be added into the bundle"* / *"Please choose at least two products to be added into the bundle"* |
| `bundle.*.product_id` | **required**, must exist in the catalogue — picking a product deleted between page load and save fails | Standard *"The selected product is invalid"* |

The constituent-product rule uses a standard existence check against the catalogue, so the picker's autocomplete is the merchant's defence against typo'd ids; an API caller passing an unknown product id gets a 422 even though no merchant-visible UI affords that input.

### Cart cleanup on bundle delete

When a bundle is deleted, all bundle-item rows for that bundle are removed from active carts. Customers who had the bundle in their cart see it disappear on the next page load — the constituent items do **not** auto-add separately. (This is also noted on [[bundles-list-stock]] where deletion intersects availability.)

## Related

- [[bundles-list]] — hub.
- [[bundle]] — the bundle entity model (per-item row fields).
- [[products-products]] — shared product validation + the constituent products.
- [[products-categories]] — categorising a bundle.

## Open questions

None.
