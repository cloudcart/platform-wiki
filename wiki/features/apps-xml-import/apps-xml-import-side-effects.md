---
type: feature
nav_path: "Apps → XML Import → Side effects"
route_name: apps.xml_import
route_path: /admin/apps/xml_import (downstream of Insert)
aliases: ["XML Import side effects", "XML Import — the search index async sync", "XML Import — storefront lag", "XML Import — MakeSearchable", "XML Import — webhooks", "XML Import — smart collections", "XML Import — cache invalidation", "XML Import — no rollback", "XML Import — disable_missings effects"]
tags: [apps, imports, xml, side-effects, search-engines, webhooks]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-xml-import]]. See the hub for the other aspects (wizard, job pipeline, fetch transport, mapping fields, plan gates).

# XML Import — side effects

## Purpose

Once Insert writes a row, the change ripples through the rest of CloudCart: the search index re-index queue, storefront page caches, smart-collection re-evaluation, webhooks, and image-download jobs. Most of these are **asynchronous** — meaning the import job CAN finish, the admin product page CAN show correct values, and the storefront CAN still show stale data while downstream queues drain. This is the #1 source of "I imported and don't see the change on the site" support tickets.

This page enumerates every downstream effect, the order they fire in, what each queue is, and how to diagnose the most common ticket pattern. For the import pipeline that produces these writes see [[apps-xml-import-job-pipeline]]; for what data flows into them see [[apps-xml-import-mapping-fields]].

## Where to find it

There is no merchant UI for the side effects. They surface in:

- The storefront (eventually) — the search index-driven listings catch up product-by-product.
- Webhook receivers — `product.created` / `product.updated` fires per imported product.
- The product's [[products-change-log|Change log]] — every Variant `quantity` change is auditable per [[inventory-debugging-playbook]].
- [[settings-hooks]] — where the merchant configures the webhook destinations that receive the burst.

## What the merchant can do here

- Subscribe to back-in-stock notifications via [[products-missing-product]] (storefront-driven, but seeded by import-time stock changes).
- Configure webhook destinations on [[settings-hooks]] knowing import will fan out one event per imported product.
- Read the Change log on each product to see the import as the Initiator. See [[inventory-debugging-playbook]].

What the merchant CANNOT do here:

- Roll back an import. There is no built-in undo (see below).
- Suppress webhooks during an import — every imported product fires `product.created` / `product.updated`.
- Force the search index to catch up synchronously — the queue drains as it drains.

## Settings & fields

Downstream targets:

| Side effect | Surface | Cadence |
|-------------|---------|---------|
| the search index re-index | `MakeSearchable` job on `searchable-import4` queue | Async, chunks of 100 |
| Storefront page cache | Product / category / search caches | Async on Save |
| Smart-collection re-eval | Per affected collection | Async on Save |
| Webhooks | `product.created` / `product.updated` | Fires per product, NOT suppressed |
| Image download | Per-image background job | Async, queued at Insert time |
| Variant images | Separate queued job | Async |
| Low-stock email | `mail_product_quantity_low` | Per [[inventory-in-stock-badge]] gating |

## Business rules

### Side effects of import

- New / updated products in [[products-products]] (written to the operational database).
- the search re-index events fired per product on save — these **queue follow-up jobs** that push updates into **the search index** (the storefront's read index). See the storefront-lag rule below.
- Per-product image jobs queued (image download from URL). See [[apps-xml-import-mapping-fields]].
- Smart-collection re-evaluation (membership changes from new / updated products).
- Cache invalidation: product / category / search pages flushed.
- XML import **does NOT suppress webhooks** — `product.created` / `product.updated` fires for every imported product. Receivers must be idempotent and ready for a burst proportional to the import size.

### the search index sync is asynchronous — storefront may lag after the import finishes

This is the most common source of confusion on import support tickets.

**The storefront does NOT read from the operational database.** Product cards, category listings, search results, filter sidebars, sort orders, and stock badges all read from the **search index**. The database is the system of record for writes; the search index is the read-side copy the storefront queries. So a product can be fully up-to-date in the database (admin shows it correctly, JSON-API v2 returns it correctly) and still appear stale or missing on the storefront if the search index hasn't caught up yet.

**Pipeline** when the XML import finishes processing a batch:

1. The import job writes / updates each product row in the operational database.
2. For each product, the import fires the search re-index event.
3. The subscriber catches the event. Because the import runs **in a queue worker (CLI context)**, the subscriber **always dispatches** a `MakeSearchable` job onto the **`searchable-import4`** queue — there is no synchronous fast-path in this context.
4. `MakeSearchable` processes products in **chunks of 100** and pushes them into the search index.
5. Storefront search + listings + sort + filter pages start returning the new data only after step 4 completes for the affected products.

### What can go wrong for the merchant

- The import job finished — the admin product page shows correct values — **but the storefront still shows the old data**. Almost always: the `searchable-import4` queue is still processing the `MakeSearchable` jobs queued by the import. Resolution: wait. Diagnostic: count pending `MakeSearchable` jobs for that site on the queue.
- Large imports (10k+ products) can leave `searchable-import4` backed up for minutes to hours depending on system load — meaning the storefront catches up product-by-product as the chunks process, not all at once.
- The merchant re-triggers the import, sees admin updated, refreshes the storefront immediately, doesn't see the change → assumes it "didn't work". The fix is queue lag, not a bug.

### What support should check first

For any "I imported and don't see it" ticket:

1. Confirm the Status page shows the task as finished.
2. Verify the storefront is the issue (not admin) — load the product in the admin and compare with storefront.
3. Check pending `MakeSearchable` jobs for the site on the `searchable-import4` queue.

See [[background-queue-inventory]] for the queue lookup procedure and [[storefront-architecture]] for the read-side architecture.

### No rollback / undo

There is **no built-in rollback**. Once products are created or updated by an XML import run, the merchant must clean up manually (delete products, restore from backup). Cancelling a running task stops further processing but does NOT reverse rows already written. The merchant should test a small mapping on a sample feed before pointing at the full catalog.

### `disable_missings` opt-in deactivation has side effects too

When the merchant enables `disable_missings` in [[apps-xml-import-wizard]], a separate job sweeps products previously imported by this task and not present in the current feed, then deactivates them. Each deactivation is itself a product save → fires the search re-index → queues a `MakeSearchable` → re-indexes the search index → eventually shows the product as unavailable on the storefront. So `disable_missings` is bound by the same async-lag rule.

### Stock writes are auditable via Change log

Every Variant `quantity` change made by the import is recorded in the parent product's [[products-change-log|Change log]] with timestamp + Initiator (the import task). For "the stock changed and we didn't change it" tickets, the Change log is the **first place to look** — see [[inventory-debugging-playbook]].

## Related

- [[apps-xml-import]] — hub.
- [[apps-xml-import-job-pipeline]] — what produces these writes (the Parse → Insert pipeline).
- [[apps-xml-import-mapping-fields]] — what data flows into the writes.
- [[apps-xml-import-wizard]] — the `disable_missings` opt-in toggle.
- [[products-products]] — products created / updated.
- [[products-change-log]] — the Change log audit trail.
- [[settings-hooks]] — `product.created` / `product.updated` webhook configuration.
- [[storefront-architecture]] — the search index read-side (why the storefront can lag).
- [[background-queue-inventory]] — `searchable-import4` queue + the search-index sync chain.
- [[inventory-debugging-playbook]] — 6-step "stock changed and we didn't change it" workflow.
- [[inventory-in-stock-badge]] — low-stock email gating that fires on import-driven stock changes.
- [[products-missing-product]] — back-in-stock subscribers seeded by import stock changes.

## Open questions

_None._
