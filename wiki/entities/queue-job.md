---
type: entity
aliases: ["Queue job", "Background job", "Scheduled job", "Worker task", "Queued task", "Cron job", "Опашкова задача", "Фонова задача", "Планирана задача"]
tags: [settings, ops, jobs, queue, background, entity]
created: 2026-05-21
updated: 2026-06-10
source_count: 12
---
# Queue Job

## Identity

A **Queue Job** is one unit of background work the platform performs OFF the merchant's request thread — a periodic chore (recurring every N seconds, hours, or once per day), a one-shot heavy task triggered by the merchant (CSV import, customer export, bulk delete, ERP sync), a delayed follow-up to a domain event (analytics denormalisation, webhook delivery, abandoned-cart sweep), or platform housekeeping (currency rates refresh, expired discounts cleanup, S3 file migration).

The merchant rarely interacts with Queue Jobs directly — most of the time they exist as invisible plumbing that makes the admin UI feel fast. Where the merchant DOES see them is on [[settings-queue-view]] (Sidebar → Settings → Queue), a read-only diagnostics surface listing the platform's visible jobs for the current store with last-run, next-run, is-running, and any inline error message.

A Queue Job is distinct from a synchronous request (which blocks until done) and from a domain Event (which is the in-process trigger that dispatches the job). The triplet **Event → Subscriber → Queue Job** is the universal pattern: a request fires an Event, a Subscriber listens, the Subscriber dispatches Jobs to one or more queues, and a Worker picks each Job up. See [[notification-delivery]] for the full diagram of how this fans out across email, SMS, webhooks, analytics, and admin alerts.

CloudCart's queue layer has six defining characteristics, each covered on its own sub-page:

- It uses **persistent background-job records** (not a transient queue that empties as jobs are picked up) — see [[queue-job-storage]].
- Recurring jobs are scheduled by an **interval-based populate-poller**, not by a fixed-time scheduler — see [[queue-job-populate-poller]].
- Every job follows a 7-phase **lifecycle** from Mapped to Completed (or Failed / Stuck) — see [[queue-job-lifecycle]].
- Jobs land on **queue families** with dedicated worker groups — see [[queue-job-families]].
- Each family's numeric suffix encodes the merchant's **plan-tier priority** — see [[queue-job-priority-tiers]].
- **Visibility, single-lock, and error preservation** rules decide what the merchant sees and how stuck jobs recover — see [[queue-job-visibility-and-errors]].

## Aliases

- **Queue job** / **Background job** / **Scheduled job** — interchangeable in product copy and support tickets.
- **Worker task** / **Queued task** — used by engineers.
- **Cron job** — informal merchant phrasing (technically inaccurate — CloudCart uses interval-based polling, not crontab — but the intent is the same: "the recurring thing that runs automatically").
- **Опашкова задача** / **Фонова задача** / **Планирана задача** — Bulgarian labels.

## Key Attributes

The fields below appear on every Queue Job row — surfaced selectively on [[settings-queue-view]] and used by support when diagnosing tickets. The merchant cannot edit any of them.

| Attribute | Notes |
|-----------|-------|
| **Mapping** (`mapping`) | A short code key like `currency_sync`, `products_import_csv`, `marketing_dashboard`, `expire_subscriptions`. Identifies which job is wired to this row. Not rendered in the table but is what support uses to locate the specific job. |
| **Title** (`title_formatted`) | Merchant-readable job name shown on [[settings-queue-view]]. If the last run errored, the platform appends *"The job has error: `<message>`"* inline so the merchant can hover for the tooltip. |
| **Queue name** (`queue`) | Which queue this job runs on (`system`, `system7`, `import6`, `order-events8`, `cc-system7`, `campaigns-messages9`, etc.). The numeric suffix maps to plan tier — see [[queue-job-priority-tiers]]. |
| **Interval** (`interval`, seconds) | For recurring jobs: how often the populate-poller re-enqueues this mapping. `null` means "one-shot" (only dispatched on demand). See [[queue-job-populate-poller]] for the schedule mechanics. |
| **Last run** (`completed_at`) | Most-recent successful completion timestamp. Empty if the job has never finished. |
| **Next run** (`next_execution_at`) | When the populate-poller will next enqueue this mapping. Computed as `completed_at + interval`. |
| **Is running** (`is_running`) | Derived: a reservation timestamp is set, the reservation window has not expired, and the row is not yet available again. See [[queue-job-storage]] for the ~10-minute window. |
| **Single** (`single`, bool) | If `true`, only ONE concurrent execution platform-wide — see [[queue-job-visibility-and-errors]]. |
| **Visible** (`visible`, bool) | If `false`, the job runs but is HIDDEN from [[settings-queue-view]] — see [[queue-job-visibility-and-errors]]. |
| **Error** (`error`) | If the last attempt failed, holds an encoded error payload. Only the message is surfaced on Queue View; full stack lives in platform exception logs. |
| **Site scope** (`site_id`) | Per-store jobs reference the site; platform-wide single jobs leave it null. See [[queue-job-families]]. |

## Where it appears

- [[settings-queue-view]] — the merchant's read-only diagnostics list (visible jobs for the current site).
- [[settings-import-history]] — one specific import job's history + status.
- [[settings-hooks]] — webhook delivery jobs run on the `order-events` family — see [[queue-job-families]].
- [[settings-admin-notifications]] — admin-notify jobs run on the `system` family.
- [[apps-csv-import]] — origin page for CSV-import jobs.
- [[customers-export]] / [[orders-export]] — origin pages for export jobs.
- [[apps-xml-feed-generator]] / [[apps-xml-import-settings]] — XML feed jobs.

## Sub-pages (in this cluster)

This entity is split into 6 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question rather than read every page.

- [[queue-job-storage]] — the persistent background-job store; durable records vs a transient queue; the `retry_after` window; per-environment queue connections.
- [[queue-job-populate-poller]] — interval-based scheduling via the `populate_*_tasks` engine; why CloudCart does NOT use a fixed-time scheduler; the 60-second cycle.
- [[queue-job-lifecycle]] — the 7 phases (Mapped → Enqueued → Reserved → Running → Completed / Failed / Stuck) and what each phase means on Queue View.
- [[queue-job-families]] — queue families (`default`, `email`, `system`, `cc-system`, `import`, `order-events`, `analytics`, `product-images`, `install`, `export`, `segments`, `subscribers`, `campaigns*`, `translate`, `tmp`, `cloudio`, `the search engine`) + worker-group mapping + per-site vs platform-wide scope.
- [[queue-job-priority-tiers]] — numeric suffix (`system1` … `system9`) encodes the merchant's plan-tier priority; how that routes their imports / exports / campaigns to a faster sub-queue.
- [[queue-job-visibility-and-errors]] — the `visible` flag (which jobs show on Queue View); `single=true` global lock; error preservation; uptime / worker monitoring.

## Related

### Related entities

- [[webhook]] — webhook delivery is implemented as Queue Jobs on the `order-events` family — see [[queue-job-families]].
- [[order]] — order-status domain events dispatch Queue Jobs.
- [[admin-notification]] — admin alerts surface from `admin_notify` Queue Jobs.
- [[campaign]] — every marketing campaign send is a chain of per-recipient Queue Jobs.
- [[subscriber]] — subscriber imports + segment assignments are Queue Jobs.
- [[customer]] — RFM aggregation runs as a Queue Job.

### Cross-cutting concepts

- [[notification-delivery]] — the Event → Subscriber → Queue Job pattern in detail with the exact queue map.
- [[plan-gates]] — plan-tier numeric priority determines which sub-queue a merchant's jobs land on — see [[queue-job-priority-tiers]].
- [[background-queue-inventory]] — catalogue of every background process the platform runs; pairs with this entity page (lifecycle of one job) by listing every job TYPE, its schedule, and its visibility on Queue View.
- [[order-processing-pipeline]] — order-processing side-effects fan out to these queue-jobs (discount usage sync, customer income, hook send, send notification).

## Open Questions

No outstanding questions — all items resolved or removed.
