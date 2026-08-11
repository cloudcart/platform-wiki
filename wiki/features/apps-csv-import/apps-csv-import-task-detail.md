---
type: feature
nav_path: "Apps → CSV Import → Task detail"
route_name: apps.csv_import.task
route_path: /admin/apps/csv_import/task/{taskId}
aliases: ["CSV Import — task detail page", "CSV Import — task progress", "CSV Import — failed records", "CSV Import — column mapping table", "CSV Import — Cancel import"]
tags: [apps, imports, csv, task-detail]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-csv-import]]. See the hub for the other aspects (wizard, row pipeline, final statuses, mapping fields, side effects, plan gates).

# CSV Import — task detail page

## Purpose

The task-detail page is where the merchant watches a single CSV import run, cancels it, or post-mortems it. It shows a stack of cards covering header summary, mid-flight interruptions, live progress, per-row failures, and the column mapping the task is using. Polling refreshes the cards every 5 seconds while the task is active; once it finalises, polling stops.

This page covers what each card surfaces and how cancel + back-navigation work. For the underlying state machine that drives the live counts see [[apps-csv-import-row-pipeline]]; for the four terminal-status outcomes the task can resolve to see [[apps-csv-import-final-statuses]].

## Where to find it

Apps → CSV Import → List of imports → click any task row. The route includes the task id (`/admin/apps/csv_import/task/{taskId}`).

A **Back to imports** button in the page header routes to `apps.csv_import.settings` (the list view).

## What the merchant can do here

### Header summary

The header renders Task #ID + filename plus inline labels:

- **Type** — products / customers / subscribers / redirects / blog (see [[apps-csv-import-mapping-fields]]).
- **Status** — a status badge (Pending / Running / Completed / Failed) rendered by the `ApplicationsCsvImportStatusBadge` component.
- **Rows in CSV** — the raw row count of the uploaded file.
- **Imported** — clickable count; links to the products-list filter `import=csv-{taskId}-` so the merchant can see exactly which products this task created. See [[apps-csv-import-side-effects]] for the tag schema behind the filter.
- **Failed** — shown in red **only when > 0**.
- **Created** + **Updated** — timestamps.

Below the labels is a yellow message box rendered whenever `data.task.message` is non-empty. The message is the finalisation summary — plan-quota interruption text, "no importable rows" diagnosis, or the first failure's exception text (truncated to 250 chars). See [[apps-csv-import-final-statuses]] for the four outcomes that populate this field.

### Task interrupted card

Appears when the task row is `in_progress` but the manager reports the import is no longer actively running. The card explains the interruption (most often plan create-quota exception) and exposes a **Cancel import** button (red) that calls the CSV-import cancel mutation with the task type.

Confirmation is a native browser `window.confirm` with the text:
> *"Are you sure you want to cancel this import? This will stop the current task and clear its progress."*

Cancelling stops the task and clears its progress; partially-imported products survive (there is no rollback — see [[apps-csv-import-side-effects]]).

### Live progress card

Renders only while the task is active (`data.is_active === true`). Shows:

- `Progress: complete / total (NN%)` — live counter pulled from the import-progress doc.
- Optional `Message` — short status string from the row processor.
- Optional bulleted `info` list — per-product progress messages.
- A second **Cancel import** button at the bottom of the card.

### Failed-records card

Renders only when `failed_count > 0`. Header: `Failed records (N)`. The card holds a table with columns **Type**, **Tries**, **Error** (the exception text — truncated to 250 chars), **Date**. Footer when the table is sampled (typical when many failures):
> *"Showing first {shown} of {total} failed records."*

For full per-row exception text beyond the sampled set, the failed-records table is queryable from the backend — see [[apps-csv-import-final-statuses]].

### Column-mapping card

Shows the merchant's mapping (saved on the `csv_tasks` row as a JSON column). Three columns:

- **Field** — the CloudCart field name (e.g. `product.name`, `variant.parent_id`, `variant.quantity`).
- **CSV column** — `#N` for the matched column index, or `"not mapped"` when blank.
- **First row value** — the sample text from the staging table's first data row, or `(empty)` rendered in warning yellow, or `—` placeholder when no sample is available.

Footer note when sample data is missing:
> *"First-row sample is not available for this task (older import or empty CSV)."*

Multi-column mapping (e.g. `properties.name = [3, 5, 7]`) is shown as `3, 5, 7` with sample values joined by ` | `. See [[apps-csv-import-mapping-fields]] for multi-column semantics.

## Settings & fields

The task-detail page is read-only — it doesn't write to the `csv_tasks` row directly. The only mutation it dispatches is the cancel action. Visible task fields:

| Field | Source | What it shows |
|---|---|---|
| `id` + `filename` | csv_tasks | Header. |
| `type` | csv_tasks | Import-type badge. |
| `status` | csv_tasks | Status badge (pending / running / completed / failed). |
| `rows_in_csv` | csv_tasks | Raw row count. |
| `imported_count` | csv_tasks | Persisted post-finalisation. |
| `failed_count` | csv_tasks | Persisted post-finalisation. |
| `message` | csv_tasks | Human-readable finalisation summary. |
| `is_active` | manager-derived | Drives the live-progress card visibility + polling. |
| `progress.complete` / `progress.total` / `progress.info` | progress doc | Live counters. |
| `mapping` | csv_tasks (JSON) | Column-mapping table. |

## Business rules

### 5-second polling while active

While the task is active (`is_active === true`), the page polls every 5 seconds (`refetchInterval`). Once `is_active` flips false, polling stops automatically. The merchant does not need to refresh the page to see the final status — the post-cancel or post-finalise message appears within 5 seconds of the backend writing it.

### `message` field doubles as diagnosis

The yellow message box surfaces:

- *"Imported 1234 products successfully"* — full success.
- *"5 errors found — click to view"* — first-failure summary with details in the Failed-records card.
- *"No importable rows — every row was filtered out…"* — `total = 0` failure (see [[apps-csv-import-final-statuses]]).
- *"Import was interrupted before completion (imported X of Y). Common cause: plan create-quota was reached. Check your plan limits or contact support."* — plan-quota interruption.

### First-error summary is truncated to 250 chars

When per-row errors occur, only the **first** failure's exception text is captured for the task `message`, truncated to 250 characters. The full per-row exception list lives in the failed-records table (record_type `app_manager`). See [[apps-csv-import-final-statuses]].

### Cancel preserves already-imported rows

Cancelling stops further processing but does NOT roll back the products already written. The merchant uses the products-list `import=csv-{taskId}-` filter to bulk-delete the partial import if they want a clean retry. See [[apps-csv-import-side-effects]].

## Related

- [[apps-csv-import]] — hub.
- [[apps-csv-import-row-pipeline]] — the state machine + polling source.
- [[apps-csv-import-final-statuses]] — terminal outcomes that populate `status` and `message`.
- [[apps-csv-import-mapping-fields]] — what the column-mapping table is showing.
- [[apps-csv-import-side-effects]] — the `import=csv-{taskId}-` filter behind the Imported clickable count.
- [[settings-queue-view]] — background queue feeding the live progress.
- [[settings-import-history]] — historical view across all imports.

## Open questions

_None._
