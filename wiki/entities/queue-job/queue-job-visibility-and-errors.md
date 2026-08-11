---
type: entity
aliases: ["Job visibility flag", "is_visible queue", "single=true global lock", "Queue error preservation", "Worker uptime monitoring", "Stuck single-lock"]
tags: [settings, ops, jobs, queue, background, visibility, errors, monitoring, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[queue-job]]. See the hub for related aspects (persistent storage, populate-poller, lifecycle, families, priority tiers).

# Queue Job — visibility, single-lock, error preservation

## Identity

Three orthogonal rules determine what the merchant sees on [[settings-queue-view]] and how stuck jobs recover:

1. **`visible`** decides whether the job appears on Queue View at all.
2. **`single = true`** prevents concurrent platform-wide execution of housekeeping jobs and creates the "stuck single-lock" failure mode.
3. **Error preservation** rules govern how long a failed job's error message remains visible to the merchant.

A fourth subsystem — **worker uptime monitoring** — is invisible to the merchant but is the safety net that catches whole-family outages and pages on-call engineering. This page documents all four.

## Aliases

- **`visible = true` / `false`** — the mapping registry flag.
- **`single = true` global lock** — the platform-wide concurrency guard.
- **Stuck single-lock** — the most common single-lock failure (worker crashed mid-execution).
- **Error preservation** — how long the error column survives.
- **Worker uptime ping** — the per-family heartbeat into the monitoring system.

## Key Attributes

| Attribute | Notes |
|-----------|-------|
| **`visible`** (bool) | If `false`, the job runs but is hidden from [[settings-queue-view]]. Most platform housekeeping is `visible = false`. |
| **`single`** (bool) | If `true`, a platform-wide lock prevents a second worker from picking up the job. Used by `currency_sync`, `subscription_payments`, all `populate_*_tasks`, etc. |
| **Single-lock release window** | The lock is bound to the row's reservation; it auto-releases when `reserved_at + retry_after` expires (~10 minutes). See [[queue-job-storage]] for the window mechanics. |
| **Error column behaviour (recurring)** | On the next successful run, the error column is cleared. Recurring jobs that fail repeatedly accumulate only the latest error (no history). |
| **Error column behaviour (one-shot)** | Stays forever. The merchant can re-run from the originating screen, but the failed row remains until support cleans it up. |
| **Worker uptime ping URL** | Each queue family has a heartbeat URL pinged after every successful job execution. Missed pings raise an alert to on-call engineering. |

## Where it appears

- [[settings-queue-view]] — only `visible = true` rows render.
- [[settings-import-history]] — per-import error message reads from the same error column.
- [[settings-hooks]] — webhook-delivery failures show their error in this column.

## The `visible` flag — what merchants see vs what runs

Each mapping carries a `visible` flag. Only `visible = true` jobs render on [[settings-queue-view]]. The platform's split (representative — full catalogue lives on [[background-queue-inventory]]):

**Visible (~20-40 rows on a typical store):**

- All imports (`erp_imports`, `products_import`, `customers_import`, `blog_import`, `redirects_import`, CSV variants)
- `currency_sync`, `subscription_payments`, `subscription_payments_notify`, `expire_subscriptions`
- `populate_*_tasks` (the populate-pollers themselves)
- `reseller_payouts`, `settlement_batch`

**Hidden (~100 rows running invisibly):**

- `disable_all_expired_discounts`, `abandoned_all_cart_email`, `clear_all_old_carts`, `delete_cart_safe`
- `statistic_records`, `delete_csv_tables`, `delete_s3_object`, `delete_temporary_product_*`
- All image-processing (`product_variants_images`, `image_from_url`, `text_image_from_url`, `product_image_color`, `product_primary_image_update`)
- All `kill_long_process`, `ping_workers`, `handle_*`
- All statistics aggregations (`statistics_orders_*`, `sites_*`)
- `admin_notify`, all marketing-dashboard / analytics / segment / search-index aggregators
- All SSL renewal jobs, modoboa sync, `expire_free_sites_notify`, `expire_offers`, `offer_tasks`
- `send_pending_events_for_approval`

So a merchant browsing [[settings-queue-view]] sees roughly 20-40 rows, not the full ~140 platform jobs running invisibly. The hidden ones are housekeeping noise that the merchant cannot influence — surfacing them would only generate confused support tickets.

## The `single = true` global lock

Jobs marked `single = true` (`currency_sync`, `subscription_payments`, all `populate_*_tasks`, `expire_subscriptions`, `marketing_dashboard`, `kill_long_process`, etc.) check for an existing in-flight execution before they enqueue. If one is already running, the populate-poller skips this cycle.

Combined with the ~10-minute `retry_after` window (see [[queue-job-storage]]), a crashed worker can hold a `single` lock for up to that window before the lock auto-releases. This is the most common cause of *"why is the currency_sync stuck?"* tickets — a worker crashed mid-execution; the merchant must wait ~10 minutes or ask support to release the lock.

`single = true` jobs always land on the family's base queue (no priority suffix) and run once platform-wide — see [[queue-job-priority-tiers]] for why priority routing skips them.

## Error preservation rules

A job's error column lives on the `site_queue` row and is preserved until the row is deleted:

- **Recurring + next success → cleared.** The next successful run UPDATEs the error column to NULL.
- **Recurring + repeated failure → latest only.** Each failure OVERWRITES the previous error. No failure history.
- **One-shot + failure → permanent.** The row stays in Failed indefinitely. The merchant can re-trigger from the originating screen (which creates a NEW row), but the failed row remains until support cleans it up.

The Queue View tooltip shows only the `message` field of the error payload. The full payload (message plus diagnostic context) lives in the platform's exception logs, accessible to support engineering only — never surfaced to merchants.

When a merchant asks *"why did this job fail?"*, the answer should always start by reading the tooltip on [[settings-queue-view]]; if more context is needed, support pulls the platform exception log entry. See [[queue-job-lifecycle]] for which lifecycle phase the error column is populated in.

## Worker uptime monitoring

Each queue family has an uptime-monitoring heartbeat URL. The platform pings the heartbeat after every successful job execution; the monitoring system raises an alert if no ping arrives within the expected interval.

So if `import10` workers stop processing for 5+ minutes:

1. The heartbeat URL stops being pinged.
2. The monitoring system raises an alert.
3. On-call engineering is paged.
4. The merchant sees the symptom (their import never runs) but the cause (worker daemon down on a specific machine) is invisible to them.

This is why merchants reporting "my import is stuck" rarely need worker-restart instructions — the monitoring system is already paging engineering before the merchant notices. See [[queue-job-families]] for the per-family worker-group mapping that the monitor watches.

## Three rules summarised

| Rule | What it controls | Merchant-visible? |
|------|------------------|-------------------|
| `visible` | Whether the job row shows on Queue View | Directly (`visible = true` rows render; `false` does not) |
| `single = true` | Whether more than one execution can run concurrently | Indirectly (stuck single-lock manifests as a single row stuck in `Is running = yes` for ~10 minutes) |
| Error preservation | How long the last error message is shown | Directly (tooltip on Queue View; cleared on next success for recurring jobs) |

## Related

- [[queue-job]] — hub.
- [[queue-job-storage]] — the `retry_after` window that releases stuck single-locks.
- [[queue-job-populate-poller]] — every populate-poller is `single = true`.
- [[queue-job-lifecycle]] — Failed and Stuck phases tie back to the rules here.
- [[queue-job-families]] — per-family uptime monitoring.
- [[queue-job-priority-tiers]] — `single = true` bypasses priority routing.
- [[settings-queue-view]] — the surface the rules govern.
- [[background-queue-inventory]] — full visible / hidden catalogue.

## Open Questions

None.
