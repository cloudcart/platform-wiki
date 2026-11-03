---
type: feature
nav_path: "Customers → Import → Background processing"
route_name: ""
route_path: ""
aliases: ["Customer import background job", "Customer import batch", "customers_import_csv", "import6 queue", "csv_import temp table", "Customer import dedup", "Customer import group auto-creation", "csv_tasks customer import", "Customer import progress"]
tags: [customers, import, csv, background, queue, batch, processing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[customers-import]]. See the hub for related aspects (wizard, fields, concurrency, side effects, plan gates, API alternative).

# Import customers — background processing pipeline

## Purpose

After the merchant clicks **Submit** in STEP 2 of the wizard ([[customers-import-wizard]]), the actual import runs **asynchronously on the `import6` queue**. This page covers the batch pipeline (500-row chunks → ERP import buffer in 50-row chunks → customer materialisation), email-dedup logic, group auto-creation, the `csv_tasks` tracking row, and the per-task progress doc + failed-records sample that powers [[settings-import-history]].

## Where to find it

- Invisible to the merchant — the job runs server-side.
- Progress is visible at **Track importing progress** ([[settings-queue-view]]) or in the wizard's success card link.
- Historical record at [[settings-import-history]].

## What the merchant can do here

Nothing directly — the pipeline is automatic. The merchant's signals:

- **Imported-count vs CSV row count** discrepancies indicate skipped rows (email-dedup or invalid email — see below).
- **Auto-created groups** appearing in [[customers-custom-groups]] after a run that mapped `group.name`.
- **Failed-records sample** (up to 25 entries) on the import-history detail page — diagnoses recurring formatter failures.

The merchant CAN cancel a running job — see [[customers-import-concurrency]] for the teardown sequence.

## Settings & fields

### Per-task tracking record (`csv_tasks` row)

Every import creates a row in the `csv_tasks` table with: `type = customers`; `tableName` (the temp CSV table name); `filename` (merchant's original); `settings` (JSON blob with header-line toggle + default group id); `mapping` (JSON of `{customer_field: csv_column_index}` pairs, added at Step 2); `mapping_sample` (first remaining data-row snapshot keyed by column index, so the import-history detail page can show "this mapping pointed to *this* value" even after the temp table is dropped); `total_products` (column-name leftover from the products-import scaffolding, but for customer imports it holds the **CSV row count** — data rows only); `imported_count`; `failed_count`; `status` (`pending` / `in_progress` / `completed` / `cancelled` / `failed`); `message` (populated on cancel / auto-recovery with the reason text).

The merchant browses this list in [[settings-import-history]] and clicks any row to see its `mapping`, `mapping_sample`, and a sample of failed records.

### Per-task progress doc + failed-records sample

The import-history detail endpoint (`GET /admin/api/core/imports/{id}`) returns the task row + its mapping, a FAILED-RECORDS sample of up to **25 entries** (with type / try count / exception message / timestamp; filtered by `record_type = 'app_manager'`), the total `failed_count` for the task, and the live progress doc IF this task is currently active (`progress.complete`, `progress.total`, `progress.msg`).

Without this endpoint, clicking any row in the import-history list would fall back to the GLOBAL progress doc — which always reflects the LAST run's state — and every row would show identical info. The per-task `mapping_sample` is the only way to see "what value did the email column point to in row 1" after the temp table is dropped.

## Business rules

### Background job pipeline

The import processes in batches of **500 rows at a time** to avoid memory pressure:

1. Step 1's upload creates a temporary database table (`csv_import_<unix-timestamp>`, e.g. `csv_import_1748263421`) and inserts the entire CSV into it as raw rows.
2. Step 2's Submit saves the mapping into the task settings and enqueues the `customers_import_csv` queue task. The CSV import job runs on the `import6` queue.
3. The job reads 500 rows at a time, formats them with the customers formatter, inserts them into the platform's ERP import buffer in chunks of 50, then continues until the temp table is drained.
4. The ERP importer then materialises the buffered rows as actual customer accounts (handling email-match update, group resolution, etc.).
5. The temp table is dropped at the end.

**Practical timing**: a 10,000-row CSV typically completes in a couple of minutes; large imports during peak hours can take longer because the `import6` queue is shared with other long-running tasks.

**Failure handling**: if the job throws mid-batch, the temp table is dropped and the exception is logged. The platform does **NOT** resume from the failure point — the merchant must re-upload. Rows inserted before the throw remain — **no atomic rollback**.

### Batch loop — cooperative cancel check

Each batch iteration: read up to 500 rows from the temp table, **check the manager's `working` flag** (cancel via the queue page sets this `false` → job exits cleanly on next iteration), run the customers formatter (dedups by email + inserts into the ERP import buffer in chunks of 50), increment the progress counter by rows consumed (progress bar advances every 500 rows), delete the processed rows from the temp table. Loops until the temp table is empty or the worker exits. See [[customers-import-concurrency]] for the cancel teardown.

### Email dedup logic — silent skip

The customers formatter rejects rows in this order — **silently** (no inline error report in the UI; the merchant detects skips via the imported-count vs CSV row count gap):

1. `trim($email)` is empty → skip
2. `filter_var($email, FILTER_VALIDATE_EMAIL)` returns false → skip
3. Email already seen in this CSV (via `seenEmails[$email]`) → skip
4. Otherwise → include

So one CSV with the same customer email twice will only import the first occurrence.

### Existing customers — update on email match

If a row's email matches an existing customer (case-sensitive, exact match), the existing customer's fields are updated rather than a new account created. **Not all fields update** — only the mapped fields are touched; un-mapped fields keep their current values. So a partial CSV (just `email,note`) updates the note on matching customers and leaves everything else alone.

This is the same `firstOrNew` semantics the JSON-API v2 [[api-customers]] create endpoint uses — see [[customers-import-api-alternative]].

### Group auto-creation on per-row `group.name`

If the merchant maps `group.name` and a row contains a group name that doesn't already exist for the store, **the platform auto-creates that group** (unexpected groups can appear in [[customers-custom-groups]] after an import). Defensive practice: pre-create groups manually, OR rely only on the Step 1 default group picker.

### Temp-table lifecycle

Created at Step 1 Submit as `csv_import_<unix-timestamp>` with one `longText` column per CSV column detected from the first row. Rows shorter than the detected count are padded with `null`; longer rows are truncated. Lives for the duration of the job; dropped at successful completion, mid-batch exception, or cancel via [[customers-import-concurrency]]. The `csv_tasks.mapping_sample` snapshot is taken **before** the temp table is dropped so the import-history detail still has data to show.

### File format auto-detection (CSV analyser)

The CSV analyser inspects the first **10 KB** of the file and counts occurrences of each candidate delimiter to pick the most likely one. Supported delimiters: comma `,`, semicolon `;`, tab `\t`, pipe `|`, colon `:`. Bulgarian semicolon-Excel exports work without extra configuration. Line endings: `\r\n`, `\n\r`, `\n`, `\r` — most-common wins. Encoding: UTF-8; non-UTF-8 files may show garbled characters.

## Related

- [[customers-import]] — hub.
- [[customers-import-wizard]] — the Step 2 Submit that enqueues the job.
- [[customers-import-fields]] — the formatter's field map (what gets dedup'd / split / auto-grouped).
- [[customers-import-concurrency]] — cancel teardown + auto-recovery for stuck imports + the `working` flag the batch loop reads.
- [[customers-import-side-effects]] — what happens per imported row (webhooks, password generation, `imported` flag).
- [[customers-import-plan-gates]] — the `customers` numeric cap that throttles batch inserts.
- [[customers-custom-groups]] — where auto-created groups appear.
- [[settings-import-history]] — the merchant-facing import history (`csv_tasks` list).
- [[settings-queue-view]] — live progress page (the per-task progress doc).
- [[background-queue-inventory]] — `import6` queue + how to spot a stuck import.

## Open questions

(All resolved.)
