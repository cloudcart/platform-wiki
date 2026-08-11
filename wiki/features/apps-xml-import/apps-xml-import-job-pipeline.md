---
type: feature
nav_path: "Apps → XML Import → Job pipeline"
route_name: apps.xml_import
route_path: /admin/apps/xml_import (backend pipeline; no UI)
aliases: ["XML Import job pipeline", "XML Import — Parse / ParseSingle / Insert", "XML Import — 12h tick", "XML Import — re-parse cadence", "XML Import — queue", "XML Import — insert chunking"]
tags: [apps, imports, xml, background-jobs, queue]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-xml-import]]. See the hub for the other aspects (wizard, fetch transport, mapping fields, plan gates, side effects).

# XML Import — job pipeline

## Purpose

Behind the wizard, XML Import runs a **3-stage background pipeline** that pulls the feed, formats each row, and writes products to the catalog. The pipeline is intentionally split — large feeds (100k+ products) would never fit in a single synchronous request — and each stage runs on a dedicated queue isolated from other imports so a slow XML feed doesn't starve CSV jobs.

This page documents the stages, the cadence rules (12h queue tick + 1h per-task gate), the dedicated queue, the insert-chunking strategy, and how the merchant manually triggers a re-parse. For what each stage WRITES into the catalog see [[apps-xml-import-mapping-fields]]; for what fires downstream see [[apps-xml-import-side-effects]].

## Where to find it

Apps → XML Import → Status — the only merchant-visible surface for the pipeline. Per-task progress + the active toggle live there. The job mechanics themselves are not exposed in the UI.

## What the merchant can do here

- Watch per-task progress as records are parsed and inserted.
- Toggle a task **Active** ON to enqueue an immediate parse.
- Cancel a running task — stops further processing but does NOT reverse rows already written.
- Force a re-parse by saving Step 3 again or toggling Active off/on (both clear the feed hash; see [[apps-xml-import-wizard]]).

What the merchant CANNOT do here:

- Change the 12h tick or the 1h per-task gate — both are hard-coded.
- Move tasks to a different queue or change priority manually (priority is plan-driven; see [[apps-xml-import-plan-gates]]).
- Pause and resume mid-record — only cancel.

## Settings & fields

Pipeline configuration is not merchant-facing. Operationally:

| Stage | Cadence / trigger | Queue |
|-------|-------------------|-------|
| `xml_import_parse` | Every **43200 s (12 h)** for active tasks | `import1` |
| `xml_import_parse_single` | Event-triggered per-record | `import1` |
| `xml_import_insert` | Event-triggered per 50-product chunk | `import1` |

The `import1` queue is **dedicated** — it does not share workers with the general `import` queue, which means a slow XML feed cannot starve CSV imports / other import jobs. See [[background-queue-inventory]] for the queue catalogue.

## Business rules

### 3-stage pipeline

The processing pipeline:

1. **Parse** (`xml_import_parse`) — runs every 12 hours for active tasks. Fetches the XML (see [[apps-xml-import-fetch-transport]]), identifies records, prepares the list of rows to process.
2. **ParseSingle** (`xml_import_parse_single`) — event-triggered per-record. Validates + formats one row through the FormatProduct helper into CloudCart-shaped product data.
3. **Insert** (`xml_import_insert`) — event-triggered. Writes the formatted record into `global_imports_records` for the generic Importer worker to pick up.

ParseSingle + Insert are **event-driven within a task run** — they do NOT wait for a clock; they fire as records flow through the pipeline.

### 12-hour queue tick

The merchant's XML feed is re-parsed **every 12 hours by default** for active tasks. Higher plans can override this interval — see [[apps-xml-import-plan-gates]] for plan-driven cadence.

### 1-hour per-task gate (additive on top of the 12h tick)

Even when the parser ticks every 12h, each individual task is gated by `last_cron_update`. A task is eligible for re-parse only if either:

- It has never run (`last_cron_update` is NULL), OR
- The last run is older than **1 hour** AND the task is marked `updatable` (Step 2's per-field Update checkbox is set on at least one field).

So a task that ran 30 minutes ago is skipped on the next tick. The 1h gate is hard-coded, not configurable per task.

### Plan-driven priority

Higher-plan merchants get higher priority in the queue (their tasks run first). When multiple merchants have active tasks queued, the worker picks up by plan tier. See [[apps-xml-import-plan-gates]] for the gating model.

### Concurrent tasks supported

Multiple XML Import tasks CAN run simultaneously (different supplier feeds in parallel). The plan caps task COUNT but doesn't enforce serial execution.

### Per-batch insert chunk = 50 products

Once Parse has produced the list of products to insert / update, it **chunks them into batches of 50** and dispatches one `xml_import_insert` job per chunk to `import1`. For a 10 000-product feed this creates 200 insert jobs. Each insert job parses its 50 XML snippets, formats them, and writes records to the generic importer's intermediate table for downstream pickup.

### Manual trigger via Status page

When the merchant flips a task's Active switch ON, the parser is enqueued immediately — no waiting for the 12h tick. Editing any Step 2/3 settings also clears the feed hash and last-update timestamp, forcing re-parse on the next tick. So the merchant CAN force a re-run by saving Step 3 again or toggling Active off/on. See [[apps-xml-import-wizard]] for the edit-clears-hash mechanics.

### Cancellation stops the queue but doesn't reverse writes

Cancelling a running task drains any subsequent `xml_import_parse_single` and `xml_import_insert` events for that task, but rows already written remain. The merchant must clean up manually. See [[apps-xml-import-side-effects]] for the no-rollback rule.

### Active-task check guards uninstall

A boolean check prevents uninstalling the app while a task is still active — the merchant must finish or cancel all running tasks first.

## Related

- [[apps-xml-import]] — hub.
- [[apps-xml-import-fetch-transport]] — what Parse calls to fetch the feed.
- [[apps-xml-import-wizard]] — how editing the task clears the feed hash and forces immediate re-parse.
- [[apps-xml-import-plan-gates]] — plan-driven priority + cadence overrides.
- [[apps-xml-import-status]] — the Status screen merchant-facing.
- [[background-queue-inventory]] — full catalogue of background processes; the `import1` queue lives there.
- [[apps-xml-import-side-effects]] — what fires after Insert (the search index sync, webhooks, smart-collection re-eval).

## Open questions

_None._
