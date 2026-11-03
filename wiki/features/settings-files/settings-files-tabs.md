---
type: feature
nav_path: "Settings → Files → Tabs"
route_name: files-index
route_path: /admin/settings/files
aliases: ["Files tabs", "User files tab", "Files tab columns", "File preview modal"]
tags: [settings, files, media, tabs]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-files]]. See the hub for the other aspects (upload flow, storage quota, delete protection, image playground, allowed types, storage backend).

# Settings → Files — tabs, tables, and previews

## Purpose

The screen at `/admin/settings/files` is a three-tab file-management surface. This page documents the three tabs as the merchant sees them: which tab shows what, the table columns, and the two file-preview modal variants that open on row click.

## Where to find it

Sidebar → Settings → **Files**. Route `/admin/settings/files` redirects to the default landing tab. The three sub-routes are:

| Label | Route name | Route path |
|-------|------------|------------|
| Files (root) | `files-index` | `/admin/settings/files` |
| Files | `files.settings` | `/admin/settings/files` (default landing) |
| User files | `files.order-files` | `/admin/settings/files/order-files` |
| Image playground | `files.playground` | `/admin/settings/files/playground` |

The page header breadcrumb reads "Settings → `<active tab label>`". The header icon is the file-alt icon.

## What the merchant can do here

### Files tab (default)

The store's general file manager. Every image, document, and asset the merchant has uploaded for use across the storefront (product photos, blog images, page assets, etc.) is listed here.

- See all files the merchant has uploaded via the file manager. **System-managed internal files** (generated thumbnails, internal exports) are hidden — the merchant only sees their own uploads.
- See the [[settings-files-storage-quota|storage usage module]] at the top.
- Click **+ Upload files** in the page header (only visible on this tab) — see [[settings-files-upload-flow]].
- Filter, search, sort, and paginate the files table.
- Click a file's name (or thumbnail) to open the image-preview modal — see below.
- Toggle bulk-select to multi-select files; bulk-delete with confirmation — see [[settings-files-delete-protection]].
- Delete a single file via the row's delete button.

### User files tab

- See files uploaded BY customers — e.g., customisation uploads attached to orders (custom product configurators, image / file upload [[product-option|Product options]]).
- See the same storage module at the top (quota is shared between admin-uploaded and user-uploaded files — see [[settings-files-storage-quota]]).
- Filter and paginate.
- Open a preview modal on click — uses the simpler variant (see below).
- Bulk-delete (with the same in-use protection).
- **No Upload button** — these files come in via customer-facing flows, not the merchant.

### Image playground tab

The interactive CDN-transform previewer. See [[settings-files-image-playground]] for the full controls and how the merchant uses it to figure out the right URL parameters for custom storefront templates or external integrations.

## Settings & fields

### Files tab — table columns

| Column | What it shows | Notes |
|--------|---------------|-------|
| **Name** (`name`) | Filename rendered by the `SettingsFilesFileName` component (icon + name + extension). Click opens preview. | |
| **Size** (`size`) | Human-formatted (`format_bytes`) — e.g., "245 KB", "1.2 MB". | |
| **Created** (`created_at`) | ISO8601 timestamp, displayed as date. | |
| **Used by** | Two counters surfaced from backend: `attached_records` (rows in `filemanager_records` — e.g., product/blog/page bindings) + `total_orders` (rows in `orders_products` referencing this file). Drives delete-protection visibility — see [[settings-files-delete-protection]]. | |
| **Actions** | Delete button (disabled / hidden if in use). | |

### User files tab — table columns

Same table component (`useFilesTable`) but with `isOrderFiles: true` adds two more columns:

| Column | What it shows |
|--------|---------------|
| **Order ID** | Click navigates to the order detail page (via `SettingsFilesOrderLink`). |
| **Product name** | The product the customer attached the file to. |

The bulk-delete behaviour matches the Files tab — see [[settings-files-delete-protection]].

## Business rules

### File preview modal — Files tab (`SettingsFilesImagePreview`)

Opens on click of a row's filename (or thumbnail) for image / video files. Size adapts: `xl` for images, `lg` for other types. The modal title is the file's name. Header actions:

- **Download** button (`href={data.url}`, `download={data.name}`, target `_blank`) — direct CDN download. The Download label is suppressed on viewports narrower than 460 px (icon-only).
- **Close** button.

Body content branches on `data.dir`:

- **`image`** → renders the same **Image playground** component embedded in `embedded=true` mode (source URL fixed to the file). The merchant gets full transform controls (width / height / crop / pad colour) inside the preview without leaving the table. See [[settings-files-image-playground]] for what the embedded controls do.
- **`video`** → standard `<video controls autoplay>` element capped at `max-h-[70vh]`.
- **Anything else** → centred fallback: a large `far fa-file-alt` icon + *"Preview not available"* text. Non-previewable files should be downloaded via the header Download button.

### File preview modal — User files tab (`SettingsUserFilesImagePreview`)

A simpler `b-modal` (size `lg`) used only for customer-uploaded order attachments. The body shows the image (cap at `max-h-[60vh]`, fetched with `width=1200` CDN param to keep size sane on retina). Header actions: Download + Close (same icon-only fallback under 460 px). **No embedded playground** — these are customer-uploaded files; the merchant just needs to look at them.

### What the merchant CANNOT do on either table

- Re-upload to a specific file's slot (each upload creates a new row — see [[settings-files-upload-flow]]).
- Rename a file after upload (the name is fixed; merchant uploads with a new name + deletes the old one).
- Move files between directories from this UI — the platform auto-decides which folder a file goes to based on its file extension. See [[settings-files-allowed-types]].
- Restore a deleted file (no undo / soft-delete from this screen).
- Delete a file that's in use (`attached_records > 0` OR `total_orders > 0`) — see [[settings-files-delete-protection]].

### Permission

The endpoints under `/admin/api/core/settings/files` are gated by `hasApiPermission:settings,settings.files`. So a moderator needs either the broad Settings permission or the specific Files permission to view, upload, or delete. Permission tree is configured under [[settings-staff]].

The platform regex `'settings/(?!files\/popup)(?!files\/delete\/\d+)...'` in sitecp routing excludes some sub-paths from the standard auth wrapper — those are direct-action endpoints with their own protections.

## Related

- [[settings-files]] — hub.
- [[settings-staff]] — staff permissions tree where `settings.files` lives.
- [[product-option]] — file-upload Options are the most common source of customer-uploaded files on the User files tab.
- [[order]] — User files tab rows link back to their parent order.

## Open questions

None.
