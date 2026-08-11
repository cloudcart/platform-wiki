---
type: feature
nav_path: "Design → Modules → Products → Bundle showcase"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/bundleShowcase
aliases: ["Bundle showcase module", "bundleShowcase module", "product.bundleShowcase", "Bundle row module", "Модул витрина с пакети", "Packages showcase"]
tags: [design, modules, products, bundles, showcase]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Product module — Bundle showcase (`product.bundleShowcase`)

> Part of [[design-modules-products]]. See the category page for the other product modules.

## Purpose

The **Bundle showcase** module (instance name `bundleShowcase`, type `product.bundleShowcase`) renders a row of merchant-curated BUNDLE packages. Unlike [[design-module-product-in-bundles]] (which surfaces the bundles that contain the current product), this module is hand-picked — the merchant chooses a specific list of bundles to surface on the homepage or any theme slot. Requires the **Bundles** app — without it the bundle picker returns no results.

This module is theme-specific — only themes that ship a `bundleShowcase` instance expose it (e.g., themes built for stores that lead with packages rather than individual products).

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab — card labelled per theme (often **"Bundle showcase"** or **"Packages row"**); appears only when the active theme declares a `bundleShowcase` instance.

Edit-panel URL: `/admin/storefront/widgets/bundleShowcase`.

Renders in the theme's bundle-row slot (typically the homepage).

## What the merchant can do here

- Master enable / disable toggle.
- Title the row.
- Pick the bundles to surface (autocomplete; drag to reorder).
- Pick how many bundles per row (1-4).
- Pick a section-header colour and icon (theme-dependent decoration).

## What the merchant cannot do here

- Cannot use this module without the Bundles app installed — see [[apps-bundles-overview-new]].
- Cannot surface non-bundle products — the picker only shows products with `product_type=bundle`.
- Cannot exceed 4 bundles per row.
- Cannot rely on auto-population — the list is purely hand-picked. For automatic surfacing, use [[design-module-product-showcase]] with `type=bundle` instead.

## Settings & fields

| Setting key | Type | Default | Allowed values | Limits / range | Validation rule | Notes |
|---|---|---|---|---|---|---|
| `enabled` | toggle | `true` | on / off | — | freeform | Master on/off |
| `title` | string | `""` | any string | 0-100 chars | `char:0,100` | Section title |
| `filter_value` | autocomplete | `null` | bundle product IDs (drag-reorder) | — | freeform; existence-validated | Bundles to surface |
| `color` | colour string | `""` | hex / preset | — | freeform | Section-header colour (theme-dependent) |
| `icon` | image select | `""` | uploaded image | — | freeform | Section-header icon (theme-dependent); save derives `icon_data` |
| `per_row` | int | `4` | 1-4 | 1-4 | `int:1,4` | Bundles per row |

### Validation strings

| Scenario | Message |
|----------|---------|
| Save success | *"Module successfully edited"* |
| Reset success | *"Module successfully reset"* |
| `filter_value` contains an unknown product ID | *"One or more products no longer exist."* (i18n key `module.product.showcase.err.one_or_more_products_no_longer_exist`) |
| `per_row` out of 1-4 | Field-level integer-range error |
| `title` longer than 100 chars | Field-level char-range error |

## All themes vs theme-specific

| Setting | All themes | Theme-specific notes |
|---------|-----------|----------------------|
| Core fields (`enabled`, `title`, `filter_value`, `per_row`) | only on themes shipping a `bundleShowcase` instance | — |
| `color`, `icon` | depends | Only on themes with decorated section headers |
| Slot rendering | theme | Theme must ship a `bundleShowcase` slot |

## Business rules

### Source is purely hand-picked

The merchant picks specific bundles from the autocomplete; the runtime fetches exactly those. Drag-reorder controls the row sequence.

### Bundles app dependency

The autocomplete pulls from products with `product_type=bundle`. Without the Bundles app installed, no such products exist (or they're hidden), and the autocomplete is empty.

### Hand-picked order is preserved

Like [[design-module-product-showcase]] with `filter=product`, the saved IDs are rendered in the order the merchant picked them.

### Bundle sub-products are eagerly loaded

The runtime not only loads the bundle product records, but also their sub-product members (the products inside each bundle) — formatted via the platform code with each sub-product's `format` applied. This lets the storefront template render "this bundle contains X, Y, Z" without extra requests.

### Reset is per-instance

Per-instance JSON; reset clears only the instance.

### Cache invalidation on save / reset

Standard — save / reset bump the per-site cache key.

### Auto-injected as system module (for themes that ship the slot)

The module helper lists `bundleShowcase` in the system map; the card is auto-injected if the theme ships the slot.

## Related

- [[design-modules-products]] — hub.
- [[apps-bundles-overview-new]] — Bundles app that creates the bundle products.
- [[design-module-product-in-bundles]] — sibling row showing bundles that CONTAIN the current product.
- [[design-module-product-showcase]] — auto-populating product row with `type=bundle`.

## How it works (verified against backend)

### Restrictions

`enabled=false (toggle), title=char:0,100, filter_value=false (freeform; existence-validated), color=false, icon=false, per_row=int:1,4`.

### Defaults

`enabled=true, title="", filter_value=null, color="", icon="", per_row=4`.

### Save pipeline

`enabled` cast to bool. `filter_value` exploded from CSV if string. Existence validated via the platform code. `icon_data` derived from `icon`.

### Source loading

`getListingDriver->setWheres(['item_id' => $ids])` → preserves admin-defined order via `array_flip($ids)` → eager-loads the platform code for each loaded bundle.

## Open questions

- 📡 **Sub-product rendering on the tile.** Whether the tile shows the bundle's sub-products inline depends on the theme template — verify per-theme.
- 📡 **Bundle pricing display.** Whether the tile shows the bundle's combined price or the discounted price is theme-controlled — verify per-theme.
