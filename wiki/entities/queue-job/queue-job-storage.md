---
type: entity
aliases: ["Queue storage", "the analytics store queue", "site_queue collection", "Persistent queue rows", "retry_after window", "the analytics store-queue connection"]
tags: [settings, ops, jobs, queue, background, the analytics store, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[queue-job]]. See the hub for related aspects (populate-poller, lifecycle, families, priority tiers, visibility).

# Queue Job — persistent storage layer

## Identity

CloudCart stores its background-job state in a **durable document store**, not in a transient in-memory queue that empties as jobs are picked up. Every queued job is a **persistent record in the `site_queue` collection** that survives worker restarts, process crashes, and deploys — distinct from a standard transient job queue which holds rows that exist only between dispatch and dequeue.

The three queue connections the platform configures are `the analytics store-queue-local`, `the analytics store-queue-hetzner-cloud`, and `the analytics store-queue-google-cloud` — one per environment / data centre. Each connection points at the same document-store cluster used by the rest of the platform; the queue rows live alongside cart, analytics, and audit-log records.

The implication for the merchant: a job that's been enqueued **does not disappear** if a worker crashes mid-execution. The record stays in the store, transitions through a stuck state, and eventually becomes pickable by another worker — see [[queue-job-lifecycle]] for the per-phase mechanics.

## Aliases

- **Queue storage** — generic term for the persistence layer.
- **`site_queue` collection** — the literal queue-store collection name.
- **Persistent queue rows** — contrast with a transient job queue's rows.
- **`retry_after` window** — the ~10-minute reservation-expiry timer that governs stuck-job recovery.
- **`the analytics store-queue-*` connection** — the per-environment queue connection names.

## Key Attributes

The `site_queue` row carries every field documented on the [[queue-job]] hub. The store-specific columns that differ from a standard transient queue row are listed below.

| Column | Notes |
|--------|-------|
| **`reserved_at`** | Timestamp set when a worker picks up the row. Cleared on completion. While set + within the `retry_after` window, the job appears as `is_running=true` on [[settings-queue-view]]. |
| **`available`** | `true` when the row is eligible for a worker to pick up. Flipped to `false` on reservation. |
| **`attempts`** | Increment per pickup. Unlike a transient queue, this counter persists — useful when diagnosing repeatedly-failing recurring jobs. |
| **`retry_after`** (per-queue config) | ~10 minutes on every CloudCart queue family. A reserved row whose reservation timestamp is still inside the window is treated as "running"; once that window expires, the row becomes available to another worker. |
| **`completed_at`** | Set on success. For recurring jobs, this becomes the anchor that the populate-poller uses to compute the next run — see [[queue-job-populate-poller]]. |
| **`error`** (JSON) | Holds the failure details (message plus diagnostic context) from the last failed attempt. Preserved across runs until the row is deleted or the job next succeeds. |

## Where it appears

- [[settings-queue-view]] — `is_running` is derived from the reservation timestamp plus the `retry_after` window against the current time; rows the merchant sees are reads off the `site_queue` collection.
- [[settings-import-history]] — failed import rows read their `error` payload from this store.
- [[settings-hooks]] — webhook-delivery rows on the `order-events` family use the same persistence model.

## Persistent records vs a transient queue

| Aspect | Standard transient queue (`jobs` table) | CloudCart durable queue (`site_queue` collection) |
|--------|---------------------------------------|---------------------------------------------------|
| **Lifetime** | Row deleted on success / final fail. | Row preserved — recurring jobs UPDATE their fields in place. |
| **Retry handling** | Failed jobs are re-released back to the queue with exponential backoff. | Recurring jobs are re-enqueued by the next populate-poll cycle (see [[queue-job-populate-poller]]); one-shot failures stay failed until manual re-trigger. |
| **Stuck-job recovery** | Lost rows on crash unless `retry_after` is configured. | `retry_after` window (~10 min) auto-releases a reserved row from a crashed worker. |
| **Audit trail** | None — gone once processed. | Last-run timestamp, last error, attempt counter all retained on the row. |

This is why CloudCart's queue is sometimes called a **"durable scheduled-task registry"** rather than a "job queue" — it behaves more like a database of scheduled work than like a transient message bus.

## Stuck-row recovery and the `retry_after` window

When a worker crashes silently mid-execution, the `site_queue` row stays `reserved_at`-set with no `completed_at`. From the merchant's point of view on [[settings-queue-view]], the job appears stuck in "running" forever. After the queue's `retry_after` window (~10 minutes), the platform's reservation check (reservation timestamp plus `retry_after` is no longer in the future) starts returning false, the row becomes `available` again, and the next polling worker picks it up.

For `single=true` jobs (e.g., `currency_sync`, `subscription_payments`, `populate_*_tasks`) this is the most common cause of a *"why is the currency sync stuck?"* support ticket — the merchant must wait ~10 minutes or ask support to release the lock manually. See [[queue-job-visibility-and-errors]] for the single-lock rules.

## Related

- [[queue-job]] — hub.
- [[queue-job-populate-poller]] — uses `completed_at` to compute next-run schedule.
- [[queue-job-lifecycle]] — Reserved / Running / Stuck phases sit on top of this storage model.
- [[queue-job-visibility-and-errors]] — `single` lock and error preservation rules on top of these columns.
- [[settings-queue-view]] — read surface that displays this collection.

## Open Questions

None.
