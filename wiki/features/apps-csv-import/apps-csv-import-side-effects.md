---
type: feature
nav_path: "Apps → CSV Import → Side effects"
route_name: apps.csv_import.overview
route_path: /admin/apps/csv_import (downstream effects)
aliases: ["CSV Import — the search index sync", "CSV Import — storefront lag", "CSV Import — webhooks", "CSV Import — no rollback", "CSV Import — no undo", "CSV Import — app_import tag", "CSV Import — bulk cleanup filter"]
tags: [apps, imports, csv, side-effects, the search index, webhooks]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-csv-import]]. See the hub for the other aspects (wizard, task detail, row pipeline, final statuses, mapping fields, plan gates).

# CSV Import — side effects

## Purpose

Every CSV import row that successfully lands triggers downstream side effects: search-index re-indexing, storefront cache invalidation, webhooks, and a tag that lets the merchant find every product the task created. The most common support ticket the integration produces is "I imported and don't see it on the site" — and the answer is almost always "the search-index queue is still catching up". This page documents the pipeline that runs *after* the row hits the operational database, the webhook timing, the lack of a rollback, and the `app_import` tag that makes cleanup possible.

## Where to find it

There is no dedicated route — side effects happen in the background after each row is processed. The merchant observes the consequences through the storefront, the [[settings-hooks|webhook delivery log]], and the products-list filter `import=csv-{taskId}-`.

## What the merchant can do here

- **Watch the storefront catch up** — after the task shows "Imported X products successfully", the storefront still reflects old data until the `searchable-import4` queue processes the affected products. The merchant should wait, not retry.
- **Filter the products list by `import=csv-{taskId}-`** — surfaces exactly the products this task created, for review or bulk cleanup. See *`app_import` tag* below.
- **Bulk-delete from that filter** — the only "undo" available, since there is no rollback action. The mass-delete operation respects normal delete rules.
- **Hook external systems to `product.created` / `product.updated`** — webhooks fire per row at import-write time (BEFORE the storefront sees the change). External integrations must be tolerant of receiving the event before the ES read-side reflects it.

## Settings & fields

| Effect | Surface | What it does |
|---|---|---|
| the search re-index event | Background — `OnProductUpsert` subscriber → `MakeSearchable` job → `searchable-import4` queue | Re-indexes the affected product into the search index in chunks of 100. |
| Storefront page-cache invalidation | Background | Flushes product-detail / category / variant-picker fragments. |
| `product.created` + `product.updated` webhooks | Webhook delivery — see [[settings-hooks]] | Fire per row at the import-write step (before search-index sync). |
| `app_import` tag | Persisted on the product record | Format `csv-{taskId}-<source>`. Drives the products-list filter `import=csv-{taskId}-` for bulk cleanup. |

## Business rules

### the search index sync is asynchronous — storefront lags after the import finishes

The storefront does **not** read from the operational database. Storefront product cards, category listings, search results, filter sidebars, sort orders, and stock badges all read from the **search index**. The operational database is the system of record for writes; the search index is the read-side copy the storefront queries.

**Pipeline** when a CSV import row finishes processing:

1. The row's product / variant is written to the operational database.
2. The row processor fires the search re-index event for the affected product.
3. The `OnProductUpsert` subscriber catches it. Because the import runs **in a queue worker (CLI context)**, the subscriber **always dispatches** a `MakeSearchable` job onto the **`searchable-import4`** queue — there is no synchronous fast-path in this context. See [[apps-csv-import-row-pipeline]].
4. `MakeSearchable` processes products in **chunks of 100** and pushes them into the search index.
5. Storefront search + listings + sort + filter + in-stock badges reflect the new data only after step 4 completes for the affected products.

**Practical consequences for the merchant:**

- The task shows "Imported 1234 products successfully" at 15:00 and the merchant's product editor confirms the change — **but the storefront still shows old data**. Almost always the `searchable-import4` queue is still processing the `MakeSearchable` jobs queued by the import. Resolution: wait. Diagnostic: count pending `MakeSearchable` jobs for the site.
- Large imports (10k+ rows) can leave `searchable-import4` backed up for minutes to hours depending on system load — the storefront catches up product-by-product as the chunks process, not all at once.
- The same caveat applies to variant-only CSV imports — variant changes propagate as parent-product re-syncs.

**What support should check first** for any "I imported and don't see it on the site" ticket: confirm the task is finished, verify the storefront is the issue (not admin), then check pending `MakeSearchable` jobs for the site. See [[background-queue-inventory]] for the queue lookup procedure and [[storefront-architecture]] for the read-side architecture.

### Webhooks fire BEFORE the storefront sees the change

The `product.created` / `product.updated` webhook fires per row at the **import-write step** (step 1 above) — not after search-index sync. External integrations receive the event **before** the storefront reflects it. Receivers that re-fetch via the storefront API or hit the public catalog page risk reading stale data immediately after the webhook. The platform offers no synchronisation primitive between webhook delivery and ES catch-up; integrations should be idempotent and tolerate "webhook fired, public read still stale" for a window. See [[settings-hooks]].

### Final message persisted on `csv_tasks.message`

After completion, a human-readable message is stored on the task (e.g., "Imported 1234 products successfully" or "5 errors found — click to view"). The merchant doesn't need to scrub job logs. See [[apps-csv-import-final-statuses]] for the message-text catalogue and [[apps-csv-import-task-detail]] for where it surfaces.

### No rollback / undo — `app_import` tag enables filter-and-delete cleanup

There is **no built-in undo button**. Once products are created or updated, the merchant must delete them manually (or restore from backup). The mitigation: the manager tags every CSV-imported product with `app_import = 'csv-{taskId}-<source>'`, so the products-list filter `import=csv-{taskId}-` cleanly selects them for bulk cleanup. This is the only path to "undo" a CSV import.

The same tag is the source of the **Imported count's clickable link** on the task-detail header — clicking jumps to the filtered products list. See [[apps-csv-import-task-detail]].

### Staging table survives the import

The temporary `csv_import_{timestamp}` staging table persists until the merchant deletes the task. It is useful for retries (the mapping JSON + staging table together let the platform re-run the import without re-uploading) or post-import inspection. See [[apps-csv-import-wizard]] for the staging-table mechanics.

### Cancel preserves already-imported rows

Cancelling a mid-flight task stops further processing but does NOT roll back the products already written. The merchant uses the `import=csv-{taskId}-` filter to bulk-delete the partial import if they want a clean retry. See [[apps-csv-import-task-detail]].

## Related

- [[apps-csv-import]] — hub.
- [[apps-csv-import-row-pipeline]] — why every row's search-index sync is async in the queue-worker context.
- [[apps-csv-import-task-detail]] — surfaces the Imported clickable filter + the post-finalisation message.
- [[apps-csv-import-final-statuses]] — what gets written to `csv_tasks.message`.
- [[apps-csv-import-mapping-fields]] — where the `app_import` tag's `<source>` portion comes from.
- [[settings-hooks]] — webhook delivery for `product.created` / `product.updated`.
- [[storefront-architecture]] — the search index read-side that lags after the import.
- [[background-queue-inventory]] — `searchable-import4` queue + `MakeSearchable` chunking.
- [[products-products]] — the products list where the `import=csv-{taskId}-` filter is applied.

## Open questions

_None._
