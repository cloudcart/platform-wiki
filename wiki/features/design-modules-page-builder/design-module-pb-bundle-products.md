---
type: feature
nav_path: "Marketing → Dynamic Pages → Page-builder modules → Bundle products"
route_name: admin.pages.builder
route_path: /admin/marketing/pages/builder/{page_id?}
aliases: ["Bundle products module", "Bundle showcase block", "Модул пакети"]
tags: [design, modules, page-builder, bundles, marketing]
plan_gates: [storefront_builder]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

# Bundle products block (`bundle-products`)

> Part of [[design-modules-page-builder]]. See the category page for the other page-builder modules.

## Purpose

The **Bundle products** block renders a row of bundle (package) products on a Dynamic page. Bundles are pre-defined product packages with their own pricing (typically discounted vs. the sum of components) — see [[inventory-bundle-stock]] for the bundle inventory model. The block lets the merchant surface bundles on a landing page, a campaign page, or a homepage hero so customers see the bundled offer alongside other content.

## Where to find it

Open a Dynamic page in [[marketing-landing-pages]] → click **+ Add block** → pick **Bundle products** from the block picker.

## What the merchant can do here

- Pick a filter (specific bundles to surface) — autocomplete search.
- Set how many bundles to show (count).
- Set how many bundles per row (`per_row`, 1-5; default 4).
- Pick a colour highlight + an icon (theme-shipped; available when the theme supports them).
- Toggle the master enable switch.

## What the merchant cannot do here

- The merchant cannot add a new bundle from this block — bundles are configured in [[products-products]] (bundle products are a product `type`).
- The merchant cannot configure bundle pricing or composition from this block.
- The merchant cannot add a "build your own bundle" picker — the block lists pre-defined bundles only.

## Settings & fields

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | toggle | `true` | Master on/off. |
| `filter_value` | bundle picker | `null` | JSON array of bundle product IDs to surface (or empty for "any bundle"). |
| `per_row` | select (1-5) | 4 | Bundles per row on the row. |
| `products` | number | 3 | How many bundles to show total. Defaults to 3 bundles. |
| `color` | text input (hex / colour name) | `''` | Theme-shipped colour highlight. Only renders when theme advertises `functions.product_showcase.color.status`. |
| `icon` | select | `''` | Theme-shipped icon. Only renders when theme advertises `functions.product_showcase.icon.status`. |

### Save / Reset / Cancel

Page-builder side panel — see [[marketing-landing-pages]].

## Business rules

### Bundle count + per-row drive the layout

The block fetches `products` bundles total and lays them out `per_row` per row. So `products=6` + `per_row=3` renders two rows of three. The actual cards are the theme's standard product-card partial, repurposed for the bundle product type.

### Filter picker drives the source

When the merchant picks specific bundles via `filter_value`, only those bundles surface. When blank, the block falls back to the most recent / featured bundles (verify the exact fallback ordering).

### Theme dependencies for colour / icon

Some themes ship per-block colour / icon options (highlighted ribbon, icon overlay). The block only renders those rows when the theme's `theme_config` declares `functions.product_showcase.color.status == true` / `functions.product_showcase.icon.status == true`. On themes without those features, the colour / icon fields are hidden.

### Helper card when there are no bundles

If the merchant hasn't created any bundles yet (or has the helper-data feature enabled and `static::$_existing_products_count == 0`), the block renders a helper card pointing to the bundle create flow.

## Related

- [[design-modules-page-builder]] — hub.
- [[design-module-pb-product]] — sibling: single-product block.
- [[design-module-pb-add-to-cart]] — sibling: add-to-cart button.
- [[inventory-bundle-stock]] — bundle inventory model (how the price + stock is derived).
- [[products-products]] — product catalogue (bundles are a product type).
- [[marketing-landing-pages]] — Dynamic pages — the surface this module appears in.

## Open questions

- 📡 **Fallback ordering.** With `filter_value` blank, what is the default bundle source (recent, featured, all-active)? (verify against listing driver)
- 📡 **Out-of-stock bundles.** When a bundle has at least one out-of-stock component, does the block hide the bundle or mark it OUT? (verify)
