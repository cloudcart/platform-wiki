---
type: feature
nav_path: "Settings → Files → Delete protection"
route_name: files.settings
route_path: /admin/settings/files
aliases: ["Delete file", "Bulk delete", "In-use protection", "File delete confirmation", "Files in use"]
tags: [settings, files, delete, protection]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-files]]. See the hub for the other aspects (tabs, upload flow, storage quota, image playground, allowed types, storage backend).

# Settings → Files — delete protection

## Purpose

When the merchant deletes a file, the platform first checks whether anything references it. If yes, the delete is blocked — both on the row's delete button and inside bulk-delete selections. This page documents the protection rules, the three confirm-message variants the bulk-delete modal renders, and what actually happens on a successful delete.

## Where to find it

Files tab and User files tab — both expose:

- A per-row **Delete** button in the Actions column (only visible when the file is deletable).
- A **bulk-select** checkbox column → bulk-delete action in the table toolbar.

## What the merchant can do here

- Delete a single file via the row's delete button (only shown if the file is not in use).
- Multi-select files via the bulk checkboxes, then trigger bulk-delete from the toolbar — the confirm modal adapts to which subset is deletable.
- See toast feedback after delete:
  - Single: *"File deleted successfully"*.
  - Bulk: *"Files deleted successfully"*.

### What the merchant CANNOT do

- Delete a file that is referenced by a product, blog post, CMS page, line item, or any other binding — see the in-use check below.
- Restore a deleted file — there is no soft-delete / undo from this screen.
- Force-delete a file with bindings — the merchant must first un-bind the file from its consumers (open the affected product editor, blog post, page, etc., and remove the image) before the delete affordance reappears.

## Settings & fields

This page has no merchant-configurable settings; protection is governed by two database relations.

| Relation checked | What it means |
|------------------|---------------|
| `filemanager_records` | Bindings to product images, blog images, CMS page images, etc. If row count > 0 → file is "in use". |
| `orders_products` | References in line-item product configurations (e.g., a customer attached this image to a product they ordered). If row count > 0 → file is "in use". |

Both counters are surfaced in the table's **Used by** column (`attached_records` + `total_orders`). The row's Delete button is shown only when **both** counters are 0.

## Business rules

### Single-row delete — `show:` callback hides the button when in use

The per-row Delete button uses CcTable's `show:` callback that requires `attached_records == 0`. So if a file is referenced anywhere, the merchant sees no delete affordance at all on that row — there's no error toast to dismiss, the button simply isn't there.

On successful delete the toast shows *"File deleted successfully"*; on a server error the standard error toast surfaces. The action is silently a no-op for in-use files since the affordance was hidden.

### Bulk-delete — three confirm-message variants

The bulk-delete confirm message in `useFilesTable` branches dynamically based on selection state vs in-use protection:

| Selection state | Confirm message | Save button |
|-----------------|-----------------|-------------|
| **All deletable** — every row has `attached_records == 0` AND `total_orders == 0` | *"Are you are sure you want to delete? Caution: This action cannot be undone."* | Enabled |
| **Mixed** — some deletable, some in use | *"Only `<X>` of `<Y>` files can be removed, other files are in use, do you want to proceed?"* | Enabled — proceeds with only the deletable subset |
| **All in use** — every row has `attached_records > 0` OR `total_orders > 0` | *"These files are in use, you cannot delete them"* | **Disabled** |

The protection is enforced client-side: the bulk-delete POST body's `ids` array is filtered to **only deletable file IDs** before sending. So an in-use file in the selection is silently dropped from the request; the merchant must un-bind the file from products / orders first.

### Foreign-key protection at the database layer

The DB schema's foreign-key constraints would also reject an attempt to delete a referenced file — so the client-side filter is the user-friendly first line, and the FK constraint is the safety net. Merchants never see the FK error message because the client never gets to send a request that would trigger it.

### Delete is synchronous — S3 + DB + storage record

When the merchant deletes a file, the model's `deleted` event triggers two things in sequence:

1. **S3 object deletion** — the bytes are removed from the storage bucket (see [[settings-files-storage-backend]]).
2. **Storage tracker row deletion** — the polymorphic `system_storage` row is removed, freeing the quota.

If the S3 delete fails (network blip, object already missing), the DB row is still removed. There is no pending-deletion / retry queue for failed S3 deletions — they are best-effort. In rare cases an orphan blob might remain on S3 with no DB pointer — those are cleaned up by infrastructure-level bucket sweeps invisible to merchants.

### No undo

There is no soft-delete column on the `filemanager` table and no restore endpoint exposed in the UI. A deleted file is gone from S3 within seconds. CDN-cached copies may keep serving the file briefly until cache expiry. Merchants who want a safety net should download a copy before deletion or rely on [[settings-backups]] (which captures DB state but **not** file contents — see the [[backups-and-restore]] concept page for the caveat that media files are NOT rolled back by a restore).

### Delete protection is the merchant's lever to spot orphans

If a file is "unused" (counters at 0) but the merchant remembers binding it somewhere, that's a hint the binding broke or was moved. The Delete button being available on a file the merchant thinks should be in use is itself diagnostic — the file is no longer referenced.

## Related

- [[settings-files]] — hub.
- [[settings-files-tabs]] — where the Delete button lives in the table column structure.
- [[settings-files-storage-quota]] — deletes free up shared quota.
- [[settings-files-storage-backend]] — what happens to bytes on S3 + CDN after delete.
- [[settings-backups]] / [[backups-and-restore]] — restores roll back the database but NOT file contents.

## Open questions

None.
