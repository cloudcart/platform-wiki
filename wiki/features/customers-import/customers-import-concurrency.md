---
type: feature
nav_path: "Customers → Import → Concurrency & cancel"
route_name: admin.complete.import
route_path: /admin/api/core/imports/cancel/{type}
aliases: ["Customer import concurrent lock", "Customer import 409", "Reset stuck import", "Import auto-recovery", "Stuck import self-healing", "Cancel customer import", "Concurrent import lock"]
tags: [customers, import, concurrency, lock, cancel, self-healing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[customers-import]]. See the hub for related aspects (wizard, fields, processing, side effects, plan gates, API alternative).

# Import customers — concurrency lock + self-healing + cancel

## Purpose

CloudCart's import subsystem allows **only one running CSV import per store at a time** — across customers, products, redirects, blog, and subscribers. This page covers the lock mechanism the merchant hits when a previous import is still active (or stuck), the **three** auto-recovery triggers that silently reset stale state, and the cancel endpoint that does the full teardown.

## Where to find it

- The **409 error + "Reset stuck import" action** surfaces in the wizard's STEP 1 ([[customers-import-wizard]]) when the merchant clicks **Next** and another import is running.
- The cancel endpoint is `POST /admin/api/core/imports/cancel/{type}` — invoked from the **Reset stuck import** action in the 409 response or from [[settings-queue-view]] / [[settings-import-history]].

## What the merchant can do here

- **Retry the import** — auto-recovery checks (below) run BEFORE the 409 is returned, so a stale lock is silently cleared on the next attempt.
- **Click "Reset stuck import"** — surfaced in the 409 response's `actions` array; hits the cancel endpoint and tears down the running task.
- **Wait for the previous import to finish** — once `working = false`, the next Step 1 Submit succeeds.

The merchant **CANNOT** run two imports simultaneously by any path (separate browser tabs, separate admin users, separate import types). The lock is global per store.

## Settings & fields

| Lock state field | Where stored | Default | Meaning |
|------------------|--------------|---------|---------|
| `working` | Per-store import manager state | `false` | `true` when a CSV import is in progress (any type). |
| `current_task_id` | Per-store import manager state | `null` | The id of the active `csv_tasks` row. |
| `dispatch_complete` | Per-store import manager state | — | Cleared on cancel so pending finalization jobs find nothing to update. |
| Progress doc timestamp | Per-store import manager progress doc | — | Rewritten by the running job on every batch; staleness > 30 min is one of the auto-recovery triggers. |

## Business rules

### Concurrent-import lock

Only one CSV import (across customers, products, redirects, blog, subscribers) can be running per store at a time. If another import is already in progress, the upload step returns an HTTP **409** with the error message *"Another import is already running. Please cancel it before starting a new one."* plus an `actions` array containing a *"Reset stuck import"* button that hits `/admin/api/core/imports/cancel/{type}`. The merchant must wait for the running import to finish (or use the cancel action) before starting a new one.

The 409 path explicitly **does NOT create a `pending` `csv_tasks` row** — this was added to prevent orphaned temp tables on retries. So a 409 is a true no-op on the back-end: no temp table, no task row, no queue entry.

### Self-healing for stuck imports (auto-recovery — 3 triggers)

Before returning the 409, the platform attempts auto-recovery if the running-import flag is stale. **Any one** of the three triggers declares the state stale and silently resets it (the merchant doesn't see any of this — they just retry the import and it succeeds):

1. **`current_task_id` references a task that is gone or in a terminal status** (cancelled / completed / failed) — most common when a worker dies mid-job and the cleanup never runs. Reason code: `task_terminal_or_missing` → message *"Auto-recovered: the referenced task was no longer running."*
2. **`working = true` but `current_task_id` is NULL** — split-brain state from a partial write. Reason code: `split_brain_no_task_id` → message *"Auto-recovered: stuck working flag with no active task."*
3. **Progress doc hasn't advanced in >30 minutes** — the progress timestamp is rewritten on every batch by the running job, so a real (even slow) import keeps it fresh. 30+ minutes without update means the worker is dead. Reason code: `progress_stale_30min` → message *"Auto-recovered: no progress for more than 30 minutes."*

The auto-recovery writes the reason to the relevant `csv_tasks.message` so the [[settings-import-history]] detail page shows what happened. The **30-minute threshold is fixed** — merchants cannot adjust it.

### Cancelling a running import

The cancel endpoint (`POST /admin/api/core/imports/cancel/{type}`) does the full teardown:

1. Removes the queue entry so no further batches start.
2. Sets `working = false` (the running job's loop reads this on each batch iteration and exits on the next one — see [[customers-import-processing]]).
3. Drops the temp CSV table so any in-flight batch fails fast.
4. Clears `current_task_id` and `dispatch_complete` so any pending finalization jobs find nothing to update.
5. Marks all `in_progress` / `pending` `csv_tasks` rows as `cancelled` with the message *"Cancelled by user."*
6. Wipes the manager's progress doc.

Result: the next import attempt starts clean. Cancelled records remain visible in the import history with the cancelled status badge.

### Worker cooperative exit on cancel

The running job's batch loop checks the manager's `working` flag **before each batch iteration**. When cancel sets `working = false`, the job exits cleanly on the next iteration without finishing the remaining rows. **Already-imported customers stay** (no rollback — see [[customers-import-processing]] for the non-atomic guarantee); un-imported temp rows are dropped along with the temp table.

### What the 409 surfaces in the wizard

The Step 1 Submit handler ([[customers-import-wizard]]) inspects the response: on HTTP 400 with `response.data.message`, the modal shows the error inline at the bottom of the modal (red banner with exclamation icon). The 409 path additionally surfaces the `actions` array as clickable buttons in that same banner so the merchant can self-resolve without leaving the wizard.

## Related

- [[customers-import]] — hub.
- [[customers-import-wizard]] — the Step 1 Submit handler that displays the 409 inline.
- [[customers-import-processing]] — the running job that reads `working` on every batch and the temp-table lifecycle.
- [[customers-import-side-effects]] — already-imported customer rows that stay on cancel (no rollback).
- [[settings-import-history]] — where the `csv_tasks.message` reasons surface in the merchant UI.
- [[settings-queue-view]] — track import-job progress; manual cancel button.
- [[background-queue-inventory]] — catalogue of background processes; how to spot a stuck import.

## Open questions

(All resolved.)
