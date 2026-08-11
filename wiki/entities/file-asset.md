---
type: entity
nav_path: "Entity → File / Asset"
aliases: ["File", "File asset", "Asset", "Media", "Media asset", "Uploaded file", "Image", "Product image", "Файл", "Медия", "Качен файл", "Изображение"]
tags: [entity, settings, media, storage, files, cdn]
created: 2026-05-21
updated: 2026-06-10
source_count: 0
---

# File / Asset

## Identity

A **File / Asset** is an uploaded file in CloudCart's file storage — product photos, category images, blog images, page-builder media, customer-attached uploads on orders, platform-generated exports (CSV / PDF), brand / OG-image assets, and theme assets. Each file counts against the merchant's storage quota (capped per plan), is served publicly through CloudCart's CDN (the image delivery service for images, direct download for documents), and is referenced from one or more places — a product card, blog post, CMS page, order line item, email template, etc.

The merchant manages files through two hubs: [[settings-files]] (central file manager — three tabs: Files / User files / Image playground) and [[orders-user-files]] (customer-uploaded files attached to orders via product-options of type `file`). Every admin upload module (product, blog, page-builder, brand logo) writes into the same storage and surfaces back in the file manager. Quota is shared across BOTH admin- and customer-uploaded files — a single used / total progress bar combines both.

This entity is split into a cluster of aspect pages; the sections below give the slim definition and point to the aspect that answers each kind of question.

## Aliases

- **File** / **File asset** / **Asset** — used interchangeably; the file manager UI uses "files".
- **Media** / **Media asset** — when emphasising images / video.
- **Uploaded file** — generic phrasing.
- **Image** / **Product image** — when the file is specifically a photo bound to a catalog entity.
- **Файл** / **Медия** / **Качен файл** / **Изображение** — Bulgarian equivalents.

## Sub-pages (in this cluster)

Split into 6 aspect pages. The Assistant should drill into the aspect matching the question, not read every page.

- [[file-asset-storage-model]] — storage backends (S3 / legacy), chunked multipart upload for large files, public-only model (no per-file privacy), folder auto-decision by extension, hidden system-managed files, no-antivirus-scanning rule.
- [[file-asset-quota]] — plan-gated storage quota shared across admin + customer uploads, the 100%-full upload block + Upgrade button, storage packs.
- [[file-asset-lifecycle]] — the uploaded → referenced → orphan → deleted path, delete-protection (two in-use counters + bulk-delete confirmation messages), failed-upload cleanup, no-replace-everywhere rule.
- [[file-asset-cdn-transforms]] — the image delivery service transform parameters, Image playground URL composer, SVG bypass, pad-to-square.
- [[file-asset-customer-uploads]] — files customers attach at checkout via file-type product-options, the User files tab, indefinite persistence (no auto-purge), download-link email, 404-on-delete consequence.
- [[file-asset-image-pickers]] — every admin surface uploading into the same storage (product / category / blog / CMS / brand / email-template editors) and the unified-backend model.

## Key Attributes

| Field | What it stores | Aspect |
|-------|----------------|--------|
| **File name** (`file_name` / `name`) | Original filename (e.g., `my-design.png`); fixed at upload, no rename | [[file-asset-lifecycle]] |
| **MIME type** (`file_mime`) | e.g., `image/png`, `application/pdf`, `image/svg+xml`; decides image vs document handling | [[file-asset-cdn-transforms]] |
| **Extension** (`file_extension`) | File extension; auto-decides the storage folder | [[file-asset-storage-model]] |
| **Size** (`file_size`) | Raw bytes; shown formatted (`1.2 MB`) via `format_bytes` | [[file-asset-quota]] |
| **Storage path / URL** (`file_url`) | Direct URL on S3 / legacy; S3 URLs are pre-signed tokens | [[file-asset-storage-model]] |
| **Upload context** | Which surface uploaded it (product / category / blog / order / brand / export) | [[file-asset-image-pickers]] |
| **Uploaded at** (`created_at`) | ISO8601 timestamp; shown as date in the grid | — |
| **Used by — `attached_records`** | Count of `filemanager_records` bindings; > 0 blocks delete | [[file-asset-lifecycle]] |
| **Used by — `total_orders`** | Count of `orders_products` references; > 0 blocks delete | [[file-asset-customer-uploads]] |
| **Storage backend** | `s3` / `legacy`; unified retrieval | [[file-asset-storage-model]] |
| **Order ID + Product name** (User files tab only) | The order + product for a customer-attached file | [[file-asset-customer-uploads]] |
| **Option label** (User files tab only) | The file-type product-option name (e.g., *"Upload your design"*) | [[file-asset-customer-uploads]] |

## Relationships

A File / Asset binds (polymorphically) to whichever entity uploaded or references it — [[product|Product]] (product / gallery / variant images), [[category|Category]] (banner / hero), [[blog-article|Blog Article]] (featured + in-body), [[order|Order]] (customer-attached files via file-type product-options), CMS pages (page-builder blocks), email templates (logo), and the brand / OG asset (per [[settings-brand]]). It counts against the plan-gated quota regardless of source (see [[file-asset-quota]]), carries two in-use counters `attached_records` + `total_orders` that delete checks before removal (see [[file-asset-lifecycle]]), and generates the image delivery service CDN variants on demand (see [[file-asset-cdn-transforms]]).

It is NOT an external-system storage record (merchants cannot link external S3 buckets from the pickers), NOT a static theme asset (bundled CSS / JS tracked separately), and NOT an export-job artifact (large aggregate exports generate temporary files that fire the `file_download` admin notification and expire after the platform's retention window).

## Where it appears

- [[settings-files]] — central file manager (Files + User files + Image playground tabs) + storage-usage module at top.
- [[orders-user-files]] — customer-uploaded files attached to orders, under Orders → User Files (same data as Settings → Files → User files, different entry point). See [[file-asset-customer-uploads]].
- In-product image uploaders — every image-capable entity editor uses the same backend; see [[file-asset-image-pickers]].
- [[orders-details]] — per-order edit hub surfaces customer-attached files inline per line item.
- [[plan-gates]] — storage quota is plan-gated; pack purchases extend it. See [[file-asset-quota]].

## Related

### Related entities

- [[product]] — product images live in the file manager (via `filemanager_records` bindings).
- [[category]] — category images.
- [[blog-article]] — blog post images.
- [[order]] — customer-uploaded files attached to orders via product-options of type `file`.
- [[plan]] — storage quota is plan-gated.
- [[customer]] — the customer who uploaded the file (for order-attached uploads).

### Cross-cutting concepts

- [[plan-gates]] — the storage-quota gating framework.
- [[checkout-flow]] — the storefront flow that produces customer-uploaded files (via file-type product-options).
- [[notification-delivery]] — the `file_download` admin notification for large exports; the customer's "Files download link" email after checkout.

### Settings & feature pages

- [[settings-files]] — the central file-manager screen.
- [[orders-user-files]] — the customer-uploads list under Orders.
- [[orders-details]] — per-order surface of customer-attached files.
- [[settings-hooks]] — order webhooks include the order's product options (file references).

## Open Questions

- ⏸️ Whether the merchant can configure storage retention to auto-purge old files (e.g., delete files older than N years for GDPR).
- ⏸️ Whether deleting a customer-attached file affects the parent order's checkout / packing-slip rendering.
- ⏸️ Behavior for files attached to refunded / cancelled orders — are they still listed in [[orders-user-files]] or hidden?
- ⏸️ Whether the platform exposes any way for the merchant to download ALL files in bulk (export-all) for backup / migration to another platform.
- ⏸️ Behaviour when the customer uploads a file larger than the platform's per-file maximum at checkout — whether the error is surfaced clearly to the customer or silently fails.
