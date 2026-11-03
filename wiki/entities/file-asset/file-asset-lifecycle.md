---
type: entity
nav_path: "Entity → File / Asset → Lifecycle & delete protection"
aliases: ["File lifecycle", "File delete protection", "File in use", "Orphan file", "Bulk delete files", "Replace file", "Delete file", "Жизнен цикъл на файл", "Изтриване на файл", "Файл в употреба"]
tags: [entity, settings, media, storage, files, lifecycle, delete]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[file-asset]]. See the hub for the other aspects (storage model, quota, CDN transforms, customer uploads, image pickers).

# File / Asset — lifecycle & delete protection

## Identity

The **lifecycle** is the state path a file moves through from upload to deletion, plus the **delete-protection** rules that block removing a file that something still references. The two facts merchants hit most often: a file with a non-zero "Used by" count **cannot be deleted**, and **deletion is irreversible** (no undo / soft-delete). There is also **no "replace this file" action** — swapping an image means uploading a new one, re-pointing each binding, then deleting the old file.

## Aliases

- **File lifecycle** — the uploaded → referenced → orphan → deleted path.
- **Delete protection** / **file in use** — the in-use-counter guard.
- **Orphan file** — an unreferenced file (deletable).
- **Bulk delete** — the multi-select delete flow.
- **Жизнен цикъл на файл** / **Изтриване на файл** / **Файл в употреба** — Bulgarian equivalents.

## Key Attributes

| State | Meaning | Trigger / exit |
|-------|---------|----------------|
| **Uploaded** | The blob exists in storage and a `Filemanager` row exists | Created on upload completion (chunked for large files — see [[file-asset-storage-model]]). |
| **Referenced** | Bound to one or more entities; `attached_records` > 0 | The file shows a non-zero "Used by" count; cannot be deleted. |
| **Unreferenced (orphan)** | Bindings removed but blob still in storage; "Used by" = 0 | Now deletable. |
| **Deleted** | Blob removed from storage + `Filemanager` row removed | Irreversible — no undo / soft-delete. |
| **Failed-upload cleanup** | Interrupted chunked upload | Orphan S3 parts swept by lifecycle rule after 7 days (see [[file-asset-storage-model]]). |

## Relationships

The lifecycle ties together the rest of [[file-asset]]:

- **[[file-asset-storage-model]]** — upload completion creates the `Filemanager` row; deletion calls the backend delete API.
- **[[file-asset-quota]]** — deleting unreferenced files is how the merchant reclaims quota.
- **[[file-asset-customer-uploads]]** — the `orders_products` counter that protects customer-attached files from deletion is the same delete-guard described here.

## Where it appears

- [[settings-files]] — per-row Delete + bulk Delete on the Files tab.
- [[orders-user-files]] — delete of customer-uploaded files runs the same guard (the `orders_products` side).

### The five lifecycle states

1. **Uploaded** — the merchant or a customer uploads via one of the upload modules (Files tab in [[settings-files]], the in-product image picker, the blog editor, the page-builder image block — see [[file-asset-image-pickers]]) OR a customer uploads via a file-type product-option at checkout (see [[file-asset-customer-uploads]]).
2. **Referenced** — the merchant binds the file to one or more entities. `attached_records` increments and the file shows a non-zero "Used by" count.
3. **Unreferenced (orphan)** — bindings are removed but the file itself stays in storage; the "Used by" count drops to 0 and the merchant can now delete it.
4. **Deleted** — the merchant clicks Delete (per-row or bulk). The platform calls the storage backend's delete API and removes the `Filemanager` row. **Deletion is irreversible** — there is no undo / soft-delete from this screen.
5. **Failed-upload cleanup** — if a chunked upload is interrupted, the partial parts on S3 are invisible and the bucket-level lifecycle rule sweeps them after 7 days, with no merchant UI.

### Delete protection — file must be unused

The delete endpoint checks two relations:

- **`filemanager_records`** — bindings to product images, blog images, CMS page images, email-template images, etc.
- **`orders_products`** — references in line-item product configurations (e.g., a customer attached this image to a product they ordered — see [[file-asset-customer-uploads]]).

If EITHER count > 0, single delete returns an error. Bulk delete filters out in-use files client-side and shows three different confirmation messages:

- **All selected deletable** → *"Are you sure you want to delete? Caution: This action cannot be undone."*
- **Mix** → *"Only X of Y files can be removed, other files are in use, do you want to proceed?"*
- **None deletable** → *"These files are in use, you cannot delete them"* with disabled Save.

### No replace-everywhere workflow

To swap a product image (or any binding), the merchant uploads a new file, binds it to the product from the product editor, and removes the old file. **There is no "replace this file" action that rewrites every reference** — each reference must be re-pointed individually. Likewise, a file **cannot be renamed** after upload; to "rename" a file the merchant uploads it again under the new name and deletes the original.

## Related

- [[file-asset]] — hub.
- [[file-asset-storage-model]] — upload completion creates / deletion removes the storage blob; 7-day orphan-part cleanup.
- [[file-asset-quota]] — deleting unused files reclaims quota.
- [[file-asset-customer-uploads]] — the `orders_products` delete-guard side.
- [[file-asset-image-pickers]] — where bindings (the `attached_records` count) originate.
- [[settings-files]] — per-row + bulk delete UI.

## Open Questions

- ⏸️ Whether a future "replace everywhere" action is planned, given how common image swaps are.
- ⏸️ Whether deleting a customer-attached file affects the parent order's checkout / packing-slip rendering.
