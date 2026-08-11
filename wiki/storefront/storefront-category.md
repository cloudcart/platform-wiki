---
type: storefront-page
route_name: category.view
route_path: /category/{slug}
themes_using: [all]
tags: [storefront, category, listing, filters, seo]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Storefront — Category landing (`/category/{slug}`)

## Purpose

The category page is the **single-category landing surface** — the SEO-canonical place where a customer reaches a curated subset of the catalogue. It carries the category's own title, optional description, optional image, optional sub-category tile strip, and a full filtered listing of every product assigned to the category (including products inherited from descendant categories, via the `child_by_path` relation).

The category page is the primary catalogue-browsing entry point: the storefront's navigation menus link here, and search engines index these pages (unlike [[products-list]] which is `noindex`). Every category created via [[products-categories]] gets its own URL of the form `/category/<url_handle>`.

## URL & route

- **Route name**: `category.view`
- **Route path**: `/category/{slug}` (the legacy alternative the platform code is commented out in the platform code)
- **Controller**: the category controller, the request handler
- **Middleware**: `uuid_generate`, `subscriber_uuid`, `TSStatistic:category`

If the URL slug does not exactly match the category's current `url_handle` (e.g., the merchant renamed the category and an old slug variant is hit), the controller 301-redirects to the canonical URL.

If the slug resolves to no active category, the controller throws a 404 with the translated message `sf.global.err.category_no_longer_exists`.

## How it loads

1. The controller resolves the slug via the category model's filter scope (the platform code) — returns the active, visible, non-archived category whose `url_handle` matches.
2. Sets the filter module's "current category" so downstream filter rendering knows which category to scope to.
3. Calls `$this->loadProducts('category', ['category_ids' => $category->child_by_path->pluck('category_id')->all])` — the abstract listing pipeline (see [[products-list]]) paginates the catalogue scoped to this category and every descendant category.
4. Returns the platform code — the SAME Smarty template as `/products` itself.

## What the customer sees

- **Breadcrumb** — full category path (e.g., "Home → Electronics → TVs → 4K TVs") rendered from the platform code. Includes microdata (`microdata/breadcrumb.tpl`) for SEO.
- **Category header block** — `<h1>` with the category name, and (only on page 1):
  - Category image (if uploaded), 600x600 srcset, with lazy-load.
  - Category description (HTML, `nofilter` so the merchant's WYSIWYG output renders raw).
- **Sub-category tiles strip** — if the category has children, each child renders as a tile (`_showcase-item one-third`) with image + name + "View more" button. This strip is unique to category pages (other listing surfaces don't have it).
- **Sidebar toggle** + **Sort dropdown** + **Per-page dropdown** — identical to [[products-list]].
- **Filter sidebar** (`products/list-sidebar.tpl`) — same as [[products-list]], but the categories filter renders the active category's descendants (the customer can drill down further), and the variants / properties shown reflect the attributes used by products in this category.
- **Product grid** — same the theme templates as [[products-list]].
- **Pagination** — same the theme templates.

## Storefront behaviour

- Same AJAX behaviour as [[products-list]] — filter toggles, sort changes, per-page changes, and pagination all swap the product grid via AJAX without a full page reload.
- The category header (image + description) only renders on page 1 (the platform code) — paginated pages 2+ hide it to keep the URL-canonical version slim.
- Sub-category tile strip is always shown (whenever the category has children) regardless of pagination page — verify.

## JavaScript behaviour

- Same hook set as [[products-list]] — see that page's "JavaScript behaviour" table for the canonical list.
- AJAX endpoints called on this page (one of the three trees — depending on theme):
  - `/ajax/category/{slug}` — route `ajax.category` (full HTML).
  - `/ajax-products/category/{slug}` — route `ajax.products.category` (products only).
  - `/filters-ts/category/{slug}` — route `ajax.filters-ts.category` (filters only).
- The `cc.filters.filters.after` custom event fires on the document after every filter swap — used by `flair` to re-apply per-property collapse state.

## Customisations available to the merchant

| Aspect | Where to configure |
|--------|--------------------|
| Category name, description, image, parent, SEO meta | [[products-categories]] → category edit |
| Whether the category is published / hidden | [[products-categories]] → status |
| URL handle (slug) | [[products-categories]] (changing it triggers a 301 from old slugs — see [[marketing-seo-301-redirects]]) |
| Which filters appear in the sidebar | [[design-modules]] → Products filters module |
| Per-page choices, sort options | [[design-modules]] → Products filters module |
| Sub-category display style | The base theme uses `_showcase-item one-third` — theme-specific override required to change |
| Category meta-title / meta-description / canonical | [[marketing-seo-meta]] for global rules + per-category SEO in [[products-categories]] |
| Custom HTML / WYSIWYG content above the product grid | Category `description` field (rendered `nofilter`) — supports arbitrary HTML |
| Hide category from menu but keep accessible | [[design-navigation]] (separate from category publish status) |

## Theme variations

- All themes render `products.list` for this route, so the page structure is consistent. Theme overrides change cosmetics (breadcrumb position, sub-category tile aspect ratio, image lazy-load library).
- The `wonderland`, `properties`, `jobs` themes have radically different "category" surfaces — e.g., `properties` shows a search-by-location form first.
- Themes that disable the sub-category tile strip do so by editing their own `products/list.tpl` — there is no admin toggle.
- See [[storefront-themes-catalog]].

## Known issues / by-design vs bug

- **By design**: the category page reuses `products/list.tpl` — every cosmetic tweak made for [[products-list]] applies here too.
- **By design**: the descendants are computed via `child_by_path` (the materialised path of category nesting), so products in deeply-nested sub-categories appear in the parent's listing automatically.
- **By design**: page 1 shows the header (image + description), pages 2+ hide it. SEO scrapers landing on `?page=2` will not see the description.
- **By design**: a slug mismatch (`/category/old-slug` when current is `/category/new-slug`) 301-redirects to the current canonical — protects SEO when categories are renamed.
- **By design**: hitting a deleted / archived category returns a 404 with the translated message *"This category no longer exists."*.
- See [[storefront-known-issues]] for cross-page bugs.

## Related

- [[storefront-architecture]] — request lifecycle.
- [[storefront-themes-catalog]] — per-theme variations.
- [[products-list]] — same template, no category scope.
- [[categories-list]] — index of all categories.
- [[product-detail]] — clicking a tile navigates here.
- [[storefront-cart]] — `js-add-to-cart` on tiles.
- [[products-categories]] — admin screen for category tree, descriptions, images, SEO.
- [[design-modules]] — filter module configuration.
- [[design-navigation]] — controls whether the category appears in the storefront menu.
- [[marketing-seo-meta]] — meta-title / meta-description.
- [[marketing-seo-301-redirects]] — old-slug redirects.
- [[storefront-category]] — entity definition.
- [[storefront-known-issues]] — cross-storefront issue register.

## Open questions

- Does the sub-category tile strip render on pages 2+ as well, or is it hidden there to match the header? (`category_childs` is loaded unconditionally in the template — verify the per-page logic.)
- How are out-of-stock products in a category sorted by default — pushed to the end or interleaved? (depends on the active sort + listing-driver settings.)
- Which JSON-LD microdata does the category page emit besides breadcrumbs? (`microdata/breadcrumb.tpl` is included; product-list microdata may be too.)
