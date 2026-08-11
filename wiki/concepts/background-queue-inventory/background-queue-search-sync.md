---
type: concept
nav_path: "Concept → Background processes → the search index sync"
aliases: ["the search index sync", "search-index sync", "searchable-import4", "searchable-import8", "cc-system7", "MakeSearchable", "ProductsSearchEnginesSync", "Storefront read-side sync", "Storefront lag", "Storefront still shows old"]
tags: [background, async, the search index, search, storefront, support, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[background-queue-inventory]]. See the hub for related aspects (recurring platform jobs, imports/exports, order side-effects, Queue View, process catalogue).

# Background processes — the search index sync (storefront read-side)

## Definition

The storefront's product cards, category listings, search results, filter sidebars, sort orders, and in-stock badges all read from the **search index (the search index)**, NOT from the primary database. Every write that affects what a customer sees on the storefront — admin save, JSON-API v2 write, CSV import row, XML / JSON sync row, order status change that touches stock — requires a corresponding search-index update. Those updates run as their own background jobs on dedicated queues.

**This is the single most common cause of "I updated something and the storefront still shows the old version" support tickets.** The primary-database write IS done; the admin shows the new data; JSON-API v2 returns the new data — but until the search-index sync runs for the affected product IDs, the storefront keeps serving the cached search-index view.

## Scope

Covered:

- The three dedicated search-index queues: `searchable-import4`, `searchable-import8`, `cc-system7`.
- Triggers that enqueue ES updates (admin save, JSON-API v2 write, import row, order status change).
- Chunk sizing on bulk re-index (chunk size = 100 products per chunk).
- Web vs CLI / queue context — synchronous fast-path vs always-queued behaviour.
- Nightly maintenance: price re-sync drift catch + orphan cleanup.
- Diagnostic flow for "storefront still shows the old version".

Not covered:

- The search index cluster topology / index schema — platform-internal infrastructure.
- The synchronous live-sync code path itself — see [[storefront-architecture]] for the architectural reasoning.
- Per-import error semantics — see [[background-queue-imports-exports]].
- The in-stock badge logic on the storefront — see [[inventory-in-stock-badge]].

## Contrasts

- **Primary database vs search index.** The primary database is the source of truth for product data (admin reads, JSON-API v2 reads). The search index (the search index) is the read-side copy the storefront serves from. They diverge whenever the sync chain has work pending.
- **Web context vs CLI / queue context.** A web write (admin save, JSON-API v2 PATCH) tries a **synchronous live-sync** first and falls back to a "fire after response" pattern if the live-sync errors — so merchant admin saves typically appear on the storefront within seconds. CLI / queue context (CSV import, scheduled XML sync, admin command) **always queues** the update — there is no synchronous fast-path. A scheduled XML Sync run that touches 5000 SKUs creates **50 chunks** (chunk size = 100); each chunk processes when a `searchable-import4` worker picks it up.
- **Single-product update vs wide-touch save.** Saving one product enqueues that one product's ES update. Renaming a vendor / brand / category / parameter / discount that touches thousands of products enqueues a bulk re-index of every affected product — same `searchable-import4` queue, much larger workload, much longer drain time.

## Where it applies

### The three search-index queues

| Queue name | Purpose | Cadence |
|---|---|---|
| `searchable-import4` | Per-product / per-variant create / update / delete re-index after any write that affects storefront-visible fields | On-demand, hot path |
| `searchable-import8` | Repeatable nightly price re-sync to ES + bulk command-driven full re-index (engineer-triggered) | Every 24 h + manual |
| `cc-system7` | Repeatable search-index orphan cleanup — removes search-index docs whose primary-database row was deleted | Every 24 h |

`searchable-import4` is the queue support cares about. Its backlog directly determines how long the storefront lags behind the admin panel. Identifiers like `MakeSearchable` and the search re-index (the actual job names dispatched on this queue) are platform-internal — the Assistant must not paste them to a merchant; explain in merchant terms ("the storefront-sync process is processing your products").

### Triggers that enqueue ES updates

| What enqueues | When |
|---|---|
| Per-product / per-variant create / update / delete re-index | After admin save, after [[api-products|JSON-API v2]] write, after [[apps-csv-import|CSV]] / [[apps-xml-import|XML]] / [[apps-xml-sync|XML sync]] row processed, after order status change touches stock |
| Bulk re-index for high-fanout objects | After a "wide-touch" save (e.g., renaming a vendor that 5000 products reference) |
| Nightly price re-sync to ES (catches any drift) | Every 24 h on `searchable-import8` |
| Nightly search-index orphan cleanup | Every 24 h on `cc-system7` |
| Engineer-triggered full re-index | Manual via the platform's `searchable:make` command on `searchable-import8` |

### Diagnostic flow — "the storefront still shows the old version"

When a merchant says *"I updated this product / ran an import / synced this feed and the storefront still shows the old version"*, the issue is almost always **queue lag on `searchable-import4`**, not a bug in the originating action. The investigation steps:

1. **Confirm the originating action completed.** For an import or sync, the Queue View row should show **Finished**. For an admin save, the admin should already show the new data.
2. **Confirm the admin reflects the change.** If the admin shows old data too, the originating action did not actually complete — investigate the import / sync failure first, not the search-index sync.
3. **Check pending search-index sync jobs for the site.** If `searchable-import4` is backed up, the merchant must wait for it to drain. Visible drain time depends on overall queue depth across the platform.
4. **Identify the contributing workload.** Tools that contribute to a backed-up `searchable-import4`: large imports, bulk JSON-API v2 writes, ERP sync runs (e.g. [[apps-microbg]] every 3 minutes), and storefront-affecting renames of high-fanout objects (vendor / category / parameter touching thousands of products).
5. **Wait or re-prioritise.** There is no merchant-side action to force-drain the queue. The watchdog (see [[background-queue-view-and-stuck]]) kills hung workers every 2 minutes so the queue keeps moving. For very large backlogs, support can escalate to platform engineering for a manual `searchable:make` run.

A common merchant-side anti-pattern: re-running the same import after seeing storefront lag. That **doubles** the workload — the original update is still pending, and now there's a second identical update behind it. Always confirm the queue state before re-running.

## Related

- [[background-queue-inventory]] — hub.
- [[storefront-architecture]] — why the storefront reads from the search index, not the primary database.
- [[settings-queue-view]] — visible-process surface (does NOT surface `searchable-import4` to the merchant — internal queue).
- [[api-products]] — JSON-API v2 writes that enqueue search-index sync.
- [[apps-csv-import]] / [[apps-xml-import]] / [[apps-xml-sync]] — bulk write sources.
- [[apps-microbg]] — example high-frequency feed contributor.
- [[inventory-tracking]] — stock changes are the most common trigger for search-index sync.
- [[inventory-in-stock-badge]] — storefront badge served from ES.
- [[background-queue-view-and-stuck]] — watchdog mechanics keeping ES workers alive.

## Open Questions

- The published merchant-side SLA for `searchable-import4` drain time under normal load is not currently documented. Worth capturing once measured (verify).
