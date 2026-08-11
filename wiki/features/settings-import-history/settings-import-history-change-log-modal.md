---
type: feature
nav_path: "Settings → Import history → Change log modal"
route_name: product-list-details
route_path: /admin/settings/import-history/items/:id
aliases: ["View detailed change log", "Import change log modal", "Import field diff", "Before/after import diff", "Import error reason modal"]
tags: [settings, import, history, change-log, modal, diff]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 9
---

> Part of [[settings-import-history]]. See the hub for the other aspects (List tab, Details tab, action states, storage / retention).

# Import history — Change log modal

## Purpose

The *View Detailed Change Log* modal opens when the merchant clicks the change-log indicator in any row of the [[settings-import-history-details-view|Details tab]]. It shows the **field-by-field diff** for that specific record: previous value → new value, for every field the import touched. For error rows it surfaces the validation / dependency / integration failure reason. This is the deepest drill-down on the Import history page — the only view where the merchant can answer *"what exactly did the import change on this product?"* or *"why did this row fail?"* at field resolution.

## Where to find it

Settings → Import history → click a row to open the [[settings-import-history-details-view|Details tab]] → click the **Change log** column indicator on any record row. The modal opens in place; no route change.

The modal does not have its own route — it is a child component of the Details view.

## What the merchant can do here

- See every field the import touched on this record, with before/after values rendered side-by-side.
- For error rows: read the failure reason captured at import time (e.g. *"SKU already exists"*, *"Required field missing: category_id"*, *"VAT validation failed against VIES"*).
- For Skip rows: confirm that no values changed (the diff renders empty or "no change" for every scanned field).
- Close the modal and continue triaging other rows from the Details tab.

What the merchant **cannot** do in the modal:

- Apply / re-apply the proposed change — the diff is historical, read-only.
- Edit any of the before/after values — to fix the underlying record the merchant must navigate to the actual entity (product, category, customer, etc.).
- Copy a "fixed payload" out of the modal — the modal renders a human-readable diff, not raw payload.
- Delete the entry from the modal — see [[settings-import-history-storage-and-retention]].

## Settings & fields

### Diff format — per field

For every field touched on the record the modal renders a row of the form:

| Field name | Before | After |
|------------|--------|-------|
| `price` | `19.90` | `21.50` |
| `quantity` | `45` | `60` |
| `name.en` | `"Old name"` | `"New name"` |

The modal renders only the **fields touched** by the import — fields the import payload omitted are not shown, even if they exist on the underlying entity.

### Error-row content

For records with `Action = Error` the modal additionally surfaces the failure reason captured by the importer. Common error texts include:

- *"SKU already exists"* — duplicate SKU on a create-only flow.
- *"Required field missing: category_id"* — a required attribute was absent in the payload.
- *"VAT validation failed against VIES"* — external dependency validation rejected the value.
- ERP-specific errors — e.g. *"Szamlazz: invoice number conflict"*, *"FGO: document number already issued"*.

The error reason is the merchant's primary diagnostic — pair it with the [[settings-import-history-details-view|Details tab]] search to find every row that hit the same failure mode.

### Shared component across importers

The modal is the same change-log viewer used on the ERP integration screens — same look, same diff format, same field-by-field rendering. So a merchant who has used the change-log modal on, say, the Szamlazz screen will recognise this one immediately.

### Format is consistent across CSV / XML / JSON / ERP

Every importer writes into the same shared change-log structure: action (create / update / skip / error), affected entity (product / category / customer / etc.), and a list of changed fields with before/after values. ERP integrations may add extra fields specific to their payload shape (e.g. Szamlazz invoice ID, FGO document number), but the core format does not vary by source — the merchant reads change logs from any importer without context-switching.

## Business rules

### The modal is the only field-resolution view

The List tab shows aggregate counts. The Details tab shows per-record actions. **Field-level resolution exists only inside this modal.** A merchant who wants to know *"did the import change the product description?"* cannot answer that from any other surface on this page.

### Read-only — no apply / no rollback

The modal renders a historical diff. There is no *"apply this diff again"* or *"undo this change"* button. To revert an unwanted change the merchant must edit the underlying record manually or run a corrective import. The platform has no undo for any completed import.

### Diff scope follows the import payload, not the entity schema

If the importer's payload contained 6 fields, only those 6 fields appear in the diff — even if the entity (e.g. a product) has dozens more. This is by design: the diff reports what the importer actually touched, not what the entity could in principle hold. Fields the import never wrote are absent from the diff (they're not shown as "no change" — they're simply not listed).

### Format is consistent across importers — read-once skill

Because all importers share the same change-log viewer, a merchant or support agent who learns how to read one change-log modal can read every other one. ERP-specific extra fields (e.g. external invoice IDs) appear as additional rows alongside the standard before/after pairs.

### Error reason is captured at import time, never updated

The failure text shown in the modal is the message the importer recorded at the moment of failure. If the underlying issue has since been resolved (e.g. the missing category was created later), the change-log entry still shows the original error — it's not a live re-check. To know whether the row would succeed today the merchant must re-run the import on a corrected payload.

## Related

- [[settings-import-history]] — hub.
- [[settings-import-history-details-view]] — the tab that hosts the row-level indicator opening this modal.
- [[settings-import-history-action-states]] — Created / Updated / Skip / Error / Pending; only Updated and Error rows have meaningful modal content.
- [[settings-import-history-storage-and-retention]] — separate logging database holding the per-record entries; why support cannot easily prune individual change-log rows.
- [[products-change-log]] — the Product entity has its own Change log modal (different surface, similar format) showing all stock / price / attribute changes regardless of origin.

## Open questions

None.
