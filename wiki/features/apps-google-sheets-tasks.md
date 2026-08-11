---
type: feature
nav_path: "Apps → Google Sheets → Tasks"
route_name: apps.google_sheets.tasks
route_path: /admin/apps/google_sheets/tasks
aliases: ["Google Sheets Tasks", "Sheets sync history", "Sheets job log"]
tags: [apps, google, sheets, tasks, history, sync]
plan_gates: ["google_sheets"]
created: 2026-05-21
updated: 2026-06-10
source_count: 2
---
# Google Sheets → Tasks

> Part of [[apps-google-sheets]]. The Tasks tab is the **UI surface** for sync jobs. The engine behind the buttons (queues, concurrency, retries, live progress) is [[apps-google-sheets-sync-pipeline]]; auth-related job failures are [[apps-google-sheets-oauth]].

## Purpose

The **Tasks** tab is the **per-sync-job history view** — each row is one sync attempt between CloudCart and Google Sheets. From here the merchant **starts** new sync jobs (one **Upload** = CloudCart → Sheets, or one **Download** = Sheets → CloudCart) and **watches** them run. Each row shows the job type, status, timestamps, live progress text, a link to the spreadsheet, and a delete action.

This page documents the **screen** — the table, the buttons, the badges, the polling. What actually happens after the click (the job queues, the one-task rule, retry resilience) lives on [[apps-google-sheets-sync-pipeline]]; what each direction does to the data is on [[apps-google-sheets-upload]] + [[apps-google-sheets-download]].

## Where to find it

Sidebar → Apps → Google Sheets → **Tasks tab**. Route: `/admin/apps/google_sheets/tasks`. The tab is visible only after the merchant connects Google (see [[apps-google-sheets-oauth]]).

## What the merchant can do here

- **Start an Upload** — the up-arrow button (primary variant) pushes the catalog to the spreadsheet. Calls `/admin/api/google_sheets/new-task/1`.
- **Start a Download** — the down-arrow button (white variant) pulls merchant edits back. Calls `/admin/api/google_sheets/new-task/2`. A Download is rejected until at least one Upload has completed — see [[apps-google-sheets-download]].
- **Watch progress** — the Status Message column updates live while a job runs (the table auto-refreshes; below).
- **Open the spreadsheet** — the per-row link opens the configured Google Sheet in a new tab.
- **Remove a row** — delete a log entry from the history.

Both action buttons live in the top-right of the table header. Each shows a small spinner while its request is in flight. On success: a toast with the response message, then the table refreshes and the new task appears at the top (Pending → Running → Completed / Failed). On an `error` response: an error toast with no refresh.

### What the merchant CANNOT do here

- **Edit the synced data** — that means editing the Google Sheet directly, or the CloudCart product; the Tasks tab is read-only history.
- **Run two tasks at once** — the platform refuses a new task while one is unfinished (see [[apps-google-sheets-sync-pipeline]]).
- **Cancel an in-progress Download** — the batch supports cancellation internally, but there is **no** Cancel button in the UI. The merchant waits for the task to finish or fail.
- **Filter or search** — the table exposes no filter dropdowns or search box (below).

## Settings & fields

No merchant-editable settings live on this tab. The columns shown per task row:

| Column | Shows |
|---|---|
| **Created At** | When the task was queued. |
| **Type** | "Upload" or "Download" (localized label). |
| **Started At** | When the worker picked it up. |
| **Finished At** | When it ended (success or failure). |
| **Status** | Badge — Pending / Running / Completed / Failed. |
| **Status Message** | Live progress / final result text (below). |
| **Sheets link** | Opens the configured spreadsheet in a new tab. |
| **Remove** | Deletes the log row from CloudCart's database (does NOT touch the Sheet). |

**Status Message** carries the live progress while RUNNING and the outcome when finished:

- Upload: *"Uploaded products: X of Y"*.
- Download: *"Downloaded products: X of Y"*.
- Failure: the progress text plus *": ERROR: &lt;message&gt;"*, e.g. *"Total products to upload: 1500: ERROR: Worksheet not found"*. Common OAuth errors (*"Please, reconnect your google account."*) are covered on [[apps-google-sheets-oauth]].

## Business rules

### Auto-refresh while a task is unfinished (5-second poll)

When the server response reports an unfinished task, the Tasks UI schedules a re-fetch every **5 seconds** (loader suppressed) and stops polling automatically once nothing is unfinished. This delivers the live progress text in the **Status Message** column without WebSockets. There is no manual refresh / stop control.

### Status badge colours

The status badge renders in one of four variants by status value:

- Pending → grey badge.
- Running → purple "in-progress" badge with a small spinner.
- Completed → green badge.
- Failed → red badge.

### Per-row "Open in Sheets" deep link

The link cell opens the configured spreadsheet (the stored spreadsheet URL) in a new tab — tooltip *"Open the spreadsheet in Google Sheets"*. It is the **same URL on every row**: clicking from any task lands on the same spreadsheet, because Sheets has no per-task deep-linking.

### Per-row Remove (confirmation + cleanup only)

The Remove action shows a confirmation modal, then calls `/admin/api/google_sheets/delete/{id}`. On success the row disappears and the table re-fetches; on failure an error toast keeps the row. Remove deletes only the CloudCart-side log entry — it never edits or deletes anything in the spreadsheet. Used to tidy old completed / failed tasks.

### No filter / search; default sort newest-first

The table has filters disabled — no status dropdown, no date range, no search box. All tasks are listed, sorted by recency (newest first), paginated via the standard table footer. Merchants with a long history scroll or page through.

### Failed tasks are kept until the merchant deletes them

There is no automated retention — completed and failed tasks stay in the list forever, until the merchant uses Remove or disconnects Google (which wipes ALL job history — see [[apps-google-sheets-oauth]]). For long-running stores the list grows; periodic manual cleanup is on the merchant. The platform also sends **no** email when a task fails — the merchant has to check this tab to spot failures (see [[apps-google-sheets-sync-pipeline]]).

## Related

- [[apps-google-sheets]] — Google Sheets hub.
- [[apps-google-sheets-settings]] — credentials + spreadsheet config (the other tab).
- [[apps-google-sheets-sync-pipeline]] — the queue / concurrency / retry engine behind the buttons.
- [[apps-google-sheets-oauth]] — connect, auto-provisioning, and the reconnect / "Worksheet not found" errors that surface as failed tasks.
- [[apps-google-sheets-upload]] — what an Upload does to the spreadsheet.
- [[apps-google-sheets-download]] — what a Download does to the catalog (and the prior-upload requirement).

## Open questions

(None currently outstanding for this page.)
