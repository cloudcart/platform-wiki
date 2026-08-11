---
type: feature
nav_path: "Settings → Files → Upload flow"
route_name: files.settings
route_path: /admin/settings/files
aliases: ["File upload", "Chunked upload", "S3 multipart upload", "Upload progress", "Auto-resize image"]
tags: [settings, files, upload, s3, chunked]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-files]]. See the hub for the other aspects (tabs, storage quota, delete protection, image playground, allowed types, storage backend).

# Settings → Files — upload flow

## Purpose

How a merchant gets a file into the store, from clicking **+ Upload files** through chunked S3 multipart transfer to a finished `Filemanager` row in the table. This page documents the workflow that's only available on the Files tab — customer-uploaded files on the User files tab arrive via storefront flows, not this button.

## Where to find it

Files tab (default landing of `/admin/settings/files`) → **+ Upload files** button in the page header. The button does NOT exist on the User files or Image playground tabs.

## What the merchant can do here

- Click the header **+ Upload files** button → native multi-file picker opens (no interstitial modal). The OS file dialog shows only extensions the platform recognises — see [[settings-files-allowed-types]].
- Select one or more files. Upload begins immediately; files upload **sequentially** (one at a time), each with its own progress bar.
- Read the live progress strip above the table during upload.
- Close the tab mid-upload — the in-flight upload is silently aborted and no orphan file appears in the list (S3 lifecycle rule sweeps any partial parts after 7 days).

### What the merchant CANNOT do

- Pause or resume an upload.
- Re-target an in-progress upload to a specific filename slot — every upload creates a new row.
- Pick a destination folder — the platform auto-routes by extension (see [[settings-files-allowed-types]]).
- Upload while storage is at 100% — the button is disabled (see [[settings-files-storage-quota]]).

## Settings & fields

The upload UI has no merchant-configurable settings on this page; it composes around two server-defined caps and the file picker's `accept` filter.

| Element | Source | Value |
|---------|--------|-------|
| Max file size | `meta.config.max_size` (server, from `upload.files_max_size`) | **1024 MB (~1 GB)** per file |
| Allowed extensions | union of all the theme templates | ~50 extensions across 7 categories — see [[settings-files-allowed-types]] |
| `accept=` on the picker | union string of all allowed extensions | sent verbatim to the OS file picker |

## Business rules

### Pre-upload client-side validation

Done in `useFilesActions.handleUpload` before any bytes leave the browser:

- **Extension check** — filename's extension must appear in the allowed-extensions union. Invalid → file is rejected at client; not even attempted to upload.
- **Size check** — file size in MB must be `<= meta.config.max_size`. Oversize → file is rejected at client.

Invalid files trigger the **Upload Error inline strip** (red, replaces the progress strip): *"Invalid files: `<filenames>`. Valid file types are: `<extensions list>`"*. Bad files are listed; valid files in the same batch are uploaded normally. The error strip auto-clears 100 ms after the upload settles.

### Auto-resize for images

Image MIME-type files (`image/*`) are run through `resizeImageIfNeeded` before chunking. This protects against the merchant uploading an 8000×6000 photo that nobody needs — it's reduced to a sensible storefront-friendly resolution before bytes are sent to S3. The merchant doesn't see this happen; they just see the resulting file row.

### Chunked S3 multipart upload — the transfer mechanism

Uploads use the `S3FilemanagerChunkedUploader` workflow. The threshold is **5 MB** (`FILEMANAGER_MIN_PART_SIZE_BYTES = 5 * 1024 * 1024`), which is S3's minimum part size:

- **Files ≤ 5 MB** — single PUT path (one request, no `upload_id` ceremony).
- **Files > 5 MB** — split into 5 MiB chunks. The first chunk POST returns an `upload_id` which the client echoes back on every subsequent chunk. The last chunk finalises the multipart upload server-side via `completeMultipartUpload`.

Every chunk hits `POST /admin/api/core/settings/files/upload`. Round-robin routing across server pods works unchanged because **state lives on S3, not on filesystem** — any pod can serve any chunk for any in-flight upload as long as it's holding the `upload_id`.

### Interrupted / cancelled uploads — no orphan rows

A `Filemanager` row exists ONLY after the multipart upload completes. If an upload is interrupted (tab closed, network drop, merchant clicks away):

- Partial parts on S3 are invisible — no finished object exists at the target key.
- The bucket-level `AbortIncompleteMultipartUpload` lifecycle rule sweeps them after **7 days**.
- The DB never points at a half-written blob.

Merchant-visible effect: large uploads show a progress bar; if the merchant closes the tab mid-upload, the file silently disappears from the queue — it does not appear half-uploaded in the table.

### Upload progress strip

While an upload runs, the page renders an animated strip above the table (via `Vue3SlideUpDown`):

- *"Uploading your file, please wait"* heading.
- A green `b-progress` bar; value = current chunk index, max = total chunk count. For single-chunk uploads the max is set to 2 so the bar shows a smooth two-tick progression rather than instant jump.
- Filename of the file currently uploading shown in small grey text below the bar.
- Files upload **sequentially**, so the progress applies to one file then resets for the next.

### Toasts at completion

- Single file: *"File uploaded successfully"*.
- Multi-file batch: *"`<N>` files uploaded successfully"* (one final toast for the whole batch).
- Server error mid-upload: surfaces the error message + the page's standard error handler.

### Unique-name handling on collision

If a merchant uploads a file whose name collides with an existing file in the same directory, the platform calls `generateUniqueName` which appends a `-<uniqid>` segment to the filename until it's unique. So uploading `photo.jpg` twice creates `photo.jpg` and `photo-67abc123.jpg` (or similar). The merchant sees both in the table with their distinct names.

**There is no overwrite / upsert flow** — every upload is a brand-new file row. To "replace" a file the merchant must upload the new one, re-bind any consumers (product editor, blog editor, page editor), then delete the old file. See the [[settings-files-storage-backend]] note on the absent "replace everywhere" workflow.

### Synchronous — no queue

Upload and delete are synchronous within the request. There is no background queue. The `file_download` admin notification (under [[settings-admin-notifications]]) fires only when LARGE aggregate exports complete (e.g., the orders CSV export) — uploads on this page do not trigger that notification.

### Internal upload log (merchant-invisible)

The platform records every file upload in an internal log used by CloudCart support / SRE for troubleshooting. The merchant doesn't see this log — for upload failure diagnosis they need to either retry, check the error message, or contact CloudCart support.

## Related

- [[settings-files]] — hub.
- [[settings-files-allowed-types]] — what extensions are accepted and which folder a file lands in.
- [[settings-files-storage-quota]] — why uploads can be blocked at 100% usage.
- [[settings-files-storage-backend]] — Hetzner Object Storage + CDN URL produced after upload completes.
- [[settings-brand]] — uses this upload via the OG-image two-step upload (`/admin/api/core/settings/files/upload`).
- [[settings-admin-notifications]] — `file_download` notification fires on aggregate exports, not on regular uploads.

## Open questions

None.
