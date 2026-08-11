---
type: feature
nav_path: "Orders → User Files → Deletion"
route_name: admin.order-files.list
route_path: /admin/order-files
aliases: ["User files delete", "Delete customer file", "Order file deletion", "Bulk delete user files", "Изтриване на файлове на потребителите"]
tags: [orders, files, customer-uploads, delete, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-user-files]]. See the hub for the other aspects (list view, data model, storage & delivery).

# User Files — deletion (per-row & bulk)

## Purpose

How the merchant removes a customer-uploaded file from the store, what exactly gets deleted, and why it cannot be undone. Deletion is the only mutating action on the [[orders-user-files|User Files]] page.

## Where to find it

On the [[orders-user-files-list|User Files list]] (`/admin/order-files`):

- **Per-row:** the X (delete) icon in the **Action** column of each row.
- **Bulk:** select rows via the checkboxes, then choose **Delete** from the bulk-action dropdown at the bottom of the table.

## What the merchant can do here

- **Delete one file** via the per-row X. A JS `confirm` dialog (triggered by `data-confirm`) appears first. The prompt is `Remove <option_name>?` where `<option_name>` is the product-option label (e.g., *"Remove Upload your design?"*) — NOT the filename.
- **Delete several files at once** via the bulk **Delete** action. The confirmation is the shared `page.confirm.delete` prompt (the same one used everywhere in the admin). On confirm, the platform loops through the selected file IDs and runs the same delete path as the per-row action.

On success the merchant sees a toast — *"File removed successfully"* — and the row disappears from the grid. If deletion empties the list, the [[orders-user-files-list|empty state]] re-appears.

## Settings & fields

There are no settings — deletion takes no parameters beyond the target file ID(s).

- **Confirmation chrome:** the only confirmation is the browser's JS `confirm` popup. There is no "Delete is irreversible" modal. On mobile / touch contexts where the popup may be auto-dismissed, the merchant should be especially careful.
- **Bulk request body — the `ids` field.** The bulk-delete POST handler accepts `ids` in two shapes: a comma-separated string (`ids=1,2,3`) OR an array (`ids[]=1&ids[]=2&ids[]=3`). The admin UI uses the array shape; API integrators may use either.

## Business rules

### Deletion is a 3-step operation, not a flag flip

Per-row delete performs THREE actions in sequence:

1. Calls the storage backend's delete to remove the actual file blob (S3 for modern stores, legacy storage for old ones) — see [[orders-user-files-storage-delivery]].
2. Sets the option's `value` field to `null` on the order-product-option row (so the [[orders-user-files-data-model|`type = file` + `value IS NOT NULL`]] list no longer surfaces it).
3. Removes the storage-counter ledger row — the per-tenant counter that tracks storage usage, so the merchant's storage quota is correctly decremented.

If any step fails, the merchant sees an error toast carrying the underlying exception message.

### No soft-delete / trash

There is no undo, no soft-delete, no trash. On success the blob is gone from storage immediately. The order-product-option row itself remains (with `value = null`) for audit purposes, but no downloadable file is attached. To audit a deletion the merchant must use webhooks ([[settings-hooks]]) or scan the order's product-option history — the User Files list will not show "this file used to exist".

### Deleting breaks the customer's download link

The customer's post-checkout *"Files download link"* email points at the same storage blob. Once the merchant deletes the file here, that link returns 404 — see [[orders-user-files-storage-delivery]].

### Only file-type options can be deleted via this path

A non-file option (e.g., a text input) cannot be removed through this delete path — the routine early-returns when the option `type` is not `file`. This path is exclusively for customer file uploads.

### Bulk-delete is single-job, in-process — no async

Unlike invoice bulk-download / export, bulk-delete processes ALL selected files INSIDE the request thread. No queue job, no chunking. For very large selections (hundreds of files) the merchant may hit a request timeout — they should delete in smaller batches if performance is a concern.

## Related

- [[orders-user-files]] — hub.
- [[orders-user-files-storage-delivery]] — what the blob delete touches + the broken email link.
- [[orders-user-files-data-model]] — why nulling `value` removes the row from the list.
- [[settings-hooks]] — the only audit trail for deletions.
- [[file-asset-lifecycle]] — the shared delete guard on the file-asset side.

## Open questions

None.
