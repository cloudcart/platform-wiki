---
type: concept
nav_path: "Concept → Storefront architecture → the search index read-side"
aliases: ["Storefront the search index read-side", "ES read-side", "ProductsSearchEnginesSync", "MakeSearchable", "searchable-import4", "Queue lag storefront", "ListingEngineManager"]
tags: [storefront, the search index, queues, sync, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-24
source_count: 5
---

> Part of [[storefront-architecture]]. See the hub for related aspects (request lifecycle, theme inheritance, JS bundles, Smarty plugins, CSS assets, caching).

# Storefront — the search index read-side

## Definition

The storefront's catalogue surfaces — product cards, category listings, search results, filter sidebars, sort dropdowns, in-stock badges, "X left" counters, vendor / brand pages — **read from the search index (the search index), not from the primary database**. The primary database remains the source of truth for writes; the search index is the denormalised read-side copy that the storefront queries on every page render.

The sync pipeline catches every write that affects the catalogue (admin saves, JSON-API v2 writes, imports, ERP syncs, order events) and propagates the change into the search index. The path depends on the runtime context: **web context** tries a synchronous live-sync first and falls back to a fire-after-response dispatch if the search index is unreachable; **CLI context** always dispatches a queued re-index job onto the `searchable-import4` queue (no synchronous fast-path).

This produces the **single most-misunderstood operational rule on the storefront**: when a merchant says *"I changed X (or ran import / sync / API write) and the storefront didn't update"*, the answer is **usually queue lag on `searchable-import4`**, not a bug in the originating action.

## Scope

Covered:

- Why the storefront reads from the search index instead of the primary database.
- The sync pipeline triggers (the catalogue-sync event).
- The web-vs-CLI context branch.
- The chunked re-index job (chunks of 100).
- The three queues involved (`searchable-import4`, `searchable-import8`, `cc-system7`).
- The "queue lag, not bug" operational rule.

Not covered here:

- Per-feature triggers of the catalogue-sync event (product save, variant edit, stock change) — see [[products-products]] + [[inventory-tracking]].
- Queue-worker provisioning and concurrency — see [[background-queue-inventory]].
- Full background queue catalogue — see [[background-queue-inventory]].

## Contrasts

- **Search-index read-side vs primary-database source of truth** — the primary database is authoritative for writes; the search index is denormalised + queryable in single-digit ms. The storefront does not query the primary database for catalogue surfaces. Admin and JSON-API v2 read the primary database.
- **Web sync path vs CLI sync path** — Web (admin save, JSON-API v2 write, storefront customer action) tries synchronous live-sync first and falls back to a fire-after-response dispatch if the search index is unreachable. CLI (queue worker, scheduled task, command-line run, imports) **always** dispatches a queued re-index job — no synchronous fast-path.
- **`searchable-import4` vs `searchable-import8`** — `import4` is per-write incremental sync (admin saves in CLI context, imports, ERP writes, order events). `import8` is the bulk full re-index (run by support) + nightly repeatables (price refresh, orphan cleanup).
- **Catalogue primary-database query vs search-index query** — a typical category page with attribute filters + price slider + sort by best-selling would require a multi-join query across product, variant, attribute, parameter, vendor, discount, stock, and sort-score tables (tens to hundreds of ms). The search index has all this data denormalised onto each variant document (single-digit ms, scales horizontally).

## Where it applies

Every storefront read of catalogue / product / vendor data:

- Catalogue: [[home]], [[storefront-category]], [[product-detail]], [[products-list]], [[search]], [[tag]], [[storefront-vendor]], [[vendors-list]], [[selection]], [[showcase]], [[storefront-bundles-list]].
- AJAX product listings: `/ajax/<entity>/<slug>`, `/ajax-products/<entity>/<slug>`, `/filters-ts/<entity>/<slug>`, `/ajax/latest-viewed`, `/module/search/autocomplete`.
- Filter sidebars + sort dropdowns + in-stock badges + "X left" counters everywhere they appear.

Writes that fire the catalogue-sync event (non-exhaustive): product save, variant save, stock change, category save, vendor save, discount save, order-driven stock decrement / re-credit, [[apps-csv-import]] / [[apps-xml-import]] / [[apps-xml-sync]], every JSON-API v2 write.

## How it works

### Why the search index instead of the primary database

A typical category page (attribute filters + price slider + sort by best-selling) needs a multi-join query across many tables (tens to hundreds of ms per request); the same query against a search index with that data denormalised onto each variant document returns in single-digit ms and scales horizontally — see the Contrasts above.

### Engine module

The active engine is resolved through a listing-engine driver layer that defaults to the search index (the search index) for all merchants today; the architecture allows additional drivers. The storefront goes through this driver abstraction rather than the search index directly, so a future swap is contained.

### The sync pipeline — keeping the search index in step with the primary database

1. Any code path that changes a product / variant / category / vendor / discount / order quantity / etc. fires a catalogue-sync event.
2. The platform catches the event.
3. It then chooses between two paths based on context:
   - **Web context** (admin save, JSON-API v2 write, storefront customer action): tries a **synchronous live-sync** first. If it succeeds the search-index update is in place before the HTTP response returns. If it errors (search index unreachable, connection timeout, etc.) it falls back to a fire-after-response dispatch — the sync runs after the response is emitted, semi-async.
   - **CLI context** (queue worker, scheduled task, command-line run, ALL import paths): **always dispatches** a re-index job onto the `searchable-import4` queue (or `searchable-import8` for nightly repeatables). No synchronous fast-path in this context.
4. The re-index job processes documents in **chunks of 100** and writes them into the search index for the affected site.
5. Subsequent storefront reads hit the updated search index and the change becomes customer-visible.

### Queues involved

| Queue | Purpose |
|---|---|
| `searchable-import4` | Per-write incremental sync (admin saves in CLI context, imports, syncs, ERP writes, order events). |
| `searchable-import8` | Bulk full re-index (run by support) + nightly repeatables (price refresh, orphan cleanup). |
| `cc-system7` | Search-index orphan cleanup (every 24h, removes search-index docs whose primary-database row was deleted). |

### The "queue lag, not bug" operational rule

Per the Definition above, *"I changed X and the storefront didn't update"* is **usually queue lag on `searchable-import4`**, not a bug. Diagnostic path:

1. Confirm the primary-database row IS updated (admin shows it; JSON-API v2 returns it).
2. Check `searchable-import4` queue depth + worker health.
3. If the queue is healthy, check whether the synchronous live-sync errored (web context only) — the failure should have downgraded to the fire-after-response dispatch, which may itself have errored if the request was killed mid-response.
4. Force a re-sync: re-save the affected row (web context) or ask support to run a bulk re-index for the affected ID.

See [[background-queue-inventory]] for the operational catalogue + [[apps-csv-import]] / [[apps-xml-import]] / [[apps-xml-sync]] for the import-specific behaviour.

### Product pages self-heal a missing search-index document

A product row can stay valid and orderable in the primary database while its **search-index document goes missing** — a dropped or failed indexing job, a partial bulk-index failure, or a miss during a re-index. The catalogue surfaces (listings, search) read from the index, so such a product silently drops out of them; worse, a direct hit on its **product page** used to answer **404** for a product that is active and orderable. (Merchants learned to "fix" it by re-saving the product — which only worked because the save triggers a re-index.)

The product page now **recovers automatically**: when the index lookup for the requested product URL returns nothing, the platform falls back to resolving the product **straight from the database**. If that product is renderable, the page renders normally instead of 404-ing, the database↔index desync is **logged** for monitoring, and a **re-index is queued** so the document self-heals and the product reappears in listings and search too. So a one-off indexing miss no longer takes a live product offline — the only residual lag is the brief window before the queued re-index repopulates the catalogue surfaces.

## Related

- [[storefront-architecture]] — hub.
- [[storefront-arch-request-lifecycle]] — where search-index reads happen in the page-dispatch step.
- [[background-queue-inventory]] — the `searchable-import4` / `searchable-import8` / `cc-system7` queue catalogue.
- [[products-products]] — product editor; every save fires the sync.
- [[inventory-tracking]] — stock changes fire the sync (most operationally relevant case).
- [[apps-csv-import]] / [[apps-xml-import]] / [[apps-xml-sync]] — bulk import paths (all CLI context → always queued).
- [[json-api-v2]] — admin writes that trigger the sync.
- [[order-processing-pipeline]] — order events that cause re-index of affected products.

## Open Questions

- **Failure mode when the fire-after-response dispatch itself errors** — does the platform retry, log, or silently drop? (verify.)
- **Per-merchant search index vs shared index with site filter** — the pipeline writes "for the affected site" but whether this is per-site indices or a single multi-tenant index with a site filter is not documented (verify).
