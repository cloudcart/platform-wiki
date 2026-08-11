---
type: feature
nav_path: "Settings → Queue → Actions"
route_name: queue.settings
route_path: /admin/settings/queue-view
aliases: ["Queue actions", "Queue retry", "Queue stuck job", "Queue cancel"]
tags: [settings, queue, actions, diagnostics, support]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-queue-view]]. See the hub for the other aspects (page UI, visibility, running-detection, recurring jobs, queue families, event subscribers).

# Queue — what the merchant can / cannot do

## Purpose

Catalogue the **deliberately-absent affordances** on the Queue page and the **recommended actions** the merchant should take when a job looks stuck, failed, or stale. This page exists because the Queue view is read-only by design — the support LLM needs a precise list of *"you can't do X here, do Y instead"*.

## Where to find it

Sidebar → Settings → **Queue**. Route `/admin/settings/queue-view`. The recommendations below apply to the rows visible on that page.

## What the merchant can do here

The Queue page itself is observation-only — see [[settings-queue-view-page]] for the UI. Beyond that, the merchant's available actions all happen **off this page**:

- **Re-trigger a one-shot job** by re-running the originating action — uploading a fresh CSV on [[apps-csv-import]] schedules a new queue entry; re-submitting an XML sync from [[apps-xml-sync]] does the same.
- **Wait for the next scheduled run** for periodic jobs (XML feed regenerate, abandoned-cart sweep, search re-index, etc.) — they re-fire at `next_execution_at`.
- **Contact CloudCart support** for anything that looks truly stuck or harmful.

## Settings & fields

### Deliberately absent controls

| Control | Status | What the merchant does instead |
|---|---|---|
| Per-row retry button | Not present | Re-run from the originating page (e.g. re-upload the CSV on [[apps-csv-import]]). |
| Per-row cancel button | Not present | Contact CloudCart support — they can mark queue entries as failed, clear them, or move them to a recovery queue. |
| "Run now" / "Schedule manual run" | Not present | Periodic jobs only run at their `next_execution_at` time. |
| Bulk operations / row checkboxes | Not present | No bulk-action bar; the merchant cannot operate on many stuck jobs at once. |
| Filter / search input | Not present | Default sort is `id desc`; for many rows the only option is scrolling. Practical workaround: re-trigger the suspect job so its entry appears near the top after the next 12-s refresh. |
| Adjustable refresh interval | Not present | 12 s is hardcoded — see [[settings-queue-view-page]]. |
| Full error / stack-trace view | Not present | Only the error `message` is surfaced via the row tooltip. Full stack lives in the platform's internal logs. |
| Cross-site visibility | Not present | Page is hard-scoped to the current `site_id` — see [[settings-queue-view-visibility-rules]]. |

## Business rules

### Recommended action by job type

**Periodic jobs** (XML feed regenerate, abandoned-cart sweep, search re-index, currency sync, etc.):

- They re-fire at `next_execution_at`. Wait until that timestamp passes; if the job still fails or never runs, contact CloudCart support to inspect the queue state.
- The watchdog `kill_long_process` reclaims stuck rows within roughly 2–12 minutes — see [[settings-queue-view-running-detection]].
- Repeated stuck patterns on the SAME mapping are worth flagging to support — the underlying cause (poison message, bad data) won't fix itself.

**One-shot jobs triggered from an app screen** (CSV import, XML import, image-from-URL, redirects import, customer import, blog import, etc.):

- Re-run the action from the originating app. Uploading a fresh CSV schedules a new queue entry; the stuck old entry will eventually time out or be cleaned up by support.
- Cross-reference [[settings-import-history]] for import-specific status / error detail.

**Anything truly stuck or harmful**:

- Contact CloudCart support. They have direct database access and can manually mark queue entries as failed, clear them, or move them to a recovery queue. There is no self-service way to do this from the admin panel.

### CSV import staging tables — dropped after 72 hours

A separate housekeeping job (`delete_csv_tables`, runs once per 24 hours, marked NOT visible on this page) iterates over per-site `csv_import_*` tables and drops any table created more than 72 hours ago.

Practical impact for the merchant: once those staging tables are gone, a stuck CSV-import queue entry **cannot** be re-triggered from the old staging data — the merchant must re-upload the source CSV. This is independent from [[settings-import-history]] retention; history rows are kept indefinitely, only the temporary staging tables are pruned at 72 h.

### Failed periodic vs failed one-shot

- **Failed periodic** — the platform's internal scheduler may or may not auto-retry depending on the job class. Typically the job tries again at its next scheduled `next_execution_at`.
- **Failed one-shot** — may stay failed until the merchant re-triggers it from the originating screen (e.g. [[settings-import-history]] / [[apps-csv-import]]). There is no automatic per-row retry.

### Support cannot diagnose by browsing this page

Because the controller hard-codes `site_id = site('site_id')` and `is_visible = true`, even CloudCart support viewing this page within a specific store sees only that store's visible queue rows. For platform-level diagnosis (looking across all stores, seeing hidden internal jobs) support uses direct database access or internal monitoring — not this merchant-facing page. See [[settings-queue-view-visibility-rules]].

## Related

- [[settings-queue-view]] — hub.
- [[settings-queue-view-page]] — what the merchant DOES see on the page.
- [[settings-queue-view-running-detection]] — why a job stays in *Running* for up to ~12 minutes after a crash.
- [[settings-queue-view-visibility-rules]] — why hidden jobs don't appear here even when stuck.
- [[settings-import-history]] — import-specific re-trigger surface.
- [[apps-csv-import]] — CSV import re-trigger.
- [[apps-xml-sync]] — XML import re-trigger.

## Open questions

None.
