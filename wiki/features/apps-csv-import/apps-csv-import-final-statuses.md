---
type: feature
nav_path: "Apps → CSV Import → Final statuses"
route_name: apps.csv_import.task
route_path: /admin/apps/csv_import/task/{taskId} (finalised state)
aliases: ["CSV Import — final status", "CSV Import — task outcomes", "CSV Import — no importable rows", "CSV Import — failed_count", "CSV Import — imported_count", "CSV Import — plan quota interruption", "CSV Import — orphaned task"]
tags: [apps, imports, csv, status]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[apps-csv-import]]. See the hub for the other aspects (wizard, task detail, row pipeline, mapping fields, side effects, plan gates).

# CSV Import — final-status outcomes

## Purpose

Every CSV import ends in one of four deterministic terminal statuses. Which one fires depends on row count, failure count, and whether the formatter collapsed rows during variant rollup. A fifth, special path applies when something halts the import mid-flight (typically a plan-quota exception). This page documents the resolution order, the message that lands on the task, and the persisted counts the task-detail page surfaces afterwards.

## Where to find it

Apps → CSV Import → task detail → header status badge + yellow message box. The status badge is rendered by the `ApplicationsCsvImportStatusBadge` component. See [[apps-csv-import-task-detail]].

## What the merchant can do here

Once the task hits a terminal status the merchant can:

- Read the diagnostic message in the yellow box on the task-detail page header.
- Click the Imported count to jump to the products-list filter `import=csv-{taskId}-` and see exactly what was created (see [[apps-csv-import-side-effects]]).
- Inspect the failed-records card for per-row errors (when `failed_count > 0`).
- Delete the task to free up the `working` lock and start another.
- Bulk-delete the imported products via the products-list filter if they want to retry from scratch — there is no built-in undo. See [[apps-csv-import-side-effects]].

## Settings & fields

After finalisation, two persisted counts on the `csv_tasks` row survive past the import:

| Field | Source | What it shows |
|---|---|---|
| `imported_count` | Calculated as `queued - failedCount` | Total rows that successfully landed as products / customers / etc. |
| `failed_count` | Filter of `global_imports_records_failed` to entries newer than the task's creation time, scoped to `record_type = 'app_manager'` + the CSV import app's ID | Total rejected rows. |

These persist to the `csv_tasks` table so the task-detail view can show them later. The live progress doc gets overwritten by the next import — these counts survive.

## Business rules

### 4 final-status outcomes (checked in order)

The task gets ONE of these terminal statuses, checked in order:

#### 1. `total = 0` → `failed` ("every row filtered out")

When the CSV produced ZERO records (every row got dropped because the mapped `product.id` column was empty or duplicated for variant collapsing), the task is marked **`failed`** with the explanatory message:

> *"No importable rows — every row was filtered out by the product.id / variant.parent_id column mapping. Check that the mapped CSV columns actually contain values."*

**This is one of the most common merchant-confusion sources** — a 1000-row CSV silently produces zero products because the merchant mapped `product.id` to the wrong column. Support workflow: open the task detail, check the column-mapping card's first-row sample values — empty cells on `product.id` are the smoking gun. See [[apps-csv-import-task-detail]] for the mapping card.

#### 2. `failed_count > 0` → `completed` (with failures)

The importer ran but rejected some rows (validation, missing fields). Status = **`completed`** with `failed_count` populated. The first failure's exception text is included in the task message (truncated to 250 chars). Full per-row exceptions are queryable from the `global_imports_records_failed` table — see *Failed-row error visibility* below.

#### 3. `total < CSV rows` → `completed` (with collapse)

The formatter collapsed rows during variant rollup OR rows were filtered out on partially-empty `product.id` columns. Status = **`completed`** with reduced `imported_count`. Variant rollup is intentional: if the CSV has 100 rows for 25 products × 4 variants each, the formatter collapses to 25 records. Useful but can surprise merchants — the wizard does not warn about the collapse before save. See [[apps-csv-import-wizard]] for the rollup rule and [[apps-csv-import-mapping-fields]] for `variant.parent_id` semantics.

#### 4. Otherwise → `completed` (full success)

Plain success — every CSV row landed as a product / record. Message:
> *"Imported {imported_count} products successfully"*

### Interrupted-by-plan-quota — separate "orphaned task" finaliser

When something external halts the import (typically a plan-quota exception caught upstream — see [[apps-csv-import-plan-gates]]), the manager's `setWorking(false)` path runs a separate `finalizeOrphanedTask` finaliser instead of the standard 4-outcome path. The task is marked **`failed`** with the message:

> *"Import was interrupted before completion (imported X of Y). Common cause: plan create-quota was reached. Check your plan limits or contact support."*

So merchants who hit "you've reached your plan's product cap" mid-import get a specific message pointing at the cap, not a generic failure. The yellow message box on the task-detail header surfaces this verbatim. See [[apps-csv-import-task-detail]].

### Failed-row error visibility — `global_imports_records_failed` table

Failed rows are stored in a dedicated `global_imports_records_failed` table:

- Filtered by `record_type = 'app_manager'` AND the current app ID AND a timestamp newer than the task's creation time.
- The **first failure's** exception text is captured (truncated to 250 chars if longer) and surfaced as the task message.

**This answers the error-reporting granularity question**: per-row errors ARE stored individually. The task UI shows the FIRST error as a summary; full per-row details are queryable from the table. The Failed-records card on the task-detail page samples this table — see [[apps-csv-import-task-detail]] for what's surfaced and what's truncated.

### `imported_count` + `failed_count` persisted on `csv_tasks`

After finalisation, the merchant sees `imported_count = queued - failedCount` and `failed_count` (from the failed-records table). These persist to the `csv_tasks` row so the task-detail view can show them indefinitely — the live progress doc, which gets overwritten by the next import, is not relied on.

### Status badge maps to the four outcomes

The `ApplicationsCsvImportStatusBadge` Vue component renders a coloured badge per task — Pending / Running / Completed / Failed. *Completed-with-failures* and *Completed-with-collapse* both render as **Completed** (with `failed_count` separately visible) — the badge does NOT distinguish them; the merchant reads the yellow message box and the Failed count for the nuance.

## Related

- [[apps-csv-import]] — hub.
- [[apps-csv-import-task-detail]] — where the final status surfaces (badge, message, Imported / Failed labels).
- [[apps-csv-import-row-pipeline]] — the 3-flag finalisation gate that decides when one of the 4 statuses resolves.
- [[apps-csv-import-wizard]] — the variant-rollup rule behind outcome #3.
- [[apps-csv-import-mapping-fields]] — `variant.parent_id` semantics behind outcome #1.
- [[apps-csv-import-plan-gates]] — the plan-quota source behind the orphaned-task message.
- [[apps-csv-import-side-effects]] — the `import=csv-{taskId}-` filter used for post-import cleanup.

## Open questions

_None._
