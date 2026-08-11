---
type: entity
nav_path: "Entity → Product Option → Order-line storage"
aliases: ["Product Option order storage", "Option order-line snapshot", "orders_products_options", "Option value on order", "Option rename immutability", "Option file-upload value"]
tags: [catalog, products, options, orders, snapshot, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[product-option]]. See the hub for the other aspects (attributes, pricing, scoping + edge cases).

# Product Option — Order-line storage

## Identity

What happens to the customer-submitted Option value once the cart converts to an order. The value is **snapshotted** onto a dedicated order-line table so the merchant can read exactly what each customer asked for when fulfilling — and so that later edits to the Option definition never rewrite history. This aspect documents the snapshot shape, the immutability rule for renames, and how File-upload values reference an uploaded [[file-asset]].

## Aliases

- **Order-line snapshot** — the saved copy of the Option value on the order.
- **`orders_products_options`** — the per-line storage table.
- **Option rename immutability** — why renaming an Option doesn't change historical orders.
- **File-upload value** — the stored reference to the customer's uploaded file.

## Key Attributes

| Attribute | What it captures | Notes |
|-----------|------------------|-------|
| **Snapshot row** | One row per Option per order line in `orders_products_options` | NOT a JSON blob on the order-product row. Each row is an independent, queryable record. |
| **`field_id`** | The Option definition the value belongs to | Links the snapshot back to the Option, but the displayed text is the snapshotted `name`, not a live lookup. |
| **`field_option_id`** | The picked value | Populated when the Option is a Select / Radio / Checkbox; identifies which discrete choice the customer picked. |
| **`name`** | The snapshotted Option name | Captured at order-creation time. This is the immutable label — renaming the Option later does NOT update it (see below). |
| **`value`** | The customer's text / amount / file reference | For Text / Textarea types, the typed string. For measurement types, the entered amount. For File-upload, a reference to the uploaded [[file-asset]]. |

## Storage rules

### Order-line storage is a dedicated table, not a JSON blob

The customer-submitted value snapshots onto the `orders_products_options` table — one row per Option per line. Each row carries `field_id` (the Option definition), `field_option_id` (the picked value when a select / radio / checkbox), `name` (snapshotted Option name), and `value` (the customer's text / amount / file reference). File-upload values store the file reference as the `value` — the merchant downloads from the Order's Files tab.

### Renames don't retroactively update orders

Snapshots are **immutable** — renaming an Option does NOT update existing order rows (the `name` column on each `orders_products_options` row is captured at order-creation time). Carts in progress DO re-render because the cart re-queries the live Option definition on each storefront load — so the rename is visible to in-progress carts but historical orders keep the old name. This is the cart-vs-order divide: live carts read the current definition; placed orders read their own snapshot.

### File-upload values reference an uploaded asset

When the input type is `file`, the snapshot `value` is a reference to a [[file-asset]] the customer uploaded at cart-add time — not the file contents inline. The merchant downloads the customer's upload from the order details (the Order's Files tab) when fulfilling print-on-demand work. The file-upload caps and the deletion cascade behaviour are documented in [[product-option-entity-scoping-and-edge-cases]].

## Where it appears

- [[order]] — the snapshot rows live on the order line; the merchant reads them when fulfilling.
- [[orders-details]] — order detail view where the per-line Option values + file downloads surface.
- [[cart]] — the live cart re-renders Option labels from the current definition (contrast with the immutable order snapshot).
- [[file-asset]] — File-upload Option values reference an uploaded asset the merchant downloads at fulfilment.

## Related

- [[product-option]] — hub.
- [[product-option-entity-attributes]] — the input types whose values land in the snapshot.
- [[product-option-entity-pricing]] — the computed surcharge snapshotted alongside the value.
- [[product-option-entity-scoping-and-edge-cases]] — file-upload caps + the File-Option deletion cart cascade.
- [[order]] — the order entity that carries the snapshot.
- [[cart]] — the live cart re-renders from the current definition.
- [[file-asset]] — uploaded files referenced by File-upload Options.

## Open Questions

None.
