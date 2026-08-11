---
type: feature
nav_path: "Orders → User Files"
route_name: admin.order-files.list
route_path: /admin/order-files
aliases: ["User files", "Order user files", "Customer attached files", "Customer uploads", "Order file uploads", "Файлове на потребителите", "Прикачени файлове от клиенти"]
tags: [orders, files, customer-uploads, smarty]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---
# User Files (customer-attached files on orders)

## Purpose

The **User Files** page lists every file a customer has uploaded as part of placing an order — typically through a product-option of type **file** (used for personalized products, custom prints, designs, documents, photos for printing, etc.). The merchant uses this page as a central hub to download, review, and delete the files customers have sent in.

This is critical for merchants whose products require customer input — printers (logo files), photo labs (photos to print), apparel customizers (design files), document services (PDFs to print). Without this view, the merchant would have to drill into each order individually to retrieve the file.

This page is the **hub** for the cluster. Each operational detail lives on a dedicated aspect page — drill into the one that matches the question.

## Where to find it

Sidebar → **Orders** → **User Files** (or directly via `/admin/order-files`).

The sidebar label is *"User Files"* (translated as `order.files`). The page breadcrumb is *"User Files"* (label `sidebar.order-files`).

## What the merchant can do here

- Browse the full paginated list of customer-uploaded files (one row per file), each linking back to its order + product + option — see [[orders-user-files-list]] for the columns, the `id DESC` default sort, the no-search filter chrome, and the empty state.
- Download a file by opening its `file_url` (a hashed-proxy URL on the merchant's own domain, not a direct S3 link) — see [[orders-user-files-storage-delivery]].
- Delete a single file (per-row X icon) or several at once (bulk **Delete**) — both run the same irreversible 3-step storage delete — see [[orders-user-files-delete]].

What the merchant **cannot** do here:

- Upload or re-attach a file from the admin side — files are customer-uploaded only, during checkout. There is no upload button — see [[orders-user-files-data-model]].
- Edit / replace an uploaded file, or recover a deleted one — deletion is permanent — see [[orders-user-files-delete]].
- See files attached to abandoned carts — only files on PLACED orders surface here — see [[orders-user-files-data-model]].
- Send the file to the customer from this page — customer delivery happens via the post-checkout download-link email — see [[orders-user-files-storage-delivery]].

## Settings & fields

The list shows two columns — a composite **File** cell (order number link + product name + product-option label) and an **Action** cell (per-row delete). Full column behaviour, sort, and the bulk-action chrome are on [[orders-user-files-list]].

Each row maps to one product-option record of type `file` with a non-null value. The per-file fields exposed (`file_name`, `file_size`, `file_size_formatted`, `file_url`, `file_mime`, `file_extension`, `product.name`, `product.order_id`, option `name`) are documented on [[orders-user-files-data-model]].

There are no merchant-configurable settings on this page — it is a read / download / delete view only. Permission is the standard `orders` section.

## Business rules

The cluster-wide rules a merchant needs up front:

- **Customer-driven creation only.** A file appears here only when the merchant configured a file-type product option AND a customer uploaded a file via that option at checkout. No file option → empty list regardless of order volume — see [[orders-user-files-data-model]].
- **List is strictly `type = file` AND `value IS NOT NULL`.** Other option types (text, select, colour) never appear; deleted files (value nulled) disappear from the list — see [[orders-user-files-data-model]].
- **Files persist indefinitely.** No scheduled cleanup / auto-purge — a file lives with the order through completion / cancellation / archive until the merchant deletes it manually (GDPR erasure is manual) — see [[orders-user-files-storage-delivery]].
- **Deletion is irreversible and three-step.** It deletes the storage blob, nulls the option `value`, and removes the storage-counter ledger row. No soft-delete / trash — see [[orders-user-files-delete]].
- **Deleting a file breaks the customer's email link.** The customer's *"Files download link"* email URL returns 404 once the merchant deletes the file — see [[orders-user-files-storage-delivery]].
- **No status filtering.** Files from cancelled / refunded orders are NOT hidden — every order status' files appear — see [[orders-user-files-list]].

## Sub-pages (in this cluster)

This page is split into 4 aspect pages, each covering one well-scoped slice. The Assistant should drill into the aspect that matches the question, not read every page.

- [[orders-user-files-list]] — the list / grid UI: the two columns, `id DESC` sort, the no-search `filters_without_search.tpl` chrome, the empty state, the AJAX grid load, and the dynamic empty-state re-show.
- [[orders-user-files-delete]] — per-row + bulk deletion: the `data-confirm` JS dialog, the irreversible 3-step storage delete, in-process (non-async) bulk-delete, and the `ids` request-body shape.
- [[orders-user-files-data-model]] — files-as-product-options model (not order-level attachments), the strict `type = file` + `value IS NOT NULL` query, per-file fields, customer-driven creation only, persistence.
- [[orders-user-files-storage-delivery]] — storage backend (S3 vs legacy), the hashed-proxy `file_url` route, dynamic per-request URL resolution, the customer download-link email, retention / manual cleanup.

## Related

- [[orders]] — parent orders list (each file row links back to a specific order).
- [[orders-details]] — per-order details page (files are also visible there per line item).
- [[orders-products]] — the line items within an order (product-options including files attach here).
- [[products]] — product editor where the merchant configures the file-type option in the first place.
- [[orders-notify-customer]] — customer notification email containing the file download link.
- [[settings-files]] — central file manager; same customer-upload data under its User files tab.
- [[settings-hooks]] — order webhooks include the order's product options (file references).
- [[file-asset]] — entity page for file-storage records.
- [[file-asset-customer-uploads]] — entity sub-page for customer-uploaded files specifically.
- [[order]] — entity page (parent of order-product-options).

## Open questions

None — all previously-flagged items resolved or distributed to aspect pages.
