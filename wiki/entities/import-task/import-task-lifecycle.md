---
type: entity
nav_path: "Entity → Import Task → Lifecycle"
aliases: ["Import task lifecycle", "Import task states", "Import task status transitions", "Single-import lock", "HTTP 409 import lock", "Cancel import task"]
tags: [entity, settings, ops, imports, lifecycle, states]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[import-task]]. See the hub for the other aspects (attributes, types + queues, processing model, provenance + recovery, history + webhooks).

# Import Task — Lifecycle

## Identity

The complete state machine an Import Task moves through, from the moment the merchant clicks **Import** in a source app to the final completed / failed / cancelled state — plus the **store-wide single-import lock** that allows only one Task to be in `processing` at a time per Site. Also documents what happens after completion (indefinite retention, no auto-cleanup, no "retry failed rows" affordance) and the operational consequences of the lock for merchants running concurrent imports.

## Aliases

- **Import task lifecycle** — the standard term for the state machine.
- **Import task statuses** — the named states.
- **Single-import lock** — the store-wide mutex held by any `processing` Task.
- **HTTP 409 import lock** — the error code returned when a second import is attempted while one is already running.

## Key Attributes

The Import Task moves through these six statuses:

| State | How to recognise | What it means |
|-------|------------------|---------------|
| **Pending (wizard in progress)** | Status = `pending`; the merchant is still in Step 1 (upload) or Step 2 (mapping) | The Task row exists with partial state; closing the wizard preserves the state for resume. The lock has NOT been acquired yet — another import can still start. |
| **Pending (queued)** | Status = `pending`; the wizard's Submit has been clicked | The Task is in the queue (`import1` / `import2` / app-specific — see [[import-task-types-and-queues]]) waiting for a worker. The single-import lock **IS** held by this Task — any other import attempt returns HTTP 409 *"There cannot be more than {N} imports running simultaneously."* |
| **Processing** | Status = `processing`; visible in [[settings-queue-view]] with live progress | A worker picked up the Task and is iterating chunks of 500 rows per pass (see [[import-task-processing-model]]). The `processed_rows` counter increments; the merchant sees live progress. The single-import lock continues to be held. |
| **Completed** | Status = `completed`; aggregate counts written | All rows processed (successfully or with per-row errors counted). Created / Updated / No-action / Errors / Total are written. The lock is released; the next queued Import Task (if any) can start. |
| **Failed** | Status = `failed`; no aggregate counts (or partial) | A critical error (corrupt CSV, database connectivity loss mid-batch) aborted the entire batch. The Task is marked `failed`; the lock is released. There is NO "retry failed rows" affordance — the merchant must fix the source data and run a new Task. |
| **Cancelled** | Status = `cancelled`; merchant clicked Cancel in [[settings-queue-view]] | Rows processed before cancellation are **KEPT** (no rollback); rows not yet processed are skipped. The lock is released. |

### The single-import lock

The lock is **store-wide, not per-type**: a customer CSV Task in `processing` blocks a product XML sync from starting (and vice versa). The lock isn't smart enough to allow parallelism between unrelated importers — the platform treats "any Import Task in `processing`" as occupying the slot. The merchant must wait for the running Task to finish (or cancel it from [[settings-queue-view]]) before launching a new one.

Why: concurrent imports would race for shared resources (temp tables, ERP staging buffers, search index rebuild slots, the per-record webhook fan-out queue — see [[import-task-history-and-webhooks]]) and would frequently corrupt one or both Tasks' state.

### HTTP 409 on concurrent attempt

Trying to start a second Import Task while one is already in `processing` for this Site returns HTTP 409 with the message *"There cannot be more than {N} imports running simultaneously."* The merchant waits for the running Task to finish (visible in [[settings-queue-view]]) or cancels it to release the lock.

### Wizard-step persistence (resume support)

If the merchant closes the browser mid-mapping, the Task remains in `pending (wizard)` state with the partial field mapping saved. Reopening the source app lets the merchant pick up where they left off — the mapping dropdowns are pre-populated. See [[import-task-attributes]] for the per-field detail.

### What happens after Completion / Failure / Cancellation

- The Task and its record-level entries persist **indefinitely** in [[settings-import-history]]. There is no auto-cleanup, no TTL, no retention purge — see [[import-task-history-and-webhooks]] for the full retention rules.
- The provenance tag on the imported records persists forever — the merchant can use the "Imported with" filter months / years later. See [[import-task-provenance-and-recovery]].
- There is **NO "retry failed rows" affordance** on the Task. To re-attempt failures, the merchant fixes the source data and runs a **NEW** Import Task from the originating app.

### Side effects on Submit (transition from `pending-wizard` → `pending-queued`)

When the merchant clicks Submit on the wizard:

- The Task status flips from `pending-wizard` to `pending-queued`.
- The Task is enqueued on the appropriate queue (see [[import-task-types-and-queues]]).
- The single-import lock is acquired.
- The merchant's wizard shows the success confirmation: *"The file was successfully uploaded and the [type] import task was added to the queue. If you wish, you could track the uploading in the queued jobs."*
- The merchant CAN close the wizard — the worker runs regardless.

### Cancellation behaviour in detail

When the merchant clicks Cancel in [[settings-queue-view]]:

- The current 500-row chunk is allowed to finish (no mid-chunk abort).
- After the chunk finishes, the worker checks the cancellation flag and stops picking new chunks.
- Records already processed are KEPT — the platform does NOT roll them back. The merchant uses the **"Imported with"** filter (see [[import-task-provenance-and-recovery]]) to find and clean up the partial import.
- The action counts reflect only the rows processed before cancellation.

## Where it appears

- [[settings-queue-view]] — surfaces `pending-queued` and `processing` Tasks; the merchant cancels in-flight Tasks here.
- [[settings-import-history]] — surfaces completed / failed / cancelled Tasks indefinitely.
- All source apps ([[customers-import]] / [[apps-csv-import]] / [[apps-xml-import]] / [[apps-xml-sync]] / [[apps-json-import]] / [[apps-blog-csv-import]]) — return HTTP 409 when a second import is attempted under the lock.

## Related

- [[import-task]] — hub.
- [[import-task-attributes]] — the status enum + processed-rows counter that drives the progress display.
- [[import-task-processing-model]] — chunked 500-row processing that the lifecycle depends on.
- [[import-task-history-and-webhooks]] — indefinite retention after completion.
- [[import-task-provenance-and-recovery]] — recovery paths when a Task fails or is cancelled (the platform does NOT roll back partial imports).
- [[settings-queue-view]] — the merchant's window into in-flight Tasks.
- [[settings-import-history]] — the historical surface.
- [[import-pipeline]] — the platform-wide bulk-import pipeline; the lock is a property of the pipeline.

## Open Questions

- ⏸️ The exact behaviour when a merchant cancels a Task from [[settings-queue-view]] — rows already processed appear to be KEPT, but verify and document the merchant-visible state of the temp table (cleaned up vs orphaned) once the cancellation completes.
