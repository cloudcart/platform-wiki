---
type: feature
nav_path: "Apps → Listing Engine → Re-index"
route_name: apps.listing_engine.overview
route_path: /admin/apps/listing_engine
aliases: ["Listing Engine re-index", "Re-index", "Rebuild search index", "Search maintenance mode", "Reactive indexing", "Nightly price patch", "the search index cleanup"]
tags: [apps, search, infrastructure, the search index, indexing, maintenance]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[apps-listing-engine]]. See the hub for the other aspects (statistics, embeddings).

# Listing Engine — Re-indexing & maintenance

## Purpose

This aspect covers how the index gets built and kept current: the on-demand "Re-index" button, what happens to the storefront during a full re-index, how a re-index batch is managed, the reactive event-driven indexing that keeps the index fresh without merchant action, and the two built-in nightly housekeeping jobs. It is the operational side the merchant must understand before triggering a re-index on a live store.

## Where to find it

Sidebar → Apps → **Listing Engine** → Overview (`/admin/apps/listing_engine`, route `apps.listing_engine.overview`). The Statistics dashboard ([[apps-listing-engine-statistics]]) is the signal that tells the merchant whether a re-index is needed.

## What the merchant can do here

- **Trigger a full re-index** — the "Re-index" button kicks off a batch that wipes and rebuilds the index for all three entity types (variants, categories, vendors).
- **Rely on automatic indexing** — product / category / vendor changes re-index reactively; the merchant does not normally trigger anything.

### What the merchant CANNOT do here

- Schedule additional periodic re-indexes from the admin — beyond the built-in nightly jobs, full re-indexing is on-demand only.
- Run a "background re-index" that keeps the storefront live — a full re-index always puts the storefront into maintenance mode.
- Queue two full re-indexes — clicking Re-index again cancels the in-flight batch and starts a new one.

## Settings & fields

| Field | Notes |
|---|---|
| **Re-index** button | Triggers a full batch re-index (returns the application framework Batch); progress visible via Batch tracking. |
| `batch_id` (app setting) | Persists the active batch ID. Used to cancel a previous run on retry. |

The full upload routes through the `listing_engine_upload_content` queue mapping for the upload job.

## Business rules

### Full re-index puts the storefront into MAINTENANCE MODE

When the merchant clicks **Re-index** (or the full upload job is dispatched any other way), the platform:

1. Sets the site's `maintenance = 1` with a maintenance reason describing the indexing run.
2. Adds upload-content jobs for each searchable type (variants, categories, vendors) to the batch.
3. On batch completion, calls `uploadContentNotify`, which surfaces a success notification AND clears maintenance mode.
4. On batch failure, maintenance is also cleared.

So **the storefront is unavailable to customers during a full re-index**. For large catalogues this could be tens of minutes — the merchant should schedule re-indexes during low-traffic windows. There is no live-storefront re-index option. This is the same maintenance behaviour described from the search-UI side on [[apps-advanced-search-indexing]].

### Re-index cancels the previous batch on retry

The active batch ID is persisted in the app's `batch_id` setting. If the merchant clicks Re-index while a previous batch is still in flight, the platform reads the previous `batch_id`; if that batch isn't finished and isn't already cancelled, it cancels it, clears `batch_id`, and starts a new batch. So clicking Re-index twice in a row **replaces** the in-progress run rather than queueing both.

### Reactive event-driven indexing keeps the index fresh

Product / category / vendor changes dispatch indexing jobs via subscribers the moment the change is persisted. So the platform actively keeps the index current with each change — a merchant editing a single product does not need to re-index manually; the change flows to the search index within seconds once the queue processes it. The "Out of sync" badge on [[apps-listing-engine-statistics]] is the fallback signal for when reactive indexing has drifted (failed jobs, bypassed hooks).

### Two built-in nightly jobs

Beyond reactive indexing, two scheduled jobs run daily without merchant action:

- **Nightly price/discount patch** runs once per day at **00:10 UTC**. It re-applies price / discount values into the index so price-driven facets stay accurate automatically.
- **the search index cleanup** runs at **05:00 UTC** daily to remove orphaned the search index documents (records that exist in the index but no longer in the database).

### Patch jobs pause while the site is in maintenance

Every reactive patch job (review patches, smart-collection patches, brand-model patches, category-property patches, product-column patches, vendor patches, etc.) checks the site's `maintenance` flag early and aborts if it is set. So during a full re-index (which sets `maintenance = 1`), all incoming index updates are paused — only the in-progress full upload runs. Once maintenance clears, queued patch jobs resume on the next worker pickup.

### Completion notification — admin alert + success toast

When the batch finishes, the manager fires a notification labelled `listing_engine_upload_content` with the message *"Content indexing has been completed successfully."* This appears in the admin's notifications panel; there is **no email by default**. After a re-index, the merchant should refresh the [[apps-listing-engine-statistics]] dashboard to confirm the indexed counts match the database counts.

## Related

- [[apps-listing-engine]] — hub.
- [[apps-listing-engine-statistics]] — the dashboard that signals when a re-index is needed and confirms it succeeded.
- [[apps-advanced-search-indexing]] — the same re-index / maintenance behaviour described from the search-UI side.
- [[brand-model]] — brand/model changes that fire reactive patch jobs into this index.

## Open questions

(None currently outstanding for this page.)
