---
type: feature
nav_path: "Orders → User Files → Storage & delivery"
route_name: admin.order-files.list
route_path: /admin/order-files
aliases: ["User files storage", "User files delivery", "Order file URL", "Customer file download link", "File proxy route", "Съхранение и доставка на файлове на потребителите"]
tags: [orders, files, customer-uploads, storage, notifications, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 5
---

> Part of [[orders-user-files]]. See the hub for the other aspects (list view, deletion, data model).

# User Files — storage & delivery

## Purpose

Where a customer-uploaded file physically lives, how the merchant's `file_url` resolves to the bytes, how the customer receives their own copy, and how long files are kept. This is the aspect to read for "the download link broke" or "where is the file actually stored" questions.

## Where to find it

The `file_url` is exposed in each row of the [[orders-user-files-list|User Files list]] (`/admin/order-files`). The customer sees their own upload as a link in the order's product list (see *Customer-side delivery* below); there is no UI for the merchant to send it from this page.

## What the merchant can do here

- **Open / download a file** by following its `file_url` from the list. The URL streams the file through the merchant's own domain.
- Nothing else — the merchant cannot send the file to the customer, change the storage backend, or configure a retention rule from this page (deletion is on [[orders-user-files-delete]]).

## Settings & fields

### Storage backend

Files are stored in the platform's configured storage backend — **S3 for newer / migrated stores**, legacy storage for older files. The list and the `file_url` retrieval handle both transparently; the merchant sees a unified list regardless of backend.

### `file_url` is resolved per request

The `file_url` attribute is computed on demand by checking the storage backend, so:

- If the backend is temporarily unreachable, the URL may resolve to null.
- Refreshing the page may produce a new URL token for the same file (the modern S3-signed variants).

## Business rules

### Customer-side delivery — a link in the order's product list

Each upload shows as a link next to its option wherever the order's product list renders: the thank-you page, the order in the customer's account, and order emails that carry the product list ([[orders-notify-customer]]). No dedicated email exists for it. The *Files download link* email (`send_order_files_download_link`) is a different thing: it goes out only for [[digital-products|digital products]] on a paid or completed order, so a file-type option never triggers it. The [[orders-user-files|User Files]] list is purely the merchant's view + management.

### Deleting a file breaks the customer's link

If the merchant [[orders-user-files-delete|deletes]] the file from the admin, the link on the customer's order and in earlier emails returns 404 — the storage blob is gone.

### Retention — manual cleanup only

There is **no scheduled cleanup task**. Uploaded files persist on storage indefinitely until the merchant deletes them from the User Files page. The merchant cannot configure a "delete files older than N years" auto-purge for GDPR / privacy. If a customer requests deletion, the merchant must manually remove the file row.

### Deleted file → option value null → downstream rendering varies

Removing a file nulls the option's `value` but leaves the option row on the order line. Whether the order's checkout summary or packing slip renders a placeholder vs an empty cell depends on the specific store theme (each handles a null value its own way). If downstream rendering matters, the merchant should preview a packing slip on an order with a deleted file. The full delete mechanics are on [[orders-user-files-delete]].

## Related

- [[orders-user-files]] — hub.
- [[orders-notify-customer]] — the order emails whose product list carries the upload link.
- [[orders-user-files-delete]] — what deleting a file does to storage + the customer link.
- [[orders-user-files-data-model]] — where `file_url` sits among the per-file fields.
- [[file-asset]] — entity page for file-storage records (shared quota).
- [[settings-files]] — central file manager (same storage + quota).

## Open questions

None.
