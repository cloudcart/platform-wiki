---
type: entity
nav_path: "Entity → Import Task → History and webhooks"
aliases: ["Import history retention", "Import task retention", "Per-record webhook fan-out", "No import.completed webhook", "Shared import history", "Import audit trail"]
tags: [entity, settings, ops, imports, retention, webhooks]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[import-task]]. See the hub for the other aspects (attributes, lifecycle, types + queues, processing model, provenance + recovery).

# Import Task — History and webhooks

## Identity

What happens to the Import Task **after** completion — the **indefinite retention** rule (no TTL, no auto-cleanup, no DELETE endpoint), the **shared site-wide audit trail** (every staff member sees every Task; no per-creator filter), and the **webhook fan-out behaviour** — which has two important properties merchants must understand: (a) there are **NO Task-level webhook events** (`import.completed` / `import.failed` do not exist), and (b) **per-record webhooks DO fire** on every row processed, creating chatty fan-outs on large imports.

## Aliases

- **Import history retention** — the indefinite-keep rule.
- **Shared import history** — Site-scoped, every staff sees every Task.
- **Per-record webhook fan-out** — `product.updated` / `customer.created` / etc. fire on every row.
- **Audit trail** — the merchant-facing term for [[settings-import-history]] + change-log modal.

## Key Attributes

### Indefinite retention — Tasks accumulate forever

There is **NO auto-cleanup, NO scheduled retention, NO DELETE endpoint** exposed on the import-history surface. Past Import Tasks and their per-record detail rows accumulate forever — a merchant running daily imports for years has years of history.

[[settings-import-history]]'s pagination handles browse-time size; the underlying records persist forever unless support intervention clears them via direct DB access. The merchant cannot trigger a cleanup from the admin UI.

Practical implications:

- **Disk usage grows unbounded.** For high-volume merchants running daily XML syncs, the import-history table grows fast. Support occasionally cleans the oldest rows when storage thresholds are hit.
- **The "Imported with" filter (see [[import-task-provenance-and-recovery]]) keeps working forever.** Months / years after an import, the merchant can still find the affected records.
- **The change-log modal stays accurate.** Per-record before/after detail persists indefinitely.

### All staff see one shared history

Import Task rows are **Site-scoped, not staff-scoped**. Every Administrator and every Moderator with permission to view [[settings-import-history]] sees the **SAME** list. Multi-staff stores cannot filter to "only my imports".

The created-by field (`user_id`) IS recorded on the Task per [[import-task-attributes]] — but it is **NOT surfaced as a list-view filter**. The merchant can see who launched each Task only by drilling into the per-Task detail (verify), not by filtering the list.

### No import-level webhook events

There are **NO** `import.completed` / `import.failed` / `import.started` webhook events emitted by the platform. Receivers cannot subscribe to "an import finished" — there is no event to subscribe to.

Receivers that need Task-level signals must:

- **Poll [[settings-import-history]]** via the JSON-API v2 endpoint that surfaces the same data (verify which endpoint).
- **OR react to per-record events** (`product.*` / `customer.*` etc.) and infer "import finished" by some downstream signal (e.g., no new events for N seconds).
- **OR rely on the merchant manually triggering an event** (no built-in support for this).

This is a known gap. Apps that integrate with imports typically poll history rather than subscribe to events.

### Webhooks fire per imported record

Every record an Import Task creates / updates fires the corresponding webhook event (`product.updated`, `customer.created`, `subscriber.created`, etc.) via [[settings-hooks]]. The webhook payload is the same as if the merchant edited the record manually in the admin — receivers cannot tell from the payload alone that an import drove the change.

Practical consequences:

- **A 10,000-row product import generates 10,000 `product.updated` webhook deliveries** (or `product.created` for new products). Receivers should be prepared for the burst.
- **Customer CSV with 5,000 rows fires 5,000 `customer.created` deliveries.** Receivers that rate-limit per-second may fall behind.
- **Receivers should be idempotent.** Even per-record events from an import can be re-delivered on retry — receivers must tolerate duplicates.
- **The merchant can temporarily disable webhooks** in [[settings-hooks]] before a large import and re-enable after. This loses some downstream sync but prevents external system overload.

### The per-record change log

Beyond webhooks, every record an Import Task touches gets a row in the parent entity's **Change log** (e.g., [[products-change-log]] for products). The change-log row stores:

- The timestamp.
- The Initiator (e.g., "Import #N" or the source-app name).
- The field-by-field before / after values.

This is the durable forensic trail that survives webhook delivery failures. Per [[import-task-provenance-and-recovery]], the Change log is the merchant's primary tool for understanding "what exactly did this import change?"

### What [[settings-import-history]] shows

The history list view shows, per Task:

- **Date** — when the merchant kicked off the Task (not when it finished).
- **Type** — which importer (customers / products / xml-sync / etc.).
- **Source filename** or feed URL.
- **Status** — completed / failed / cancelled (in-flight Tasks are on [[settings-queue-view]] instead).
- **Action counts** — Created / Updated / No-action / Errors / Total.
- A drill-in link to the per-record detail (each row processed by the Task).
- A **"View detailed change log"** modal accessible per-record showing field-by-field before/after.

The list is paginated (default 25 rows per page); the merchant searches by date range, type, source filename.

## Where it appears

- [[settings-import-history]] — the canonical surface for completed / failed / cancelled Tasks.
- [[settings-hooks]] — per-record webhook events fire here (no Task-level events).
- [[products-change-log]] — the per-product audit trail showing import-driven changes.
- (Equivalent change logs on customer / subscriber / blog-article entities.)

## Related

- [[import-task]] — hub.
- [[import-task-attributes]] — the created-by + action-counts fields surfaced in the history list.
- [[import-task-lifecycle]] — what status the Task is in determines whether it's on history or queue-view.
- [[import-task-processing-model]] — per-record webhooks fire during chunk processing.
- [[import-task-provenance-and-recovery]] — the change log is the forensic trail for recovery.
- [[settings-import-history]] — the merchant-facing audit surface.
- [[settings-hooks]] — the webhook configuration; per-record events fan out from imports.
- [[products-change-log]] — the per-product change-log modal.
- [[notification-delivery]] — broader notification framework (imports do NOT trigger the standard `file_download` admin alert).

## Open Questions

- ⏸️ Whether the per-Task drill-in surface includes the created-by user name in a visible way (verify) — the field is stored but its surfacing in the list / detail view varies.
- ⏸️ Whether the platform exposes a JSON-API v2 endpoint that lets external apps poll [[settings-import-history]] for Task-level signals (verify path and shape).
- ⏸️ The disk-usage threshold at which support cleans old history rows — not merchant-controllable but useful to document for very-high-volume merchants.
