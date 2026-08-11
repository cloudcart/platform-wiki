---
type: feature
nav_path: "Settings → Files"
route_name: files-index
route_path: /admin/settings/files
aliases: ["Files", "File manager", "Filemanager", "User files", "Image playground", "Файлове", "Файлов мениджър"]
tags: [settings, files, media, storage, cdn]
plan_gates: ["storage"]
created: 2026-05-21
updated: 2026-06-10
source_count: 6
---

# Files

## Purpose

A three-tab file-management screen at `/admin/settings/files`. The first tab is the store's general file manager — every image, document, and asset the merchant uploaded for use across the storefront (product photos, blog images, page assets, etc.) is listed and editable here, plus a "Upload files" workflow with chunked upload for large files. The second tab shows files uploaded BY customers when they attached them to orders (e.g., file-upload [[product-option|Product options]]). The third tab is an interactive image-transform playground that previews how the CDN renders any filemanager image under different width / height / crop / format / quality / pad-colour parameters.

The page enforces a storage quota: a real-time used/total progress bar sits at the top; uploads are blocked when the quota hits 100% with an *"Upgrade storage space"* call-to-action. The quota counts ALL platform files (admin uploads, customer uploads, product images, logos, blog images, fiscal-printer audit files, etc.) — not just files on this tab.

## Where to find it

Sidebar → Settings → **Files**. Route `/admin/settings/files`. Breadcrumb: "Settings → `<active tab label>`".

Three sub-tabs:

| Label | Route name | Route path |
|-------|------------|------------|
| Files (default landing) | `files.settings` | `/admin/settings/files` |
| User files | `files.order-files` | `/admin/settings/files/order-files` |
| Image playground | `files.playground` | `/admin/settings/files/playground` |

## Sub-pages (in this cluster)

Split into 7 aspect pages — drill into the one that matches the question, not every page.

- [[settings-files-tabs]] — the three sub-tabs, table columns per tab, the two file-preview modal variants (with vs without embedded playground), permissions.
- [[settings-files-upload-flow]] — the Upload button workflow, pre-upload validation, auto-resize for images, chunked upload for files > 5 MB, sequential progress strip, unique-name handling on collision.
- [[settings-files-storage-quota]] — the used/total module, the Statistics modal (Item Type / Records Count / Total Size), what counts against quota across the whole platform, plan-feature pack purchase via *"Upgrade storage space"*.
- [[settings-files-delete-protection]] — single-row vs bulk delete, the three confirm-message variants (all-deletable / mixed / all-in-use), the in-use / attached-to-order checks, no undo / no soft-delete.
- [[settings-files-image-playground]] — standalone vs embedded mode, the four control fields (width / height / crop / pad colour), client-side CDN URL composition, the reset / copy-URL actions, what the playground can and cannot transform.
- [[settings-files-allowed-types]] — the 7 directory types and their ~50 extensions, the 1024 MB per-file cap, common formats rejected (HEIC, AVIF input, RAR, EPS, RAW), auto-routing by extension.
- [[settings-files-storage-backend]] — where files are hosted, the CDN host `cdncloudcart.com`, public CDN URLs (no signed-URL option), no antivirus, no "replace everywhere" workflow.

## What the merchant can do here

Each item has a dedicated aspect page above:

- See admin-uploaded files; sort / filter / search; preview; bulk-delete. → [[settings-files-tabs]]
- See files uploaded by customers via the User files tab. → [[settings-files-tabs]]
- Click **+ Upload files** to upload (chunked for large files, sequential progress strip). → [[settings-files-upload-flow]]
- Watch the storage usage module + Statistics modal; buy a storage pack at 100%. → [[settings-files-storage-quota]]
- Delete unused files individually or in bulk. → [[settings-files-delete-protection]]
- Preview CDN transforms in the Image playground and copy the generated URL. → [[settings-files-image-playground]]

### What the merchant CANNOT do

- Rename a file after upload, pick a folder manually (auto-routed by extension — [[settings-files-allowed-types]]), replace a file's bytes at the same URL, restore a deleted file, delete a file in use ([[settings-files-delete-protection]]), or mark a file private ([[settings-files-storage-backend]]).

## Settings & fields

Every operational field is documented in its aspect page; overview below.

| Surface | Field / element | Aspect page |
|---------|-----------------|-------------|
| Files tab + User files tab | Storage usage module (Used / Total / progress bar / 100% banner) | [[settings-files-storage-quota]] |
| Files tab | + Upload files button | [[settings-files-upload-flow]] |
| Files tab | Table columns: Name, Size, Created, Used by, Actions | [[settings-files-tabs]] |
| User files tab | Table columns: Name, Size, Created, Used by, Order ID, Product name | [[settings-files-tabs]] |
| Upload validation | Max file size 1024 MB, allowed extensions union | [[settings-files-upload-flow]] + [[settings-files-allowed-types]] |
| Image playground | Width, Height, Crop / gravity, Padding color | [[settings-files-image-playground]] |
| Delete confirmation | Three message variants based on selection-vs-protection state | [[settings-files-delete-protection]] |

## Business rules

These rules cut across aspects; box-specific rules live in each aspect page.

### Storage quota is shared and platform-wide

The "Used" number counts every stored file: admin uploads, customer uploads, product images, logos, vendor / category / page / blog / parameter-option images, admin avatars, shipping / payment-provider images, discount labels, product banners, N-18 audit files, form-field and cart-item option files, and order-product option files. A single Files-tab delete may not free the expected quota if the bottleneck is elsewhere — see [[settings-files-storage-quota]] for the Statistics breakdown.

### All filemanager files are public; no malware scanning

There is no per-file privacy flag, no signed-URL option, no owner-only access — anyone with the CDN URL can fetch the file. Uploads are also not virus-scanned; the platform's primary defensive layer is the [[settings-files-allowed-types|extension whitelist]]. Merchants storing confidential files (signed contracts, ID scans, KYC) should host them elsewhere, and should treat customer uploads (User files tab) as potentially hostile — especially SVG (embedded scripts), Office docs (macros), and archives.

### Permission

A moderator needs the broad `settings` permission or the specific `settings.files` permission to view, upload, or delete. The permission tree lives under [[settings-staff]].

### Upload and delete are immediate; system files hidden

Upload and delete take effect within the request — there is no background queue and no "pending" state. The `file_download` admin notification ([[settings-admin-notifications]]) fires only on LARGE aggregate exports, not on regular uploads. System-managed internal files (thumbnails, generated exports) don't appear in the merchant's file manager view.

### CDN cache may lag after a delete or replace

A CDN cache sits between storage and the customer. After a delete or replace, the old file may keep serving for a few minutes before the cache refreshes — see [[settings-files-storage-backend]].

## Related

- [[settings]] — parent hub.
- [[settings-brand]] — uses the file manager via the OG-image two-step upload.
- [[settings-import-history]] — imports may generate or consume files; long-running aggregate exports trigger the `file_download` admin notification.
- [[settings-backups]] / [[backups-and-restore]] — restores roll back the database but NOT file contents; media is current-state only.
- [[settings-staff]] — `settings.files` permission lives in the permissions tree.
- [[settings-admin-notifications]] — `file_download` notification on aggregate exports.
- [[settings-queue-view]] — aggregate exports trigger `file_download` notifications.
- [[product]] — product images live in this file manager.
- [[product-option]] — file-upload Options are the most common source of customer uploads on the User files tab.
- [[blog-article]] — blog post images.
- [[order]] — customer-uploaded files attached to orders appear on the User files tab.
- [[file-asset]] — entity page.
- [[plan]] — storage quota is plan-gated.
- [[plan-gates]] — concept page.
- [[plan-vs-feature-pack]] — pack purchase model used by the *"Upgrade storage space"* button.
- [[account]] — shares the same storage progress bar.
- [[storefront-architecture]] — wider CDN architecture context.

## Open questions

- Format (`ex`) and Quality (`q`) controls are documented the image delivery service parameters but not exposed in the Image playground UI as of the May 2026 audit. (verify) whether they will be added.
