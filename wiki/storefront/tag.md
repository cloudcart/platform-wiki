---
type: storefront-page
route_name: site.tag
route_path: /tags/{slug}
themes_using: [all]
tags: [storefront, tag, listing, taxonomy, seo]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Storefront — Tag landing (`/tags/{slug}`)

## Purpose

The tag page lists every product tagged with a given product tag. It is the storefront-side counterpart of [[products-tags]] — the admin assigns a tag to a product, and the customer can reach the tag's URL `/tags/<url_handle>` via menu links, product-detail "tag" chips, banners, or page-builder blocks.

This page reuses `products/list.tpl` (the same template as [[products-list]]) — the tag controller seeds the listing scope with the tag's ID.

> **Note on URL pattern**: the route is registered as `/tags/{slug}` (plural), not `/tag/{slug}`. Verify per theme that menu / link helpers use the plural form.

## URL & route

- **Route name**: `site.tag`
- **Route path**: `/tags/{slug}`
- **Controller**: the tag controller, the request handler (the `index` method is an alias that delegates to `view`)
- **Middleware**: `uuid_generate`, `subscriber_uuid`, `TSStatistic:tag`

If the URL slug does not match the current `url_handle`, the controller 301-redirects to the canonical URL. If the slug resolves to no tag, the controller throws a not-found error with `sf.global.err.tag_no_longer_exists`.

## How it loads

1. The tag controller resolves the slug via the tag model's filter scope (the platform code). Returns the active tag or throws 404.
2. Sets the filter module's "current tag" so downstream surfaces know which tag is in scope.
3. Calls `$this->loadProducts('tag', ['tag_ids' => $tag->id])` — the abstract listing pipeline paginates products carrying this tag.
4. Returns the platform code — the same template as [[products-list]].

## What the customer sees

- **Breadcrumb** — "Home → <Tag name>" (verify exact label).
- **Page heading** — the tag name (rendered via the products-or-bundles title module; the template prioritises the selection name only when a selection is active, so for tags the standard title shows).
- **Sort dropdown** + **Per-page dropdown** + **Filter sidebar** — identical to [[products-list]].
- **Product grid** — products with this tag, paginated.
- **Pagination** — same.

The base `flair` `products/list.tpl` does NOT render a dedicated tag header block (the way it does for category and vendor). Themes that want to show the tag's image / description above the listing must override the template.

## Storefront behaviour

- Identical AJAX behaviour to [[products-list]] — filter / sort / pagination changes swap content via AJAX.
- No tag-specific JS behaviour.

## JavaScript behaviour

- Same hook set as [[products-list]] — see that page's "JavaScript behaviour" table.
- AJAX endpoints called from this page:
  - `/ajax/tags/{url_handle}` — route `ajax.tags` (full HTML).
  - `/ajax-products/tags/{url_handle}` — route `ajax.products.tags` (products only).
  - `/filters-ts/tags/{url_handle}` — route `ajax.filters-ts.tags` (filters only).

## Customisations available to the merchant

| Aspect | Where to configure |
|--------|--------------------|
| Tag name, slug, image (if model supports), description, SEO meta | [[products-tags]] |
| Which products carry the tag | [[products-products]] → product edit → tags field |
| Whether the tag appears in the storefront menu | [[design-navigation]] |
| Filter sidebar / sort / per-page in the listing | [[design-modules]] → Products filters module |
| Tag chips on product-detail pages (links to `/tags/{slug}`) | Theme-managed — usually visible by default; see [[product-detail]] |

## Theme variations

- All themes render `products.list` for this route — the structure is consistent.
- Themes that customise the tag page (e.g., adding a hero with the tag description) override `products/list.tpl` directly — there is no separate `templates/tag/*.tpl` convention.
- See [[storefront-themes-catalog]].

## Known issues / by-design vs bug

- **By design**: the URL pattern is `/tags/{slug}` (plural) — singular `/tag/{slug}` is not registered, requests to it 404.
- **By design**: the page reuses `products/list.tpl` — the base theme renders no tag-specific header (no image, no description).
- **By design**: a renamed tag's old slug 301-redirects to the new canonical.
- **By design**: a deleted tag returns 404 with the translated message *"This tag no longer exists."*.
- **By design**: tags are flat — there is no parent-child hierarchy like [[storefront-category]].
- See [[storefront-known-issues]] for cross-page bugs.

## Related

- [[storefront-architecture]] — request lifecycle.
- [[storefront-themes-catalog]] — per-theme variations.
- [[products-list]] — same template, no scope.
- [[storefront-category]] — same template, category scope.
- [[storefront-vendor]] — same template, vendor scope.
- [[selection]] — same template, curated selection.
- [[product-detail]] — destination of tile click; also surfaces tag chips that link here.
- [[products-tags]] — admin screen for tag taxonomy.
- [[products-products]] — admin product edit (assign tags).
- [[design-modules]] — filter module configuration.
- [[design-navigation]] — tags in storefront menu.
- [[marketing-seo-meta]] — per-tag SEO meta.
- [[storefront-known-issues]] — cross-storefront issue register.

## Open questions

- Whether the tag model exposes an image / description / SEO meta editor in [[products-tags]] — and whether any themes surface it as a header on this page.
- Whether tags inherit SEO meta from a global rule in [[marketing-seo-meta]] or each tag has its own per-record SEO fields.
- The full list of theme overrides that render a tag-specific header (none observed in `flair`).
