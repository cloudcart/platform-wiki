---
type: feature
nav_path: "Orders → User Files → Data model"
route_name: admin.order-files.list
route_path: /admin/order-files
aliases: ["User files data model", "Customer file data model", "Files as product options", "Order file record source", "Модел на файловете на потребителите"]
tags: [orders, files, customer-uploads, data-model, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-user-files]]. See the hub for the other aspects (list view, deletion, storage & delivery).

# User Files — the data model

## Purpose

What a "user file" actually IS underneath the [[orders-user-files|User Files]] list — how the platform records a customer's upload, when a record comes into existence, and which fields the merchant sees. This explains why a single order can carry several files, and why the list only ever shows real uploads.

## Where to find it

The model is what populates the [[orders-user-files-list|User Files list]] (`/admin/order-files`). The same customer-upload records also surface on the User files tab of [[settings-files]] (same data, different entry point) and per line item on [[orders-details]].

## What the merchant can do here

There is nothing to configure in the data model itself — it is read-only structure. The merchant interacts with it indirectly: by defining a file-type product option (in the [[products|product editor]]) so customers CAN upload, and by browsing / deleting the resulting records. The only creation lever the merchant controls is the file-type option on the catalog.

## Settings & fields

### File record source

Each row represents **one product-option record of type `file` with a non-null value**. The platform models customer file uploads as product-option entries on the line item — so the file is attached to a specific PRODUCT within a specific ORDER, not to the order as a whole. There is no "order has files" attachment table.

### Per-file fields

| Field | What it shows |
|-------|---------------|
| `file_name` | Original filename the customer uploaded (e.g., `my-design.png`). |
| `file_size` | File size (raw bytes). |
| `file_size_formatted` | Human-readable size (e.g., `1.2 MB`). |
| `file_url` | URL to the file — a hashed-proxy route, see [[orders-user-files-storage-delivery]]. |
| `file_mime` | MIME type (e.g., `image/png`, `application/pdf`). |
| `file_extension` | File extension. |
| `product.name` | The product the option belongs to. |
| `product.order_id` | The order containing the product. |
| `name` (option label) | The merchant-facing name of the file option (e.g., *"Upload your design"*). |

## Business rules

### Files are product-options, not order-level attachments

Because the file is one of a line item's options (alongside size, colour, custom text, etc.):

- A single order can have **multiple files** if the customer ordered several products each with a file option.
- A single product line can have **multiple file options** if the merchant configured them (e.g., *"Upload front design"* + *"Upload back design"*).
- Each file is independently downloadable / deletable — see [[orders-user-files-delete]].

### Customer-driven creation only

A file appears in the list ONLY when both are true:

1. The merchant configured a product with a product-option of type **file** (set up in the [[products|product editor]] under product options).
2. A customer placed an order containing that product AND uploaded a file via the option during checkout.

Without a file-type product option on the catalog, the list stays empty regardless of order volume. The merchant has **no upload button** on the admin side — uploads are strictly customer-side at checkout.

### List query — strict `type = file` AND `value IS NOT NULL`

The grid filters to option rows where `type` equals `file` AND `value` is not null. Consequences:

- Options of other types (text, select, colour picker) are excluded — only actual customer file uploads surface.
- Files [[orders-user-files-delete|deleted from this page]] (where `value` became null) NO LONGER appear — there is no record of "this file used to exist" in the list.
- Options that are *defined but never uploaded to* never appear — only `value`-bearing uploads count. This is also what drives the [[orders-user-files-list|empty-state]] COUNT.

### Files persist with the order

Once uploaded, a file lives with the order even after it is completed / cancelled / archived. It remains downloadable until the merchant explicitly deletes it OR the storage backend's lifecycle policy removes it. There is no scheduled auto-purge — see [[orders-user-files-storage-delivery]] for retention details.

### Only placed orders

Only files attached to PLACED orders surface here — files associated with abandoned carts do not appear (the upload becomes a real order-product-option record only when the order is placed).

## Related

- [[orders-user-files]] — hub.
- [[orders-products]] — the line items the file options attach to.
- [[products]] — product editor where the file-type option is configured.
- [[orders-user-files-storage-delivery]] — how `file_url` is resolved and stored.
- [[file-asset-customer-uploads]] — entity sub-page for customer-uploaded files.
- [[order]] — entity page (parent of order-product-options).

## Open questions

None.
