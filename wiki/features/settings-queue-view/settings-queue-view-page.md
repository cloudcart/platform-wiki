---
type: feature
nav_path: "Settings → Queue → Page UI"
route_name: queue.settings
route_path: /admin/settings/queue-view
aliases: ["Queue page UI", "Queue table", "Queue auto-refresh", "Queue error tooltip"]
tags: [settings, queue, ui, diagnostics]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-queue-view]]. See the hub for the other aspects (actions, visibility, running-detection, recurring jobs, queue families, event subscribers).

# Queue — page UI

## Purpose

Document exactly what the merchant sees on the Queue page: the four table columns, the 12-second auto-refresh, the error-tooltip pattern on failed rows, the binary status badge, and the deep-audit finding that this page has **zero** modals, wizards, drill-downs, retry buttons, or any other interactive affordance beyond hovering a row.

## Where to find it

Sidebar → Settings → **Queue**. Route `/admin/settings/queue-view`.

## What the merchant can do here

- See the queue entries for the current site, ordered `id` descending.
- Hover a row whose title shows a red exclamation icon to read the underlying error message.

Everything else is observation only — see [[settings-queue-view-actions]] for the full list of deliberately-absent affordances.

## Settings & fields

### Table columns

| Column | Field | What it shows |
|---|---|---|
| **Title** | `title_formatted` | Job title (e.g. *"Generate XML feed"*, *"Abandoned cart send"*, *"Search index rebuild"*). For failed rows, the title also appears in a `CcTooltip` triggered by a red `fa-exclamation-circle` icon; the tooltip body shows the error message. |
| **Last run** | `completed_at` | Most recent successful completion. Empty / null when the job has never completed. |
| **Next run** | `next_execution_at` | Next scheduled execution. Empty for one-shot jobs already completed. |
| **Is running** | `is_running` | Boolean. Renders as a single `CcBadge` — green **Running** when `true`, red ("critical" variant) **Pending** when `false`. |

The table is a flat `CcTable` with `hide-pagination=true` and `default-sorting` `id desc`. The API response is keyed by job mapping name on the backend; the client iterates `Object.values(queueData)` so all visible rows render at once with no virtualised scrolling. A store with 80 visible scheduled jobs renders 80 rows at once.

### Auto-refresh — every 12 seconds

The page uses a `setInterval(..., 12000)` on mount → `refetch`; `clearInterval` on unmount. There is no manual **Refresh** button, no "auto-refresh paused" indicator, and the interval is hardcoded (not adjustable). Polling continues silently even while the merchant interacts with the page.

The fetch goes to the database every cycle — no client-side cache between polls beyond standard Vue-Query staleness.

### Error tooltip on the Title column

Title renders in one of two modes based on whether the row has an `error` value (verify):

- **No error** → renders the raw `title_formatted` HTML.
- **Has error** → wraps the title in a `CcTooltip` with icon `fas fa-exclamation-circle text-red-500`, label text = `title_formatted`, tooltip text = the error `message` string.

This tooltip is the only diagnostic UI on the page. The full exception stack lives in the platform's internal logs and is not surfaced here.

### Status badge — binary only

The "Is running" badge is binary:

- `is_running = true` → green **Running**.
- `is_running = false` → red **Pending**.

"Pending" covers BOTH *"scheduled to run later"* (`next_execution_at` in the future) AND *"completed and idle"* (job has finished its work). The merchant infers which by reading the `Last run` and `Next run` timestamps. There is no intermediate *"Queued / waiting"* badge.

How `is_running` is computed is non-trivial — see [[settings-queue-view-running-detection]].

## Business rules

### No modals, no wizards, no drill-downs

Confirmed by deep audit of `SettingsQueuePage.vue` plus both child components (`SettingsQueueTitle.vue`, `SettingsQueueStatus.vue`): the page is a pure read-only listing with **zero** modal / dialog / wizard / drill-down panel. Rows are not clickable. There is no panel that shows the full payload, the full error stack, the originating event, or the worker that handled the job. See [[settings-queue-view-actions]] for the full inventory of absent controls.

### `mapping` and `class` fields ship to the frontend but are not rendered

The `mapping` (a key like `xml_feed_regenerate`) and `class` (the job class identifier) fields ARE shipped in the API response but the table renders only the formatted title to keep the merchant view simple. For support diagnosis these two values uniquely identify which job is involved — CloudCart support reads them directly from the API response.

### Backend sort vs frontend sort

The backend query fetches rows ordered by `reserved_at` descending (most-recently-attempted first). The Vue table applies its own `default-sorting` of `id desc`, so the rows the merchant sees are ordered by creation id (newest-created at the top) — NOT by last-run time. After the 12-second auto-refresh re-fetches, newly-created entries appear at the top.

### Job error message — `message` only, not full stack

When a job fails, the platform stores the failure as a JSON-encoded object on the queue row's `error` column (verify). The page surfaces only the `message` field via `title_formatted` and the tooltip. The full exception chain (file, line, stack trace, related causes) is preserved on the platform's separate exception log, not on this row.

## Related

- [[settings-queue-view]] — hub.
- [[settings-queue-view-actions]] — what's deliberately absent (retry, cancel, filter, search, bulk) and what the merchant can do instead.
- [[settings-queue-view-running-detection]] — how the binary `is_running` badge maps to the underlying reservation state.
- [[settings-queue-view-visibility-rules]] — what controls which rows are eligible to appear here.

## Open questions

None.
