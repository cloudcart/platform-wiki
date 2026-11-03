---
type: feature
nav_path: "Products → (any product) → Change log → logged fields & diff"
route_name: ""
route_path: "/admin/products (modal)"
aliases: ["Change log fields", "What is logged in change log", "Change log diff", "Product diff history", "variants.updated block", "To long placeholder", "Single-entry detail modal", "Load all change log", "Кои полета се логват", "Дифф на промени"]
tags: [catalog, products, audit, history, debugging, support]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[products-change-log]]. See the hub for the other aspects (initiator decoding, business rules).

# Products → Change log → Logged fields & diff

## Purpose

This aspect documents **what the Change log records and how the diff is presented** — which fields are captured, which are excluded, how variant changes appear, and how the merchant reads, expands, and paginates the per-field before/after diff. It answers *"why don't I see the full description text in the log?"*, *"where do I see which variant changed?"*, and *"how do I load older history?"*.

## Where to find it

The diff is the middle (**Changes**) column of the [[products-change-log|Change log]] modal — open it from the [[products-products]] list row history icon or the product editor header dropdown. See the hub [[products-change-log]] for the launch points.

## What the merchant can do here

- See every change ever made to this product as a per-field before/after diff, newest first.
- Click any row to open the **single-entry detail modal** — the same data expanded to fit long diffs.
- Paginate 25 entries per page; toggle **Load all** to fetch the full history in one request.
- Read a `variants.updated` block to see which variant SKU changed and how.

### What the merchant CANNOT do here

- See the full rich-text body of `description` / `short_description` — those render as the placeholder *"To long"*.
- See storefront-only fields (sales counters, view counts, cache state) — those are not logged.
- Filter by field name inside the modal — the merchant scrolls the chronological list.
- Export the diff to CSV — the merchant copies values manually.

## Settings & fields

The modal renders a 3-column table:

| Column | Shows | Detail |
|---|---|---|
| **Date added** (`created_at`) | Timestamp of the change. | Formatted via the platform's date helper. |
| **Changes** (`dirty`) | Per-field before / after diff. Renders as a list: `<field>: <old> → <new>`. | Long-text fields (`description`, `short_description`) show the placeholder *"To long"* instead of the actual content. Variant changes render under a `variants.updated` group with one sub-block per affected variant SKU. Tags and other relations render under their relation key. |
| **Initiator** | Who / what caused the change + the action taken. | Decoded fully on [[products-change-log-initiator]]. |

### What gets logged

The Change log captures the product master record + all of its variants — `quantity`, `price`, SKU, barcode, tags, options, status, active flag, threshold, tracking, `continue_selling`, vendor, category, images, dimensions, and the per-variant equivalents of each. **Storefront-only fields are NOT logged**: sales counters, view counts, and cache state are excluded.

### Single-entry detail modal

Clicking any row opens a wider variant of the modal showing the full diff for that one change. Useful when:

- The change touched many fields at once and the row's inline diff is truncated.
- A variant block in `variants.updated` covers multiple SKUs.
- The merchant wants to copy a specific before/after pair.

The detail modal is read-only — no edit or revert actions.

### Pagination + Load all

The modal paginates 25 entries per request. The **Load all** checkbox at the top fetches every entry in one call — useful for products with sparse history where the change the merchant is hunting could be months back. For products with thousands of entries (frequent imports, high-write integrations), the merchant should leave Load all OFF and paginate to keep the modal responsive.

## Business rules

### Variant changes are logged on the PARENT product's change log

A [[variant|Variant]] has no change log of its own. When a Variant's `quantity`, `price`, `sku`, `barcode`, or any other column changes, the diff is registered against the parent product under `variants.updated`. So when investigating *"why did my Red Large SKU's quantity drop?"*, the merchant opens the **parent product's** Change log and looks for entries with a `variants.updated` block matching the SKU. This makes the parent product's log the audit trail for the whole product + all its variants — see [[inventory-variant-model]] for why the Variant is the unit of stock.

### `description` and `short_description` are not logged in full

To keep log entries small, the long-text rich-content fields `description` and `short_description` are stored with the literal placeholder string `"To long"` for both the old and new value. The merchant can SEE that those fields changed in a given save, but the full body is not retained in the log. The actual current body is on the product editor.

### One save = one entry with all diffs

When a save touches several fields, the **Changes** column lists every diff in a single row — the platform does not split a multi-field save into multiple rows. The mechanics of one-entry-per-save are covered on [[products-change-log-rules]]; here the consequence is that a single row can be long, which is exactly what the single-entry detail modal exists to expand.

## Related

- [[products-change-log]] — hub.
- [[product]] — the product entity whose fields are diffed.
- [[variant]] — variant changes are logged under the parent product (`variants.updated` block).
- [[inventory-variant-model]] — why the Variant is the unit of stock, so variant `quantity` diffs appear here.
- [[products-change-log-initiator]] — the Initiator column that pairs with each diff.
- [[products-products]] — the product editor that holds the current (full) field values.

## Open questions

- Per-field filtering inside the modal (e.g., "show me only `variants.quantity` changes") is not currently supported — the merchant scrolls the chronological list. (verify)
