---
type: storefront-page
route_name: products.search
route_path: /search
themes_using: [liquid]
tags: [storefront, search, predictive, instant, autocomplete, liquid, search-engine]
created: 2026-06-11
updated: 2026-06-11
source_count: 1
---

# Storefront — New search (predictive, `/search`)

## Purpose

The **new storefront search** — the search experience rendered by CloudCart's **new (Liquid) storefront engine**. As the customer types, a **predictive search-as-you-type** dropdown shows matching products and suggested terms; on submit, a results page renders with **live faceted filters** powered by the indexed search engine. This is the modern replacement for the legacy Smarty results page documented at [[search]]; both answer the same `/search` URL — which one renders depends on the store's storefront engine.

## URL & route

- **Route name**: `products.search` — **Route path**: `/search` (same route as the legacy [[search]]).
- The search controller dispatches by storefront engine: the **new (Liquid)** engine renders this predictive search; a store still on the **legacy (Smarty)** engine renders [[search]] (the `products/list.tpl` results page) instead.
- Query params: `?query=...` (preferred) or `?q=...` (legacy alias) — trimmed and truncated to 200 characters.
- Supporting AJAX endpoints:
  - **Predictive / autocomplete** — `site.search.autocomplete` (and an inline section load via `section_id`) feeds the as-you-type dropdown.
  - **Faceted filters** — `ajax.filters-ts.search` returns the filter facets + matching products from the indexed search engine as the customer refines.

## How it loads

The page renders through the new engine's `templates/search` Liquid template (or a merchant-chosen layout — see Customisations). The predictive dropdown is served as an autocomplete **section**, so it updates without a full page load.

## What the customer sees

- **Search box** — typing opens a **predictive dropdown** (search-as-you-type): up to **15 matching products** (image, name, price) plus **suggested search terms**. The dropdown matches the **product name with typo tolerance**, so a small misspelling still finds the product.
- **Results page** — on submit, the matched products with **filters / facets** (category, vendor / brand, price, product attributes) the customer can toggle to narrow results live.

## How it searches & what it finds

The new search runs on the **indexed search engine** (see [[storefront-arch-search-read-side]]), not a raw database `LIKE`. That widens what it can find and how it ranks:

- **Which fields it matches.** A query is matched against the product's **name, short & long description, SKU, barcode, tags, vendor / brand, the category name(s) and full category path, the variant parameters** (e.g. *"Color: Red"*) and **category properties / specs** (e.g. *"Material: Cotton"*). So *"red cotton shirt"* can match a product named just "Shirt" that has a Red colour option and a Cotton material spec; a **SKU or barcode** lands the exact product; a **brand or category name** surfaces its products.
- **Typo tolerance.** Matching is fuzzy — a small misspelling still matches (most visibly in the predictive dropdown).
- **Meaning-based matching.** Beyond exact keywords, the engine also ranks **semantically related** products (meaning-based, not just literal words), so close synonyms / related wording can still surface relevant items.
- **Relevance ranking.** Results are ordered by **relevance to the query first**; sellable items are favoured and (when the store hides out-of-stock) out-of-stock items are pushed to the end. Variants of the same product are **grouped** into one result. For search, the store's usual "featured / on-sale first" ordering is intentionally **not** applied — relevance wins so the best match is on top.
- **Synonyms / boosts.** Merchant-defined synonyms and term boosts come from [[apps-advanced-search]].

## Storefront behaviour

- **What can appear at all.** A product shows in results only if it is **active, published (not draft), inside its publishing window, not hidden, and available in the customer's geo-zone**; when the store hides out-of-stock products, only **sellable** ones appear (otherwise out-of-stock items appear, pushed to the end). So a product missing from search is usually hidden / draft / out-of-window / out-of-zone / out-of-stock — not a search bug.
- **Stays in sync.** The index is kept current as the catalogue changes (price, stock, name, category) — see [[apps-listing-engine]]; a just-edited product may take until the next index sync to reflect.
- Every search **logs analytics** (the query string + total hits), surfaced under [[apps-advanced-search]] / the search dashboards.
- **Crawlers are blocked**: a bot request to `/search` returns **403 + `X-Robots-Tag: noindex`** — search-result pages are deliberately not indexed.

## JavaScript behaviour

- The search box fires the predictive/autocomplete request as the customer types and renders the dropdown section.
- Selecting a filter fires the faceted-search request (`ajax.filters-ts.search`) and refreshes the results + facet counts in place.

## Customisations available to the merchant

- **`searchLayout`** setting — choose a custom search template/layout for the results page (when set, the engine renders `templates/<searchLayout>` ahead of the default `templates/search`).
- Theme controls the dropdown and results-page layout.

## Theme variations

Available only on the **new (Liquid) storefront engine**. Stores on the legacy Smarty engine use [[search]].

## Known issues / by-design vs bug

- **noindex on `/search`** — by design (search pages must not be indexed).
- **Predictive dropdown capped at 15 products** — by design.
- Exact facet set offered on the results page — (verify against a live new-engine theme).

## Related

- [[search]] — the legacy (Smarty) search-results page for the same `/search` URL.
- [[storefront-architecture]] — the storefront rendering engines (Smarty vs the new engine).
- [[storefront-arch-search-read-side]] — the indexed search engine behind results + facets.
- [[apps-listing-engine]] — keeps the search index in sync with the catalogue.
- [[apps-advanced-search]] — search analytics + search-engine settings.
- [[products-list]] — the standard catalogue listing the results resemble.

## Open questions

- Whether the predictive dropdown also surfaces categories / vendors / pages (not just products) (verify).
- The default `searchLayout` and the full facet list on the new-engine results page (verify against a live theme).
