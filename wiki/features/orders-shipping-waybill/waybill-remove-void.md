---
type: feature
nav_path: "Orders → Order details → Shipping → Waybill → Remove"
route_name: admin.internal.waybill-remove
route_path: /admin/orders/action/shipping/:order_id/waybill-remove
aliases: ["Mark as unfulfilled", "Маркирай като неизпратена", "Remove waybill", "Void waybill", "Cancel waybill", "Анулиране на товарителница"]
tags: [orders, shipping, waybill, void, remove, cancel, restock]
plan_gates: []
created: 2026-06-10
updated: 2026-11-09
source_count: 4
---

> Part of [[orders-shipping-waybill]]. See the hub for other aspects (generate flow, courier specifics, payer side, print PDF, generic modal, API path).

# Waybill — remove / void

## Purpose

The flow for **voiding an active waybill** on the courier's side and reverting the order locally to `not_fulfilled`. Used when the merchant picked the wrong courier, the wrong package weight, the wrong address — anything requiring re-generation.

## Where to find it

[[orders-details]] → Shipping action row → **Mark as unfulfilled** (**Маркирай като неизпратена**), the red button shown once the order is fulfilled. There is no separate "Remove waybill" button, and the click runs **at once, with no confirmation dialog**. The JSON-API v2 `DELETE` of an order fulfillment also removes it and cancels the stored courier waybill ([[waybill-api-fulfillment]]).

## What the merchant can do here

- Click **Mark as unfulfilled** → the platform:
  1. Removes any associated fulfillment-return records first.
  2. Returns the order to `status_fulfillment = not_fulfilled` and deletes the fulfillment record.
  3. Asks the courier to cancel the waybill, only when the order carries a waybill number stored by a courier integration. A tracking number typed by hand or sent through the API is never cancelled anywhere.

## Settings & fields

No form fields and no confirmation dialog.

## Business rules

### Cancellation may fail at the courier

Voiding requires that the courier's dispatch is still cancellable. Once the courier has picked up the package, voiding may fail (e.g., Econt: *"Package already in transit"*). The merchant must then handle the return process separately via the courier's dashboard.

### Courier failure is SWALLOWED — verified hidden quirk

**If the courier's cancellation fails for any reason** (network timeout, "already in transit", courier API down), the platform CATCHES the exception silently and proceeds to delete the LOCAL fulfillment record anyway. The merchant sees a success toast.

This means: after **Mark as unfulfilled**, the order returns to `not_fulfilled` locally — but the actual dispatch on the courier side may still be active, in transit, or already delivered. **The merchant should ALWAYS verify removal in the courier's dashboard for orders that may have shipped.**

The only message specifically treated as success is *"is already cancelled"* — silently ignored as a no-op.

### Remove cascades through ALL fulfillment returns first

The platform deletes any fulfillment-return records (e.g., from [[apps-econt]]) before voiding the courier dispatch and the fulfillment. Returns are removed WITHOUT warning. Order history records the removal.

### Stock RESTORATION

Stock is incremented back on remove. The merchant doesn't see a separate "stock returned" message — it's part of the remove side-effect cascade. See [[inventory-restock]] for the symmetric re-credit flow and the per-line decrement-tracking flag that prevents double-counting.

### Order status RECALCULATED based on payment history

When the waybill is removed, the order's `status` is recalculated:

- If the order's last payment record is `completed` → status reverts to `paid`.
- Otherwise → status reverts to `pending`.

So a previously `completed` order with a removed waybill drops back to `paid` (or `pending` if the COD payment hadn't been marked yet). This can trigger workflow rules / segments based on status. Status history records both transitions.

### Side effects of Mark as unfulfilled

- Order's `status_fulfillment` → `not_fulfilled`.
- Order `status` recalculated per the rule above.
- Fulfillment returns removed first.
- Stock restored per [[inventory-restock]].
- `order.updated` webhook fires per [[settings-hooks]].
- History entry `order_fulfillment_remove` (action 47) in [[orders-history]].
- Customer is NOT auto-emailed about removal (no notification template for void).
- The shipping price, the order totals and a manually set cash-on-delivery amount are not changed.

### Re-generation is a fresh waybill

After **Mark as unfulfilled**, the merchant can change the shipping method and generates a NEW waybill via [[waybill-generate-flow]]. The original tracking number is gone; the new dispatch gets its own tracking number from the courier. The platform does not attempt to "update" a voided waybill in place.

### History captures void events

`order_fulfillment_remove` (action 47) is written on void/remove. Edits to an existing fulfillment (e.g., side change, insurance change) write `order_fulfillment_edit` (action 28). The merchant audits in [[orders-history]].

## Related

- [[orders-shipping-waybill]] — hub.
- [[waybill-generate-flow]] — re-generation flow afterwards.
- [[inventory-restock]] — symmetric stock re-credit (automatic on `not_fulfilled` transition).
- [[orders-history]] — `order_fulfillment_remove` (action 47) audit entry.
- [[orders-status-change]] — the status-recalculation rule reuses the same logic.
- [[orders-details]] — parent screen.
- [[settings-hooks]] — `order.updated` webhook on remove.
- [[apps-econt]] — Econt-specific "Package already in transit" failure mode.

## Open questions

None.
