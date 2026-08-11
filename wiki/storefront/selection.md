---
type: storefront-page
route_name: selection
route_path: /selection/{slug}
themes_using: [all]
tags: [storefront, selection, smart-collection, listing, curated]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Storefront — Selection (`/selection/{slug}`)

## Purpose

A **selection** is a merchant-curated collection of products — either hand-picked (manual) or rule-driven (smart). Each selection has its own URL of the form `/selection/<url_handle>` and renders as a product listing scoped to the products in that selection.

Selections are CloudCart's equivalent of "Shopify collections" — the merchant builds them via [[products-smart-collections]] (also reachable as the "Smart collections" admin screen) and surfaces them from menus, banners, or page-builder blocks. Use cases: "Summer sale 2026", "New arrivals", "Bestsellers under 50 BGN", "Curated gift ideas".

The page reuses `products/list.tpl` — the same template as [[products-list]] — with the listing scope set to the selection's products. The page heading shows the selection's name instead of "Products".

## URL & route

- **Route name**: `selection`
- **Route path**: `/selection/{slug}`
- **Controller**: the selection controller, the request handler
- **Middleware**: `uuid_generate`, `subscriber_uuid`, `TSStatistic:selection`

If the URL slug does not match the current `url_handle`, the controller 301-redirects to the canonical URL. If the slug resolves to no selection, the controller 404s with `sf.global.err.page_not_found`.

## How it loads

1. The selection controller resolves the slug via the smart-collection model's filter scope. Returns the active selection or 404.
2. Sets the filter module's "current selection" so the page heading and breadcrumbs reflect the selection's name.
3. Reads the current customer's group (the platform code or the platform's guests-group ID — see [[customer-group]]).
4. Calls `$this->loadProducts('collection', ['collection_ids_' . $groupId => $selection->id])` — the abstract listing pipeline scopes to products in this selection **resolved for this customer group**. (Selections can be customer-group-specific via [[products-smart-collections]] rules.)
5. Returns the platform code — the same template as [[products-list]].

## What the customer sees

- **Breadcrumb** — "Home → <Selection name>" (the breadcrumb module surfaces the selection in the trail).
- **Page heading** — the selection's name (the template prioritises the platform code over the generic products title).
- **Sort dropdown** + **Per-page dropdown** + **Filter sidebar** — all behave identically to [[products-list]].
- **Product grid** — paginated products in the selection (scoped to the customer group).
- **Pagination** — same as [[products-list]].

The selection's description / image / SEO meta are honoured if the merchant set them (verify — depends on whether the selection model exposes those fields and the template renders them; observed in `flair`'s `products/list.tpl` only category/vendor headers exist, not selection headers).

## Storefront behaviour

- Identical AJAX behaviour to [[products-list]] — filter / sort / pagination changes swap content via AJAX.
- **Customer-group scoping**: when a logged-in customer belongs to a group, the selection's product set may differ from the guest version (smart-collection rules can reference group). The page therefore varies per customer — caching at the HTML level must be customer-group-aware.

## JavaScript behaviour

- Same hook set as [[products-list]] — `.js-sidebar-toggler`, `.js-products-container`, `.js-products-pagination`, `.js-order-by-select`, etc.
- AJAX endpoints called from this page:
  - `/ajax/selection/{url_handle}` — route `ajax.selection` (full HTML).
  - `/ajax-products/selection/{url_handle}` — route `ajax.products.selection` (products only).
  - `/filters-ts/selection/{url_handle}` — route `ajax.filters-ts.selection` (filters only).

## Customisations available to the merchant

| Aspect | Where to configure |
|--------|--------------------|
| Selection name, slug, products (manual or rule-driven) | [[products-smart-collections]] |
| Customer-group scope (which groups see the selection) | [[products-smart-collections]] — group rules |
| Selection's SEO title / description / canonical | [[products-smart-collections]] (verify) |
| Whether the selection appears in the storefront menu | [[design-navigation]] |
| Filter sidebar / sort / per-page in the listing | [[design-modules]] → Products filters module (shared across all listings) |
| Promote a selection on the home page | [[design-modules]] → Products showcase module (`showcaseProducts`) can target a selection |

## Theme variations

- All themes render `products.list` for this route — the structure is consistent with [[storefront-category]] / [[products-list]].
- Some themes (verify per theme) inject a selection-header block (image + description) at the top of the listing similar to a category header — this is theme-specific.
- See [[storefront-themes-catalog]].

## Known issues / by-design vs bug

- **By design**: the selection page reuses `products/list.tpl` — every cosmetic tweak made for [[products-list]] applies here.
- **By design**: scoping by customer group means the same `/selection/{slug}` URL can return different product sets for different customers — analytics / SEO scrapers see the guest-group version.
- **By design**: a renamed selection's old slug 301-redirects to the new canonical URL.
- **By design**: a deleted / unpublished selection 404s with the page-not-found message.
- See [[storefront-known-issues]] for cross-page bugs.

## Related

- [[storefront-architecture]] — request lifecycle.
- [[storefront-themes-catalog]] — per-theme variations.
- [[products-list]] — same template, no scope.
- [[storefront-category]] — same template, category scope.
- [[tag]] — same template, tag scope.
- [[storefront-vendor]] — same template, vendor scope.
- [[product-detail]] — destination of tile click.
- [[products-smart-collections]] — admin screen for creating selections.
- [[smart-collection]] — entity definition.
- [[customer-group]] — entity that scopes selection visibility.
- [[design-modules]] — Products showcase module can target a selection.
- [[design-navigation]] — selections in the storefront menu.
- [[storefront-known-issues]] — cross-storefront issue register.

## Open questions

- Whether selections expose an SEO meta editor in [[products-smart-collections]] — and whether the storefront emits per-selection canonical tags.
- Whether the selection's name / description / image render as a header block in the base `flair` theme — the observed template only shows category and vendor header blocks.
- How customer-group-specific selections interact with the platform edge cache layer (see [[platform-rate-limits]]) — is the cache key keyed on the customer group?
