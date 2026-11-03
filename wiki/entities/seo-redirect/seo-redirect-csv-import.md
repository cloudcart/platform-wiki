---
type: entity
nav_path: "Entity → SEO 301 Redirect → CSV import"
aliases: ["Import redirects", "Bulk redirect import", "CSV upload of 301s", "Three-step import modal", "Redirect import 2FA"]
tags: [entity, seo, marketing, redirects, csv, import, bulk-operations]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[seo-redirect]]. See the hub for the other aspects (types, lookup and cache, marketing passthrough, auto-tracking, validation and UI).

# 301 Redirect — CSV import

## Identity

The **Import redirects** button on [[marketing-seo-301-redirects]] opens a three-step wizard for bulk-uploading [[seo-redirect|301 rules]] from a CSV file. This is the canonical migration tool: a merchant moving from another platform typically has a spreadsheet of old-URL / new-URL pairs that they upload here in one shot rather than creating hundreds of rules by hand.

The import is **idempotent** on `old_url` — re-uploading the same CSV deletes the previous row for the same `old_url` and re-inserts it, so the merchant can iteratively refine the spreadsheet without ending up with duplicates. The job runs as a background task on the `import` queue and surfaces in [[settings-queue-view]].

## Aliases

- **Import redirects** — the literal button label.
- **CSV upload** — generic merchant phrasing.
- **Bulk import** — when the conversation is about hundreds-of-rules migrations.
- **301 import wizard** — internal phrasing for the three-step modal.

## Key Attributes

| Step | What the merchant does | Validation |
|---|---|---|
| **Step 1 — Upload file** | Pick the CSV file. Toggle *"Check this if your file has a header line explaining the columns"*. | Only `.csv` files accepted. The header-line toggle determines whether row 1 is skipped during mapping. |
| **Step 2 — Column mapping** | Bind each CSV column to `redirect.old_url` and `redirect.new_url`. Both fields are **required**. | Submit is disabled until both required mappings are bound. |
| **Step 3 — Submit** | Click submit. The import enqueues as a background job on the `import` queue. Toast: *"The import started"*. | Successful row count is logged after completion. |

### Auto-typing on import

Imported rows are auto-typed based on the `new_url` value:

- **Starts with `http://` or `https://`** → typed as `external`. The full URL is stored in `new_url`.
- **Anything else** → typed as `manual`. The value is treated as a relative path; if it begins with the store's own scheme+host, the host is stripped on save (see [[seo-redirect-types]]).

The CSV import does NOT support entity-typed rules (`product`, `category`, etc.). To create entity-typed rules at scale, the merchant must use [[api-redirects]] (JSON-API v2) or create them manually.

### Idempotency on duplicate `old_url`

Within the same import, if the CSV contains two rows with the same `old_url`, **last-write-wins**: the second row's `new_url` replaces the first. Across imports, a re-imported row with an `old_url` that already exists in the database deletes the existing row and inserts the new one. This is the opposite of the admin-create flow, which **rejects** duplicate `old_url` with *"Old URL is already exist"* — see [[seo-redirect-validation-and-ui]] for the inconsistency.

## Relationships

- **Creates** [[seo-redirect|301 Redirect rules]] in bulk, all typed as `external` or `manual`.
- **Triggers** the same save-side effects per row: `redirects301` cache invalidation, `has_301_redirects` site-setting recomputation.
- **Surfaces in** [[settings-queue-view]] (`import` queue) — the merchant can see the job progress and any error log there.
- **May require** two-factor authentication via the `required_2fa` flag returned in the import metadata.

## Lifecycle

1. **Open the modal** — the merchant clicks "Import redirects" on [[marketing-seo-301-redirects]].
2. **Optional 2FA challenge** — if the `required_2fa` flag is set on the import metadata, the merchant must complete a 2FA challenge before proceeding.
3. **Three-step wizard** — upload + map + submit as documented above.
4. **Job enqueued** — the import runs on the `import` queue. The merchant sees the progress in [[settings-queue-view]].
5. **Per-row processing** — each row is validated and saved via the standard create pipeline (including type-detection, duplicate-handling, save-time normalisation per [[seo-redirect-types]]).
6. **Completion** — successful row count is logged. Failed rows surface in the queue view's error log.

## Business rules

### 2FA gate on import

The import endpoint returns a `required_2fa` flag in the metadata. When set, the merchant must complete a 2FA challenge before the import enqueues. This is a security measure — bulk URL rewriting is a high-leverage operation that can break SEO at scale if misused, so the platform forces a stronger authentication for the bulk path than for single-row edits.

### Per-row uniqueness — last-write-wins (NOT rejection)

Unlike the single-row create flow, the CSV import resolves duplicate `old_url` via delete-then-insert (last-write-wins per `old_url`). Re-importing the same CSV is therefore idempotent — the merchant can iterate on the spreadsheet without manually cleaning up. **This contrasts with the admin-create flow, which rejects duplicates** — the legacy bulk-update endpoint behaved like the CSV import (silent-skip) but the modern Vue manager rejects.

### Only `external` / `manual` types are creatable via CSV

Entity-typed rules (`product`, `category`, etc.) cannot be created via CSV import. The auto-typer chooses between `external` (URL has `http://` / `https://`) and `manual` (everything else). For entity-typed rules at scale, the merchant uses [[api-redirects]] (which can accept `location = "product"` with `item_id`).

### Job runs on the `import` queue

The background job runs on the `import` queue, surfaceable in [[settings-queue-view]]. Errors per row appear in the queue's error log. The merchant doesn't get an email summary — they need to check the queue manually.

### Header-line toggle decides row 1's treatment

If the merchant ticks *"Check this if your file has a header line explaining the columns"*, the importer treats row 1 as headers and skips it. Forgetting to tick this when the file DOES have headers means row 1 ("Old URL,New URL") gets saved as a literal redirect — a common merchant error.

### Toast message is short and non-blocking

The "The import started" toast is the merchant's only immediate feedback. To see progress, the merchant goes to [[settings-queue-view]] or refreshes the redirects list after a delay.

## Where it appears

- [[marketing-seo-301-redirects]] — the manager screen with the "Import redirects" button.
- [[settings-queue-view]] — the queue view where the import job runs and surfaces errors.
- [[api-redirects]] — programmatic alternative for entity-typed rules at scale.
- [[apps-csv-import]] — the broader CSV import surface (this redirect import is a separate flow but shares the merchant mental model).

## Related

- [[seo-redirect]] — hub.
- [[seo-redirect-types]] — what each imported row becomes (`external` or `manual`).
- [[seo-redirect-validation-and-ui]] — single-row validation messages and the duplicate-rejection contrast.
- [[marketing-seo-301-redirects]] — the manager screen.
- [[settings-queue-view]] — the queue view for the background job.

## Open Questions

- Whether failed rows produce a downloadable error report (CSV-of-failures) so merchants can fix and re-upload (verify — currently merchants check the queue's error log row by row).
- Whether the importer supports multi-language `new_url` values (per-locale redirects) or always treats `new_url` as language-independent (verify).
