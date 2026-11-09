---
type: feature
nav_path: "Orders → Order details → Products → Shipping re-quote and save errors"
route_name: admin.orders.products.store
route_path: /admin/orders/action/products/:order_id/add/:product_id
aliases: ["Shipping re-quote after adding a product", "Courier re-quote on order edit", "Request cannot be modified after it has been sent!", "Add product to order error popup", "Order opened by another admin", "Поръчката се обработва от", "Преизчисляване на доставката при добавяне на продукт"]
tags: [orders, products, shipping, courier, errors, locking]
plan_gates: []
created: 2026-11-09
updated: 2026-11-09
source_count: 1
---

> Part of [[orders-products]]. See the hub for the other aspects (add, edit, delete, line discount, fulfillment popover, stock effects, side effects).

# Order products — courier re-quote and save errors

## Purpose

What a product-line change in the admin does to the order's shipping, why such a save can fail with a courier's message (for example *"Request cannot be modified after it has been sent!"*), and what the order lock blocks. This is the reference for those questions; [[orders-products-add]], [[orders-products-edit]] and [[orders-products-side-effects]] point here.

## Where to find it

[[orders-details]] → products table → `+ Add product`, a line's **Edit**, or **Delete**. There is no screen of its own: it all runs when the line is saved.

## What the merchant can do here

- Check the shipping total after a line change on an unlocked, unpaid order: it may have changed.
- Keep the stored shipping price by locking the order's recalculation from the order page ([[order-pipeline-recalculation]]); a paid order keeps it anyway.
- Read a failed save's popup knowing that nothing was saved.

## Settings & fields

None. The outcome depends on whether the order has a shipping method, on the recalculation lock and the payment status ([[order-pipeline-recalculation]]), and on the courier's answer.

## Business rules

### Every add, edit and remove re-quotes the shipping

When the order has a shipping method, adding a line, saving an edit that changed something, or removing a line asks for a fresh shipping price: a live quote from the courier integration, or a new rate lookup for a method without one. It does so whether or not weight or dimensions changed. The result is written to the order's shipping line; no waybill is created or changed (a line on a generated waybill cannot be edited, see [[orders-shipping-waybill]]).

- **Unlocked and unpaid:** the new price replaces the shipping line silently.
- **Recalculation locked, or payment completed:** the stored shipping amount is kept. The courier is still asked, so a courier error still stops the save.

### A failed re-quote stops the whole save

When the re-quote returns no price, nothing is saved: the line is not added, changed or removed, and stock, totals, history and the customer email stay as they were. The popup gives the reason:

- the courier's own error text, translated where CloudCart has a translation for it;
- for a method priced by rates, the "no matching rate" message with the rate range, when the new total or weight falls outside it;
- the invalid-address message when the shipping address is incomplete.

### "Request cannot be modified after it has been sent!"

This English sentence is not a CloudCart check on the order, its status or the store's settings. It is an internal safeguard of the courier integration: during the re-quote the integration tried to change a courier request it had already sent, the quote failed, and the popup shows that text as the courier's message. The add is rolled back as above. Nothing on the order or in the settings causes it or fixes it; it is a case for CloudCart's team, with the order number and the courier (verify whether a retry goes through).

### The order lock blocks opening the order, never saving

With **Lock orders** on ([[orders-list-locking]]), opening the order page writes a lock for that admin. The lock is checked only when the order page is opened:

- **Another moderator** opening the order inside the lock time gets an access-denied screen saying *"Поръчката се обработва от <username>"* (EN *"Order is opened from <username>"*) with a back button. It is not a read-only view, and not "not found" (that screen means the order no longer exists).
- **The lock holder** is never blocked: opening again renews the lock.
- **Saves are never checked against the lock.** A line added, edited or removed from a page that was already open goes through.
- **The owner** is never blocked and writes no lock, so an owner with the order open does not shut moderators out.

### Stock for an added line

Stock is taken at once only when the order has already reached the store's stock-decrease status, or is fulfilled; otherwise when it reaches that status. See [[orders-products-stock-effects]].

## Related

- [[orders-products]] — hub.
- [[orders-products-add]] — the add flow whose save triggers the re-quote.
- [[orders-products-edit]] — edits re-quote too.
- [[orders-products-delete]] — removals re-quote too.
- [[orders-products-side-effects]] — the rest of the recalculation cascade.
- [[order-pipeline-recalculation]] — the recalculation lock.
- [[orders-list-locking]] — the **Lock orders** setting and lock time.
- [[apps-sameday]] — Sameday's services and cross-border contract.

## Open questions

- Which step of a courier integration re-uses an already-sent request, producing *"Request cannot be modified after it has been sent!"*, is not settled from the code (verify with engineering on a reproduced order).
