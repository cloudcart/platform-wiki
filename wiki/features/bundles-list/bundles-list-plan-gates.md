---
type: feature
nav_path: "Products → Bundles → Plan gates & sync"
route_name: bundles-list.new
route_path: /admin/products/bundles-new
aliases: ["Bundle plan gates", "Bundle limit", "Hidden bundle", "Bundle storefront sync", "Bundle banner exclusion"]
tags: [apps, administration, products, bundles, plan-gates]
plan_gates: ["bundles", "hidden_products"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---
# Bundles — plan gates, sync & banner exclusion

> Part of [[bundles-list]]. See the hub for the other aspects (creation, pricing, stock).

## Purpose

This aspect covers the **plan-feature gates** on bundles (the dual app-install + numeric `bundles` cap, and the `hidden_products` boolean), plus two downstream behaviours that distinguish a bundle from a regular product: the storefront sync events fired on save, and the exclusion of bundles from banner/label auto-population.

## Where to find it

The gates surface on the Bundles list and editor (route `bundles-list.new`, path `/admin/products/bundles-new`). The app-install gate sits on `/admin/apps/bundles/install`.

## What the merchant can do here

- Create bundles up to the plan's numeric `bundles` cap; above the cap the **+ Create bundle** CTA is disabled.
- Mark a bundle Hidden (B2B / catalog-only) when the plan allows `hidden_products`.
- Edit existing bundles freely (the numeric cap only blocks NEW creation).

## Settings & fields

- `bundles` plan-feature — dual gate: app-install URL gate + numeric cap on bundle records.
- `hidden_products` plan-feature — boolean gate on the bundle's Hidden flag.
- The editor reads `feature.current` (cap) vs `feature.used` (existing bundle count) to decide whether to disable the create CTA.

## Business rules

### `bundles` — app-install gate + numeric cap

This feature is gated by these plan-features (see [[plan-gates]], [[plan-vs-feature-pack]], [[plan-features]]):

| Mapping | Shape | What it controls |
|---|---|---|
| `bundles` | App-install URL gate + Numeric (max bundles) | The `/admin/apps/bundles/install` URL is access-gated — without the plan-feature the merchant cannot install the Bundles app at all. Once installed, the **same `bundles` mapping ALSO carries a numeric cap** on the maximum number of bundle records. The editor reads `feature.current` (cap) vs `feature.used` (existing bundle count) and disables the **+ Create bundle** CTA when the cap is reached. Editing existing bundles bypasses the cap; only NEW bundle creation is gated. Per-plan add-on packs are available via [[plan-features]]. |
| `hidden_products` | Boolean | Whether a bundle can be set to Hidden (B2B / catalog-only). Toggling a bundle's hidden flag ON via `PATCH /api/bundles/hidden/<id>` returns HTTP 402 with the feature payload on plans that don't allow hidden products. Lower plans can still create visible bundles freely (subject to the numeric `bundles` cap). |

The dual app-install + numeric `bundles` cap is unusual — most app-install gates are pure booleans. The numeric cap surfaces the per-feature upsell modal at [[plan-features]] when the merchant tries to create the (N+1)th bundle. The count compared against the cap is the number of `type = bundle` products (checked alongside `products`, `categories`, etc.); the plan-limit page shows `used` vs `current`. The `hidden_products` boolean redirects to a plan-upgrade panel when the merchant tries to hide a bundle. See [[plan-vs-feature-pack]] for the pack-vs-upgrade decision.

### Storefront sync on save

On bundle save, the platform dispatches the same `ProductSaved` / `ProductCreated` / `ProductUpdated` / the search re-index events that fire for regular product changes — catalogue cache, search index, and webhooks all update — because **a bundle IS a product** under the hood (its row lives in the catalogue with `type = bundle`). See [[inventory-tracking]] for the stock-side ripple of these events.

### Bundles excluded from banner/label auto-population

Per the banner-target and label-target sync logic in [[products-banners-labels]]: bundles (`is_bundle = true`) are EXCLUDED from auto-populating banner/label conditions. A category-target banner targeting "Electronics" attaches to all regular electronics products but NOT to electronics bundles. A merchant who wants to advertise a bundle with a banner must add it manually as a product-target.

## Related

- [[bundles-list]] — hub.
- [[plan-gates]] — the plan-gating model.
- [[plan-features]] — per-feature upsell + add-on packs.
- [[plan-vs-feature-pack]] — pack-vs-upgrade decision.
- [[products-banners-labels]] — banner/label auto-population that excludes bundles.
- [[inventory-tracking]] — stock-side ripple of the save events.
- [[bundle]] — the bundle entity.

## Open questions

None.
