---
type: feature
nav_path: "Apps → XML Sync → Side effects"
route_name: apps.xml_sync
route_path: /admin/apps/xml_sync (downstream of Insert)
aliases: ["XML Sync side effects", "XML Sync the search index sync", "XML Sync storefront lag", "XML Sync MakeSearchable", "XML Sync webhooks", "XML Sync smart collections", "XML Sync cache invalidation", "XML Sync no failure email", "XML Sync searchable-import4"]
tags: [apps, imports, xml, sync, side-effects, search-engines, webhooks]
plan_gates: ["xml_sync_limit"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[apps-xml-sync]]. See the hub for the other aspects (job pipeline, update policy, discontinued handling, fetch transport).

# XML Sync — side effects

## Purpose

Each XML Sync run writes / updates / deactivates products in the operational database — and every one of those writes ripples through the rest of CloudCart: the search index re-index queue, storefront page caches, smart-collection re-evaluation, and webhooks. Most of these are **asynchronous**, so a sync can show "Last sync: 14:32 ✓" while the storefront still shows old data. This is the #1 source of "the sync ran but the site didn't change" support tickets. This page enumerates every downstream effect, the pipeline order, and why the storefront lags. It also documents the failure-notification surface (there is no failure email).

For what produces these writes see [[apps-xml-sync-job-pipeline]]; for what data flows into them see [[apps-xml-sync-update-policy]] and [[apps-xml-sync-discontinued]].

## Where to find it

There is no merchant UI for the side effects. They surface in:

- The storefront (eventually) — the search index-driven listings catch up product-by-product.
- Webhook receivers — `product.created` / `product.updated` fires per affected product.
- The product's [[products-change-log|Change log]] — every Variant `quantity` change is auditable per [[inventory-debugging-playbook]].
- [[settings-hooks]] — where the merchant configures the webhook destinations that receive the burst.

## What the merchant can do here

- Configure webhook destinations on [[settings-hooks]] knowing each sync run fans out one event per affected product.
- Read the Change log on each product to see the sync task as the Initiator. See [[inventory-debugging-playbook]].
- Wait for the `searchable-import4` queue to drain before judging whether a run "worked".

What the merchant **cannot** do here:

- Suppress webhooks during a sync — every affected product fires `product.created` / `product.updated`. Bulk sync does **NOT** suppress them.
- Force the search index to catch up synchronously — the queue drains as it drains.
- Receive an **email** when a sync fails — there is no failure-email notification (see below).

## Settings & fields

| Side effect | Surface | Cadence |
|-------------|---------|---------|
| the search index re-index | `MakeSearchable` job on `searchable-import4` queue | Async, chunks of 100 |
| Storefront page cache | Product / category / search caches | Async on Save |
| Smart-collection re-eval | Per affected collection | Async on Save |
| Webhooks | `product.created` / `product.updated` | Fires per product, NOT suppressed |
| Disable-missings | the search re-index with `action=update` per deactivated product | Async; drops them from listings as ES catches up |
| Sync history entry | Run stats (created / updated / skipped / failed) | Per run, on [[apps-xml-sync-status]] |

## Business rules

### Side effects on each sync run

- New products from the feed → created in the operational database.
- Existing products with changes → updated per the policy in [[apps-xml-sync-update-policy]].
- Missing products → handled per [[apps-xml-sync-discontinued]] (`disable_missings`); when set, missing products are deactivated **and** fire the search re-index with `action=update` so the storefront drops them on the next search-index sync chunk.
- A **sync history entry** is created with stats (created / updated / skipped / failed counts), visible on [[apps-xml-sync-status]].
- the search re-index events fire **per affected product** → queue follow-up `MakeSearchable` jobs on `searchable-import4`.
- **Webhooks fire per product** (`product.created` / `product.updated`) — the same [[settings-hooks]] channel as admin saves. **Bulk sync does NOT suppress them**; receivers must be idempotent and ready for a burst proportional to the row count.
- **Smart-collection re-evaluation** runs (membership changes from new / updated products).
- **Cache invalidation**: product / category / search pages flushed.

### the search index sync is asynchronous — storefront may lag after each sync run

The storefront does **not** read from the operational database. Storefront product cards, category listings, search results, filter sidebars, sort orders, and out-of-stock badges all read from **the search index**. The operational database is the system of record for writes; the search index is the read-side index.

**Pipeline** when a scheduled run completes:

1. The sync worker writes / updates / deactivates each affected product.
2. For each touched product, the search re-index event fires (including `disable_missings` deactivations).
3. Because the sync runs in a queue worker (CLI context), the subscriber **always dispatches** a `MakeSearchable` job onto **`searchable-import4`** — there is no synchronous fast-path.
4. `MakeSearchable` processes products in **chunks of 100** and pushes them into the search index.
5. Storefront search + listings + filter + sort + in-stock badges reflect the new data only after step 4 completes for the affected products.

### Practical consequences for the merchant

- Seeing "Last sync: 14:32 ✓" but the storefront still showing old prices at 14:33 is **not** a sync bug — the sync wrote the database, but the `MakeSearchable` jobs for those products are still working through `searchable-import4`. Wait, then refresh.
- A `disable_missings` run flipping thousands of products to inactive does **not** make them disappear from the storefront immediately — each is dropped from ES as its chunk processes.
- A price change appears in [[products-products]] (admin) immediately when the worker finishes, but the storefront's category card and search result keep the old price until ES catches up.
- If `searchable-import4` is backed up by other heavy ingest (CSV import, JSON-API v2 writes, ERP sync), an XML Sync run's products **wait behind everyone else's jobs**.

### No built-in failure email — failures surface only on the Status page

There is **no admin-email notification** when a sync fails N times. Failures are logged to the run-history records (visible on [[apps-xml-sync-status]]) and the task's `error` column on the listing. The merchant is, however, alerted **in-CP** via admin notifications on each failure strike — see the 3-strike rule in [[apps-xml-sync-job-pipeline]]. So the signal exists, just not over email.

### Stock writes are auditable via the Change log

Every Variant `quantity` change made by a sync run is recorded in the parent product's [[products-change-log|Change log]] with timestamp + Initiator (the sync task). For "the stock changed and we didn't change it" tickets, the Change log is the **first place to look** — see [[inventory-debugging-playbook]].

## Related

- [[apps-xml-sync]] — hub.
- [[apps-xml-sync-job-pipeline]] — what produces these writes + the 3-strike in-CP alerting.
- [[apps-xml-sync-update-policy]] — what data flows into the writes.
- [[apps-xml-sync-discontinued]] — deactivations that also trigger search-index re-index.
- [[apps-xml-sync-status]] — the run-history surface where failures appear.
- [[products-products]] — products created / updated / deactivated.
- [[products-change-log]] — the Change log audit trail.
- [[settings-hooks]] — `product.created` / `product.updated` webhook configuration.
- [[storefront-architecture]] — the search index read-side (why the storefront can lag).
- [[background-queue-inventory]] — `searchable-import4` queue + the search-index sync chain.
- [[inventory-debugging-playbook]] — 6-step "stock changed and we didn't change it" workflow.
- [[apps-xml-import-side-effects]] — the sibling import's identical downstream model.

## Open questions

_None._
