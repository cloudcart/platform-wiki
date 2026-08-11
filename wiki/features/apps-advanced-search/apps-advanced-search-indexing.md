---
type: feature
nav_path: "Apps → Advanced Search → Indexing"
route_name: apps.advanced_search.overview
route_path: /admin/apps/advanced_search
aliases: ["Advanced Search indexing", "Re-index", "Search maintenance mode", "Engine selection", "Search result freshness", "Multi-language search index"]
tags: [apps, others, search, indexing]
plan_gates: ["advanced_search"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-advanced-search]]. See the hub for the other aspects (settings, analytics, usage, orders, support).

# Advanced Search — Indexing & engine

## Purpose

This aspect covers what happens beneath the search box: which engine actually serves queries, how the index is built and rebuilt, what the merchant sees during a re-index, how quickly catalogue changes appear in results, and how multi-language stores are handled. It is the operational side the merchant needs to understand before triggering a re-index on a live store.

## Where to find it

The re-index control sits on the Advanced Search app (`apps.advanced_search.overview`); the engine choice (`searchBarEngine`) is on the Settings tab — see [[apps-advanced-search-settings]]. The index itself is owned by [[apps-listing-engine]].

## What the merchant can do here

- **Trigger a full re-index** — rebuild the entire index. This puts the storefront into maintenance mode while it runs (see Business rules).
- **Choose the engine** (via Settings `searchBarEngine`) — built-in [[apps-listing-engine]] or [[apps-algolia]].
- **Rely on automatic re-indexing** — product / category / vendor / variant changes re-index reactively; the merchant doesn't normally trigger anything.

### What the merchant CANNOT do here

- Run two indexings in parallel — a new re-index cancels the running batch first (see Business rules).
- Pin a product to the top of a query — ranking is weight + boost + semantic score only (see [[apps-advanced-search-settings]]).

## Settings & fields

| Field | Notes |
|-------|-------|
| `searchBarEngine` | `cloudcart` (built-in) or `algolia`. Selects which engine serves queries. |
| `batch_id` (app setting) | The active re-index batch; one at a time. |

## Business rules

### Engine selection logic (built-in vs Algolia)

```
IF Algolia ([[apps-algolia]]) is NOT installed OR NOT active:
  → Use the CloudCart engine (gated by isSearchEngine availability + Advanced Search isActive).
ELSE:
  → Use the engine specified by setting 'searchBarEngine':
     - 'cloudcart' → built-in [[apps-listing-engine]].
     - 'algolia' → [[apps-algolia]].
```

So the SAME `searchBarEngine` setting toggles built-in vs Algolia. Without Algolia installed, the setting is irrelevant — built-in is forced.

**Install order matters.** On install, the platform checks whether Algolia is installed + active; if yes, it sets `searchBarEngine = 'algolia'` immediately, overriding the `'cloudcart'` default. Install Algolia first → install Advanced Search → engine is Algolia. Install Advanced Search first → engine stays `cloudcart`.

### Full re-index puts the storefront into MAINTENANCE MODE

When the merchant clicks **Re-index** (or the platform triggers it), the underlying [[apps-listing-engine]] full-upload job sets `maintenance = 1` on the site with a reason describing the index operation. **The storefront shows a maintenance page until the batch completes.** On completion (or error) the platform automatically lifts maintenance mode and surfaces a success notification. This is critical to know before re-indexing a live store — large catalogues may be in maintenance for an extended period.

### One batch at a time

The active batch ID is stored on the app settings (`batch_id`). Clicking "Re-index" while a previous batch is still running **cancels the previous batch first**, then queues the new one. Two indexings cannot run in parallel.

### Result freshness — near-instant via reactive jobs

Product changes (and sibling events for categories, vendors, variants, etc.) dispatch indexing jobs on a background queue. Once the worker processes the job (typically seconds), the product appears in / disappears from search results. There is **no nightly-only batch** — re-indexing happens reactively per change. Bulk imports may temporarily lag while the queue catches up.

### Multi-language — per-language index with language-aware analyzers

Each language gets its own analyzer with the right stemmer + stopword filter (Bulgarian, English, German, French, Polish via the stempel plugin, etc.; Macedonian / Bosnian / Croatian fall back to the closest related language). When the store runs multiple languages, each storefront language uses its own analyzers, and re-indexing builds the correct mappings. Custom stopwords saved on the Stopwords tab are stored in site settings (`search_stopwords`) and applied across the site's indexes — see [[apps-advanced-search-settings]].

## Related

- [[apps-advanced-search]] — hub.
- [[apps-listing-engine]] — the index + embedding service that does the indexing.
- [[apps-algolia]] — alternative engine selected via `searchBarEngine`.

## Open questions

(None currently outstanding for this page.)
