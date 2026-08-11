---
type: feature
nav_path: "Settings → Queue"
route_name: queue.settings
route_path: /admin/settings/queue-view
aliases: ["Queue", "Queue list", "Queue view", "Background jobs", "Опашка", "Фонови задачи"]
tags: [settings, queue, jobs, background, diagnostics]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 12
---

# Queue

## Purpose

A read-only diagnostics page that lists the background-job entries the platform has scheduled or recently run for the store. The merchant uses it as a *"is the system working?"* pulse check — to see when each recurring job last ran, when it's scheduled to run next, whether it's currently running, and any error message attached to a failed run. Useful when the merchant is asking *"why hasn't my import finished?"*, *"why is my XML feed stale?"*, *"is the abandoned-cart pipeline actually firing?"*.

The page auto-refreshes every 12 seconds so the merchant can watch jobs progress in real time. Beyond that — no retry button, no cancel button, no row click-through, no filter / sort / search.

## Where to find it

Sidebar → Settings → **Queue**.

The page's breadcrumb reads *"Settings → Queue list"*. The route is `/admin/settings/queue-view`. The header icon is the list-ul icon.

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[settings-queue-view-page]] — the page UI: four table columns, 12-second auto-refresh, error-tooltip pattern on failed rows, binary Running / Pending badge, deep-audit finding of zero modals / wizards / drill-downs.
- [[settings-queue-view-actions]] — the **deliberately-absent** affordances (no retry, no cancel, no run-now, no bulk) and the recommended off-page actions when a job looks stuck.
- [[settings-queue-view-visibility-rules]] — the three filter layers (`settings.queue` permission → `site_id` hard-scope → `is_visible=true`) and the catalogue of jobs the platform ships visible vs hidden.
- [[settings-queue-view-running-detection]] — how the *Running / Pending* badge is computed (NOT a stored boolean), the 10-minute reservation retry window, and the 2-minute `kill_long_process` watchdog that reclaims stuck rows.
- [[settings-queue-view-recurring-jobs]] — the populate-poller engine that runs every 60 seconds (CloudCart does NOT use the application framework's Scheduler) plus the full table of recurring + one-shot mappings with their intervals and queues.
- [[settings-queue-view-queue-families]] — the 22 worker daemon groups, the queue families each one listens on, the numeric-suffix routing rule that makes higher plan tiers process work faster, and the UptimeRobot heartbeats.
- [[settings-queue-view-event-subscribers]] — how domain events fan out to queued jobs via the application framework Subscribers (order events → the platform code → `HooksSendRaw` per active webhook on `order-events8`).

## What the merchant can do here

- See the list of queue entries that are eligible to appear (per [[settings-queue-view-visibility-rules]]), ordered by `id` descending — most-recently-created at the top.
- See per-entry **Title**, **Last run** (`completed_at`), **Next run** (`next_execution_at`), and an **Is running** badge — see [[settings-queue-view-page]] for column details.
- Hover a failing row to read the error message in a tooltip — that's the only interactive affordance on the page.
- Watch the table auto-refresh every 12 seconds without manual page reload.

What the merchant **cannot** do here: cancel, retry, pause, run-now, drill-down, bulk-act, filter, sort, search, see hidden / internal jobs, or see jobs from other sites. The full catalogue of absent affordances and the recommended workarounds live on [[settings-queue-view-actions]].

## Settings & fields

This is a read-only page — no mutations, no inputs. The only top-level "knob" is the **12-second auto-refresh interval** (hardcoded — not adjustable). The four table columns and the binary status badge are documented on [[settings-queue-view-page]].

The merchant's plan tier indirectly affects what they see here: jobs that belong to a paid plan feature (e.g., XML import, ERP integrations) read a `<feature>-priority` value (1-9) and route onto the matching numeric-suffix queue, so higher tiers process work sooner. See [[settings-queue-view-queue-families]].

## Business rules (cluster-wide)

The cluster's rules are catalogued on the aspect pages. The headline rules:

- **Read-only by design.** No mutations exposed. Jobs are scheduled by event triggers + the populate-poller and processed by worker daemons. See [[settings-queue-view-actions]].
- **Three filter layers determine row eligibility.** Permission (`hasApiPermission:settings,settings.queue`) → per-site `site_id` hard-scope → `is_visible=true` flag per mapping (code-level, not merchant-toggleable). See [[settings-queue-view-visibility-rules]].
- **`is_running` is a derived state, not stored.** Approximately `reserved_at + retry_after_seconds ≥ now AND !available`, with `retry_after` configured at **610-630 seconds** (~10 min) on the queue connection. The `kill_long_process` watchdog runs every **2 minutes** and reclaims rows that a crashed worker left stuck — so a stuck row resolves within ~2-12 minutes without merchant intervention. See [[settings-queue-view-running-detection]].
- **Recurring jobs are NOT driven by the application framework Scheduler / crontab.** Every 60 seconds a set of `populate_*_tasks` jobs scan the mapping registry and enqueue any mapping whose `last completed_at + interval` has elapsed. The merchant-visible **Next run** is computed from this — NOT from a cron expression. See [[settings-queue-view-recurring-jobs]].
- **Numeric-suffix queue routing → plan tier priority.** Higher plan tiers route onto higher-suffix queues (e.g. `import6` → `import7` → `import8` → ... → `import10`), processed by workers with higher priority. Invisible to the merchant on this page, but is the architectural reason higher-tier merchants see their imports start running sooner. See [[settings-queue-view-queue-families]].
- **Error message inline only — full stack is not exposed.** When a row fails, the title cell shows a red `fa-exclamation-circle` icon; hovering reveals the error MESSAGE in a `CcTooltip`. The full exception chain (file, line, stack trace) lives in the platform's internal exception log, NOT on the row. For deep diagnosis the merchant must contact CloudCart support. See [[settings-queue-view-page]].
- **Webhook delivery jobs ride `order-events8`, not the per-site queue.** A single order save fans out to one webhook-delivery task per active subscribing webhook, all on the `order-events8` queue. Their visibility on this page depends on the per-mapping `is_visible` flag. See [[settings-queue-view-event-subscribers]].
- **"Single" jobs run platform-wide, not per site.** Mappings flagged `single => true` (e.g. `currency_sync`, `subscription_payments`, `expire_subscriptions`) run once with `site_id = NULL` covering the whole platform — not once per store. See [[settings-queue-view-recurring-jobs]].

## Related

- [[settings]] — parent hub.
- [[settings-hooks]] — webhook deliveries originate here and ride the `order-events8` queue.
- [[settings-import-history]] — product / order imports run on the queue; failures diagnosed by cross-referencing this page.
- [[import-pipeline]] — the bulk-import model whose CSV / XML / ERP jobs run on the import queues shown here.
- [[settings-cart]] — abandoned-cart reminder pipeline runs on the `system` queue.
- [[settings-general]] — storefront language change triggers `js:data-generate` and a search-engine re-index via `OnLanguageChange`.
- [[settings-files]] — chunked S3 uploads use the queue; aggregate exports trigger `file_download` notifications.
- [[settings-admin-notifications]] — admin notifications run on `admin_notify` / `system7`.
- [[settings-staff]] — `settings.queue` permission grant gates moderator access.
- [[settings-statuses]] — status-change notification emails / SMS dispatched by the platform code.
- [[apps-csv-import]] — CSV import is queued; its tasks appear here when visible.
- [[apps-xml-feed-generator]] — XML feed regeneration runs periodically on the queue.
- [[apps-xml-sync]] — XML supplier sync is queued.
- [[account-plan]] — plan tier controls numeric-suffix queue routing.
- [[queue-job]] — entity page.
- [[background-queue-inventory]] — catalogue of every background process the platform runs.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
