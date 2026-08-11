---
type: storefront-page
route_name: products.list
route_path: /products
themes_using: [all]
tags: [storefront, products, catalogue, filters, listing]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Storefront — Products listing (`/products`)

## Purpose

The `/products` page is the **whole-catalogue listing surface** — every active product in the store, filterable by category, vendor, brand-model, custom property, variant option, price range, "new", "sale", and "featured" flags, sortable by the merchant's configured sort options, and paginated.

`/products` shares the `products/list.tpl` template and the same listing pipeline with [[storefront-category]], [[tag]], [[storefront-vendor]], [[selection]], [[storefront-bundles-list]], and [[search]] — each just seeds a different filter scope.

The route carries the `robots:noindex` middleware — `/products` is excluded from search engines because a flat catalogue dump is poor SEO (category pages are the canonical landing targets).

## URL & route

- **Route name**: `products.list`
- **Route path**: `/products`
- **Middleware**: `robots:noindex` (the page emits `X-Robots-Tag: noindex`).
- **Search redirect**: a request with `?search=...` 301-redirects to `/search?query=...` — kept for legacy theme URLs.

Query-string filters (applied by the search-engine driver):

- `?page=N` — pagination page; `?sort=<key>` — sort key; `?per_page=N` — page size override.
- `?categories=slug1,slug2`, `?vendors=...`, `?price_from=...`, `?price_to=...`, `?p_<property>=...`, `?v_<variant>=...`, `?new=1`, `?sale=1`, `?featured=1` — facet selections (verify exact param names per filter type).

## How it loads

1. Emits the products-list SEO meta (`sf.products.seo_title`, `sf.products.seo_description` with product count, `sf.products.seo_keywords`).
2. Runs the listing pipeline:
   - Reads the merchant's filter settings (which filters to display, per-page count, sort order, "show facet counts" toggle).
   - Asks the active **product-listing driver** (the search-engine abstraction — the search engine in the modern stack, the database in fallback mode) to paginate the catalogue with the active filters applied.
   - Hydrates the filter sidebar models for brand-model, categories, category-properties, vendors, price-ranges, sale, new, featured, and variants.
3. Renders `themes/<active-theme>/templates/products/list.tpl` via Smarty.

## What the customer sees

(Base `flair` theme.)

- **Breadcrumb** — "Home → Products"; the breadcrumb module is shared with category / vendor / tag pages and reflects whichever filter scope is active.
- **Page heading** — the products-or-bundles title (e.g., "Products"); arriving via a selection click shows the selection name instead.
- **Sub-category tile strip** — rendered only on [[storefront-category]] when the category has children; empty on `/products` proper.
- **Sidebar toggle** — `js-sidebar-toggler` button that opens/closes the filter sidebar on mobile and toggles the desktop sidebar between 9-col and 12-col layout; state persisted in a `sidebar` cookie (365 days).
- **Sort dropdown** (`.js-order-by-select`, `.js-order-by-link`) and **per-page dropdown** (`.js-per-page-by-select`, `.js-per-page-by-link`). Sort dropdown is hidden on `/search`.
- **Filter sidebar** (left, col-md-3): brand-model filter (if the BrandModel app is installed and the filter is enabled), categories tree (arrow-collapse), vendors (collapsible "Show all"), category properties (checkboxes for list-type, slider for range-type), variants (radios / colour swatches / image swatches), "New" / "Sale" flags, and price range slider.
- **Product grid** (right, col-md-9 with sidebar open, col-md-12 closed) — tile per product, image srcset 300x300 (≥992px) / 600x600 (mobile).
- **Pagination** — `.js-products-pagination`.

## Storefront behaviour

- **Filter, sort, and per-page changes trigger AJAX** — toggling a sidebar checkbox or changing a dropdown re-renders the product grid and filter sidebar in place, with no full page reload.
- **Pagination is AJAX-on-click** — the `js-products-pagination` element resolves to one of the `/ajax/*` endpoints below; the URL bar updates via `history.pushState` (verify).
- The loading state shows a `js-loading-products` spinner inside `js-product-list`; `js-products-container` is the swap target.
- **Sidebar collapse state is cookied** — `sidebar=open|closed` (365 days). **Sub-filter collapse state is cookied** per property — `products.list.filter.<name>=0|1`.

## JavaScript behaviour

Hooks on this page:

| Hook | Purpose |
|------|---------|
| `.js-sidebar-toggler` | Opens / closes the filter sidebar; toggles desktop col widths via `js-products-box`; persists state to `sidebar` cookie. |
| `.js-sidebar` | The sidebar container — gets `open` / `mobile-open` classes. |
| `.js-sidebar-buttons` | The mobile open / close button row inside the sidebar. |
| `.js-sidebar-ajax` | The container the filter-state AJAX response replaces. |
| `.js-sidebar-list-collapsing`, `.js-sidebar-list-all` | "Show all" collapse for long vendor lists. |
| `.js-products-box` | The main column — width swaps between `col-md-9` and `col-md-12`. |
| `.js-product-list` | Wrapper for the product grid + loader. |
| `.js-loading-products` | Spinner shown during AJAX swaps. |
| `.js-products-container` | The swap target the AJAX response writes into. |
| `.js-empty-on-ajax` | Marker — wrapper that should be emptied before AJAX replace. |
| `.js-order-by-select`, `.js-order-by-link` | Sort dropdown. |
| `.js-per-page-by-select`, `.js-per-page-by-link` | Per-page dropdown. |
| `.js-products-pagination` | Pagination AJAX trigger. |
| `.js-add-to-cart`, `.js-quick-view`, `.js-add-to-wishlist` | Product-tile actions (see [[storefront-cart]], [[product-detail]]). |

Custom jQuery events:

- `cc.filters.filters.after` — fired on `document` after a filter AJAX response swaps in; the handler re-applies the per-property collapse state.

AJAX endpoints (one of three trees, depending on theme):

- `/ajax/category/{slug}` — full HTML (products + filters + pagination); route `ajax.category`.
- `/ajax-products/category/{slug}` — products-only HTML; route `ajax.products.category`.
- `/filters-ts/category/{slug}` — filter-sidebar HTML only; route `ajax.filters-ts.category`.

The modern theme stack typically uses `/ajax-products/*` and `/filters-ts/*` in parallel. See [[storefront-architecture]] for the three-tree contract.

## Customisations available to the merchant

| Behaviour | Where to configure |
|-----------|--------------------|
| Which filters appear, sort options offered, per-page choices | [[design-modules]] → Products filters module |
| Show / hide facet counts next to filter labels | [[design-modules]] → `show_facet_counts` |
| Grid columns per breakpoint | [[design-modules]] → Products module → `per_row_desktop` |
| Show "Quick view" button on tiles | Setting `show_product_quick_view` (yes/no) |
| Show "Buy" button on tiles | [[design-modules]] → `listing_show_buy` |
| Product card visuals (price / labels / etc.) | [[products-banners-labels]], [[design-theme-editor]] |
| SEO title / description for `/products` | Translation strings (`sf.products.seo_title` etc.) — not editable per-merchant |

## Theme variations

- `flair` is the base. Most child themes (`flair-*`, `motivation-*`, `summer*`, `jeans*`, another custom theme, `wonderland`, `zooland`, etc.) ship their own `products/list.tpl` with cosmetic differences (breadcrumb position, sidebar styling, masonry vs. uniform grid). Every theme must ship its own listing template.
- The `properties` and `jobs` themes have radically different listing UIs (facets specific to real-estate / jobs).
- See [[storefront-themes-catalog]] for the full catalogue.

## Known issues / by-design vs bug

- **By design**: `robots:noindex` hides `/products` from search engines; `?search=...` 301-redirects to `/search?query=...` (legacy theme URLs).
- **By design**: arriving via [[selection]] shows the selection name as the heading, but the URL stays on `/selection/{slug}` — the same template is reused.
- **By design**: filter counts show `0` next to checkboxes when the merchant disabled `show_facet_counts`.
- **By design (verify)**: the `sidebar` collapse-state cookie has a 365-day expiry — switching themes or clearing cookies resets the layout to the theme default.
- See [[storefront-known-issues]] for cross-page bugs.

## Related

- [[storefront-architecture]] — request lifecycle and three-tree AJAX contract.
- [[storefront-themes-catalog]] — per-theme variations of `products/list.tpl`.
- Same template, different filter scope: [[storefront-category]], [[tag]], [[storefront-vendor]], [[selection]], [[storefront-bundles-list]], [[search]].
- [[product-detail]] — clicking a tile navigates here.
- [[storefront-cart]] — `js-add-to-cart` opens the cart drawer.
- [[design-modules]] — filter module, per-page, sort options.
- [[design-theme-editor]] — colours and typography.
- [[products-products]] — admin product list (what populates the storefront).
- [[products-categories]] — category tree; [[products-tags]], [[products-vendors]] — tag and vendor taxonomies.
- [[products-banners-labels]] — promotional labels on product tiles.
- [[storefront-known-issues]] — cross-storefront issue register.

## Open questions

- Exact param names for filter query strings (`?p_<slug>=`, `?v_<slug>=`, etc.) — to confirm against the search engine driver's URL conventions.
- Whether the modern theme stack always uses `/ajax-products/*` + `/filters-ts/*` in parallel, or whether some themes still use the legacy `/ajax/*` single-shot endpoint.
- Whether the `sidebar` cookie scope includes the path — i.e., does opening the sidebar on `/products` persist across to [[storefront-category]] pages too?
