---
type: feature
nav_path: "Settings → Files → Delete protection"
route_name: files.settings
route_path: /admin/settings/files
aliases: ["Delete file", "Bulk delete", "In-use protection", "File delete confirmation", "Files in use", "Delete file used by metafield", "Metafields use it", "Изтриване на файл", "Файл в метаполе"]
tags: [settings, files, delete, protection]
plan_gates: []
created: 2026-06-10
updated: 2026-11-03
source_count: 4
---

> Part of [[settings-files]]. See the hub for the other aspects (tabs, upload flow, storage quota, image playground, allowed types, storage backend).

# Settings → Files — delete protection

## Purpose

When the merchant deletes a file, the platform first checks whether it is bound to a product, blog post, CMS page or order line. If yes, the delete is blocked — both on the row's delete button and inside bulk-delete selections. A file that only metafields use can still be deleted, after a confirmation that counts them. This page documents the protection rules, the confirm messages, and what actually happens on a successful delete.

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

- Delete a file that is bound to a product, blog post, CMS page or line item — see the in-use check below. A metafield value is not one of those bindings: see "Files that metafields use".
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

### Files that metafields use

A file field's value ([[metafields-definitions]]) blocks nothing and does not count in the **Used by** column. The list only knows whether metafields use each file.

- **Single delete**: a confirmation titled *"Delete «{name}»?"* reads the counts when it opens: *"Metafields use it; it is removed from them:"*, a line per owner type with its count (Products, Customers, Categories, Entries), or *"No metafield uses it any more."*, then *"This can't be undone."* While counting it says *"Counting where it is used…"*. If the counts cannot be read it says *"Where it is used could not be counted."* and Delete stays disabled.
- **Bulk delete**: the confirm message gains *"Metafields use {count} of these files; they lose them."*
- **After deleting**: a single reference is cleared, and a list loses the item and is removed when empty. Very large clean-ups finish in the background.
- The counts need the file manager's own permission (Settings or Settings → Files).

### Delete is synchronous — S3 + DB + storage record

When the merchant deletes a file, the model's `deleted` event triggers two things in sequence:

1. **S3 object deletion** — the bytes are removed from the storage bucket (see [[settings-files-storage-backend]]).
2. **Storage tracker row deletion** — the polymorphic `system_storage` row is removed, freeing the quota.

If the S3 delete fails (network blip, object already missing), the DB row is still removed. There is no pending-deletion / retry queue for failed S3 deletions — they are best-effort. In rare cases an orphan blob might remain on S3 with no DB pointer — those are cleaned up by infrastructure-level bucket sweeps invisible to merchants.

### No undo

There is no soft-delete column on the `filemanager` table and no restore endpoint exposed in the UI. A deleted file is gone from S3 within seconds. CDN-cached copies may keep serving the file briefly until cache expiry. Merchants who want a safety net should download a copy before deletion or rely on [[settings-backups]] (which captures DB state but **not** file contents — see the [[backups-and-restore]] concept page for the caveat that media files are NOT rolled back by a restore).

## Related

- [[settings-files]] — hub.
- [[settings-files-tabs]] — where the Delete button lives in the table column structure.
- [[settings-files-storage-quota]] — deletes free up shared quota.
- [[settings-files-storage-backend]] — what happens to bytes on S3 + CDN after delete.
- [[settings-backups]] / [[backups-and-restore]] — restores roll back the database but NOT file contents.
- [[metafields-definitions]] — what happens to a value when the record it points to is deleted.

## Open questions

None.
