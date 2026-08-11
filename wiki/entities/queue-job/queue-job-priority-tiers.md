---
type: entity
aliases: ["Priority queue", "Queue priority tiers", "Plan-tier queue routing", "Numeric suffix priority", "system1 system9", "import2 import9", "Priority feature"]
tags: [settings, ops, jobs, queue, background, priority, plan-gates, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[queue-job]]. See the hub for related aspects (persistent storage, populate-poller, lifecycle, families, visibility).

# Queue Job — plan-tier priority routing

## Identity

Each queue family in CloudCart has up to **10 numerically-suffixed siblings** (`<name>`, `<name>1`, … `<name>9`, sometimes `<name>10`). When a job is dispatched, the platform looks up a `<feature>-priority` value (1-9) from the merchant's active plan features and routes the job onto the corresponding numbered queue. Higher-numbered queues are processed by workers configured to prioritise them — so a merchant on the highest plan tier sees their imports / exports / segments / campaigns start running noticeably sooner than a merchant on a lower tier.

This is invisible to the merchant — there is no UI control for "priority". But it is the architectural reason CloudCart can offer **"priority queue"** as a tier feature on the higher plans.

For the family catalogue (which families have which suffixes), see [[queue-job-families]].

## Aliases

- **Priority queue** — the merchant-facing plan-feature label.
- **Queue priority tiers** — generic term.
- **Plan-tier queue routing** — engineering term.
- **`<feature>-priority`** — the underlying plan-feature key (e.g., `imports-priority`, `campaigns-priority`).
- **`system1` … `system9`** / **`import2` … `import9`** — concrete examples of suffixed queue names on Queue View.

## Key Attributes

| Attribute | Notes |
|-----------|-------|
| **`<feature>-priority` plan feature key** | Numeric value 1-9 attached to the merchant's active plan. The dispatcher reads this and appends the digit to the family name when enqueueing. |
| **Default suffix** | The bare family name (no suffix) is the lowest tier. So a merchant on the free / lowest plan lands on `system`, `import`, `order-events`, `campaigns-messages` — no digit. |
| **Highest suffix** | Usually `9`, occasionally `10` for the very-top-tier families. The bare-name → `9`/`10` spread is roughly 10x throughput between worst and best tier. |
| **Worker concurrency** | Higher-suffixed queues are listened to by workers configured with more concurrent processes — so the throughput differential is built into the worker daemon config, not the queue infrastructure itself. |
| **Single-lock interaction** | `single = true` jobs do NOT use priority routing (they bypass the dispatcher's suffix selection) — they always land on the family's base queue and run once platform-wide. See [[queue-job-visibility-and-errors]] for the single-lock rules. |
| **Per-merchant variability** | The priority feature may differ across queue families on the same plan (e.g., a plan might grant `imports-priority = 8` but `campaigns-priority = 4`). |

## Where it appears

- [[settings-queue-view]] — each visible job row shows its full queue name including the suffix (e.g., `import7`, `campaigns-messages8`).
- [[plan-gates]] — the `<feature>-priority` feature keys live in the plan-features catalogue.
- [[settings-import-history]] — imports show which suffixed queue they ran on.

## How a job actually lands on a suffixed queue

The dispatch sequence for a one-shot job from a domain-event subscriber:

1. **Subscriber decides the family** — based on the job's category (e.g., "this is an import" → `import` family). Hard-coded in the subscriber.
2. **Dispatcher looks up the priority feature** — reads the merchant's plan-feature value for the family's priority key (e.g., `imports-priority`).
3. **Dispatcher appends the digit** — if the value is `7`, the queue name becomes `import7`. If the value is `1`, it becomes `import1`. If the value is missing or 0, it falls back to the base name `import`.
4. **Row written to `site_queue`** — the row's `queue` column is the suffixed name. See [[queue-job-storage]] for the row layout.
5. **Worker daemon picks up** — only workers configured to listen on the family pick the row, regardless of suffix. But workers tuned for the higher suffixes have more concurrency (so rows on `import9` clear faster than rows on `import`).

## Practical implications for the merchant

- **CSV imports start sooner on higher plans.** A 50 000-row product import on the lowest plan might wait minutes for a worker slot; on the highest plan it starts within seconds. The job content + duration is identical — only the queue dwell time changes.
- **Campaign sends complete faster on higher plans.** A 100 000-recipient email blast on `campaigns-messages9` finishes meaningfully sooner than the same blast on `campaigns-messages` — same per-message work, more workers per queue.
- **The merchant can't ask for "run this now."** Priority is plan-tier-driven, not per-action. The dispatcher does not accept a per-job priority override from the admin UI.
- **Upgrading the plan upgrades the priority on subsequent dispatches.** Rows already in `site_queue` keep their original suffix and finish on the old tier; future dispatches use the new tier.

## Single-lock jobs ignore priority

Jobs marked `single = true` — `currency_sync`, `subscription_payments`, `expire_subscriptions`, `marketing_dashboard`, every `populate_*_tasks` poller — land on the family's BASE queue (no suffix) and run once platform-wide. Priority routing only applies to **per-site dispatches**. A merchant on the highest plan sees `currency_sync` run at the same cadence as a merchant on the lowest plan — every 12 hours, on the `cc-system` family. See [[queue-job-visibility-and-errors]] for the full single-lock semantics.

## Why this design

Encoding priority into the queue name (instead of, say, a separate priority column on each row) lets the worker configuration be the single source of truth for throughput allocation. A capacity-planning change is a worker-config edit, not a change to the data store or the queue plumbing. It also means the per-family populate-poller doesn't need to understand priority at all — see [[queue-job-populate-poller]].

The merchant-facing trade-off is transparency: a merchant looking at [[settings-queue-view]] sees `import7` and has no obvious way to know `7` corresponds to their plan tier. Support staff with the plan-features map can decode this in seconds; merchants generally do not need to.

## Related

- [[queue-job]] — hub.
- [[queue-job-families]] — the family + suffix catalogue.
- [[queue-job-populate-poller]] — pollers land on the base family queue, ignoring priority.
- [[queue-job-visibility-and-errors]] — `single = true` jobs bypass priority routing.
- [[queue-job-storage]] — the suffixed queue name is persisted on the row.
- [[plan-gates]] — `<feature>-priority` plan-feature keys.
- [[settings-queue-view]] — the suffix is visible per row.

## Open Questions

None.
