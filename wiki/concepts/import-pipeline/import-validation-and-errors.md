---
type: concept
nav_path: "Concept → Import pipeline → Validation & errors"
aliases: ["Import validation", "Silent skip on import", "Import failed rows", "Import error handling", "Counted error import", "Import abort"]
tags: [ops, imports, validation, errors, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[import-pipeline]]. See the hub for the other aspects (stages, concurrency lock, upsert + provenance, plan gates + 2FA, history + recovery, XML Sync).

# Import pipeline — validation & errors

## Definition

Different importers handle bad rows differently. There are **three behaviours** in the pipeline: **silent skip** (row is dropped, no inline error surfaced), **counted error** (row is recorded as failed in [[settings-import-history]] with reason), and **abort** (the entire batch fails). The merchant sees aggregate counts after the import completes — *Imported: 487 of 500 rows* with 13 unaccounted. To find out what happened to the missing rows, they drill into [[settings-import-history]] → details, which shows every record's action (Create / Update / Skip / Error) and a per-record change-log indicator with the failure reason.

Crucially, **silent skip on validation failure** is the most common pitfall: customer CSV silently drops rows with missing required fields or invalid format. No inline error report appears — only the aggregate count differs from the input row count.

## Scope

Covered:

- The three validation outcomes — silent skip, counted error, abort — and which importers apply each.
- How the merchant detects skipped rows (input count vs imported count comparison).
- The per-record failed-row table and how the first failure surfaces as the task message.
- The re-import workflow for failed rows (no retry button — fix the source and re-run).
- The absence of `import.completed` / `import.failed` webhook events.

Not covered here:

- The wizard's required-field validation at the Map step (those are pre-submit) — see [[import-pipeline-stages]].
- The audit-log retention of failed rows — see [[import-history-and-recovery]].
- Plan-feature row-count caps that abort imports beyond the limit — see [[import-plan-gates-and-2fa]].

## Contrasts

- **Silent skip vs counted error vs abort** — three categorically different outcomes for bad rows. Customer CSV is heavy on silent skip; product CSV is heavy on counted error; only critical errors (corrupt file, DB connectivity loss) abort.
- **Pre-submit validation vs runtime validation** — required-field unmapped at Step 2 (Map) is a **pre-submit** error that blocks Submit entirely. Validation failures during background row processing are **runtime** and surface in [[settings-import-history]] after the fact.
- **Silent skip vs the "Imported" success message** — the success toast tells the merchant the FILE was queued. It does NOT confirm row-level success. Skipped rows are invisible in the success path.

## Where it applies

The validation outcomes apply during **Stage 4 — Background processing** ([[import-pipeline-stages]]). Each worker iteration validates rows before applying them. The outcomes differ per importer:

| Importer behaviour | Triggered by |
|---------------------|------|
| **Silent skip** — row is dropped, no inline error to merchant | Missing required field (e.g., empty email on customer CSV), invalid email format, duplicate within-file detection |
| **Counted error** — row is recorded as failed in import-history with reason | Required CSV columns missing entirely from the mapping, foreign-key resolution failure (e.g., category not found), business-rule violation (e.g., duplicate SKU) |
| **Abort the import** — the entire batch fails | Critical errors during file upload (corrupt CSV), database connectivity loss mid-batch |

### Per-importer behaviour

- **Customer CSV** — silent skip on invalid / duplicate email, missing required fields. Aggregate count tells the merchant how many were skipped. NO per-row error reasons surface.
- **Product CSV** — failed rows are stored in a dedicated failed-records table; the first failure's exception is surfaced as the task message on [[settings-import-history]]; full per-row details are queryable from the details view.
- **XML import / XML sync** — per-run history records `created_count`, `updated_count`, `skipped_count`, `failed_count`; failures don't block subsequent runs. See [[import-xml-sync-recurring]].
- **App-specific importers** — varies; most follow the counted-error pattern of product CSV.

### How the merchant discovers skipped rows

Because silent skip emits no per-row error, the merchant has to detect skips by **counting**:

1. Open the source CSV — read the row count (subtract 1 for header if "Has header line" was ON).
2. Open [[settings-import-history]] → find the import → read the aggregate counts (Created + Updated + Errors + No-action).
3. If `(Created + Updated + Errors + No-action) < source row count`, the difference is silently skipped.

The merchant drills into the import → details tab to see per-record outcomes. Counted-error rows show up here with reasons; silently-skipped rows may or may not appear depending on the importer.

### Re-importing failed rows

There is **no "retry failed rows from history" button**. The re-run is a separate import from scratch:

1. Merchant identifies the failures in [[settings-import-history]] → details.
2. Fixes the source data — the spreadsheet, the supplier feed, the ERP mapping.
3. Re-runs the importer from the originating screen with the corrected file.

Because most importers operate in **upsert mode** (see [[import-upsert-and-provenance]]), the re-run safely updates already-imported records and adds the previously-failed ones — no duplicate creation as long as the match identifier (email / SKU / `product.id`) is consistent.

### No `import.completed` / `import.failed` webhook events

The current webhook catalog does NOT include `import.completed` or `import.failed` events. Merchants who need programmatic notification of import outcomes have two options:

- **Poll [[settings-import-history]]** via the JSON-API v2 if available, or scrape the admin UI.
- **Rely on the in-admin bell-icon notification** that fires when an import finishes (visible in the bell-icon notification list).

This is a recurring ERP-integrator request; the current platform forces them to poll. See [[settings-hooks]] for the webhook catalog.

### Example — silent skip discovery

1. Merchant uploads a 500-row customer CSV with `email, first_name, last_name` columns.
2. 13 rows have blank `email`.
3. Import completes; the admin notification says *"Customers import completed: 487 imported."*
4. Merchant compares: 500 input rows, 487 imported. 13 missing.
5. Opens [[settings-import-history]] → finds the import → drills in. The details view shows 487 Create actions; the 13 blank-email rows are NOT listed (silently skipped on the customer importer).
6. Merchant opens the source CSV, finds the 13 blank rows, fills in the missing emails, re-runs the import. Upsert ensures the previously-imported 487 are updated (no-op) and the 13 new are created.

## Related

- [[import-pipeline]] — hub.
- [[import-pipeline-stages]] — Stage 4 (Background processing) is where validation runs.
- [[import-history-and-recovery]] — where the merchant drills into per-record outcomes to find counted errors.
- [[settings-import-history]] — the audit screen showing aggregate counts + per-record drill-in.
- [[import-upsert-and-provenance]] — explains why re-running a corrected file is safe.
- [[settings-hooks]] — webhook catalog (does NOT include `import.completed` / `import.failed`).

## Open Questions

- Exact per-importer list of which validations silent-skip vs count-error (verify against each importer's row-handler).
