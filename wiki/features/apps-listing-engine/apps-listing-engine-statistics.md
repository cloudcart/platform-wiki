---
type: feature
nav_path: "Apps → Listing Engine → Statistics"
route_name: apps.listing_engine.settings
route_path: /admin/apps/listing_engine/statistic
aliases: ["Listing Engine Statistics", "Search index statistics", "Out of sync badge", "Indexed count", "Sync status", "Listing Engine sync"]
tags: [apps, search, infrastructure, the search index, indexing, statistics]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-listing-engine]]. See the hub for the other aspects (re-indexing, embeddings).

# Listing Engine — Statistics dashboard

## Purpose

The Statistics dashboard is the primary view of the Listing Engine app. It tells the merchant, per indexable entity type, how many records sit in the CloudCart database versus how many sit in the CC Search Engine (the search index) index — and whether the two agree. It is the one place a merchant looks to answer "is my storefront search showing current data?"

## Where to find it

Sidebar → Apps → **Listing Engine** → Settings/Statistics (`/admin/apps/listing_engine/statistic`, route `apps.listing_engine.settings`). The Settings UI is currently statistics-focused — there are no configurable knobs here, only read-out cards.

## What the merchant can do here

- **Read the indexed-vs-database counts** per entity type.
- **See the sync status badge** (Synced / Out of sync) per entity type.
- **Decide whether a re-index is needed** — the dashboard is the signal; the action lives on [[apps-listing-engine-reindex]].

### What the merchant CANNOT do here

- Disable indexing for a single entity type (e.g., keep variants but drop vendors) — indexing is all-or-nothing across the three types.
- See the search index operator metrics (query latency, cache hit rate, shard health) — those are platform-operator metrics, not surfaced here. See [[apps-listing-engine-embeddings]] for the boundary of what the merchant can observe.

## Settings & fields

### Statistic cards

Each indexed entity type displays a card with:

- **Indexed count** — number of records in the CC Search Engine index. Display format: *"CC Search Engine: {count}"*.
- **Database count** — number of records in the CloudCart database. Display format: *"CC db storage: {count}"*.
- **Status badge**:
  - **Synced** (green) — counts match; search engine reflects current DB state.
  - **Out of sync** (orange) — counts diverge; a re-index is needed to bring search results current.

### Indexed entity types — exactly three

The product-listing config registers **three** searchable model types and no others:

- `categories`
- `vendors`
- `variants`

**Products are NOT indexed directly** — they are represented through their variants, the leaf-level entity that is actually searched. Tags, properties, blog articles, and smart collections are NOT separately indexed; they are searched via the variant's denormalised data (tags appear ON variants for filtering). So the dashboard shows counts for variants, categories, and vendors — that is the complete list.

Each searchable type has its **own the search index index** — Categories live in their own index, Vendors in theirs, Variants in theirs. The schema is constructed per type, which is why the dashboard reports one card per type rather than a single aggregate count.

## Business rules

### Out-of-sync detection is informational, not a trigger

The Statistics page constantly compares indexed-count vs database-count per entity. Divergence flips the badge to orange "Out of sync". Common causes:

- Bulk product imports just completed; index lagging.
- Manual DB edits that bypassed the model's indexing hooks.
- A batch job failed partway.
- the search index was down during an update.

Critically, the badge is **informational only**. There is **no automatic full re-index** triggered when divergence is detected. The platform does keep the index current reactively per change (see [[apps-listing-engine-reindex]] for the event-driven jobs), but reconciling a drift shown here requires the merchant to click "Re-index".

### Per-site scoping — isolated indexes for multi-store

Every the search index count and query filters by `site_id`. So **multi-store merchants get isolated indexes per site** — the counts on one site's dashboard reflect only that site's catalogue. For high-traffic stores, each site can even be pointed at its own the search index cluster connection (loaded dynamically per site), useful for sharding load across clusters.

### All-or-nothing indexing scope

All three searchable types are indexed whenever Listing Engine is active. The merchant cannot disable indexing for one type while keeping another on. The dashboard reflects this all-or-nothing scope — the merchant always sees counts for all three types.

## Related

- [[apps-listing-engine]] — hub.
- [[apps-advanced-search]] — the search UI that queries the index these counts describe.
- [[products-variants-options]] / [[products-categories]] / [[products-vendors]] — the entities whose records these counts measure.

## Open questions

(None currently outstanding for this page.)
