---
type: feature
nav_path: "Orders → Order details → Products → Delete"
route_name: admin.orders.products.delete
route_path: /admin/orders/action/products/:order_id/delete/:line_id
aliases: ["Remove product from order", "Delete order line", "Remove line item", "Izbrishi produkt ot porachka"]
tags: [orders, products, line-items, delete, restock]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-products]]. See the hub for the other aspects (add, edit, line discount, fulfillment popover, stock effects, side effects).

# Order products — Delete line

## Purpose

The flow for **removing a product line from an order**. Triggers a transactional cascade that strips per-line digital files, taxes, discounts, options, modifications, and fulfillments. If the line was decremented from stock, the variant's quantity is automatically restocked. Bundles are removed atomically.

## Where to find it

[[orders-details]] → products table → per-row cog → **Remove product**. A `data-confirm` browser dialog asks the merchant to confirm.

## What the merchant can do here

- **Delete a single non-fulfilled line** — confirmation → DB-transactional cascade.
- **Cannot delete the last line** — see business rules below.
- **Cannot delete a fulfilled line directly** — must void the waybill first via [[orders-shipping-waybill]].

## Settings & fields

The delete flow has no fields — only the confirmation. The route fires GET `admin.orders.products.delete/<line_id>`.

The cog → Remove option is visible only when:
- `order.status_fulfillment == 'not_fulfilled'`.
- `order.status == 'pending'` OR `order.status == 'paid'`.
- The line itself is NOT already fulfilled (`order_fulfillment_id` empty).
- The line is digital OR the order is still in editable state.

## Business rules

### Cannot remove the LAST product on an order

The platform BLOCKS deletion of the last product line with the error *"Order must have at least one product"*. To empty an order, the merchant must cancel it via [[orders-status-change]] or delete the whole order from the order list bulk action on [[orders]].

### Delete cascade — what gets removed in the same transaction

When a line is deleted, the platform also deletes (within the same DB transaction):

- The line's digital file links.
- The line's tax records.
- The line's discounts (manual + code-applied + auto-applied).
- The line's options (per-item + per-order options).
- The line's modifications (length / square / etc.).
- The line's meta data.
- The line's fulfillment record (if it was already fulfilled and the cog still allowed delete — usually for digital lines).

So deleting a fulfilled DIGITAL line REMOVES its fulfillment record without prompting — the merchant should be aware that the per-line fulfillment audit is lost. Physical-product fulfillments tied to a waybill are separately protected (the waybill must be voided first via [[orders-shipping-waybill]]).

### Bundle product deletion cascades the whole bundle

If the merchant deletes a line that belongs to a bundle (introduced via [[bundles-list]]), the platform deletes the **entire bundle** — all sibling lines AND the bundle wrapper. Bundle-related discounts on sibling lines are also stripped. Bundles are atomic. To "split" a bundle, the merchant deletes it and re-adds each product individually via [[orders-products-add]].

### Bundle-related discounts auto-cleanup on sibling delete

When a line in a bundle is deleted, the platform also removes any bundle-related discounts attached to OTHER lines in the same bundle. This prevents orphan bundle discounts on the surviving lines.

### Removing a line restocks the variant

When the line was tracked at the time of creation (the variant's `tracking` flag was ON when the line was added), the platform restores its quantity to the variant's stock — automatic restock. Untracked lines do NOT restore stock (no decrement happened originally). See [[inventory-restock]] for the symmetric restock flow and [[orders-products-stock-effects]] for the tracked-snapshot rule.

### Refund-after-modification — no auto credit note

Removing a line from a paid order does NOT auto-issue a credit note. Totals + tax + shipping update, but the credit note is a separate merchant action via [[orders-credit]]. The platform stops short of automatic refund accounting.

### Customer is NOT notified on remove

The platform's auto-notify only fires on ADD events. Remove (and edit) do NOT email the customer. For comms, the merchant uses [[orders-notify-customer]] manually.

### Fulfilled physical lines are blocked

Once a line has a non-null `order_fulfillment_id` from a generated waybill, the cog → Remove option is BLOCKED. The merchant must:
1. Void the waybill via [[orders-shipping-waybill]] (Remove action).
2. Then delete the line.
3. Optionally re-generate the waybill.

This protects courier-side dispatch integrity.

### History entry — `order_product_removed`

Removing a line writes a history entry with action key `order_product_removed` (action code 25) on [[orders-history]] — see [[orders-products-side-effects]].

### Drafts skip the `order.updated` webhook

For draft orders, delete does NOT fire `order.updated`. See [[orders-products-side-effects]] for webhook gating.

## Related

- [[orders-products]] — hub.
- [[orders-products-add]] — must add a replacement before removing the last line.
- [[orders-products-edit]] — re-quantity an existing line as an alternative to delete + re-add.
- [[orders-products-stock-effects]] — tracked-snapshot rule for restock-on-delete.
- [[orders-products-side-effects]] — history entries + webhook gating after delete.
- [[orders-details-products]] — products table where the cog → Remove lives.
- [[orders-shipping-waybill]] — void waybill before deleting a fulfilled physical line.
- [[orders-status-change]] — cancel route for emptying an order without deleting lines individually.
- [[orders-credit]] — credit-note flow (manual after deletes on paid orders).
- [[inventory-restock]] — symmetric restock semantics on delete.
- [[bundles-list]] — bundle structure; bundle delete is atomic.
- [[products-change-log]] — restock writes a `variants.updated` entry there with the order as Initiator.

## Open questions

None.
