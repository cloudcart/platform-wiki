---
type: feature
nav_path: "Apps → Algolia → Indexing"
route_name: apps.algolia.overview
route_path: /admin/apps/algolia
aliases: ["Algolia indexing", "Upload data to Algolia", "Algolia sync", "Algolia auto-sync", "Algolia nightly sync", "Algolia plan cap", "Algolia chunks"]
tags: [apps, algolia, search, indexing, sync, background-jobs]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[apps-algolia]]. See the hub for the other aspects (credentials, dashboard-side configuration, settings tab).

# Algolia — Indexing & sync

## Purpose

Covers how CloudCart pushes catalog data into Algolia: the manual **Upload data to Algolia** button, how that upload is chunked and plan-capped, the automatic event-driven sync that keeps the index fresh as products change, the nightly belt-and-braces full re-sync, and exactly which entity types do (and do not) sync. This is the page to read for "why is product X missing from Algolia search" or "do I have to re-index after editing a product".

## Where to find it

Sidebar → Apps → Algolia → **Settings tab** → **Upload data to Algolia** button. Route: `/admin/apps/algolia`. The auto-sync and nightly sync run in the background — there is no merchant UI for them.

## What the merchant can do here

- Click **Upload data to Algolia** (`btn.start_indexing`) to enqueue a full batch upload of products + categories + vendors. Success toast: *"Sending data to Algolia was added to the queue."* (`success.set_on_queue`).
- Watch in-flight state — the app exposes progress data for the upload pipeline so the merchant can see when a sync is running.
- Rely on automatic sync — most product / category / vendor changes propagate without any manual action.

### What the merchant CANNOT do here

- Index more products than the `algolia` plan-feature cap allows (excess products silently skip).
- Sync entity types other than products, categories, vendors (tags, properties, smart collections, brand-models do NOT sync).
- Configure or trigger the nightly repeatable sync — it is automatic when Algolia is enabled.

## Settings & fields

| Control (lang key) | Notes |
|---|---|
| `btn.start_indexing` | "Upload data to Algolia" — enqueues the batch upload. Gated by `isConfigured` (see [[apps-algolia-credentials]]). |
| `success.set_on_queue` | *"Sending data to Algolia was added to the queue."* |

No persistent per-field configuration on this aspect — indexing behaviour is driven by product state + plan cap, not by toggles.

## Business rules

### Queue-backed upload

The "Upload data to Algolia" button enqueues a batch job (background job tagged `algolia_content`) rather than running synchronously. Large catalogs (100k+ products) upload in chunks; the merchant doesn't have to wait, and the integration tracks in-flight state so the merchant can see when a sync is running.

### Indexing chunks of 300 products + plan limit on TOTAL product count indexed

When the merchant clicks **Upload data to Algolia**, the platform:

1. Chunks the product ID list into batches of **300 products per job**.
2. Applies the `algolia` plan-feature cap — if the merchant's plan limits how many products may be indexed (e.g., 5000), and they have 20000 products, **only the first 5000 are indexed** and a plan-denied exception is logged. Products beyond the plan cap silently skip Algolia indexing; they're still in the database but won't appear in Algolia search results until the merchant upgrades.

This is a hidden plan-tier gate the merchant won't see explicitly in the UI — they may notice products missing from search, and only after upgrading their plan + re-running the upload will those products appear.

### Auto-sync on product / category / vendor save via listener

The integration subscribes to product / category / vendor create / update / delete events. Each event automatically toggles the affected record's searchable state, which pushes the change to Algolia within seconds (active + visible products go to the index; inactive / hidden go out). The merchant doesn't have to manually re-sync after each product save.

### Listener only indexes when product is `active` AND not `is_hidden` AND not `draft`

The auto-sync listener checks the product's state on every save:

- `active = 1` (the merchant has the product enabled).
- `is_hidden = 0` (not hidden from the storefront).
- `draft = 0` (not in draft state).

A product matching ALL three becomes searchable (pushed to Algolia). A product failing any one becomes unsearchable (removed from Algolia). So toggling visibility / activating drafts triggers an Algolia sync within seconds — the merchant doesn't have to manually re-index after these flag changes.

### Repeatable nightly full sync runs at 00:00 + 10 minutes UTC

Per the queue config, `algolia_repeatable` runs every 86400 seconds (24 hours) on the `export` queue. The dispatched repeatable job re-runs the full upload for **all sites** that have Algolia active + configured, restarting the next day at 00:10 UTC. This belt-and-braces full sync keeps the index aligned even if individual event-based syncs were lost (e.g., due to a transient Algolia outage). The merchant doesn't configure or trigger it.

### Algolia listener handles ONLY products, categories, vendors

The integration subscribes to product, category, and vendor create / update / delete events. **Tags, properties, smart collections, brand-models, etc. do NOT trigger Algolia sync** — only the three top-level types. Searching for a property name or smart-collection name on Algolia-powered storefronts will not match unless the storefront UI separately exposes them.

### Disabled app accumulates drift

The Algolia listener is gated by the app's enabled flag — if the merchant toggles Algolia inactive (without uninstall), every event listener returns early and skips the Algolia API call. Product changes during this period accumulate "drift": the Algolia index goes stale. When the merchant reactivates, only NEW changes resync; the historical drift persists until the next 00:10 UTC repeatable run (or a manual Upload).

### Permission

Standard apps permission scope.

## Related

- [[apps-algolia]] — hub.
- [[apps-algolia-credentials]] — the `isConfigured` gate that must pass before any upload or auto-sync runs.
- [[background-queue-inventory]] — queue model context (the `export` queue carries the repeatable sync).
- [[products-products]] / [[products-categories]] / [[products-vendors]] — the three synced entity types.

## Open questions

(None currently outstanding for this page.)
