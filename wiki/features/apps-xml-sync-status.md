---
type: feature
nav_path: "Apps → XML Sync → Status"
route_name: apps.xml_sync.status
route_path: /admin/apps/xml_sync/status/:id
aliases: ["XML Sync Status", "XML Sync progress", "Xml Sync per-task status"]
tags: [apps, imports, xml, sync, status, progress, monitoring]
plan_gates: ["xml_sync_limit"]
created: 2026-05-21
updated: 2026-11-09
source_count: 5
---
# XML Sync → Status

## Purpose

The **Status** page is the per-task progress and monitoring view for an XML Sync task. After [[apps-xml-sync-step3]] has saved the task config, this is where the merchant monitors progress (rows parsed, created, updated, deactivated, deleted, errors), views run history, sees the next scheduled run time, and sees plan-feature usage (sync-task slot consumption + per-sync product totals). The `:id` URL parameter is the task ID. It uses the same status pattern as [[apps-xml-import-status]].

For the full feature set, see [[apps-xml-sync]].

## Where to find it

Sidebar → Apps → XML Sync → click on a task → Status. Route: `/admin/apps/xml_sync/status/:id`.

## What the merchant can do here

- **Activate / Deactivate** button (page header) — switches XML Sync's schedule on or off for the **whole store**, not this task (see Business rules).
- **Last updated** — when the most recent run finished.
- **Next execution** — for active recurring tasks, when the next auto-run is scheduled.
- **History link** — drill into run history.
- **Plan-feature usage** — shows current product usage / limit / percentage, with text *"Your package allows total <b>{limit}</b> products for all tasks"* when a total is set, plus an upgrade CTA when approaching the cap.

The product cap is shared across all sync tasks — 3 sync tasks each pulling 500 products = 1500 total, and the plan's product cap applies to that sum. The upgrade modal opens via the CTA; after payment, limits refresh automatically.

### Run history (per-sync)

Each historical sync execution shows run date / time, duration, and statistics (rows parsed / created / updated / deactivated / deleted / failed) plus per-row error drill-down. For recurring syncs, history accumulates one row per scheduled run — useful for spotting trends (e.g., "the supplier's feed shrank by 30% last week").

The History link opens the **shared import history page** (a separate page, not an inline expansion). It lists every product record this sync task processed across runs. Clicking a row opens a wide details panel showing the imported data plus any exception captured during processing. The Status page itself only shows aggregate counts; per-row error text and failed-row detail are one click away in History.

### What the merchant CANNOT do here

- Edit task config — go back to Step 2 / Step 3.
- Delete the task — delete via [[apps-xml-sync-settings]].
- Force a sync that exceeds the plan's product cap — upgrade required.

## Settings & fields

### Status response

| Field | Notes |
|---|---|
| **active** | Whether the store's XML Sync schedule exists (all tasks), not this task's own switch; the button then reads Deactivate. |
| **last_update** | Timestamp of last sync completion. |
| **next_update** | Timestamp of next scheduled run. |
| **history** | URL / route to per-task run history. |
| **with_task** | Boolean — status data availability (gates display when no status data exists). |

`last_update` and `next_update` are stored in UTC and converted to the site's configured timezone before they reach the page — no client-side conversion is needed.

### Feature usage

| Field | Notes |
|---|---|
| **featureTotalProducts.current** | Current product count across all sync tasks. |
| **featureTotalProducts.limit** | Plan-imposed maximum. |

## Business rules

### Recurring schedule respected

A task whose list switch is on runs on the store's schedule. The header button does not run a task early: **Deactivate** removes the schedule for every task, **Activate** puts it back.

### Next execution is shared across all sync tasks

All sync tasks share one parser tick for the whole app, so the **Next execution** time shown on a per-task Status page is actually the next tick for every active task, not just the one being viewed. Each tick scans every active task.

### Stop is app-level — it halts ALL sync tasks for the store

**Deactivate** stops **every** sync task on the store, not just the one viewed, and turns off no task's switch, so the list still shows them on. To pause one task, use its switch on [[apps-xml-sync-settings]]; that task's page can still read **Deactivate** and show a Next execution time, because both describe the store's schedule, while the parser skips the task.

### No rollback on Stop

**Deactivate** cancels the store's pending XML Sync work without changing any task's switch; products already written stay. The merchant restores via product backup or manual cleanup.

### Plan-feature gating across tasks

The plan caps the number of **active sync tasks** (`xml_sync_limit`) AND, separately, the **total products processed** across all sync tasks (the product allowance shown above). Adding or activating tasks beyond `xml_sync_limit` is blocked up front; the **product limit** is enforced inside the sync run itself — see *Errors and notifications* below for exactly what happens when it is reached.

The total-products counter that drives the plan cap counts every synced product still on the store, **including products from previously-deleted tasks**. Deleting a sync task does NOT decrement this counter — the merchant must delete those products themselves to free up plan headroom.

### Errors and notifications

- **Fetch failures → in-CP alert, NO email.** On a fetch problem — connection / ping failure, HTTP non-200, or empty feed — the platform pushes an in-CP admin notification (visible in the notifications dropdown) but does **not** send an email. The alert is keyed `xml_sync_curl_error_{task_id}` or `xml_sync_empty_feed_{task_id}`; the same key suppresses duplicate alerts for the same task within a short window, so 5 consecutive 404s produce one notification, not five. Fetch errors also surface via the task's `error` field on the listing and the History details panel.
- **Product limit reached → in-CP notification AND email.** This is a separate event from a fetch failure. When a run would sync **more products than the plan's product limit** allows, the sync **processes only the products up to the cap and stops there — the products above the limit are NOT processed** (silently dropped from that run; the rest completes with the allowed products). The platform then raises an in-app notification **and emails the store**: *"The limit was reached by application XML Sync."* So the "no email" rule above is about fetch failures only — a reached **product limit does email** the merchant. To sync the remaining products, raise the product allowance (product feature pack — see [[plan-vs-feature-pack]]) and let the next run pick them up.

### Per-sync product diff is by record list, not field diff

The History grid shows WHICH products changed in a run, but does not present a per-field "old vs new" diff. The details panel shows the imported payload; comparing against the pre-sync state requires the merchant to know what the product looked like before.

### History accumulates

Recurring syncs accumulate history quickly (a daily sync produces 365 history rows per year per task). The Status page typically shows recent history with pagination; older entries may be archived (verify retention).

### Permission

Standard apps permission scope.

## Related

- [[apps-xml-sync]] — XML Sync hub.
- [[apps-xml-sync-settings]] — task list.
- [[apps-xml-sync-step2]] / [[apps-xml-sync-step3]] — wizard.
- [[apps-xml-sync-features]] — features docs.
- [[apps-xml-import-status]] — parallel page in one-time XML Import.
- [[plan]] — plan definitions.

## Open questions

_None._
