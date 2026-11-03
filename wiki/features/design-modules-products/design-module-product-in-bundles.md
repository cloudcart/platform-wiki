---
type: feature
nav_path: "Design → Modules → Products → Product in bundles"
route_name: admin.storefront.widget
route_path: /admin/storefront/widgets/productInBundles
aliases: ["Product in bundles module", "Product in packages module", "productInBundles module", "product.productInBundles", "Модул в пакети", "Bundle membership row"]
tags: [design, modules, products, bundles]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Product module — Product in bundles (`product.productInBundles`)

> Part of [[design-modules-products]]. See the category page for the other product modules.

## Purpose

The **Product in bundles** module (instance name `productInBundles`, type `product.productInBundles`) renders the row of bundle packages that CONTAIN the currently viewed product. On the product detail page for a shoe, for example, it surfaces the "Spring outfit", "Sports kit", or "Gift box" bundles that include that shoe — driving cross-sell from individual products into multi-product packages. Pulls data from the **Bundles** app — without the app installed the module does nothing.

## Where to find it

Sidebar → **Design** → **Modules** → **Products** tab → card labelled **"Product in packages"** (theme-translated).

Edit-panel URL: `/admin/storefront/widgets/productInBundles`.

Renders on the product detail page only — slot is theme-controlled.

## What the merchant can do here

- Master enable / disable toggle.
- Set how many bundles to show (cap).
- Pick bundles per row.
- Pick a section-header colour and icon (theme-dependent decoration).

## What the merchant cannot do here

- Cannot pick WHICH bundles to surface — the list is derived from the product → bundle membership table.
- Cannot exceed 10 bundles in the row (`int:1,10`).
- Cannot show more than 4 per row (`int:1,4`).
- Cannot use this module without the Bundles app installed — see [[apps-bundles-overview-new]].

## Settings & fields

| Setting key | Type | Default | Allowed values | Limits / range | Validation rule | Notes |
|---|---|---|---|---|---|---|
| `enabled` | toggle | `true` | on / off | — | freeform | Master on/off |
| `products` | int | `3` | 1-10 | 1-10 | `int:1,10` | Cap on bundles in the row |
| `per_row` | int | `4` | 1-4 | 1-4 | `int:1,4` | Bundles per row |
| `color` | colour string | `""` | hex / preset | — | freeform | Section-header colour (theme-dependent) |
| `icon` | image select | `""` | uploaded image | — | freeform | Section-header icon (theme-dependent); save derives `icon_data` |

### Validation strings

| Scenario | Message |
|----------|---------|
| Save success | *"Module successfully edited"* |
| Reset success | *"Module successfully reset"* |
| `products` out of 1-10 | Field-level integer-range error |
| `per_row` out of 1-4 | Field-level integer-range error |

## All themes vs theme-specific

| Setting | All themes | Theme-specific notes |
|---------|-----------|----------------------|
| `enabled`, `products`, `per_row` | yes | Universal — every theme with the slot reads them |
| `color`, `icon` | depends | Only on themes with decorated section headers |
| Slot rendering | depends | Theme must ship a `productInBundles` slot; without it the module settings are saved but nothing renders |

## Business rules

### Source is the bundle-membership join

The runtime reads `products_bundle` to find every bundle that contains the current product, then loads the bundle records via the listing driver (filtered to `product_type=bundle`). The merchant cannot bias this list — it is purely membership-driven.

### Empty list hides the row

If the product is in zero bundles, the row self-hides — no empty "Product in packages" header is rendered.

### Bundles app dependency

The module is auto-injected as a SYSTEM module on the Modules screen, but if the Bundles app is not installed, the bundle-membership table is empty and the row stays hidden everywhere. Install / configure bundles in [[apps-bundles-overview-new]] before tuning this module.

### Order of bundles

Bundles render in whatever order the listing driver returns them — typically ID-DESC (newest first). The merchant cannot override the order.

### Reset is per-instance

Each instance has its own saved JSON. Reset clears one instance's settings without touching others (unlike `product.related`).

### Cache invalidation on save / reset

Standard — save / reset bump the per-site cache key.

## Related

- [[design-modules-products]] — hub.
- [[apps-bundles-overview-new]] — the Bundles app that powers the membership data.
- [[products-products]] — products that belong to bundles.
- [[design-module-product-bundle-showcase]] — sibling module showing a hand-picked bundle row on the homepage.

## How it works (verified against backend)

### Restrictions

`enabled=false (toggle), color=false, icon=false, per_row=int:1,4, products=int:1,10`.

### Defaults

`enabled=true, color="", icon="", per_row=4, products=3`.

### Source query

`SELECT bundle_id FROM products_bundle WHERE product_id = :id` → distinct bundle IDs → fed to the listing driver with `item_id` and `product_type=bundle` constraints → returns at most `products` bundle records.

### Save pipeline

Casts `enabled` to bool, derives `icon_data` if `icon` is set, persists. No shared `Configuration` group — per-instance only.

### Auto-injected as system module

Same mechanism as `productsDetails` and `filters` — listed in the module-helper system map so the card always appears on the Modules screen even when the theme JSON omits the instance.

## Open questions

- 📡 **Sort order of bundles.** Likely most-recent-first; verify whether the listing driver applies a stable order.
- 📡 **Behaviour when bundles are inactive / hidden.** Whether disabled bundles still render needs verification.
