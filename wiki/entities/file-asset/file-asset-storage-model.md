---
type: entity
nav_path: "Entity → File / Asset → Storage model"
aliases: ["File storage model", "S3 vs legacy storage", "Chunked upload", "Multipart upload", "Public file storage", "File folder auto-decision", "No antivirus scanning", "Складиране на файлове", "Публични файлове"]
tags: [entity, settings, media, storage, files, s3, cdn, security]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[file-asset]]. See the hub for the other aspects (quota, lifecycle, CDN transforms, customer uploads, image pickers).

# File / Asset — storage model

## Identity

The **storage model** is how CloudCart physically stores uploaded files, where they live, how large files get uploaded, and what security properties the storage carries. Files are stored on **S3** for newer / migrated stores and on a **legacy storage** backend for older files. The URL-retrieval logic handles both transparently — the merchant sees a unified [[settings-files]] list regardless of where each file is stored. Two security facts about this model matter to merchants and are documented here: every file is **public**, and **nothing is virus-scanned**.

## Aliases

- **File storage model** / **storage backend** — the S3 / legacy split.
- **Chunked upload** / **multipart upload** — the large-file path.
- **Public file storage** — the no-per-file-privacy model.
- **Складиране на файлове** / **Публични файлове** — Bulgarian equivalents.

## Key Attributes

| Aspect | Behaviour | Notes |
|--------|-----------|-------|
| **Storage backend** | `s3` (newer / migrated stores) vs `legacy` (older files) | Unified retrieval — the merchant never sees the distinction in the UI. |
| **Folder placement** | Auto-decided by the platform based on the file's **extension** | The merchant cannot pick a folder manually. |
| **Per-file privacy** | None — every file is PUBLIC | No signed-URL admin option, no "owner-only access" flag. |
| **Antivirus / malware scan** | None | Applies to both admin and customer uploads. |
| **Large-file upload** | Chunked S3 multipart | A `Filemanager` row exists only AFTER completion. |
| **Orphan-part cleanup** | `AbortIncompleteMultipartUpload` lifecycle rule after **7 days** | Automatic; no merchant UI. |

## Relationships

The storage model underpins every other aspect of [[file-asset]]:

- **[[file-asset-quota]]** — the size of stored blobs is what counts against the plan-gated quota.
- **[[file-asset-lifecycle]]** — the chunked-upload completion step is what creates the `Filemanager` row; the delete step calls the backend's delete API.
- **[[file-asset-cdn-transforms]]** — image files stored here are served through the image delivery service; non-image files are served as direct downloads.

## Where it appears

- [[settings-files]] — the Files tab lists every stored file regardless of backend.
- All admin upload modules write into this same storage. See [[file-asset-image-pickers]].

### Chunked S3 multipart upload for large files

For small files, a single PUT works. For larger files, the client requests a multipart upload — it gets an `upload_id`, uploads each chunk to S3, and the server completes the multipart upload on the last chunk. **Round-robin routing across server pods works unchanged** because state lives on S3, not on a pod's filesystem. A `Filemanager` row exists only AFTER completion — so the DB never points at a half-written blob. If the merchant closes the tab mid-upload, the upload is silently aborted and no orphan file appears in the list. Partial parts on S3 are invisible (no finished object exists) and the bucket-level `AbortIncompleteMultipartUpload` lifecycle rule sweeps them after **7 days**.

### Folder auto-decision + allowed extensions

The folder a file gets stored in is **auto-decided by the platform based on the file's extension** — the merchant cannot pick a folder manually. The file picker only accepts extensions the platform recognises for each upload folder; the list shown as the `accept` filter is the union across all folder types. Allowed extensions include `jpeg`, `jpg`, `gif`, `png`, `svg`, `webp` for images plus a few document / spreadsheet / PDF types for non-image folders. The platform default **maximum file size is 1024 MB (~1 GB) per file**; larger files are rejected with an inline error.

### All filemanager files are PUBLIC (no per-file privacy flag)

Every file uploaded through the file manager is stored on S3 and served publicly through CloudCart's CDN (the image delivery service + nginx-images). There is **no per-file privacy flag, no signed-URL admin option, and no way to mark a file as "owner-only access"** from the admin UI. Anyone with the URL can fetch the file. Order-attached customer uploads served through the platform's order-download endpoint are also public — they sit at obscure URLs but are not authenticated.

Merchants who must store genuinely confidential files (signed contracts, ID scans, etc.) should NOT use the filemanager; they should host such files elsewhere with proper access control.

### No antivirus / malware scanning of uploaded files

The platform does **NOT** scan uploaded files for viruses or malware before storing or serving them. This applies to both admin uploads on the Files tab and customer uploads on the User files tab (see [[file-asset-customer-uploads]]). Merchants should treat customer-uploaded files as potentially hostile content — they should not be downloaded or opened locally without the merchant's own antivirus check. **SVG uploads from customers are especially risky** since SVG can carry embedded scripts (and SVG bypasses the image delivery service — see [[file-asset-cdn-transforms]]).

### System-managed files are hidden from the merchant

The platform generates internal files (thumbnails, exports, etc.) that don't appear in the merchant's file-manager view. The merchant only ever sees their own uploads plus customer uploads.

## Related

- [[file-asset]] — hub.
- [[file-asset-quota]] — stored-blob size counts against the plan-gated quota.
- [[file-asset-lifecycle]] — upload-completion creates, and delete removes, the storage blob.
- [[file-asset-cdn-transforms]] — image serving via the image delivery service; SVG bypass.
- [[settings-files]] — the central file-manager screen.
- [[plan-gates]] — the storage-quota gating framework.

## Open Questions

- ⏸️ Whether the merchant can configure storage retention to auto-purge old files (e.g., delete files older than N years for GDPR).
- ⏸️ Whether any merchant-facing setting exists to restrict customer SVG uploads given the embedded-script risk.
