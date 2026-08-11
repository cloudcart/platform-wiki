---
type: storefront-page
route_name: products.search
route_path: /search
themes_using: [all]
tags: [storefront, search, results, listing, autosuggest]
created: 2026-06-08
updated: 2026-06-08
source_count: 3
---

# Storefront — Search results (`/search`)

## Purpose

The search page renders **catalogue search results** for the query a customer typed (or that the storefront search bar / autosuggest box redirected them to). It funnels through the SAME `products/list.tpl` template as [[products-list]] — the search controller just seeds a different listing scope (`'search'` with the query string as the where-clause).

Search results also feed the platform's **search analytics** — every search performed on `/search` logs the query string and the total-hits count via `logSearchAnalytics` in the abstract listing pipeline, which surfaces under [[apps-advanced-search]] / search-engine dashboards.

## URL & route

- **Route name**: `products.search`
- **Route path**: `/search`
- **Controller**: the search controller, the request handler
- **Middleware**: `uuid_generate`, `subscriber_uuid`, `TSStatistic:search`. The controller adds an inline middleware that aborts with **403 + `X-Robots-Tag: noindex`** when the request is detected as a crawler (`isCrawlerRequest`) — search-result pages must not be indexed.

Query-string params:

- `?query=...` (preferred) or `?q=...` (legacy alias). Both are normalised — trimmed and truncated to 200 characters.
- All filter / sort / pagination params from [[products-list]] apply (`?page=`, `?sort=`, facet params, etc.).

**Scanner hardening**: the controller scalar-guards `?query[$eq]=...` style scanner injection. PHP would otherwise parse those into nested arrays and the bare cast triggered an "Array to string conversion" warning that surfaced ~62 hits / 24h in the exception log. If `query` is not a string, the search term falls back to empty.

## How it loads

1. The controller reads `?query` (or `?q`), trims it, and truncates to 200 chars.
2. Calls the platform code to emit the search SEO meta.
3. Calls `$this->loadProducts('search', ['search' => $searchQuery])` — the abstract listing pipeline runs the active search-engine driver with the query as the where-clause.
4. If the query is non-empty, calls `logSearchAnalytics($query, $products->total)` — records the query + hit count for analytics.
5. Returns the platform code — the same template as [[products-list]].

## What the customer sees

The visible structure is identical to [[products-list]]:

- **Breadcrumb** — "Home → Search" (verify exact translation).
- **Page heading** — typically shows the query string and result count (depends on the products-or-bundles-title module setting).
- **Sort dropdown** — **hidden on `/search`** — the template explicitly conditions on `!activeRoute('products.search')` when deciding whether to show the sort dropdown. Search results are sorted by relevance and the merchant cannot reorder them.
- **Per-page dropdown** — shown.
- **Filter sidebar** — shown, scoped to facets present in the matching products.
- **Product grid** — paginated results.
- **"No results" state** — when the query returns 0 products, the product-list module renders an empty-state message (translation strings under `sf.products.no_results.*`) (verify).

## Storefront behaviour

- Same AJAX behaviour as [[products-list]] — filter / per-page / pagination changes swap content via AJAX.
- Sort changes are NOT available on this page (no dropdown rendered) — relevance order is fixed.
- The search bar in the header (which appears on every page) is a separate module — see [[design-modules]] → Search module. Typing into it typically opens an **autosuggest** dropdown that calls `/ajax/search` (route `ajax.search`) for live suggestions and links each result either to the product detail page or to `/search?query=...` for the "see all results" link (verify per theme).

## JavaScript behaviour

- Same hook set as [[products-list]] — `.js-sidebar`, `.js-product-list`, `.js-products-container`, `.js-products-pagination`, etc.
- The search autosuggest dropdown (in the header search module) is theme-specific — `flair` typically uses `.js-search-input` + `.js-search-results` (verify the exact hooks per theme).
- AJAX endpoints called from this page (one of the three trees):
  - `/ajax/search` — route `ajax.search` (full HTML).
  - `/ajax-products/search` — route `ajax.products.search` (products only).
  - `/filters-ts/search` — route `ajax.filters-ts.search` (filters only).
- The autosuggest dropdown in the header calls `/ajax/search` directly for live suggestions (verify).

## Customisations available to the merchant

| Aspect | Where to configure |
|--------|--------------------|
| Search bar visibility / placement / placeholder text | [[design-modules]] → Search module |
| Whether autosuggest is enabled and how many suggestions to show | [[design-modules]] → Search module settings |
| Which filters appear in the result sidebar | [[design-modules]] → Products filters module |
| Per-page choices on results | [[design-modules]] → Products filters module |
| Whether facet counts show next to filters | [[design-modules]] → `show_facet_counts` |
| Sort order on results | Not configurable — fixed to relevance |
| Search-engine choice (the search engine vs. fallback) | Platform-managed; merchants can opt in to [[apps-advanced-search]] |
| Synonyms, stop-words, boost rules | [[apps-advanced-search]] (advanced search app) |
| SEO meta on `/search` | Translation strings — `/search` is `noindex` for crawlers anyway |

## Theme variations

- All themes render `products.list` for this route — the structure is consistent.
- The search bar that lives in the header is module-driven per theme — every theme that exposes a header search module feeds `/search` (or `/ajax/search` for autosuggest) on submit.
- Themes that ship a richer "No results" landing block (suggested categories, popular searches, etc.) override the theme templates to render those extras when `$products->isEmpty`.
- See [[storefront-themes-catalog]].

## Known issues / by-design vs bug

- **By design**: crawlers (e.g., Googlebot) get 403 + `X-Robots-Tag: noindex` instead of the search page — search-result pages are intentionally excluded from indexing.
- **By design**: sort dropdown is hidden on `/search` — results are ranked by relevance and the merchant cannot override.
- **By design**: query strings are truncated to 200 characters server-side — longer queries are silently shortened.
- **Hardened bug fix**: scanner injection (`?query[$eq]=foo`) used to throw "Array to string conversion" — the controller now scalar-guards and falls back to empty string. The log spike (~62 hits / 24h) prompted this guard.
- **By design**: the `?search=...` legacy param on `/products` 301-redirects to `/search?query=...` (handled by [[products-list]]'s controller).
- **By design**: empty query (`/search` with no `?query=`) renders the page with zero results — does not 404 or redirect.
- See [[storefront-known-issues]] for cross-page bugs.

## Related

- [[storefront-search-new]] — the **new (Liquid-engine) predictive search** for the same `/search` URL; this page is the legacy Smarty path.
- [[storefront-architecture]] — request lifecycle.
- [[storefront-themes-catalog]] — per-theme search bar / autosuggest variations.
- [[products-list]] — same template, full catalogue.
- [[storefront-category]] — same template, category scope.
- [[product-detail]] — destination of result click.
- [[design-modules]] — search module + filter module configuration.
- [[apps-advanced-search]] — advanced search app (synonyms, boosts).
- [[storefront-known-issues]] — cross-storefront issue register.

## Open questions

- Exact behaviour of the autosuggest dropdown across themes — does every theme bundle it, or do lightweight themes ship a "submit to /search on Enter" only?
- Are there theme-specific "popular searches" or "recent searches" modules shown on the empty-state, and where is that data sourced from?
- How does the search-engine driver handle multi-language stores — is the query routed to a per-language the search engine index, or a single multi-language index?
