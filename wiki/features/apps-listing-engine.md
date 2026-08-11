---
type: feature
nav_path: "Apps → Listing Engine"
route_name: apps.listing_engine.overview
route_path: /admin/apps/listing_engine
aliases: ["Listing Engine", "Search Engine", "the search index indexer", "CC Listing Engine", "Search index", "no enable disable button", "app has no active toggle"]
tags: [apps, search, infrastructure, the search index, embeddings, indexing]
plan_gates: []
created: 2026-05-22
updated: 2026-08-06
source_count: 5
---
# Listing Engine (search index + embeddings)

## Purpose

**Listing Engine** is the platform's **underlying search infrastructure** — the search index-based indexer + vector embedding service that powers fast storefront search and semantic relevance. It sits BELOW [[apps-advanced-search]] (which is the merchant-facing search UI) — Listing Engine is the engine room.

It maintains TWO storage layers and keeps them in sync:

- **CloudCart database** (the source of truth — fields, relations, prices).
- **CC Search Engine** (the search index + vector store — the indexed copy used for queries).

Only **three** entity types are indexed: **variants**, **categories**, and **vendors**. Products are searched through their variants (the leaf-level entity); tags / properties / blog articles / smart collections are NOT separately indexed — they ride on the variant's denormalised data. When the two storage layers diverge, the Statistics page surfaces it with an "Out of sync" badge per entity type.

This page is the **hub** for the Listing Engine cluster. It carries the navigation map; each aspect below carries the detail.

> **No on/off control — this app has no "active / inactive" state.** Once it is installed it simply works; there is no Enable / Disable button and no "Activate application" switch on its screen. So *"the app is disabled"* is never the explanation for it not working — check its own settings, credentials, or plan access instead, and use **Uninstall** if the merchant genuinely wants it off.

## Where to find it

Sidebar → Apps → install → **Listing Engine**. Routes: `/admin/apps/listing_engine` (Overview — `apps.listing_engine.overview`) and `/admin/apps/listing_engine/statistic` (Settings/Statistics — `apps.listing_engine.settings`). The Settings UI is currently statistics-focused.

## What the merchant can do here

- **Read the Statistics dashboard** — per-entity indexed count vs database count + Synced / Out-of-sync badge. See [[apps-listing-engine-statistics]].
- **Trigger a full re-index** — the "Re-index" button rebuilds the index (storefront goes into maintenance mode while it runs). See [[apps-listing-engine-reindex]].
- **Rely on automatic indexing** — every product / category / vendor change re-indexes reactively without merchant action. See [[apps-listing-engine-reindex]].
- **Monitor embedding-token usage** — the metric behind AI Semantic Search. See [[apps-listing-engine-embeddings]].

### What the merchant CANNOT do here

- Pick a different embedding model (platform-managed). See [[apps-listing-engine-embeddings]].
- Manually edit, or search, the index directly (use [[apps-advanced-search]] for search).
- Disable individual entity types from indexing — it is all-or-nothing across the three types. See [[apps-listing-engine-statistics]].

## Settings & fields

| Setting | What it controls | Aspect |
|---|---|---|
| `PRODUCT_LISTING_DRIVER` | `mysql` (default fallback) vs `the search index` (full features). | [[apps-listing-engine-embeddings]] |
| `batch_id` (app setting) | The active re-index batch; one at a time. | [[apps-listing-engine-reindex]] |
| Embedding model env keys | Platform-level embedding backend selection (e5-small / OpenAI). | [[apps-listing-engine-embeddings]] |

The detailed field-by-field breakdown lives in each aspect page.

## Business rules

- **Index vs query split** — Listing Engine indexes; [[apps-advanced-search]] queries. Both must be installed and synced for storefront search to work.
- **Per-site scoping** — every the search index count / query filters by `site_id`, so multi-store merchants get isolated indexes per site. See [[apps-listing-engine-statistics]].
- **Re-index = maintenance mode** — a full re-index takes the storefront offline for the duration. See [[apps-listing-engine-reindex]].
- **AI Semantic Search depends on embeddings + the AI search driver** — the standard search driver does lexical (keyword) filtering only. See [[apps-listing-engine-embeddings]].
- **Permission** — standard apps permission scope. `supportUninstall` / `supportChangeStatus` control whether the merchant can uninstall / pause the engine (verify return values).

## Sub-pages (in this cluster)

- [[apps-listing-engine-statistics]] — the Statistics dashboard: indexed-vs-database counts, the Synced / Out-of-sync badge, the three indexed entity types, per-site scoping, all-or-nothing indexing scope.
- [[apps-listing-engine-reindex]] — the Re-index button, maintenance mode during a full re-index, batch lifecycle (cancel-previous-on-retry), reactive event-driven indexing, the two built-in nightly jobs, patch-job pausing, completion notification.
- [[apps-listing-engine-embeddings]] — the vector embedding service (e5-small / OpenAI), embedding-token usage tracking, the `advanced_search_ai_semantic_search` plan gate, the `mysql` vs `the search index` driver, and which metrics are NOT surfaced to the merchant.

## Related

- [[apps]] — App Store hub.
- [[product-visibility]] — this index drives storefront listing visibility; the index-sync delay is why a just-saved change may not appear instantly.
- [[storefront-architecture]] — the search index read-side that serves listings + search from this index.
- [[apps-advanced-search]] — search UI that consumes Listing Engine's index.
- [[apps-algolia]] — alternative search stack that replaces the built-in engine.
- [[apps-cloudio-overview]] — Cloudio AI may use the same embedding infrastructure for some skills.
- [[products-products]] / [[products-categories]] / [[products-vendors]] / [[products-property]] / [[products-variants-options]] — indexed (or variant-denormalised) entities.
- [[plan]] — plan tiers may gate embedding token quotas / semantic search.

## Open questions

(None currently outstanding for this page.)
