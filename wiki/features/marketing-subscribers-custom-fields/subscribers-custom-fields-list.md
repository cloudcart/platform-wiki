---
type: feature
nav_path: "Marketing → Subscribers → Custom Fields → List"
route_name: subscribers-fields-list-new
route_path: /admin/marketing-new/subscribers/fields
aliases: ["Subscriber custom fields list", "Subscriber custom fields table", "Custom fields list page", "Subscriber fields sort order", "Subscriber fields reorder"]
tags: [marketing, subscribers, custom-fields, list]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[marketing-subscribers-custom-fields]]. See the hub for the other aspects (editor modal, field types, downstream surfaces).

# Subscriber Custom Fields — the list page

## Purpose

The **list view** of all subscriber custom fields the store has defined — the landing surface of the Custom fields screen. It shows every field with its type and option count, lets the merchant filter / search / reorder them, and is the entry point to the Create field modal ([[subscribers-custom-fields-editor]]) and to per-row delete.

## Where to find it

Sidebar → **Marketing** → **Subscribers** → **Custom fields**. Route: `/admin/marketing-new/subscribers/fields`. Breadcrumb: Marketing → Subscribers → Custom fields.

## What the merchant can do here

- **See the full list** of subscriber custom fields with: Name, Type, Option values count, Sort order, and a row-delete button.
- **Filter** the list by Type (Dropdown, Radio button, Checkbox, Text field, Text area, Phone).
- **Search** by name via the table's built-in search.
- Click **Add custom field** (primary button) — opens the Create field modal (see [[subscribers-custom-fields-editor]]).
- Click a **field name** to edit it (opens the Edit field modal pre-filled — see [[subscribers-custom-fields-editor]]).
- **Drag-and-drop reorder** rows (the grip handle on the left of each row). The new order is persisted server-side; toast *"Sorted successfully"* on save, *"Error occured while sorting"* on failure.
- **Bulk-delete** selected fields via the table's checkbox + bulk-action bar.
- **Single-row delete** via the trash icon; confirmation prompt: *"Are you sure you want to delete this field?"* On success: *"Field deleted successfully."*
- **Inspect option values** for selection-type fields — the "Option values" cell shows a count (e.g., *"(3)"*) that opens a dropdown listing each option name. Text / textarea / phone fields show **N/A** in this cell.

## Settings & fields

### List columns

| Column | What it shows |
|--------|---------------|
| Name | The internal (admin-only) field name; clickable — opens the edit modal. |
| Type | One of **Dropdown** (`select`), **Radio button** (`radio`), **Checkbox** (`checkbox`), **Text field** (`text`), **Text area** (`textarea`), **Phone** (`phone`). See [[subscribers-custom-fields-types]]. |
| Option values | For selection-type fields, a dropdown listing each option's name with a small count badge (e.g., *(3)*). For text-type fields, N/A. |
| Sort order | The numeric position used when these fields are rendered on subscribe forms and in the segment-condition picker. |
| (actions) | Trash icon — single-row delete with confirm prompt. |

On initial load failure the page shows *"Error while loading data"*.

## Business rules

### Sort order — controls render position

The drag-reorder on this page persists a numeric `sort_order` per field. This same order is used everywhere the fields are rendered as a list — the subscribe-form builder's custom-field picker, the storefront subscribe form, and the segment-condition picker. See [[subscribers-custom-fields-downstream]] for the full list of downstream surfaces that honour this order.

Toast on success: *"Sorted successfully."* Toast on failure: *"Error occured while sorting"* — and the list silently refetches the server's last-known order so the merchant's view doesn't desync.

The sort endpoint accepts `ids: required|array` (the new order), then assigns each field its position in that array as the new `sort_order` (0-indexed). All updates run inside a single transaction — if any fail, the entire reorder rolls back and the failure toast shows. Newly-created fields are auto-assigned `sort_order = max(sort_order) + 1`, so they always sort **last** by default until the merchant drags them up.

### Delete is permanent and cascades

Both the single-row trash icon and the bulk-delete action remove the field definition **and** all stored per-subscriber values for it — there is no undo and no soft-delete. Bulk delete uses the table's generic bulk-delete confirmation. The full cascade (option rows, segment references, subscribe-form references) is documented on [[subscribers-custom-fields-downstream]].

### Option-values cell only populates for selection types

The Option values count cell is populated only for `select`, `radio`, and `checkbox` fields; the three text-family types (`text`, `textarea`, `phone`) show **N/A** because they have no options. See [[subscribers-custom-fields-types]].

## Related

- [[marketing-subscribers-custom-fields]] — hub.
- [[subscribers-custom-fields-editor]] — the create / edit modal reached from this page.
- [[subscribers-custom-fields-types]] — the six types shown in the Type column + filter.
- [[subscribers-custom-fields-downstream]] — what the delete cascade affects + where sort order propagates.
- [[marketing-subscribers]] — parent screen.

## Open questions

No outstanding questions.
