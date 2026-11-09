---
type: entity
nav_path: "Entity → File / Asset → Customer uploads"
aliases: ["Customer uploads", "User files", "Customer-attached files", "Order file upload", "File-type product option", "Uploaded design", "Потребителски файлове", "Клиентски файлове", "Прикачен файл към поръчка"]
tags: [entity, orders, media, storage, files, customer-uploads, checkout]
created: 2026-06-10
updated: 2026-11-09
source_count: 1
---

> Part of [[file-asset]]. See the hub for the other aspects (storage model, quota, lifecycle, CDN transforms, image pickers).

# File / Asset — customer uploads

## Identity

**Customer uploads** are files that customers attach to their orders at checkout via a **product-option of type `file`** (e.g., *"Upload your design"*). They are listed on the **User files** tab of [[settings-files]] and, with extra order columns, on the dedicated [[orders-user-files]] screen. They share the merchant's [[file-asset-quota]] with admin uploads. The two facts merchants ask about most: these files **persist indefinitely** (no auto-purge after the order completes / ships / is archived), and **deleting one breaks the customer's download link** (returns 404).

## Aliases

- **Customer uploads** / **user files** — the customer-attached files.
- **Customer-attached files** / **order file upload** — phrasing on the order surface.
- **File-type product option** — the mechanism that captures the upload.
- **Upload link** — the link to the file in the order's product list (not the *Files download link* email, which is for [[digital-products]] only).
- **Потребителски файлове** / **Клиентски файлове** / **Прикачен файл към поръчка** — Bulgarian equivalents.

## Key Attributes

| Field | What it stores | Notes |
|-------|----------------|-------|
| **Order ID** | The order containing the customer-attached file | Clickable link to the order detail page (User files tab column). |
| **Product name** | The product the file-type option belongs to | Shown alongside the Order ID. |
| **Option label** | The merchant-facing option name (e.g., *"Upload your design"*) | Part of the composite "File" cell on [[orders-user-files]]. |
| **`total_orders` counter** | Count of `orders_products` rows referencing the file | Drives delete protection — see [[file-asset-lifecycle]]. |
| **Customer link** | The link next to the option in the order's product list (thank-you page, account order, order emails) | Breaks (404) if the merchant deletes the file. |

## Relationships

Customer uploads are the order-bound subset of [[file-asset]]:

- **[[order|Order]]** — each customer upload is attached to a line item on an order via a file-type product-option.
- **[[customer|Customer]]** — the customer who uploaded the file; they see it linked on their order.
- **[[file-asset-quota]]** — customer uploads consume the same shared quota and are the usual cause of unexpected quota growth.
- **[[file-asset-lifecycle]]** — the `orders_products` (`total_orders`) counter is the delete-guard that blocks removing an in-use customer file.

## Where it appears

- [[settings-files]] — the **User files** tab.
- [[orders-user-files]] — the dedicated list under Orders → User Files (same data, extra order columns).
- [[orders-details]] — the per-order edit hub surfaces customer-attached files inline per line item.

### Lifecycle of a customer-uploaded file

- **Created** — the customer uploads at checkout via a file-type product-option (part of [[checkout-flow]]).
- **Persists with the order** — lives indefinitely under the merchant's quota even after the order is completed / cancelled / archived. **There is NO auto-purge** after the order ships.
- **Customer link** — the upload shows as a link next to its option on the thank-you page, the order in the customer's account and order emails carrying the product list. No dedicated email is sent: the *Files download link* email is for digital products only.
- **Deleted** — the merchant deletes from the User files tab OR uses the per-order admin action ("Remove uploaded file") that NULLs the file reference on the line item but keeps the order history.

### Customer link breaks if the merchant deletes the file

When the merchant deletes a customer-uploaded file from the User files tab, the link on the customer's order returns **404** — the storage blob is gone. The order history retains the option name but no longer has a downloadable file attached. The merchant should warn the customer before deleting if the customer might still need the file.

### Customer uploads persist indefinitely (no auto-purge)

Files customers attach to their orders are stored under the merchant's quota and stay there indefinitely. There is **no auto-purge after the order completes, ships, or is archived**. The merchant must manually delete them from the User files tab to reclaim quota (see [[file-asset-quota]]). There IS internal infrastructure-level cleanup of orphan blobs that lost their DB references (e.g., a partial cart-to-order failure), but that is invisible to the merchant and does not free up quota for files the merchant still owns.

## Related

- [[file-asset]] — hub.
- [[file-asset-quota]] — customer uploads share the same quota and never auto-purge.
- [[file-asset-lifecycle]] — the `orders_products` delete-guard.
- [[file-asset-storage-model]] — public, unscanned storage of customer files.
- [[order]] — the order each upload is attached to.
- [[customer]] — the uploading customer; recipient of the download-link email.
- [[orders-user-files]] — the dedicated list under Orders.
- [[settings-files]] — the User files tab.
- [[orders-details]] — per-order surface of customer-attached files.
- [[checkout-flow]] — the storefront flow that produces these uploads.
- [[notification-delivery]] — the "Files download link" email.

## Open Questions

- ⏸️ Behavior for files attached to refunded / cancelled orders — are they still listed in [[orders-user-files]] or hidden?
- ⏸️ Behaviour when the customer uploads a file larger than the platform's per-file maximum at checkout — whether the error is surfaced clearly or silently fails.
- ⏸️ Whether deleting a customer-attached file affects the parent order's checkout / packing-slip rendering.
