---
type: feature
nav_path: "Apps → XML Import → Status"
route_name: apps.xml_import.status
route_path: /admin/apps/xml_import/status/:id
aliases: ["XML Import Status", "XML Import progress", "Xml Import per-task status"]
tags: [apps, imports, xml, status, progress, monitoring, plan-gated]
plan_gates: ["xml_import_limit"]
created: 2026-05-21
updated: 2026-05-27
source_count: 3
---
# XML Import → Status

## Purpose

The **Status** page is the **per-task progress + monitoring view**. After the merchant has completed the wizard ([[apps-xml-import-step2]] + [[apps-xml-import-step3]]) and saved the task, this is where they:
- Trigger the task to run.
- Monitor real-time progress (rows parsed, created, updated, skipped, errors).
- View the run history (each historical execution with its statistics).
- See the next scheduled execution time (if recurring is set up).
- See plan-feature usage (how many total products imported across all tasks vs plan limit).

The `:id` URL parameter is the task ID. Uses the shared `TaskStatus` component (typical pattern for background-job apps).

For the full feature set, see [[apps-xml-import]].

## Where to find it

Sidebar → Apps → XML Import → click on a task → Status. Route: `/admin/apps/xml_import/status/:id`.

## What the merchant can do here

### TaskStatus module

Top of page, hosts the primary task controls:
- **Start / Stop button** — triggers / interrupts the task. Loading state during state change.
- **Last updated** timestamp — when the last execution finished.
- **Next execution** timestamp — for recurring tasks, when the next run is scheduled.
- **History link** — drill into run history.
- **Has status info** flag — gates whether status data is available.

### Plan-feature usage

Below the TaskStatus module, a feature usage section shows:
- *"Your package allows total <b>{limit}</b> products for all tasks"* — when `featureTotalProducts` is set.
- Current usage / limit / percentage.
- If usage is approaching the limit, an upgrade CTA appears.

### Plan feature modal

When the merchant hits the plan limit (via the upgrade CTA), the `PlanFeature` modal opens in place to show upgrade pricing and unlock more capacity; after payment (`handleAfterPay`) the limit refreshes. Full gate semantics: [[apps-xml-import-plan-gates]].

### What the merchant CANNOT do here
- Edit task config from this view — go back to Step 2 / Step 3.
- Delete the task from this view — delete via [[apps-xml-import-settings]].
- Force a task above the plan limit without upgrading first.

## Settings & fields

### Status response data

| Field | Notes |
|---|---|
| **active** | Boolean — whether the task is currently running. |
| **last_update** | Timestamp of last execution end. |
| **next_update** | Timestamp of next scheduled execution (recurring tasks). |
| **history** | URL / route to per-task run history. |
| **with_task** | Boolean — whether status data is available. |

### Feature usage data

| Field | Notes |
|---|---|
| **featureTotalProducts.current** | Current product count across all tasks. |
| **featureTotalProducts.limit** | Plan-imposed maximum. |

### Plan feature modal flow

Triggers via the upgrade CTA:
1. Modal opens with current plan + suggested upgrade.
2. The merchant confirms payment.
3. `handleAfterPay` reloads the status with the new limits.

## Business rules

### Per-task active / inactive

When `active = true`, the task is running. The merchant can stop it — useful when a bad import is running.

### Recurring task scheduling

`next_update` shows when the next auto-run happens (recurring tasks). The cadence itself is the platform 12h parser tick, not a per-task schedule — see [[apps-xml-import-job-pipeline]]. The merchant can manually trigger an early run before the schedule.

### Plan-feature gating

`featureTotalProducts` reflects the plan limit on total products imported across all tasks (not per-task): 5 tasks of 200 products = 1000 total, and a 1000 cap blocks further imports until the merchant upgrades. Full gate semantics: [[apps-xml-import-plan-gates]].

### Side effects of Start / Stop

Start queues the import job; Stop cancels pending queue jobs and flips status to inactive. **Partial imports stay in CloudCart — already-written rows are not rolled back.** For the downstream consequences of a run (search re-index, webhooks, smart-collection re-evaluation, no undo) see [[apps-xml-import-side-effects]].

Permission: standard apps permission scope.

## Plan gates

The Status page enforces and surfaces the task-count cap (see [[plan-gates]], [[plan-vs-feature-pack]]):

| Mapping | Shape | What it controls on this screen |
|---|---|---|
| `xml_import_limit` | Numeric (max concurrent active tasks) | Start / activate from this view re-checks the cap — over cap returns HTTP 402 + opens the `PlanFeature` upgrade modal in place. After successful payment (`handleAfterPay`), the status is re-fetched with the new limits. |

The page also DISPLAYS (but does NOT directly enforce on Start) the cumulative product cap: `featureTotalProducts.current` vs `featureTotalProducts.limit`, sourced from the platform's `xml_import_total_products` plan-feature. The product-cap enforcement runs inside the importer pipeline, not on Start.

### When the product limit is reached during a run

When a run would import **more products than the plan's product limit** (`xml_import_total_products`) allows, the importer **processes only the products up to the cap and stops there — the products above the limit are NOT processed** (they are silently dropped from that run, not imported; the rest of the run completes normally with the allowed products). At the same time the platform raises an **in-app notification AND an email** to the store: *"The limit was reached by application XML Import."* To import the remaining products the merchant must raise the product allowance (buy the product feature pack — see [[plan-vs-feature-pack]]) and re-run. Upsell flows route through [[plan-features]].

## Related

- [[apps-xml-import]] — XML Import hub.
- [[apps-xml-import-settings]] — task list (parent).
- [[apps-xml-import-step2]] / [[apps-xml-import-step3]] — wizard steps that built this task.
- [[apps-xml-import-features]] — feature docs.
- [[plan]] — plan definitions that gate the product-total limit.
- [[plan-gates]] / [[plan-features]] / [[plan-vs-feature-pack]] — gating concept + upsell + extension.
- [[apps-xml-sync-status]] — parallel page in XML Sync.

## How it works (verified against backend)

These are the behaviours specific to the Status screen. For the parse → insert pipeline and cadence see [[apps-xml-import-job-pipeline]]; for downstream effects and the no-rollback rule see [[apps-xml-import-side-effects]]; for the 402 upsell flow and cumulative cap see [[apps-xml-import-plan-gates]].

### History link opens a separate per-task records grid

The History link routes to the **shared Importer history page** (`admin.importer.history.list.items`) — a separate page, not an in-place expansion. It lists every product record this task processed, with the task's name in the header. Each row links to a per-record details panel that opens inline, showing the imported product's data plus any exception captured during processing. Failed records appear in the same grid with their exception text. The Status page itself does NOT show per-row errors — the merchant drills in via History.

### Next-run timestamp is the whole-app parser tick

`next_update` is the next execution time of the single shared parser tick — there is one schedule for all tasks, so a task's "next run" is really the next tick for the whole app. Because the parser scans all active tasks per tick, this is also when this task runs again. There is no per-task schedule editor; recurring-cadence configuration lives in [[apps-xml-sync]]. Cadence and concurrency details: [[apps-xml-import-job-pipeline]].

### `grand_total_products` shows cross-task usage

The Status response includes `grand_total_products` — every product on the store whose `app_import` field begins with `xml_import`, across ALL XML Import tasks (including deleted tasks' leftover products). This is the value compared against the plan's `xml_import_total_products` cap; deleting a task does NOT decrement it.

### Displayed timestamps are converted to the store timezone

Both `last_update` and `next_update` are stored in UTC and converted to the site's configured timezone (`site('timezone')`) before serialisation, so the displayed times match the merchant's expectations without client-side conversion.

### Start / Stop on Status are app-level, not task-level

The Start/Stop control calls the app-level `apps.xml_import.change-status` route. "Start" re-installs the shared parser; "Stop" uninstalls it (drops the queue mappings + clears the global import records). So **Stop from this view halts ALL XML Import tasks for the store**, not just the one being viewed. To pause a single task, the merchant uses the Active toggle on [[apps-xml-import-settings]].

## Open questions

_None._
