---
type: feature
nav_path: "Apps → Google Sheets → Sync pipeline"
route_name: apps.google_sheets.tasks
route_path: /admin/apps/google_sheets/tasks
aliases: ["Google Sheets sync pipeline", "Sheets job queues", "Sheets sync concurrency", "Sheets live progress"]
tags: [apps, google, sheets, sync, queue, jobs]
plan_gates: ["google_sheets"]
created: 2026-06-10
updated: 2026-06-10
source_count: 7
---
# Google Sheets → Sync pipeline

> Part of [[apps-google-sheets]]. See the hub for related aspects (upload, download, OAuth, columns & filters).

## Purpose

Explains **how a Google Sheets sync actually runs** behind the Tasks tab: which background queues the jobs route through, the difference between the serial upload and the parallel download batch, how live progress reaches the merchant, the one-task-at-a-time rule, and the per-job plan / maintenance gating. The merchant doesn't configure any of this — it's the engine behind the **Upload** / **Download** buttons.

## Where to find it

Sidebar → Apps → Google Sheets → **Tasks tab** (`/admin/apps/google_sheets/tasks`). The merchant starts jobs here; this page documents what happens after the click. The button UI itself is on [[apps-google-sheets-tasks]].

## What the merchant can do here

- Start one **Upload** (CloudCart → Sheets) or one **Download** (Sheets → CloudCart) task at a time.
- Watch live progress in the **Status Message** column while a job runs (auto-refreshes every 5 seconds — see [[apps-google-sheets-tasks]]).
- Nothing to tune: there are no queue, concurrency, or retry settings exposed to the merchant.

### What the merchant CANNOT do here

- Run two sync tasks at once.
- Cancel an in-progress Download from the UI (the batch supports cancellation internally, but there's no Cancel button).
- Choose which queue the work runs on, or change retry counts.

## Settings & fields

No merchant-editable fields. The mechanics below are platform-fixed.

### The 4-step background pipeline (bidirectional)

| Direction | Background queue | What it does |
|---|---|---|
| `sheets_upload` | outbound (export) | CloudCart → Sheets — seeds the upload, writes the header, starts the export loop. |
| `sheets_export` | outbound (export) | CloudCart → Sheets — the repeating chunk writer (see [[apps-google-sheets-upload]]). |
| `sheets_download` | inbound (import) | Sheets → CloudCart — reads the whole sheet, fans out import chunks. |
| `sheets_import` | inbound (import) | Sheets → CloudCart — the parallel per-chunk importer (see [[apps-google-sheets-download]]). |

Outbound steps run on the shared export queue; inbound steps run on the shared import queue. These background queues are **shared with other apps' export / import work**, so heavy Sheets activity competes with other integrations and vice versa. All four steps allow concurrent execution at the worker level — but the platform still enforces the one-task-at-a-time rule below.

### Task statuses

A sync job carries one of four status values and two types:

- `STATUS_PENDING` (1) — queued, not yet started.
- `STATUS_RUNNING` (2) — currently executing.
- `STATUS_COMPLETED` (3) — finished successfully.
- `STATUS_FAILED` (4) — finished with errors.
- Types: `TYPE_UPLOAD` (1), `TYPE_DOWNLOAD` (2).

## Business rules

### One concurrent task at a time

The platform refuses to start a new sync if there's an unfinished task (status `PENDING` or `RUNNING`). Error: *"You have unfinished tasks. You can start a new task when there are no unfinished tasks!"* The merchant must wait for the in-flight task to finish or fail.

### Upload is serial; Download is parallel

- **Upload** runs as a two-phase serial pipeline — one seeding job, then a chunk-writer that re-dispatches itself 500 products at a time. This is why a large catalog uploads gradually. Full detail on [[apps-google-sheets-upload]].
- **Download** runs as a parallel background batch — the read step stages all rows, chunks them by 50, and creates one parallel import task per chunk, with a finalisation step at the end. Full detail on [[apps-google-sheets-download]].

### Live progress for running jobs

For RUNNING jobs the platform merges in live progress data. Parallel import tasks each atomically increment a shared counter in a fast key-value store (a single relational-database row would deadlock under parallel writes). Progress shows as *"Uploaded products: X of Y"* / *"Downloaded products: X of Y"*. If the fast store is unavailable, it falls back gracefully to the values stored in the main database.

### Deadlock-resilient per-product saves

Each product import retries its save up to 6 times on a database deadlock (clustered-database resilience). Combined with the 3-attempt per-product retry at the task level, a single product can be retried up to 18 times before being given up on. There is **no** auto-retry of the whole task, and **no** failure email — the merchant must check the Tasks tab to spot failures.

### Plan + maintenance gating: jobs skip silently

Each Upload / Download run checks the site state before touching Sheets:

- Plan expired? → returns `SITE_PLAN_EXPIRED`, no sync.
- Maintenance mode? → returns `SITE_MAINTENANCE`, no sync.
- Wrong platform / migrated? → returns `WRONG_PLATFORM`, no sync.
- Task deleted mid-flight? → returns `EXECUTE_DESTROY`, abort.

Tasks in these states sit but don't push to / pull from Sheets — the merchant must lift the underlying restriction (renew plan, exit maintenance) and queue a fresh task.

### Job-level error message persists to the Status Message column

When a job fails, its `status_message` is updated with the human-readable error, e.g. `Total products to upload: 1500: ERROR: Worksheet not found`. The Tasks table shows this column directly, so the merchant reads failure causes without digging into logs. Common messages: `Worksheet not found`, `Please, reconnect your google account.`, `Invalid Credentials. Please, reconnect your google account.` (the OAuth ones are covered on [[apps-google-sheets-oauth]]).

## Related

- [[apps-google-sheets]] — hub.
- [[apps-google-sheets-upload]] — the serial outbound pipeline.
- [[apps-google-sheets-download]] — the parallel inbound batch.
- [[apps-google-sheets-tasks]] — the Tasks tab UI (buttons, table, polling).
- [[apps-google-sheets-oauth]] — auth-related job failures.

## Open questions

(None currently outstanding for this page.)
