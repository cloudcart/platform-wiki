---
type: feature
nav_path: "Orders → User Files → Storage & delivery"
route_name: admin.order-files.list
route_path: /admin/order-files
aliases: ["User files storage", "User files delivery", "Order file URL", "Customer file download link", "File proxy route", "Съхранение и доставка на файлове на потребителите"]
tags: [orders, files, customer-uploads, storage, notifications, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-user-files]]. See the hub for the other aspects (list view, deletion, data model).

# User Files — storage & delivery

## Purpose

Where a customer-uploaded file physically lives, how the merchant's `file_url` resolves to the bytes, how the customer receives their own copy, and how long files are kept. This is the aspect to read for "the download link broke" or "where is the file actually stored" questions.

## Where to find it

The `file_url` is exposed in each row of the [[orders-user-files-list|User Files list]] (`/admin/order-files`). The customer's copy is delivered out-of-band via the post-checkout download-link email — there is no UI for the merchant to resend it from this page.

## What the merchant can do here

- **Open / download a file** by following its `file_url` from the list. The URL streams the file through the merchant's own domain.
- Nothing else — the merchant cannot re-send the customer email, change the storage backend, or configure a retention rule from this page (deletion is on [[orders-user-files-delete]]).

## Settings & fields

### Storage backend

Files are stored in the platform's configured storage backend — **S3 for newer / migrated stores**, legacy storage for older files. The list and the `file_url` retrieval handle both transparently; the merchant sees a unified list regardless of backend.

### `file_url` — a hashed-proxy route, not a direct CDN URL

The `file_url` is shaped as:

```
https://<merchant-domain>/api/v1/order/order-file/<md5_hash>
```

where the hash is `md5(option_id + product_id)` and the route is `order.option.file`. The backend streams the file bytes from the storage disk on demand. Implications:

- The URL is **NOT** a direct S3 link — it goes through the merchant's domain.
- The hash is deterministic but **not signed / not expirable** — anyone who has the hash can fetch the file.
- The URL works regardless of where the blob is stored (S3 vs legacy).
- The merchant cannot share a CDN URL — only the proxy URL.
- The host portion comes from the site's `primaryHost` (falling back to `getMainHost`).

### `file_url` is resolved per request

The `file_url` attribute is computed on demand by checking the storage backend, so:

- If the backend is temporarily unreachable, the URL may resolve to null.
- Refreshing the page may produce a new URL token for the same file (the modern S3-signed variants).

## Business rules

### Customer-side delivery — automatic download-link email

When a customer places an order containing a file-type option, the platform automatically sends them a *"Files download link for order #X in <store>"* email (notification template `send_order_files_download_link`) containing the proxy URL(s) for the customer's own uploads. The customer therefore has the file before the merchant ever opens the [[orders-user-files|User Files]] list — this list is purely the merchant's view + management. Email delivery is set up earlier in the order pipeline — see [[orders-notify-customer]].

### Deleting a file breaks the customer's link

If the merchant [[orders-user-files-delete|deletes]] the file from the admin, the customer's email link returns 404 — the storage blob is gone.

### Retention — manual cleanup only

There is **no scheduled cleanup task**. Uploaded files persist on storage indefinitely until the merchant deletes them from the User Files page. The merchant cannot configure a "delete files older than N years" auto-purge for GDPR / privacy. If a customer requests deletion, the merchant must manually remove the file row.

### Deleted file → option value null → downstream rendering varies

Removing a file nulls the option's `value` but leaves the option row on the order line. Whether the order's checkout summary or packing slip renders a placeholder vs an empty cell depends on the specific store theme (each handles a null value its own way). If downstream rendering matters, the merchant should preview a packing slip on an order with a deleted file. The full delete mechanics are on [[orders-user-files-delete]].

## Related

- [[orders-user-files]] — hub.
- [[orders-notify-customer]] — the customer download-link email is part of the order-notification flow.
- [[orders-user-files-delete]] — what deleting a file does to storage + the customer link.
- [[orders-user-files-data-model]] — where `file_url` sits among the per-file fields.
- [[file-asset]] — entity page for file-storage records (shared quota).
- [[settings-files]] — central file manager (same storage + quota).

## Open questions

None.
