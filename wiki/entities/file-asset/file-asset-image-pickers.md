---
type: entity
nav_path: "Entity → File / Asset → Image pickers & upload surfaces"
aliases: ["Image pickers", "Upload surfaces", "Image uploader", "Product image uploader", "Page-builder image picker", "Brand logo uploader", "Unified file backend", "Качване на изображения", "Избор на изображение", "Галерия с файлове"]
tags: [entity, settings, media, storage, files, uploaders, catalog]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[file-asset]]. See the hub for the other aspects (storage model, quota, lifecycle, CDN transforms, customer uploads).

# File / Asset — image pickers & upload surfaces

## Identity

**Image pickers** are the many places across the admin where the merchant uploads or selects a file — the product image uploader, the category banner uploader, the blog editor's image picker, the CMS page-builder image block, the brand / OG-image uploader, and the email-template logo pickers. The key model: **every one of these writes into the same storage** behind [[settings-files]] and surfaces back in the central file manager. There is one backend, one quota, and one [[file-asset-cdn-transforms|the image delivery service]] pipeline — the pickers are just different doorways into it.

## Aliases

- **Image pickers** / **upload surfaces** — the admin doorways into file storage.
- **Image uploader** — the generic component.
- **Unified file backend** — the single-storage model behind every picker.
- **Качване на изображения** / **Избор на изображение** / **Галерия с файлове** — Bulgarian equivalents.

## Key Attributes

| Picker | Where | Binding (`attached_records`) |
|--------|-------|------------------------------|
| **Product image uploader** | [[product|Product]] editor | Product images, gallery images, variant images. |
| **Category image uploader** | [[category|Category]] editor | Category banner / hero image. |
| **Blog image picker** | [[blog-article|Blog Article]] editor | Featured image + in-body images. |
| **Page-builder image block** | CMS page builder | Image / gallery blocks (no dedicated entity page). |
| **Brand / OG uploader** | [[settings-brand]] | Store-wide logo + OG image. |
| **Email-template logo picker** | Email-template editors | Header / footer logo images. |

## Relationships

Image pickers are the origin of most bindings on [[file-asset]]:

- **[[file-asset-lifecycle]]** — every picker selection increments `attached_records`, which is the delete-guard for that file.
- **[[file-asset-storage-model]]** — all pickers write into the same S3 / legacy storage and obey the same extension / folder / size rules.
- **[[file-asset-cdn-transforms]]** — images selected through any picker are served through the image delivery service with the same transform parameters.
- **[[file-asset-quota]]** — every picker upload counts against the shared quota.

## Where it appears

- [[product|Product]] editor — product images, variant images. See [[products-products]].
- [[category|Category]] editor — category banner / hero image.
- [[blog-article|Blog Article]] editor — featured image + in-body images.
- CMS page builder — image blocks, gallery blocks.
- [[settings-brand]] — OG image, logo.
- Email-template editors — header / footer logo.
- [[settings-files]] — the same files all surface back here in the central manager.

### One backend, many doorways

Every entity editor that supports images uses the **same upload backend**. When the merchant uploads a product photo from the product editor, that file is identical in storage to a file uploaded directly on the Files tab of [[settings-files]] — same backend, same quota line, same the image delivery service URL scheme. This is why a file bound to a product shows a non-zero "Used by" count in the central manager and cannot be deleted there until it is unbound from the product (see [[file-asset-lifecycle]]).

Because there is **no "replace this file" action** (see [[file-asset-lifecycle]]), swapping an image always means re-selecting through the relevant picker: upload the new file, bind it from the editor, then remove the old file. The pickers do not offer a folder choice — placement is auto-decided by extension (see [[file-asset-storage-model]]).

### Customer-facing upload surface is separate

The pickers documented here are **admin-facing**. The customer's upload doorway is the file-type product-option at checkout, which writes to the same storage but surfaces on the User files tab — see [[file-asset-customer-uploads]].

## Related

- [[file-asset]] — hub.
- [[file-asset-lifecycle]] — picker selections create the `attached_records` bindings + delete-guard.
- [[file-asset-storage-model]] — the shared backend + extension / folder / size rules.
- [[file-asset-cdn-transforms]] — the image delivery service serving for picked images.
- [[file-asset-quota]] — picker uploads count against the shared quota.
- [[file-asset-customer-uploads]] — the separate customer-facing upload doorway.
- [[product]] / [[category]] / [[blog-article]] — entity editors with image pickers.
- [[products-products]] — the product editor surface.
- [[settings-brand]] — brand / OG uploader.
- [[settings-files]] — the central file manager every picker surfaces into.

## Open Questions

- ⏸️ Whether any picker exposes a "choose from existing files" gallery vs always uploading anew.
- ⏸️ Whether the email-template logo picker shares the exact same `accept` extension filter as the catalog pickers.
