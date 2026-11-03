---
type: feature
nav_path: "Customers → Custom fields → List view"
route_name: customers-custom-fields
route_path: /admin/customers/custom-fields
aliases: ["Custom fields list", "Custom fields table", "Drag-reorder custom fields", "Списък къстъм полета"]
tags: [customers, custom-fields, list-view]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Custom fields — list view

> Part of [[customers-custom-fields]]. See the hub for the other aspects (editor modal, types, system linkage, validation & storage, storefront behaviour, programmatic access).

## Purpose

The list-view table at `/admin/customers/custom-fields` is the merchant's home for browsing, reordering, status-toggling, and deleting custom-field definitions. Every action on this surface either reorders the storefront-checkout layout or changes a definition's availability — it does **not** touch stored customer answers (those live on a separate table; see [[customers-custom-fields-validation-storage]]).

## Where to find it

Sidebar → Customers → **Custom fields** (or directly via `/admin/customers/custom-fields`). The page title is *"Custom fields"* with the user-group header icon.

## What the merchant can do here

- **See all defined custom fields** in a paginated table. Default sort: ID descending (newest first).
- **Drag-to-reorder** the rows — the order here determines the order customers see at checkout. Drop fires a POST to `/admin/api/core/customers/fields/sort` with payload `{ids: [<id-array>]}`. Toast on success: *"Sorted successfully"*; failure toast: *"Error occured while sorting"*.
- **Click any row's Name** to open the Edit modal pre-filled (sets the row id and opens the side-panel modal — see [[customers-custom-fields-editor-modal]]).
- **Toggle Status** (Active / Inactive) per row — clicking the toggle calls `GET /admin/api/core/customers/fields/status/{0|1}/{id}`. The toggle shows its own per-row loader during the call. Toast on success: *"Status changed successfully"*. On error the toggle is reverted to the previous value and the global error handler surfaces the message.
- **Per-row Delete** (red trash icon) — bypasses the bulk modal and shows a built-in confirm. On confirm calls the delete endpoint for the single id; toast *"Field deleted successfully"*. The row is removed locally from the table without a refetch.
- **Bulk-select for bulk Delete** — selecting rows reveals the standard table-actions toolbar above the table. Bulk Delete hits `/admin/api/core/customers/fields` with the standard `deleteType="delete"` payload. The bulk action shows the standard confirm modal before sending.
- **Load all** button (above the table) — toggles between paginated mode and "show every row at once". When ON, pagination controls are disabled and the URL query is cleared. Useful when the merchant has 30+ fields and wants the full picture for drag-reorder.

## Settings & fields

The table renders these columns:

| Column | Source | Behaviour |
|--------|--------|-----------|
| **Name** | `storefront_name` | Customer-facing label. Click → opens the Edit modal. |
| **Type** | `type` (localised) | Dropdown / Radio button / Checkbox / Text field / Text area / Phone / URL field. |
| **Option values** | `value[]` join | Comma-separated option names for select / radio / checkbox; empty for text-types. |
| **Required** | `required` | Yes / No. |
| **Status** | `active` | Inline Active / Inactive toggle — calls the per-row status endpoint. |
| **(actions)** | — | Red trash icon → per-row delete confirm. |

The merchant cannot edit any cell inline — all edits happen through the side-panel modal. The only direct table-row actions are the **Status toggle** and the **Delete trash icon**.

## Business rules

### Order of fields on storefront = drag-order on this page

The drag-reorder is the **only** way to control checkout-field order. There is no per-field "sort priority" input; the visual position in this table IS the source of truth. Reorder fires the sort endpoint synchronously — if the request fails, the table reverts.

### Status toggle is independent of Required

A field can be Active = OFF (hidden from checkout) but still marked Required = ON. The Required flag only matters when the field is actually rendered to the customer — see [[customers-custom-fields-storefront-behaviour]] for the rendering rules.

### Per-row delete vs bulk delete

Both code paths end up calling the same `deleteBulk` API with an array of ids — the difference is purely UX. The per-row trash sends `[id]`; the bulk delete sends every selected id at once.

### Deleting a field is destructive

The trash icon (per-row or bulk) hard-deletes the field definition AND all stored customer answers for that field. There is no archive / restore — see [[customers-custom-fields-validation-storage]] for the cascade.

### Permission

The list page requires the `customers` permission section plus the `customers.custom_fields` sub-permission. Moderators without write grants may see the table read-only — the create / edit / delete actions are then disabled.

### Load all + filter / search

When **Load all** is ON, the paginate is set to `(1, total)` — every row is rendered. Pagination controls become inactive and the URL query string is cleared. Switching back resumes default paginated mode.

## Related

- [[customers-custom-fields]] — hub.
- [[customers-custom-fields-editor-modal]] — opens from row-name click or the **+ Add custom field** button.
- [[customers-custom-fields-validation-storage]] — what happens on delete (cascade to stored answers).
- [[customers-custom-fields-storefront-behaviour]] — how the drag-order maps to checkout ordering.

## Open questions

None.
