---
type: entity
nav_path: "Entity → Import Task → Processing model"
aliases: ["Import task processing", "Chunked import", "500-row chunks", "Upsert default", "Import validation handling", "Silent skip", "Counted error", "Import file format constraints"]
tags: [entity, settings, ops, imports, processing, validation]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[import-task]]. See the hub for the other aspects (attributes, lifecycle, types + queues, provenance + recovery, history + webhooks).

# Import Task — Processing model

## Identity

How the worker actually executes an Import Task — the **500-row chunked iteration** that avoids memory pressure on long imports, the **upsert-by-default** semantics that the merchant cannot toggle off, the three-tier **validation handling** matrix (silent skip vs counted error vs abort), and the **file-format constraints** (csv / txt only, auto-detected delimiter, UTF-8 expected, header-row toggle, plan-capped row count).

## Aliases

- **Chunked import** — emphasises the 500-row batching.
- **Upsert default** — the create-or-update semantics every importer uses.
- **Validation handling** — the three buckets a bad row falls into (silent skip / counted error / abort).
- **Import file format** — the input constraints (csv / txt, UTF-8, etc.).

## Key Attributes

### Chunked processing — 500 rows per iteration

The worker does NOT process the entire file in one shot. It batches rows and processes incrementally: **500 rows per iteration** for most importers, **sub-chunked into 50-row batches** for ERP staging on customer CSV. The chunking avoids memory pressure on the worker (a 50,000-row CSV would consume too much RAM if loaded all at once) and lets the queue scheduler interleave other store work between batches.

Practical implications for the merchant:

- **Long imports take many minutes.** A 10,000-row customer CSV typically completes in a couple of minutes; a 100,000-row XML feed can take 30+ minutes.
- **Imports during peak hours run slower** — the queue is shared across stores on the same infrastructure tier.
- **Failure mid-batch does NOT resume.** If the worker crashes during processing, the Import Task does NOT pick up from the failure point. The merchant re-uploads. See [[import-task-lifecycle]] for the no-retry rule.

### Upsert by default

Most importers operate in **upsert mode**: if a row's identifier matches an existing record, the existing record is **UPDATED**; otherwise a **NEW** record is created. Only mapped fields are touched; unmapped fields keep their current values.

Identifier resolution per importer:

| Importer | Identifier(s) used to match existing records |
|----------|----------------------------------------------|
| Customers CSV | `email` (primary), optionally backed by stored customer-ID column |
| Products CSV | `product.id` (if column mapped), then SKU, then barcode |
| XML sync | `xml_import_product_id` written on first sync, then matched on subsequent runs |
| Subscribers CSV | `email` |
| Blog articles CSV | Slug or article-ID |
| Redirects CSV | Source URL |

There is no **"update only"** or **"create only"** toggle on most importers — the upsert is the default. The merchant who wants to ONLY add new (skip existing) typically filters the source data to exclude existing identifiers before upload.

### Validation handling — three buckets

| Behaviour | When |
|-----------|------|
| **Silent skip** — row dropped, no inline error | Missing required field on customer CSV, invalid email format, within-file duplicate detection. The row does NOT appear in the Errors count — it's just gone. The merchant detects silent skips by comparing input row count to imported count + error count. |
| **Counted error** — recorded as failed in [[settings-import-history]] with reason | Required CSV columns missing entirely from the mapping, foreign-key resolution failure (category not found), business-rule violation (duplicate SKU). The error is visible in the per-record drill-in on [[settings-import-history]] with a human-readable reason. |
| **Abort the Task** — entire batch fails (Task → `failed`) | Critical errors during file upload (corrupt CSV), database connectivity loss mid-batch, fatal parser errors. The Task transitions to `failed` per [[import-task-lifecycle]]; no rows after the failure point are processed. |

The per-record drill-in on [[settings-import-history]] shows the reason for every counted error and lets the merchant correct the source row and re-import.

### File-format constraints

- **CSV importers** accept `csv` or `txt` extensions. Excel formats (`.xls`, `.xlsx`) are **REJECTED at upload** with a clear error.
- **Delimiter** is auto-detected from the first 10KB of the file (comma, semicolon, tab, pipe, etc.). There is **NO manual delimiter picker** — if auto-detection picks the wrong delimiter, the merchant adjusts the source file.
- **Encoding** is **UTF-8 expected**. Non-UTF-8 files may show garbled characters in the imported records; the merchant saves as UTF-8 before uploading.
- **Header row** toggle is per-Task (default OFF). Auto-detection is NOT performed — the merchant explicitly tells the importer whether the first row is headers.
- **Row count** is plan-capped per importer; the error *"The maximum number of import items is {limit}."* surfaces if the merchant uploads beyond their plan limit. See [[import-task-types-and-queues]] for the plan-feature keys.

### What happens per chunk

For each 500-row chunk:

1. The worker reads rows N to N+499 from the staging temp table (or the XML cursor).
2. For each row, the worker applies the importer's per-row logic: resolve identifier → upsert → write provenance tag (see [[import-task-provenance-and-recovery]]) → fire the per-record webhook (see [[import-task-history-and-webhooks]]).
3. After the chunk completes, the worker increments `processed_rows` on the Task, updates the action counts, and checks the cancellation flag.
4. If cancellation requested, the worker stops; otherwise it picks the next chunk.

### Why 500 (not 1, not 10,000)?

- **Too small (e.g., 10 rows)**: queue overhead per chunk dwarfs the work done; throughput tanks.
- **Too large (e.g., 10,000 rows)**: memory pressure on a single worker; long mid-chunk cancellation lag (the worker finishes the chunk before honouring Cancel).
- **500 rows** is the empirical sweet spot — workers finish a chunk in seconds, cancellation feels responsive, and queue overhead is negligible.

### ERP customer CSV — 50-row sub-chunks

The customer CSV importer has tighter per-row work (PII validation, ERP staging buffer writes) so it sub-chunks 500-row windows into 50-row mini-batches. The merchant sees the same 500-row progress increment but the worker is doing 10× smaller atomic operations under the hood.

## Where it appears

- [[settings-queue-view]] — the `Processed rows / Total rows` counter updates per chunk.
- [[settings-import-history]] — the per-record drill-in shows the validation outcome for every row.
- All source apps — the file-format errors fire at upload time, before the Task is queued.

## Related

- [[import-task]] — hub.
- [[import-task-attributes]] — the `processed_rows` counter incremented per chunk and the action-counts breakdown.
- [[import-task-lifecycle]] — the chunked execution drives the lifecycle (no mid-chunk abort on Cancel).
- [[import-task-provenance-and-recovery]] — the provenance tag is written per-row during chunk processing.
- [[import-task-history-and-webhooks]] — per-record webhooks fire on every row in every chunk.
- [[import-task-types-and-queues]] — the plan-feature row-cap is enforced before chunk processing begins.
- [[import-pipeline]] — the platform-wide bulk-import pipeline this Task belongs to.

## Open Questions

- ⏸️ Whether the 500-row chunk size is configurable per-importer or hard-coded across the platform (verify).
- ⏸️ How the worker handles partial-row reads (e.g., a CSV row split across the chunk boundary) — confirm the staging temp table normalises row boundaries before the chunked read.
