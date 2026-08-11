---
type: storefront-page
route_name: site.vendors
route_path: /vendors
themes_using: [all]
tags: [storefront, vendors, brands, index, directory]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Storefront — Vendors index (`/vendors`)

## Purpose

The vendors index is the **directory page** for all vendors (brands) in the store — typically rendered as a grid of vendor logos / cards grouped alphabetically by first letter, with each vendor linking to its own [[storefront-vendor]] landing.

The page only lists vendors that have at least one active product (vendors with all products archived or hidden disappear from the directory automatically). It is the storefront equivalent of "shop by brand".

## URL & route

- **Route name**: `site.vendors`
- **Route path**: `/vendors`
- **Controller**: the vendor controller, the request handler
- **Middleware**: `uuid_generate`, `subscriber_uuid`, `TSStatistic:vendors`

No slug, no pagination, no filters.

## How it loads

1. The vendor controller calls the platform code — emits the vendors-index SEO meta (`seo.vendors.title`, `seo.vendors.description`).
2. Calls `getListingDriver->getAllVendors` — returns every vendor with at least one active product.
3. Stores the result in the platform registry (for downstream module access).
4. Returns the platform code — Smarty renders `themes/<active-theme>/templates/vendors/list.tpl` with the vendors pre-grouped by their first letter.

## What the customer sees

- **Breadcrumb** — "Home → Vendors" (`{t}sf.global.act.vendors{/t}`).
- **Section title** — `<h1>` with the translated label `sf.vendors.header.find_your_favorite_brand` ("Find your favourite brand").
- **Vendors grouped by letter** — rendered via the shared the theme templates module partial:
  - One section per letter (A, B, C, …).
  - Each vendor in a section renders as a card / logo (`300x300` image; `srcset` 300x300 desktop / 600x600 mobile).
- **Breadcrumb microdata** — emitted via the theme templates for SEO.

## Storefront behaviour

- Pure server-rendered HTML — no AJAX, no filters, no pagination.
- Clicking a vendor card navigates via plain `<a href>` to that vendor's `/vendor/{slug}`.

## JavaScript behaviour

- The page itself emits no page-specific `.js-*` hooks. Standard layout hooks from the header / footer (e.g., `.js-navigation-hamburger`) still apply.
- No AJAX traffic.

## Customisations available to the merchant

| Aspect | Where to configure |
|--------|--------------------|
| Vendor logo, name, slug, description | [[products-vendors]] |
| Which vendors appear (must have ≥ 1 active product) | Implicit — driven by product assignment in [[products-products]] |
| Whether a link to `/vendors` appears in the storefront menu / footer | [[design-navigation]] |
| SEO meta for `/vendors` | Translation strings (`seo.vendors.title`, `seo.vendors.description`) — global, not per-merchant |
| Vendor card layout (cards, logos, columns) | Theme-specific — see [[design-theme-editor]] for theme variables |
| Promote a vendor on the home | [[design-modules]] → Featured brands module (`showcaseBrand`) |

## Theme variations

- All themes render `vendors.list` for this route. The shared the theme templates is the default group-by-letter layout — most themes use it.
- Themes can override `templates/vendors/list.tpl` to render a non-alphabetical layout (e.g., logo wall without letter sections), or override the theme templates to change the per-letter card style.
- See [[storefront-themes-catalog]].

## Known issues / by-design vs bug

- **By design**: vendors with zero active products do not show up in the directory — the listing-driver's `getAllVendors` excludes them.
- **By design**: vendors are grouped by their first letter (`$vendor->letter`) — the model exposes a `letter` attribute used by `groupBy` (verify the exact derivation: likely `strtoupper(substr($name, 0, 1))`).
- **By design**: the page has no pagination — every active vendor renders on one page. Stores with hundreds of vendors get a long page.
- **By design**: there is no per-vendor SEO meta editor on this index — vendor SEO lives on [[storefront-vendor]] individually.
- **By design**: the Liquid-engine path (Nitrogen-style themes, see [[headless-storefront]]) renders `templates/list-collections` instead of the Smarty `vendors/list.tpl`.
- See [[storefront-known-issues]] for cross-page bugs.

## Related

- [[storefront-architecture]] — request lifecycle.
- [[storefront-themes-catalog]] — per-theme variations.
- [[storefront-vendor]] — destination of every card click.
- [[products-list]] — flat catalogue listing.
- [[storefront-category]] — categories alternative for browsing.
- [[products-vendors]] — admin screen for vendor records (logo, description, SEO).
- [[products-products]] — admin product edit (assign vendor).
- [[storefront-vendor]] — entity definition.
- [[design-navigation]] — vendors link in storefront menu.
- [[design-modules]] — Featured brands module on the home.
- [[design-theme-editor]] — visual customisation.
- [[storefront-known-issues]] — cross-storefront issue register.

## Open questions

- How `vendor->letter` is computed — is it the first letter of `name`, or a denormalised column updated on save?
- Whether multi-language stores group vendors by the localised name's first letter or the source-language name.
- Whether stores with hundreds of vendors get any pagination / alphabet-jump-nav, or always render flat.
