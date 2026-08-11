---
type: feature
nav_path: "Apps → CSV Import → Row pipeline"
route_name: apps.csv_import.overview
route_path: /admin/apps/csv_import (background pipeline)
aliases: ["CSV Import — async row processing", "CSV Import — working lock", "CSV Import — finalize gate", "CSV Import — concurrent imports", "CSV Import — dispatcher"]
tags: [apps, imports, csv, pipeline, queues]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-csv-import]]. See the hub for the other aspects (wizard, task detail, final statuses, mapping fields, side effects, plan gates).

# CSV Import — async row pipeline

## Purpose

The row pipeline is the background plumbing that turns a saved import task into actual product / customer / subscriber / redirect / blog records. It runs entirely outside the request cycle: the wizard saves a task, the dispatcher batches rows into queue jobs, workers process each row, and a finalisation gate decides when the task is done. A `working` lock serialises imports to one per store.

This page covers the lock, the dispatcher, the row-job lifecycle, and the 3-flag finalisation gate. For terminal outcomes see [[apps-csv-import-final-statuses]]; for the live UI that surfaces this pipeline see [[apps-csv-import-task-detail]].

## Where to find it

There is no dedicated route — the pipeline runs in background workers triggered by the wizard save. The merchant observes it through the task-detail page's live progress card. See [[apps-csv-import-task-detail]] and [[settings-queue-view]].

## What the merchant can do here

The merchant doesn't interact with the pipeline directly. Their observable touchpoints:

- **Start a second import while one is running** — blocked by the `working` lock; the second upload gets rejected or queued behind the first. See *Business rules* below.
- **Watch live progress** — the progress doc is updated as rows process; the task-detail page polls every 5 seconds. See [[apps-csv-import-task-detail]].
- **Cancel mid-flight** — the Cancel button stops further row processing; already-imported rows survive (no rollback — see [[apps-csv-import-side-effects]]).
- **Navigate away and return** — the import keeps running on background workers; the task-detail page picks up the live state on next visit.

## Settings & fields

The pipeline reads from the saved `csv_tasks` row + the temporary staging table. Key internal fields:

| Field | What it does |
|---|---|
| `working` (manager flag) | Per-store boolean — true while an import is running. Acts as the concurrency lock. |
| `csvRows` | Total rows in the staging table after rollup. |
| `queued` | Per-row job-completion counter. |
| `dispatch_complete` | True once the dispatcher has finished queueing every batch. |
| Progress doc — `complete` / `total` / `info` | Live counters surfaced to the task-detail page's progress card. |

Two key manager methods drive the pipeline:

- `working: bool` — checks whether an import is currently running. Used to prevent concurrent imports.
- `finalizeIfComplete: bool` — checks if the in-progress import has all queued rows processed; finalises the task with a final status + human-readable message stored on `csv_tasks`.

## Business rules

### One concurrent import per store

The `working` lock prevents the merchant from starting a second import while one is in progress. This serialises imports — predictable execution + no DB contention. Concurrent-import serialisation is at the **manager level**, independent of the plan (high-tier plans don't get parallel imports). See [[apps-csv-import-plan-gates]].

### Async row processing — every row is a background job

Each row is queued as a background job. Large imports don't block the UI. The merchant can navigate away and return to see results without losing progress. Per-row jobs are dispatched in batches by the import dispatcher; workers process them on a CSV-import queue handled by the background worker pool. See [[background-queue-inventory]] for the queue inventory.

### Queue-worker context — the search index sync is always async

Because the import runs in a queue-worker (CLI) context, every the search re-index event the row processor fires gets dispatched to a `MakeSearchable` job on the `searchable-import4` queue — there is **no synchronous fast-path in this context**. The storefront lags the admin view until that queue catches up. This is the #1 source of "I imported and don't see it" tickets. See [[apps-csv-import-side-effects]].

### 3-flag finalisation gate — protects against the "momentary zero" race

The finalize step requires **all three** conditions to be true before declaring a task done:

1. `dispatch_complete = true` — the product-import dispatcher has finished queueing all batch jobs.
2. **No pending import records remain** for this app.
3. **Progress complete ≥ progress total** — the per-row completion counter has caught up.

Without all three, the finalize step waits. This protects against the **momentary-zero race** where the pending count drops to 0 between batch dispatches (the dispatcher may still be queueing more rows). Without the gate, a momentary zero between batches would prematurely finalise the task. Once all three are true, the task transitions to its final status — see [[apps-csv-import-final-statuses]].

### `finalizeIfComplete` runs after each queued row

The `finalizeIfComplete` method runs after each queued row is processed. It counts total `csvRows` vs `queued` (already processed). When `queued >= csvRows`, the task is marked complete. If `csvRows > 0` but `queued < csvRows`, more rows are still in flight.

### Polling cadence — 5 seconds while active

The task-detail page polls every 5 seconds while `is_active === true`. Once active flips false, polling stops. The merchant does not need to refresh. See [[apps-csv-import-task-detail]].

### `working = false` triggers orphaned-task finaliser

When something external halts the import (typically a plan-quota exception caught upstream), the manager's `setWorking(false)` path runs a separate `finalizeOrphanedTask` finaliser that marks the task `failed` with a specific plan-quota message rather than letting it linger in `in_progress`. See [[apps-csv-import-final-statuses]] for the message text and [[apps-csv-import-plan-gates]] for the quota source.

### Modern Vue UI on top of CcDomain

The integration uses modern Vue (CcDomain) — newer UI, TypeScript types. Different from older XML Import which uses legacy Vue. The task-detail Vue stack consumes the same backend pipeline this page describes.

## Related

- [[apps-csv-import]] — hub.
- [[apps-csv-import-task-detail]] — the live UI surfaced on top of this pipeline.
- [[apps-csv-import-final-statuses]] — the four terminal outcomes the finalisation gate resolves to.
- [[apps-csv-import-side-effects]] — the search index sync + webhook ordering downstream of each row.
- [[apps-csv-import-plan-gates]] — the plan-quota source that triggers the orphaned-task finaliser.
- [[settings-queue-view]] — the background queue view.
- [[background-queue-inventory]] — catalogue of background processes including the CSV-import queue.

## Open questions

_None._
