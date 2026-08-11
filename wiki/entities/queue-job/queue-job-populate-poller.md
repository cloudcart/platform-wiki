---
type: entity
aliases: ["Populate poller", "populate_*_tasks", "Recurring-job scheduler", "Interval-based scheduler", "PopulateTasksInQueues", "Polling scheduler"]
tags: [settings, ops, jobs, queue, background, scheduler, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[queue-job]]. See the hub for related aspects (persistent storage, lifecycle, families, priority tiers, visibility).

# Queue Job — populate-poller (recurring-job scheduler)

## Identity

The **populate-poller** is the engine that drives every recurring job in CloudCart. Every 60 seconds, the platform runs a set of `populate_<group>_tasks` jobs — one per queue family. Each of these scans the mapping registry of recurring jobs, checks every entry's last `completed_at` plus its `interval` against the current time, and enqueues whichever are due.

**CloudCart does NOT use the application framework's Scheduler or crontab.** The populate-poller IS the schedule. So a recurring job's first run after completion is at most `interval + 60 seconds` later — there is no minute-precision cron expression involved.

The mapping registry that the poller scans lives in the platform's queue configuration — a list of mapping entries each with: a short code key (`currency_sync`, `marketing_dashboard`, etc.), the job to dispatch, the queue family it lands on, its `interval` in seconds, and its `single` / `visible` flags. The registry is platform-defined (not editable by merchants).

## Aliases

- **Populate poller** — internal nickname.
- **`populate_*_tasks`** — the mapping-code prefix; appears in [[settings-queue-view]] as its own visible row.
- **Recurring-job scheduler** — generic term used in support tickets.
- **Interval-based scheduler** — contrast with a cron-based scheduler.
- **Populate-tasks engine** — the engineering shorthand.

## Key Attributes

| Attribute | Notes |
|-----------|-------|
| **Polling cadence** | Every **60 seconds**, per queue family. Each family has its own poller (`populate_system_tasks`, `populate_import_tasks`, `populate_order_events_tasks`, `populate_campaigns_tasks`, etc.) — so a slow family doesn't block another family's recurring schedule. |
| **Scope** | One poller per queue family — see [[queue-job-families]]. |
| **Comparison rule** | current time is at or past last `completed_at` plus `interval` → enqueue. |
| **Visibility on Queue View** | The populate-poller itself is `visible = true` — merchants see `populate_system_tasks`, `populate_order_events_tasks`, etc. as their own rows on [[settings-queue-view]]. |
| **`single = true`** | Every populate-poller is single-locked — only one execution platform-wide per family at any moment. See [[queue-job-visibility-and-errors]] for single-lock rules. |
| **Skipped cycle** | If a recurring job is still running (its row hasn't reached `completed_at` yet) when its next interval elapses, the poller does NOT enqueue a duplicate — the populate-poller skips this entry until the in-flight execution finishes. |

## Where it appears

- [[settings-queue-view]] — the merchant sees one row per populate-poller (one per queue family); their *Next run* is always "in the next 60 seconds".
- [[background-queue-inventory]] — populate-pollers are catalogued as the schedule-driving meta-jobs.
- [[queue-job-families]] — every family has its own poller; the family table on that page lists them implicitly.

## How a recurring job actually runs (end-to-end)

A typical recurring job goes through this sequence on every cycle:

1. **Mapping registered** — at deploy time, the entry sits in the mapping registry with `interval`, queue, `single`, `visible`.
2. **Poller cycle (every 60s)** — `populate_<group>_tasks` runs on its family's worker. It iterates the registry entries for that family.
3. **Due check** — for each entry, the poller compares the current time against the persisted last `completed_at` plus `interval`. If due, the corresponding row in `site_queue` is updated to `available = true` with a fresh `next_execution_at` — see [[queue-job-storage]] for the row layout.
4. **Worker picks up** — a worker on that family reserves the row, executes the job, and on success writes the `completed_at` timestamp.
5. **Next-run anchor** — the *Next run* column on [[settings-queue-view]] becomes the completion time plus `interval`, ready for the poller's next cycle.

## Consequences of the polling model

- **First run after a code-level interval change lags.** Existing scheduled rows continue with their previously-set `next_execution_at` until they next complete; only at the FOLLOWING cycle do they adopt the new interval.
- **Cluster pauses ripple.** If `worker-system` is down, NONE of its mappings' recurring jobs make progress — `populate_system_tasks` itself can still enqueue, but the populate row also lives on `system` and won't execute. Worker uptime is monitored via uptime-monitoring heartbeats — see [[queue-job-visibility-and-errors]].
- **Minimum interval is 60 seconds.** Even a mapping with `interval = 10` re-fires no faster than once per poll cycle (60s). The mapping registry generally uses `interval ≥ 60`.
- **`single` doesn't prevent duplicate enqueues across cycles** if the previous row already cleared. It only prevents two RESERVED rows running at the same moment.

## Sample recurring-job cadences (excerpt)

A representative selection of mapping intervals (the full table lives on [[settings-queue-view]]):

| Mapping | Interval | Notes |
|---|---|---|
| `populate_<group>_tasks` | every 60 s | The poller itself. |
| `kill_long_process` | every 2 min | Terminates HTTP / worker processes exceeding the CPU-time budget. |
| `ping_workers` | every 2 min | Worker liveness ping for monitoring. |
| `delete_s3_object` | every 2 min | Deferred-deletion sweep for orphaned S3 objects. |
| `abandoned_all_cart_email` | every 3 min | Abandoned-cart reminder sweep. |
| `delete_cart_safe` | every 1 h | Removes carts older than the retention window. |
| `disable_all_expired_discounts` | every 1 h | Closes expired discounts. |
| `product_change_new_status` / `product_change_featured_status` | every 4 h | Demotes products from New / Featured flags. |
| `marketing_dashboard` | every 6 h | Triggers the collector chain for every active store. |
| `currency_sync` | every 12 h | Refreshes platform-wide exchange rates. |
| `subscription_payments` / `expire_subscriptions` / `ssl_*` | every 24 h | Daily platform-wide chores. |

One-shot jobs (no `interval`) are dispatched directly by domain-event subscribers or by the admin UI — they never enter the populate-poller's loop. See [[queue-job-lifecycle]] for the difference between recurring and one-shot paths.

## Related

- [[queue-job]] — hub.
- [[queue-job-storage]] — the `site_queue` row layout that the poller reads / writes.
- [[queue-job-lifecycle]] — Enqueued / Reserved phases triggered by the poller.
- [[queue-job-families]] — one poller per family; the family table lists all of them.
- [[queue-job-visibility-and-errors]] — the populate-poller is `single = true`; family workers report uptime.
- [[settings-queue-view]] — surface where merchants see populate-poller rows.

## Open Questions

None.
