---
type: feature
nav_path: "Settings → Files → Allowed file types"
route_name: files.settings
route_path: /admin/settings/files
aliases: ["Allowed file extensions", "File type whitelist", "Upload extensions", "Maximum file size", "Auto-routing by extension"]
tags: [settings, files, mime, extensions, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[settings-files]]. See the hub for the other aspects (tabs, upload flow, storage quota, delete protection, image playground, storage backend).

# Settings → Files — allowed file types and size cap

## Purpose

What the platform will let the merchant upload, what it routes where, and what it silently rejects. The allowed-types whitelist is the platform's primary defensive layer — there is no antivirus scan — so understanding which extensions land in which "folder" matters both for organisation and for safe handling of customer-uploaded content.

## Where to find it

These rules are enforced invisibly during the upload flow on the Files tab (Sidebar → Settings → **Files**). The native file picker's `accept=` filter is the union of all categories; the merchant sees the result (a file is accepted, rejected, or routed to one of seven folders) but the rules themselves are not surfaced in the UI.

## What the merchant can do here

- Upload any file whose extension is in the whitelist below — see [[settings-files-upload-flow]] for the upload flow itself.
- Read the inline error strip *"Invalid files: `<filenames>`. Valid file types are: `<extensions list>`"* if any file in the batch is rejected — the error strip itself is the only place the merchant sees the full allowed-extensions list in UI form.

### What the merchant CANNOT do

- Pick which "folder" a file lands in — the platform auto-routes by extension.
- Add new extensions to the whitelist — the theme templates is a server-side configuration.
- Override the 1024 MB per-file cap — it is hardcoded server-side, not plan-based.
- Upload files with extensions not in the union — the picker doesn't even show them on most operating systems, and any that get through are rejected at client validation.

## Settings & fields

### Seven directory types with explicit extension whitelists

The platform organises uploads into 7 "directory types", each with its own MIME-type and extension allowlist. The upload picker's `accept` filter is the UNION of all categories. The platform auto-routes a file to the right directory by extension.

| Directory | Extensions allowed |
|-----------|-------------------|
| **image** | `bmp`, `gif`, `png`, `jpg`, `jpe`, `jpeg`, `tif`, `tiff`, `svg`, `webp` |
| **doc** | `pdf`, `doc`, `docx`, `xls`, `xlsx`, `ppt`, `pptx`, `txt`, `csv`, `rtf`, `xml`, `json` |
| **archive** | `gz`, `gzip`, `zip`, `tar`, `tar.gz`, `tgz`, `7z` |
| **audio** | `mp3`, `wav`, `ogg`, `m3u` |
| **video** | `mpeg`, `mpg`, `mpe`, `mov`, `avi`, `flv`, `mp4`, `wmv`, `m3u8` |
| **font** | `woff2`, `woff`, `eot`, `ttf` |
| **text** | `css`, `js` |

Total whitelist: **~50 extensions across 7 categories**. The file picker accepts the full union; the auto-routing decides which folder the file lands in.

### Common formats NOT in the list — silently rejected

The following common formats are rejected at upload (extension not in any category):

- HEIC / HEIF (Apple's iPhone photo format).
- AVIF (modern image format — note: the CDN can OUTPUT AVIF, but the input whitelist doesn't accept it).
- AIFF (audio).
- MKV (video).
- EPS / AI / PSD (Adobe formats).
- BMP variants other than `bmp` itself.
- RAR (archive).
- RAW camera formats (`.cr2`, `.nef`, `.arw`, etc.).
- Anything with no extension.

Merchants whose customers upload iPhone HEIC photos via storefront forms will see those uploads fail; the workaround is for the customer to convert to JPEG first.

### Per-file size cap — 1024 MB

The cap is configured by `upload.files_max_size`. This is a **hardcoded server-side limit, not plan-based**. The same cap applies on the Files tab and on customer uploads through storefront file-upload [[product-option|Product options]]. There is no way to raise this from the admin UI.

Pre-upload client validation rejects oversize files before sending bytes — see [[settings-files-upload-flow]]. The inline error strip identifies which files exceeded the cap.

## Business rules

### Auto-routing decides the folder

The folder a file gets stored in is auto-decided by the platform based on the file's extension — the merchant cannot pick a folder manually. This determines:

- The `dir` field on the Filemanager row (e.g., `image`, `doc`, `video`).
- The CDN URL path: `cdncloudcart.com/{site_id}/files/{dir}/{name}` (see [[settings-files-storage-backend]]).
- Whether the file goes through the image delivery service on read (`image` directory) or is served as a passthrough (everything else).

### Image directory → the image delivery service transform pipeline

Files in the `image` directory are served through nginx-images → the image delivery service → S3. They support the full CDN-transform query parameters (see [[settings-files-image-playground]]). The exception: **SVG bypasses the image delivery service entirely** and is served as-is from S3.

All other directories (`doc`, `archive`, `audio`, `video`, `font`, `text`) are S3 passthroughs — no transform layer, the bytes the merchant uploaded are exactly the bytes customers download.

### Allowed extensions are the platform's primary defensive layer

The platform does **NOT** scan uploaded files for viruses or malware before storing or serving them. This applies to both admin uploads on the Files tab and customer uploads on the User files tab. So the allowed-extensions list is the **primary defensive layer**. Merchants should treat customer-uploaded files as potentially hostile content — they should not be downloaded or opened locally without the merchant's own antivirus check.

Specific risk areas:

- **SVG uploads from customers** — SVG can carry embedded scripts. Merchants accepting customer SVG uploads on storefront forms should be especially cautious.
- **Doc category extensions** (`pdf`, `docx`, `xlsx`, etc.) — Office documents and PDFs can carry macros or exploits. Merchants reviewing customer attachments should open them inside sandbox apps.
- **Archive category** — `zip`, `7z`, `tar.gz` can contain anything when unpacked; the platform does not inspect contents.

### Extension is checked client-side AND filtered by the picker

The pre-upload validation in `useFilesActions.handleUpload` checks the extension before bytes leave the browser — this is the user-friendly check that produces the *"Invalid files"* error strip. The native file picker's `accept=` filter (passed as the union of all allowed extensions) is the first line: it stops the OS from showing disallowed files in the chooser at all on most platforms.

A determined merchant can still drag-and-drop a disallowed file or paste a `File` object via developer tools — but the client validation will reject it. There is no third server-side rejection that produces a different message; the server trusts that the client has filtered.

### Unique-name generation on collision

If a merchant uploads two files with the same name, the second gets a `-<uniqid>` suffix to keep the URL path unique. See [[settings-files-upload-flow]] for the mechanics. The extension and folder-routing rule still applies to the renamed file — the suffix is inserted before the extension.

### File-upload [[product-option|Product options]] inherit these limits

Customer-facing file-upload Options (e.g., "Upload your custom design") use the same platform-wide caps from this page. There is **no per-Option override** for size or MIME — the Option editor lets the merchant accept-or-deny a file-upload field but not configure stricter limits per field.

## Related

- [[settings-files]] — hub.
- [[settings-files-upload-flow]] — pre-upload validation enforces these limits.
- [[settings-files-storage-backend]] — `image` directory goes through the image delivery service; others are passthrough.
- [[settings-files-image-playground]] — preview is for `image` directory only.
- [[product-option]] — customer-facing file-upload Options inherit these caps.

## Open questions

None.
