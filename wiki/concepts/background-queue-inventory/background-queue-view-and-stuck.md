---
type: concept
nav_path: "Concept → Background processes → Queue View + stuck process diagnosis"
aliases: ["Queue View visibility", "Stuck process", "Watchdog", "kill_long_process", "Hung process", "Background process retry", "Plan-tier priority", "Shared queue priority"]
tags: [background, async, troubleshooting, support, queue-view, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[background-queue-inventory]]. See the hub for related aspects (recurring platform jobs, imports/exports, the search index sync, order side-effects, process catalogue).

# Background processes — Queue View visibility + stuck-process diagnosis

## Definition

[[settings-queue-view]] is the merchant's **read-only diagnostics surface** for background processes. It does not list every background process the platform runs — only the ones flagged visible because the merchant has an actionable interest in their progress. This aspect documents the visibility rules, the per-row layout, the 10 / 30-minute stuck-process thresholds, the watchdog that automatically kills hung workers, the retry behaviour for recurring vs on-demand failures, and the plan-tier priority that governs shared-queue order.

The single most important rule: **a process showing Running for more than 10 minutes is suspicious; for more than 30 minutes, escalate to support.** The platform's watchdog (every 2 minutes) kills hung workers automatically, so a stuck row past 30 minutes points to a deeper issue — not just a worker that hung.

## Scope

Covered:

- The per-row layout on Queue View (Title, Last run, Next run, Status, Error message).
- The visible / hidden split — what surfaces and what runs silently.
- 10 / 30-minute thresholds for stuck-process diagnosis.
- Watchdog behaviour: kills hung workers every 2 minutes.
- Recurring-vs-on-demand retry semantics on Failed status.
- Plan-tier priority on shared queues.

Not covered:

- The inventory of which specific processes are visible — see each aspect ([[background-queue-recurring-platform]], [[background-queue-imports-exports]], [[background-queue-order-side-effects]]) for per-process visibility flags, or the full catalogue [[background-queue-process-catalogue]].
- Single-process Failed remediation specifics (e.g., re-trigger an import) — see the originating aspect.
- The Cron daemon configuration — platform-internal.

## Contrasts

- **Visible process vs hidden process.** Visibility is a per-process flag. Visible processes get a row on Queue View; hidden ones still run identically but are not surfaced. The merchant cannot toggle visibility — it is fixed per process by the platform.
- **Running vs Failed.** **Running** means the platform has started the process and it has not finished. **Failed** means the platform tried to run it and an error occurred. A Failed row carries a one-line summary in the Error message column; a Running row that has been running far too long is *probably* hung but not Failed (the watchdog will mark it Failed when it kills the worker).
- **Recurring retry vs on-demand retry.** Failed recurring processes automatically retry on the next schedule (every 3 min, every hour, every day — whatever the cadence is). Failed on-demand processes **stay failed** — the merchant must re-trigger (re-upload the CSV, re-click Export, re-paste the image URL).

## Where it applies

### Queue View row layout

For visible processes, the merchant sees a row with these columns:

- **Title** — human-readable name of the process (e.g., "Subscription renewals", "Currency exchange-rate sync", "CSV product import — `customers.csv`").
- **Last run** — when the process last completed.
- **Next run** — when the process is scheduled to run again (for recurring processes; blank for on-demand).
- **Status** — running / idle / failed.
- **Error message** — only when the last run failed; the merchant sees a one-line summary, not a stack trace.

Hidden processes still run — they're just not surfaced on the Queue View screen because they are platform-internal housekeeping the merchant has no actionable role in.

### When a process is "stuck"

If a visible process shows **Running** for more than **10 minutes**, it's likely the underlying worker daemon has crashed and the process is holding a lock. The diagnostic sequence:

1. **Wait a few minutes and refresh.** The watchdog (which runs every 2 minutes) kills hung processes automatically. After the next watchdog tick, a hung worker is killed, the lock releases, and the process either restarts (recurring) or moves to Failed status (on-demand).
2. **If still Running after 30 minutes, contact support.** This is a platform-side issue — the watchdog has tried and failed to kill the worker, or the process is genuinely active but pathologically slow (very large import, very large segment recalculation).
3. **For Failed status:** recurring processes automatically retry on the next scheduled run. On-demand processes (imports, exports, image fetches) stay failed — the merchant can re-trigger them.

### Watchdog mechanics

The watchdog is itself a recurring background process — it runs every 2 minutes (see [[background-queue-recurring-platform]]). Its job is to inspect long-running processes and kill any that have exceeded their per-process budget. This means:

- A merchant complaining about a stuck process at minute 5 is **probably premature** — the watchdog hasn't necessarily ticked yet, and the budget for the specific process may not have elapsed.
- A stuck process at minute 12 has likely been caught by the watchdog; the merchant should refresh.
- A still-stuck process at minute 30 has survived multiple watchdog passes — escalate.

Worker daemons also report their health every 2 minutes (the **Worker health probe** internal process — see [[background-queue-process-catalogue]]). When a worker stops reporting, the platform on-call team gets paged. The merchant does not see this.

### Plan-tier priority on shared queues

For shared on-demand queues (imports, exports, image fetching, campaign delivery), **higher-tier merchants are processed before lower-tier merchants**. So a CC Master merchant uploading a CSV at the same time as a Starter Pack merchant will finish first.

There is no merchant-configurable override — the priority follows the plan tier:

- CC Master / higher → highest priority.
- Mid-tier plans → standard priority.
- Starter Pack / lowest → lowest priority.

This applies only to **shared** queues. Single-platform-wide-locked processes (subscription renewals, settlement batches, SSL renewal) run in a fixed schedule order regardless of plan.

**What this means for support.** A Starter Pack merchant who says *"my CSV import has been waiting 10 minutes while a higher-tier merchant uploaded the same time"* is observing expected behaviour, not a bug. The wait time is a function of overall platform load + the merchant's plan tier. There is no documented SLA the merchant can quote.

### What the merchant should do

For any stuck-looking process:

1. Refresh Queue View after waiting a few minutes.
2. If still Running past 30 minutes — escalate to support.
3. If Failed and the process is recurring — wait for the next scheduled run.
4. If Failed and the process is on-demand — re-trigger (re-upload the file / re-click the button).
5. For the search index-related "old version on storefront" lag — see [[background-queue-search-sync]] (Queue View does **not** surface search-index sync; the diagnostic flow is different).

## Related

- [[background-queue-inventory]] — hub.
- [[settings-queue-view]] — the diagnostics surface this aspect documents.
- [[settings-import-history]] — drill-down for import-specific failures.
- [[queue-job]] — the entity for a single job's lifecycle.
- [[background-queue-recurring-platform]] — the recurring jobs visible / hidden on Queue View.
- [[background-queue-imports-exports]] — on-demand jobs and their failure semantics.
- [[background-queue-search-sync]] — the not-surfaced-on-Queue-View case for storefront lag.
- [[background-queue-process-catalogue]] — internal-identifier reference.

## Open Questions

- The exact per-process budget the watchdog enforces is not documented — the 10 / 30-minute thresholds above are merchant-side guidance, not the watchdog's actual budget. Worth capturing once verified (verify).
