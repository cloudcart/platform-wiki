---
type: feature
nav_path: "Settings → Import history → List tab"
route_name: history-list
route_path: /admin/settings/import-history
aliases: ["Import history list tab", "Import history root tab", "Import history jobs list", "Import history main view"]
tags: [settings, import, history, list, jobs]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---

> Part of [[settings-import-history]]. See the hub for the other aspects (Details tab, change-log modal, action states, storage / retention).

# Import history — List tab

## Purpose

The default landing tab of the Import history page. Shows one row per past import job with five aggregate counts (Created / Updated / No action / Errors / Total), the job name, and the job's start date. The merchant uses this tab to scan recent imports at a glance, spot the one with errors, and click straight into the relevant subset of records on the Details tab.

## Where to find it

Sidebar → Settings → **Import history**. The List tab is the default route — the same URL `/admin/settings/import-history` serves both the page root and the list view.

## What the merchant can do here

- Read the seven-column row for every past import (date, name, four action counts, total).
- Click any cell except *Total* and *Date* to drill into the Details tab — see [[settings-import-history-details-view]] for what the Details tab shows.
- Use the per-action count cells (Created / Updated / No action / Errors) as a **pre-filter shortcut** — clicking *Errors=12* opens Details with the Action chip set to `Error` so only those 12 rows render.
- Watch the Pending count tick down on successive manual refreshes as a poor-man's progress indicator for an in-flight import — see [[settings-import-history-action-states]].
- Sort columns (default: `created_at desc`).
- Use server-side pagination at the bottom of the table.

What the merchant **cannot** do from the List tab:

- Re-trigger or retry the import — re-imports happen on the originator screen ([[apps-csv-import]], [[apps-xml-import-settings]], etc.).
- Delete a row — there is intentionally no row-delete or bulk-delete affordance on this tab (see [[settings-import-history-storage-and-retention]]).
- Cancel a still-running import — that's controlled from the originator app or [[settings-queue-view]].
- Compare two imports side-by-side.

## Settings & fields

### List-table columns

| Column | What it shows |
|--------|---------------|
| **Date** (`created_at`) | When the import job row was inserted — i.e. when the merchant kicked it off from the originating app, not the completion time. So a long-running import shows the *start* moment; comparing it against the still-rising counts is the merchant's manual way to estimate progress. |
| **Name** (`name`) | Display name computed from the linked app (e.g. *"Szamlazz - Daily sync"*, *"CSV products import 2026-05-20"*) rather than the internal `mapping` code. Clickable — opens the Details tab. |
| **Created** | Number of new records this import added. Clickable — opens Details with `Action = Created`. |
| **Updated** | Number of existing records this import modified. Clickable — opens Details with `Action = Updated`. |
| **No action** | Number of records scanned that already matched the payload (nothing to do). Clickable — opens Details with `Action = Skip`. |
| **Errors** | Number of records the importer couldn't apply (validation failure, missing dependency, integration timeout, etc.). Clickable — opens Details with `Action = Error`. |
| **Total** | `created + updated + no_action + errors (+ pending while running)`. Non-clickable plain number. |

`Date` and `Total` are the only non-link cells. Every other cell is a deep-link into Details, and the action-count cells additionally pre-populate the Details Action filter chip.

### Total = processed + pending — what the merchant actually sees

While an import is running, the API response carries both a `processed` count (sum of created + updated + no-action + error) and a `pending` count (the platform code). The Total column the merchant sees is the upper bound. Once the import finishes, `processed = total` and `pending = 0`. Watching pending tick down to zero on successive manual page refreshes is the official "is it done yet?" workflow — the List tab does **not** auto-refresh.

### Default sort and pagination

Default sort: `created_at desc` — most recent import at the top. The table is paginated server-side via the standard `Grid` page-size control. A merchant with years of imports browses page by page; the underlying record count is unbounded — see [[settings-import-history-storage-and-retention]].

### No retry / no delete / no cancel — by design

There is intentionally **NO retry-row button**, **NO bulk-retry**, **NO row-delete**, and **NO row-cancel** affordance on the List tab. The page is read-only audit. To re-process records the merchant must fix the source data and re-run the import from the originating app's screen. To clean up old rows the merchant must contact CloudCart support — see [[settings-import-history-storage-and-retention]] for the rationale.

## Business rules

### Date is start-time, not finish-time

The `created_at` value on the row is when the import job *row* was inserted — typically the moment the merchant kicked off the import from the originator app. It is **not** the completion time. A long-running import shows a *Date* far earlier than when its counts finally settle.

### Counts are real-time accurate

The importer bumps each count atomically (one increment per processed record). Even with high parallelism the create / update / no-action / error counts stay consistent — no lost updates. So the numbers the merchant sees while a job runs reflect actual progress, not eventually-consistent estimates.

### Pending shows up only while a job is in flight

If the merchant browses the List tab after every import has finished, no row will show a pending count (`pending = 0` is hidden). Pending appears in the Total computation only while at least one record has been seen but not yet processed.

### All staff see the same history

Rows are store-scoped, not staff-scoped. Every administrator and moderator who has the Settings permission sees the same list — see [[settings-import-history-storage-and-retention]] for permission-scope details.

## Related

- [[settings-import-history]] — hub.
- [[settings-import-history-details-view]] — what each row links into.
- [[settings-import-history-action-states]] — the five action states the count cells expose as pre-filters.
- [[settings-import-history-storage-and-retention]] — why row counts grow unbounded and how the `Name` column is computed.
- [[settings-queue-view]] — sister page for live-running and queued jobs (auto-refreshing, unlike this tab).

## Open questions

None.
