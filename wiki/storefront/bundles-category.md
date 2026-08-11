---
type: storefront-page
route_name: bundles.list.category
route_path: /bundles/category/{slug}
themes_using: [all]
tags: [storefront, bundles, listing, category]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Bundles category listing (storefront)

## Purpose

A category-scoped listing of bundle products only. Identical visual layout to the normal category page but filtered to `product_type = bundle`, so customers browsing the bundles section by category see only bundle SKUs (and not the individual children that make them up).

## URL & route

- **Route name:** `bundles.list.category`
- **Path:** `/bundles/category/{slug}`
- **Middleware:** `TSStatistic:bundles-category`.
- **Sibling routes:**
  - `bundles.list.list` → `/bundles` (full unfiltered bundles listing).
  - `bundles.list.category.ajax` → `/ajax-products/bundles/category/{slug}` (AJAX paging / filter refresh).
  - `ajax.products.bundles.list.category.ajax` (`/ajax/products-only/bundles/category/{slug}`) and `ajax.filters-ts.bundles.list.category.ajax` (`/ajax/filters-ts/bundles/category/{slug}`) — used by the storefront search engine layer for AJAX-only products and facet refreshes.

## How it loads

1. Route resolves to the request handler.
2. Engine branch:
   - **Smarty themes** — `viewSmartyEngine($slug)`:
     - the platform code looks up the category; missing → `abort(404, sf.global.err.category_no_longer_exists)`.
     - If the canonical `url_handle` differs from the requested `slug`, a `301` redirect is issued.
     - the platform code wires the facet module to the category.
     - the platform code queries bundles in this category AND all descendants.
     - Renders `products.list` (the same template used by every regular category page).
   - **Liquid themes** — `viewLiquidEngine` builds a `BundleListDrop` for the category and renders the Liquid template.
3. Because the template is reused, all the usual category-page behaviour (facets, sort, pagination, view modes) applies — see [[storefront-category]].

## What the customer sees

- Breadcrumb: **Home › Bundles › <Category name>** (verify the exact "Bundles" segment label per theme).
- Category title and description (inherited from the category record).
- Facet sidebar (price, brand, attributes) populated by the filter module for the bundles-only product set.
- Grid/list of bundle product cards — same template as a normal category but every card represents a bundle SKU.
- Pagination + sort dropdown identical to the normal [[storefront-category]] page.
- "No products" empty state if the category contains no published bundles.

## Storefront behaviour

- The listing includes bundles from the requested category AND every descendant category (`child_by_path`).
- Mismatched slug capitalisation / accents → 301 to the canonical `url_handle`.
- Category missing or unpublished → `404` with `sf.global.err.category_no_longer_exists`.
- Statistics: every page view is recorded under the `bundles-category` event by `TSStatistic` middleware.
- Same AJAX endpoints as the regular category page; the storefront filter framework hits the `*.ajax` variants when the customer changes a facet.

## JavaScript behaviour

- Inherits everything from the shared products list template:
  - `.js-products-container` — the grid wrapper.
  - Storefront facet/filter framework — debounced AJAX calls to `bundles.list.category.ajax`.
  - `.js-sidebar-toggler` — mobile facet drawer.
- Per-card actions (compare / wishlist) work exactly as on a regular category page — see [[compare]] and [[wishlist]].

## Customisations available to the merchant

- **Bundles** themselves are managed under [[storefront-bundles-list]] and the [[apps-bundles-overview-new]] / [[apps-bundles-settings-new]] app pages.
- **Category assignment** — every bundle has a `category_id` like a normal product; the listing reflects the standard category tree.
- **Facets** — same attribute / brand / price facets as a regular category page; the storefront filter module reuses the configuration.
- **Per-category page text & SEO** — inherited from the category record (description, SEO title, SEO description, OG image).

## Theme variations

- Same `products.list` template as [[storefront-category]]; visual differences are entirely the merchant's standard category-page styling.
- Liquid themes use their own bundle category layout via `BundleListDrop`.

## Known issues / by-design vs bug

- The route deliberately reuses `products.list`, so anything that affects regular category pages (sort options, facet behaviour, infinite scroll on supported themes) affects this page too — no separate template override.
- An empty bundles category still returns `200` (with the empty-state copy), not `404` — `404` is reserved for missing/unpublished categories.
- Bundles in subcategories show in the parent's listing because of the `child_by_path` expansion — by design.

## Related

- [[storefront-category]]
- [[storefront-bundles-list]]
- [[apps-bundles-overview-new]]
- [[apps-bundles-settings-new]]
- [[storefront-architecture]]

## Open questions

- Confirm whether the parent `/bundles` listing exposes a breadcrumb link that links here on every theme.
- Confirm exact behaviour when a category contains a mix of bundles and regular products — only bundles render, but does the facet sidebar count include or exclude non-bundles?
- Confirm the canonical "Bundles" breadcrumb segment label per theme.
