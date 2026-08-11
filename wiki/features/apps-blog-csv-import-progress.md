---
type: feature
nav_path: "Apps → Blog CSV Import → Progress"
route_name: apps.blog_csv_import.progress
route_path: /admin/apps/blog_csv_import/progress
aliases: ["Blog CSV Import Progress", "Blog import progress", "Blog import task"]
tags: [apps, imports, blog-csv-import, progress, status, plan-gated]
plan_gates: ["blog_articles"]
created: 2026-05-22
updated: 2026-05-27
source_count: 3
---
# Blog CSV Import → Progress

## Purpose

The **Progress** sub-page shows the **per-task import progress** for an active Blog CSV Import job. After the merchant uploads a CSV via [[apps-blog-csv-import]], this page tracks:
- How many rows have been processed.
- Success / failure counts.
- Per-row errors (when failed).
- Estimated completion time.

For the full Blog CSV Import feature set, see [[apps-blog-csv-import]].

## Where to find it

Sidebar → Apps → Blog CSV Import → click on an active task → **Progress**. Route: `/admin/apps/blog_csv_import/progress`.

The Vue component: `ApplicationsBlogCsvImportProgressPage.vue` (CcDomain).

## What the merchant can do here

### Progress display

| Field | Notes |
|---|---|
| **Total rows** | CSV row count. |
| **Processed** | Rows already attempted. |
| **Success** | Successfully imported articles. |
| **Failed** | Rows that errored out. |
| **Status** | Active / Completed / Failed / Cancelled. |
| **Started at** | Job start timestamp. |
| **Completed at** | (When done) Completion time. |

### Per-row error log

For failed rows, the merchant can drill down:
- Row number in the CSV.
- Specific error message (e.g., "Invalid slug format", "Category not found", "Author email not registered").
- The row's source data for context.

### Actions actually present on this screen

The Progress page is **read-only with one possible side-action**: a "Purchase additional bundle of products" upsell appears when the importer hits the plan's article cap mid-run. No Cancel button, no Retry-failed button, no Download-error-report button is rendered by the CcImportStatus component.

To stop an in-flight import, the merchant uses the manager-level `setWorking(false)` flow (see "Cancel = manager.setWorking(false)" in the How it works section) — typically by navigating away and starting a new task, which the import pipeline interprets as cancellation of the previous one.

### What the merchant CANNOT do here
- Edit the source CSV mid-import — start a new task instead.
- Rollback successfully-imported articles — manual delete required.
- Re-run only failed rows — fix the CSV and start a fresh import.
- Download an error report — there is no export button. Per-row errors are queryable only via the `global_imports_records_failed` table (developer-side).

## Settings & fields

Per [[apps-blog-csv-import]] Manager: `working: bool` lock prevents concurrent imports.

## Business rules

### One concurrent import per store

The `working` lock means only ONE blog import runs at a time. Starting a second would fail.

### Partial completion semantics

When the merchant cancels mid-flight, already-processed rows STAY imported (no rollback). The merchant manually cleans up if needed.

### Permission
Standard apps permission scope.

## Plan gates

Same gating as the parent [[apps-blog-csv-import]] (see [[plan-gates]], [[plan-vs-feature-pack]]):

| Mapping | Shape | What it controls on this screen |
|---|---|---|
| `blog_articles` | Numeric (per-plan max blog articles) | Each row that creates a NEW article counts against the cap. If the importer hits the cap mid-run, the orphaned-task finaliser sets the task to `failed` with the "interrupted-by-plan-quota" message — visible on this Progress page in the Status field. |

The Progress page itself does NOT have a separate plan-feature paywall — it's a read-only monitor of the underlying import. The gate is enforced inside the import-pipeline insert stage, not on this page. Upsell flows route through [[plan-features]].

## Related

- [[apps-blog-csv-import]] — hub.
- [[apps-csv-import]] — sister CSV import for products.
- [[marketing-blog-articles]] — articles created by the import.
- [[plan-gates]] / [[plan-features]] / [[plan-vs-feature-pack]] — gating concept + upsell + extension.

## How it works (verified against backend)

### Live updates: polled every 5 seconds while running

The progress page polls every **5 seconds** while the import is still in flight, re-fetching the status block. Once the import completes, the polling stops. **The merchant does NOT need to refresh manually** — counts and the progress bar update on their own.

### Three status badges + "Live" indicator

The header renders a coloured pill showing one of:
- **Running** (blue) — task is in flight; an animated blue dot + "Live" label appears next to the badge, plus a separate spinning "Auto-refreshing..." indicator on the right.
- **Stopped** (grey) — task is paused or not started.
- **Completed** (green) — task finished; a separate green banner with checkmark appears above ("Import completed successfully!").

The header is the merchant's only at-a-glance signal about whether the polling is still happening. Once it flips to Completed/Stopped, the Auto-refreshing indicator disappears.

### Error categorisation: failed list shows raw exception per row, not grouped

Failed rows are listed individually with their captured exception text. **There is no grouping by error type (slug / category / author / format)** — the merchant scans the raw list, optionally filtering by the failure type column. For categorisation by type, the merchant uses CSV column sort externally.

### Bulk retry: NOT supported per-error-type

Per the controller endpoints: there's no "retry failed rows" action. To re-run failed rows the merchant must fix the source CSV, delete the existing task, and run a new import. The `working` lock ensures the new import only starts after the previous finalises.

### Multi-file imports: serialised, NOT queued

Only **ONE blog import can run at a time per store**. Attempting to start a second while the first is in flight is blocked by an internal "working" lock. The merchant **cannot queue a batch of CSVs** to run sequentially — they wait for the current one to finish (or cancel it) before starting the next.

### Progress doc lives in app settings, overwritten by next import

The live progress (`complete`, `total`, `msg`, `info`) is stored as app-meta settings on the BlogCsvImportManager, NOT on the task row itself. When the next import starts, those settings are reset — the previous run's live progress data is lost. The `csv_tasks` table preserves the FINAL counters (imported_count, failed_count, message) post-finalisation, so the historical task detail panel survives, but the row-by-row progress timeline of an old run is not recoverable.

### Cancel = manager.setWorking(false) — drops pending records, persists task as failed

The Cancel action calls the manager's `setWorking(false)` which:
- Deletes all pending records belonging to this app.
- Removes the progress settings.
- Uninstalls the related queue mappings.
- Persists the final orphaned-task message: "Import was interrupted before completion (imported X of Y)."

Already-imported articles stay in the catalog — there is no rollback. The merchant manually deletes them if needed.

## Open questions

_None._
