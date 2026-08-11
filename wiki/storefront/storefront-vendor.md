---
type: storefront-page
route_name: site.vendor.view
route_path: /vendor/{slug}
themes_using: [all]
tags: [storefront, vendor, brand, listing, seo]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Storefront — Vendor landing (`/vendor/{slug}`)

## Purpose

The vendor page lists every product attributed to a given vendor (brand). It is the storefront-side counterpart of [[products-vendors]] — the admin assigns a vendor to a product, and the customer can reach the vendor's URL `/vendor/<url_handle>` via menu links, the vendors index ([[vendors-list]]), brand chips on product pages, or banners.

This page reuses `products/list.tpl` — the same template as [[products-list]] — with the listing scope set to this vendor's ID. Unlike most other listing surfaces, the **vendor filter is hidden from the sidebar** on this page (the customer is already on a vendor page — re-filtering by vendor is meaningless).

## URL & route

- **Route name**: `site.vendor.view`
- **Route path**: `/vendor/{slug}`
- **Controller**: the vendor controller, the request handler
- **Middleware**: `uuid_generate`, `subscriber_uuid`, `TSStatistic:vendor`

If the slug resolves to no vendor, the controller 404s with `sf.global.err.page_not_found`.

## How it loads

1. The vendor controller resolves the slug via the vendor model's filter scope (the platform code). Returns the active vendor or 404.
2. Sets the filter module's "current vendor" so the breadcrumb and page heading surface the vendor's name.
3. Calls `$this->loadProducts('vendor', ['vendor_id' => $vendor->id])` — the abstract listing pipeline paginates this vendor's products.
4. The vendor filter in the sidebar is force-hidden on this route — `AbstractProductsListing` explicitly disables the `vendors` filter when the active route is `site.vendor.view` (and its three AJAX variants).
5. Returns the platform code.

## What the customer sees

- **Breadcrumb** — "Home → Vendors → <Vendor name>" or similar.
- **Vendor header block** (page 1 only) — the template explicitly renders a `<h1>` with the vendor name, plus:
  - **Vendor image / logo** (if uploaded) — 600x600 srcset, lazy-loaded.
  - **Vendor description** (HTML, `nofilter`) — the merchant's WYSIWYG content.
- **Sort dropdown** + **Per-page dropdown** + **Filter sidebar** — same as [[products-list]], **minus the vendor filter** (force-hidden).
- **Product grid** — this vendor's products, paginated.
- **Pagination** — same as [[products-list]].

The vendor header (image + description) only renders on page 1 — pages 2+ hide it to keep paginated URLs slim.

## Storefront behaviour

- Identical AJAX behaviour to [[products-list]] — filter / sort / pagination changes swap content via AJAX.
- The vendor sidebar filter never shows, on any AJAX response either — the same `activeRoute('site.vendor.view ajax.vendor ajax.products.vendor ajax.filters.vendor')` guard applies to AJAX endpoints.

## JavaScript behaviour

- Same hook set as [[products-list]] — `.js-sidebar-toggler`, `.js-products-container`, `.js-products-pagination`, etc.
- AJAX endpoints called from this page:
  - `/ajax/vendor/{vendor}` — route `ajax.vendor` (full HTML).
  - `/ajax-products/vendor/{vendor}` — route `ajax.products.vendor` (products only).
  - `/filters-ts/vendor/{vendor}` — route `ajax.filters-ts.vendor` (filters only).

## Customisations available to the merchant

| Aspect | Where to configure |
|--------|--------------------|
| Vendor name, slug, logo, description, SEO meta | [[products-vendors]] |
| Which products belong to the vendor | [[products-products]] → product edit → vendor field |
| Whether the vendor appears in the storefront menu | [[design-navigation]] |
| Whether the vendor appears on [[vendors-list]] (only vendors with active products show) | Implicit — driven by the vendor having at least one active product |
| Filter sidebar / sort / per-page in the listing | [[design-modules]] → Products filters module |
| Per-vendor SEO meta | [[products-vendors]] (verify) + [[marketing-seo-meta]] (global rules) |
| Promote a vendor on the home page | [[design-modules]] → Featured brands module (`showcaseBrand`) |

## Theme variations

- All themes render `products.list` for this route — the structure is consistent.
- The base `flair` template includes the vendor header block (image + description) explicitly; child themes inherit it.
- See [[storefront-themes-catalog]].

## Known issues / by-design vs bug

- **By design**: the vendor filter is hidden in the sidebar on `/vendor/{slug}` and its AJAX endpoints — re-filtering by vendor on a vendor page is meaningless.
- **By design**: the vendor header (logo + description) only renders on page 1 — paginated pages hide it.
- **By design**: a deleted / inactive vendor 404s with the page-not-found message.
- **By design**: [[vendors-list]] only shows vendors with at least one active product — vendors with all products archived disappear from the directory.
- See [[storefront-known-issues]] for cross-page bugs.

## Related

- [[storefront-architecture]] — request lifecycle.
- [[storefront-themes-catalog]] — per-theme variations.
- [[vendors-list]] — index of all vendors.
- [[products-list]] — same template, no scope.
- [[storefront-category]] — same template, category scope.
- [[tag]] — same template, tag scope.
- [[product-detail]] — destination of tile click; also surfaces a vendor chip linking back here.
- [[products-vendors]] — admin screen for vendors.
- [[products-products]] — admin product edit (assign vendor).
- [[storefront-vendor]] — entity definition.
- [[design-modules]] — Featured brands module; filter module configuration.
- [[design-navigation]] — vendors in storefront menu.
- [[marketing-seo-meta]] — per-vendor SEO meta.
- [[storefront-known-issues]] — cross-storefront issue register.

## Open questions

- Whether vendor SEO meta is editable per-vendor in [[products-vendors]] or if every vendor inherits global rules from [[marketing-seo-meta]].
- Whether the vendor's description supports the same WYSIWYG features as category descriptions (it's rendered `nofilter` either way).
- Whether the vendor page emits product-list microdata in addition to breadcrumbs.
