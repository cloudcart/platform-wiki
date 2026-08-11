---
type: storefront-page
route_name: category.list
route_path: /categories
themes_using: [all]
tags: [storefront, categories, navigation, index]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Storefront — Categories index (`/categories`)

## Purpose

The categories index is the **directory page** for the whole category tree — a grid of every top-level category, each tile showing the category image, name, and (in the standard layout) a list of its first-level children. It's a hub the customer can reach from the storefront footer or a navigation link, useful for stores with many categories where the menu alone doesn't expose the full tree.

Unlike [[storefront-category]], this page does not list any products — only category tiles. Clicking a tile (or a child link inside a tile) navigates to the corresponding `/category/{slug}`.

## URL & route

- **Route name**: `category.list`
- **Route path**: `/categories`
- **Controller**: the category controller, the request handler
- **Middleware**: `uuid_generate`, `subscriber_uuid`, `TSStatistic:categories`

There is no slug, no pagination, no filters — this is a flat directory.

## How it loads

1. The category controller calls `getListingDriver->getAllCategories` — fetches every active, visible category in one go.
2. Filters to the top-level categories (`parent_id == null`) and sorts each by the merchant's `order` field, ascending.
3. For each top-level category, attaches its children (also sorted by `order`).
4. Calls the platform code to emit SEO meta — uses the category-list specific translation strings.
5. Returns the platform code — the `global::` prefix forces the platform-shared the theme templates to render rather than a per-theme override (verify — `mainResponse` typically resolves via theme inheritance; the `global::` namespace bypasses the theme).

## What the customer sees

- **Section title** — `<h1 class="_h2">` with the translated label `sf.products.filter.categories`.
- **Masonry grid** — `<div class="_products-list _products-list-masonry">` — each top-level category renders as a one-fourth tile:
  - **Category image** — `getImage('300x300')`, lazy-loaded with `aspect-ratio` style when the category record has one.
  - **Category name** — `<h3>` linking to `/category/{slug}`.
  - **Child list** — bulleted list of first-level children (each linking to its own `/category/{slug}`). Border removed below the name when the category has no children (`style="border-bottom: none;"` inline rule).
- The page does NOT show product counts, descriptions, sub-children-of-children, or any filters.

A trailing `<script>` block calls `$('._products-list-masonry').masonry` if jQuery Masonry is loaded — produces the brick-style packed layout. Otherwise the tiles fall back to a normal flex / float grid (verify per theme).

## Storefront behaviour

- Pure server-rendered HTML — no AJAX, no filters, no pagination.
- Masonry layout (when the plugin is present) recalculates on resize.
- Clicking any tile or child link navigates via plain `<a href>` to the category page — no JS interception.

## JavaScript behaviour

- The page emits one inline `<script>` block wrapped in `CCEvents.ready` — invokes jQuery Masonry on `._products-list-masonry`.
- No `.js-*` hooks live on this page; there is no AJAX traffic.

## Customisations available to the merchant

| Aspect | Where to configure |
|--------|--------------------|
| Which categories appear (publish / hide each) | [[products-categories]] |
| Category order on the index | [[products-categories]] — the `order` field on each category |
| Category image, name, slug | [[products-categories]] |
| Whether a link to `/categories` appears in the storefront menu / footer | [[design-navigation]] |
| SEO meta for `/categories` | translation strings (`pages.categories`, etc.) — global, not per-merchant |
| Tile image aspect ratio | The category's own image — `aspect_ratio` attribute (verify) |
| Number of tiles per row, masonry on/off, theme variables (colours) | [[design-theme-editor]] / per-theme `_products-list-masonry` rule |

## Theme variations

- The shared the theme templates is the default — themes that have not overridden it (most child themes) render this exact layout.
- The base `flair` theme does **not** ship its own `templates/product/categories.tpl` — it inherits the global fallback. Verify per theme: some themes (e.g., `wonderland`, `properties`) override with a more visual hero treatment.
- See [[storefront-architecture]] for the theme-inheritance rule and [[storefront-themes-catalog]] for per-theme overrides.

## Known issues / by-design vs bug

- **By design**: only top-level categories are tiles — children render as a bullet list inside the parent tile, grandchildren do not appear. Stores with very deep trees should rely on the storefront menu ([[design-navigation]]) for full drill-down.
- **By design**: there is no product count per category on this index — the merchant cannot toggle counts on.
- **By design**: the page is fully server-rendered with no filters or AJAX — a request to `/categories?something=...` is identical to `/categories`.
- **By design**: the Liquid-engine path (Nitrogen-style themes, see [[headless-storefront]]) renders `templates/list-collections` instead; that is not the Smarty path described here.
- See [[storefront-known-issues]] for cross-page bugs.

## Related

- [[storefront-architecture]] — request lifecycle, theme inheritance for `global::`-prefixed views.
- [[storefront-themes-catalog]] — themes that override the categories index.
- [[storefront-category]] — the destination of every tile click.
- [[products-list]] — the flat catalogue listing (different surface).
- [[products-categories]] — admin screen for the category tree.
- [[design-navigation]] — surface that exposes `/categories` to customers.
- [[design-theme-editor]] — visual customisation of tiles.
- [[storefront-category]] — entity definition.
- [[storefront-known-issues]] — cross-storefront issue register.

## Open questions

- Whether the masonry plugin is shipped by every theme — some lightweight themes may not bundle it, in which case the grid falls back to a default float layout.
- Whether the platform code view path bypasses theme overrides entirely (the `global::` namespace is intentional — verify against [[storefront-architecture]]).
- How categories without an image render — does the template fall back to a no-image placeholder, or does the tile lose its image area?
