---
type: storefront-page
route_name: bundles.list.list
route_path: /bundles
themes_using: [all]
tags: [storefront, bundles, listing, filters]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Storefront — Bundles listing (`/bundles`)

## Purpose

The bundles page is the catalogue listing **scoped to bundle products only** — products whose `product_type` is `bundle` (the platform's bundle entity, see [[bundle]]). It is the storefront-side counterpart of the admin bundles app ([[apps-bundles-overview-new]], [[apps-bundles-settings-new]]) — when the merchant defines a bundle product (a "buy A + B + C as one SKU at a special price"), it shows up here.

The page reuses `products/list.tpl` (the same template as [[products-list]]) — the bundles controller seeds the listing scope with `product_type = bundle`. There's also a per-category variant at `/bundles/category/{slug}` for bundles assigned to a specific category.

## URL & route

- **Route name**: `bundles.list.list`
- **Route path**: `/bundles`
- **Controller**: the bundles controller, the request handler
- **Middleware**: `TSStatistic:bundles`

Per-category variant:

- **Route name**: `bundles.list.category`
- **Route path**: `/bundles/category/{slug}`
- **Controller method**: the request handler
- **Middleware**: `TSStatistic:bundles-category`

Both variants reuse the same Smarty template and the same `loadProducts('bundles' | 'bundle-category', ...)` listing pipeline.

## How it loads

1. The bundles controller calls the platform code — the abstract listing pipeline paginates products whose `product_type` is `bundle`.
2. For the per-category variant, the controller first resolves the category slug via the category model's filter scope (the platform code), 301-redirects to the canonical slug if needed, sets the filter module's "current category", and calls the platform code.
3. Returns the platform code — the same template as [[products-list]].

If the per-category variant's slug resolves to no active category, the controller 404s with `sf.global.err.category_no_longer_exists`.

## What the customer sees

The visible structure is identical to [[products-list]]:

- **Breadcrumb** — "Home → Bundles" (or "Home → Bundles → <Category name>" for the per-category variant).
- **Page heading** — the products-or-bundles title module surfaces a "Bundles" label.
- **Sub-category tile strip** — renders on `/bundles/category/{slug}` when the category has children (same as on [[storefront-category]]); on `/bundles` proper, no tiles.
- **Sort dropdown** + **Per-page dropdown** + **Filter sidebar** — same as [[products-list]].
- **Product grid** — bundle products only.
- **Pagination** — same as [[products-list]].

Product tiles for bundle products are typically marked with a "Bundle" badge / pricing display (theme-specific).

## Storefront behaviour

- Identical AJAX behaviour to [[products-list]] — filter / sort / pagination changes swap content via AJAX.
- Clicking a tile navigates to the bundle's product-detail page ([[product-detail]]) where the customer sees the bundle's components and pricing.

## JavaScript behaviour

- Same hook set as [[products-list]] — `.js-sidebar-toggler`, `.js-products-container`, `.js-products-pagination`, etc.
- AJAX endpoints called from this page:
  - `/ajax/bundles` — route `bundles.list.list.ajax` (full HTML for `/bundles`).
  - `/ajax/bundles/category/{slug}` — route `bundles.list.category.ajax` (full HTML for `/bundles/category/{slug}`).
  - `/ajax-products/bundles` — route `ajax.products.bundles.list.list.ajax` (products only).
  - `/ajax-products/bundles/category/{slug}` — route `ajax.products.bundles.list.category.ajax`.
  - `/filters-ts/bundles` — route `ajax.filters-ts.bundles.list.list.ajax`.
  - `/filters-ts/bundles/category/{slug}` — route `ajax.filters-ts.bundles.list.category.ajax`.

## Customisations available to the merchant

| Aspect | Where to configure |
|--------|--------------------|
| Bundle products themselves (components, pricing, inventory) | [[apps-bundles-overview-new]], [[apps-bundles-settings-new]] |
| Categories assigned to bundles | [[products-products]] → bundle product edit → categories |
| Whether a link to `/bundles` appears in the storefront menu | [[design-navigation]] |
| Filter sidebar / sort / per-page on the listing | [[design-modules]] → Products filters module |
| Bundle pricing display on tiles | [[design-modules]] / [[design-theme-editor]] (theme-specific) |
| Promote bundles on the home | [[design-modules]] → Products showcase module |

## Theme variations

- All themes render `products.list` for both `/bundles` routes — the structure is consistent.
- Bundle pricing badges / "Bundle" labels on tiles depend on the theme's the theme templates partial.
- Themes that have a dedicated bundle-detail layout differ on [[product-detail]] rather than on this listing page.
- See [[storefront-themes-catalog]].

## Known issues / by-design vs bug

- **By design**: `/bundles` is a separate URL from `/products` — bundles are filtered out of the generic catalogue listing (verify) so the customer can browse them as a distinct shop.
- **By design**: the per-category variant `/bundles/category/{slug}` honours descendant categories via the same `child_by_path` mechanism as [[storefront-category]].
- **By design**: a renamed category's old slug 301-redirects to the canonical URL on the per-category bundles variant.
- **By design**: if the merchant has zero bundle products, the page renders an empty listing (the "no products" state from the theme templates) rather than 404.
- See [[storefront-known-issues]] for cross-page bugs.

## Related

- [[storefront-architecture]] — request lifecycle.
- [[storefront-themes-catalog]] — per-theme variations.
- [[products-list]] — same template, no scope.
- [[storefront-category]] — same template, single category, all product types.
- [[product-detail]] — bundle detail page (shows components + pricing).
- [[storefront-cart]] — adding a bundle to cart.
- [[bundle]] — entity definition.
- [[apps-bundles-overview-new]] — admin screen listing bundles.
- [[apps-bundles-settings-new]] — bundle configuration.
- [[products-products]] — admin product list (bundle products live here too).
- [[design-modules]] — filter module configuration; Products showcase module.
- [[design-navigation]] — bundles link in storefront menu.
- [[analytics-top-bundles-by-traffic]] — analytics on bundle traffic.
- [[analytics-top-order-bundles-by-sales]] — analytics on bundle sales.
- [[storefront-known-issues]] — cross-storefront issue register.
- [[bundles-category]] — storefront category listing filtered to bundle products.

## Open questions

- Whether bundle products are excluded from `/products` (the flat catalogue) by default, or whether they appear there too unless the merchant filters them out.
- Whether the per-category bundles variant is exposed in the storefront menu by default, or only via direct links.
- Whether the bundle pricing on the listing tile uses the bundle's discounted price or the sum-of-components price (theme- and bundle-config-dependent).
