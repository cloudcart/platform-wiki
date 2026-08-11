---
type: concept
nav_path: "Concept → Import pipeline → Stages"
aliases: ["Import wizard stages", "Upload-map-submit", "Import stages", "Import processing stages", "Background import processing", "Import chunking"]
tags: [ops, imports, csv, xml, queues, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[import-pipeline]]. See the hub for the other aspects (concurrency lock, validation, upsert + provenance, plan gates + 2FA, history + recovery, XML Sync).

# Import pipeline — stages

## Definition

The **import pipeline stages** are the canonical sequence every CSV / file-based importer in CloudCart follows: **Upload → Preview / Map → Submit → Background processing → Audit**. The first three stages are a synchronous wizard the merchant clicks through (takes seconds); the fourth is asynchronous on a dedicated background queue (takes minutes); the fifth is the merchant returning to [[settings-queue-view]] or [[settings-import-history]] to verify the result.

XML imports and feed-based syncs follow the same shape with one substitution: the "upload" step is replaced with a URL configuration (and credentials / parameters), and the mapping is shown against the parsed XML structure instead of CSV columns.

## Scope

Covered:

- The standard wizard shape — Upload → Map → Submit — and what happens in each step.
- The three main import pathways (customers, products, app-specific) and their entry-points.
- Background processing — row chunking, queue names (`import1`, `import2`, app-specific), practical timing.
- Where the merchant sees progress vs completion.

Not covered here:

- The single-import lock that gates the Submit step — see [[import-concurrency-lock]].
- How rows that fail validation are handled — see [[import-validation-and-errors]].
- Plan-feature gates and 2FA on the Upload step — see [[import-plan-gates-and-2fa]].
- Recurring XML Sync's schedule and feed transport — see [[import-xml-sync-recurring]].

## Contrasts

- **Synchronous wizard vs asynchronous processing** — the Upload + Map + Submit steps are synchronous and take seconds; the actual row processing is asynchronous on the queue and takes minutes. The merchant's "Success" toast acknowledges the QUEUE, not row-level completion.
- **One-shot vs recurring** — customer CSV, product CSV, and one-time XML imports run once. [[apps-xml-sync]] reuses the same staged shape but loops on a schedule. See [[import-xml-sync-recurring]].
- **CSV vs XML upload** — CSV uploads a file; XML configures a URL. The Map step looks similar (column-to-field for CSV, structure-to-field for XML) but the source of the structure differs.

## Where it applies

The three main import pathways all funnel through the same staged shape:

| Pathway | Where | Source data | Run mode |
|---------|-------|-------------|---------|
| **Customers CSV import** | [[customers-import]] (Customers → Import button in header) | CSV / TXT spreadsheet uploaded by merchant | One-shot |
| **Products CSV / XML / JSON imports** | [[apps-csv-import]], [[apps-xml-import]], [[apps-json-import]] (Apps → install → app's screen) | CSV / XML / JSON file or URL | One-shot or recurring (XML Sync) |
| **App-specific imports** | Inside each ERP / channel integration's screen (e.g., Etsy listings sync, Szamlazz invoice pull, FGO export, etc.) | App-specific protocol (XML over HTTP, JSON over REST, etc.) | Varies — typically recurring |

The merchant picks the pathway based on what they're importing (customers vs products vs invoices vs blog articles) and the format of their source data.

### Step 1 — Upload

- Drag-and-drop a file, OR pick via file picker.
- Set "Has header line" toggle (default OFF) — when ON, the first row is treated as column headers and skipped during import.
- Set any importer-specific Step-1 options (e.g., customer-group picker for customers, update-policy picker for XML).
- Click **Next** to upload.

For XML pathways the file picker is replaced with a feed URL field + optional `parameters` (query-string key/value pairs) — see [[import-xml-sync-recurring]] for transport constraints.

### Step 2 — Preview / Map

- The platform reads the file's first row and shows the column count.
- For each CSV column, the merchant picks the target field from a dropdown of valid fields for the entity (Product / Customer / etc.).
- Unmapped columns are dropped during import.
- Required fields (e.g., `customer.email` for customers, `product.name` + `product.id` for products) cannot be left unmapped — validation blocks submit.
- Click **Submit** to commit the mapping and enqueue the import.

The mapping is stored on the task row itself for resume support but is NOT a reusable preset — every new task starts from scratch. See [[import-upsert-and-provenance]] for the merchant's column-order workaround.

### Step 3 — Submit / Success

- Confirmation message: *"The file was successfully uploaded and the [type] import task was added to the queue. If you wish, you could track the uploading in the queued jobs."*
- The merchant can close the modal — the job runs regardless.
- Direct link to [[settings-queue-view]] for live progress.

The Submit step is where the [[import-concurrency-lock]] gate fires — if another import is already running, the platform returns HTTP 409 instead of enqueuing.

### Stage 4 — Background processing

The import jobs do NOT process the entire file in one shot. They batch rows and process incrementally on dedicated queues:

| Importer | Chunk size | Queue |
|----------|------------|-------|
| Customers CSV | 500 rows per iteration, sub-chunks of 50 into ERP staging | `import2` |
| Products CSV | Dispatcher batches; final commit per task | `import1` (or app-specific) |
| Products XML import | Parse pipeline + insert pipeline split | `import1` |
| Products XML sync | Same as XML import + recurring scheduler | `import1` (shared) |
| App-specific | Varies per integration | App-specific queue |

The chunking exists to avoid memory pressure on the worker (a 50,000-row CSV would consume too much RAM if loaded all at once) and to allow the queue scheduler to interleave other store work between batches.

Practical implications:

- **Long imports take many minutes.** A 10,000-row customer CSV typically completes in a couple of minutes; a 100,000-row XML feed can take 30+ minutes.
- **Imports during peak hours run slower** — the queue is shared across stores on the same infrastructure tier.
- **Failure mid-batch doesn't resume** — if the worker crashes during processing, the import does NOT pick up from the failure point. The merchant re-uploads.

### Stage 5 — Audit

After the queue marks the import complete, the merchant returns to [[settings-import-history]] to verify aggregate counts (Created / Updated / No-action / Errors / Total) and drill into per-record outcomes. See [[import-history-and-recovery]] for the audit-trail mechanics and cleanup paths when something went wrong.

## Related

- [[import-pipeline]] — hub.
- [[settings-queue-view]] — live in-flight queue progress (Stage 4 visibility).
- [[settings-import-history]] — historical audit (Stage 5).
- [[customers-import]] — customer CSV pathway.
- [[apps-csv-import]] — product CSV pathway.
- [[apps-xml-import]] — one-time XML pathway.
- [[apps-json-import]] — JSON pathway.
- [[apps-blog-csv-import]] — blog-article CSV pathway.
- [[background-queue-inventory]] — `import1` / `import2` queue tiers and worker concurrency per plan.

## Open Questions

None.
