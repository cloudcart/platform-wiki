---
type: feature
nav_path: "Orders → Order details → Shipping → Waybill → Remove"
route_name: admin.internal.waybill-remove
route_path: /admin/orders/action/shipping/:order_id/waybill-remove
aliases: ["Remove waybill", "Void waybill", "Cancel waybill", "Анулиране на товарителница"]
tags: [orders, shipping, waybill, void, remove, cancel, restock]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-shipping-waybill]]. See the hub for other aspects (generate flow, courier specifics, payer side, print PDF, generic modal, API path).

# Waybill — remove / void

## Purpose

The flow for **voiding an active waybill** on the courier's side and reverting the order locally to `not_fulfilled`. Used when the merchant picked the wrong courier, the wrong package weight, the wrong address — anything requiring re-generation.

## Where to find it

[[orders-details]] → Shipping action row → **Remove waybill** button (visible only when a waybill exists). The button triggers a confirmation dialog before the AJAX call.

## What the merchant can do here

- Click **Remove waybill** → confirm → the platform:
  1. Wraps in a DB transaction.
  2. Removes any associated fulfillment-return records first.
  3. Calls the courier's API to VOID the dispatch (`cancelBillOfLading`).
  4. Deletes the local fulfillment record.
  5. Returns order to `status_fulfillment = not_fulfilled`.

## Settings & fields

No form fields — confirmation dialog only.

## Business rules

### Remove may fail at the courier

Voiding requires that the courier's dispatch is still cancellable. Once the courier has picked up the package, voiding may fail (e.g., Econt: *"Package already in transit"*). The merchant must then handle the return process separately via the courier's dashboard.

### Courier failure is SWALLOWED — verified hidden quirk

**If the courier's `cancelBillOfLading` call fails for any reason** (network timeout, "already in transit", courier API down), the platform CATCHES the exception silently and proceeds to delete the LOCAL fulfillment record anyway. The merchant sees a success toast.

This means: after Remove waybill, the order returns to `not_fulfilled` locally — but the actual dispatch on the courier side may still be active, in transit, or already delivered. **The merchant should ALWAYS verify removal in the courier's dashboard for orders that may have shipped.**

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

### Side effects on Remove

- Order's `status_fulfillment` → `not_fulfilled`.
- Order `status` recalculated per the rule above.
- Fulfillment returns removed first.
- Stock restored per [[inventory-restock]].
- `order.updated` webhook fires per [[settings-hooks]].
- History entry `order_fulfillment_remove` (action 47) in [[orders-history]].
- Customer is NOT auto-emailed about removal (no notification template for void).

### Re-generation is a fresh waybill

After Remove, the merchant generates a NEW waybill via [[waybill-generate-flow]]. The original tracking number is gone; the new dispatch gets its own tracking number from the courier. The platform does not attempt to "update" a voided waybill in place.

### History captures void events

`order_fulfillment_remove` (action 47) is written on void/remove. Edits to an existing fulfillment (e.g., side change, insurance change) write `order_fulfillment_edit` (action 28). The merchant audits in [[orders-history]].

## Related

- [[orders-shipping-waybill]] — hub.
- [[waybill-generate-flow]] — re-generation flow after Remove.
- [[inventory-restock]] — symmetric stock re-credit (automatic on `not_fulfilled` transition).
- [[orders-history]] — `order_fulfillment_remove` (action 47) audit entry.
- [[orders-status-change]] — the status-recalculation rule reuses the same logic.
- [[orders-details]] — parent screen.
- [[settings-hooks]] — `order.updated` webhook on remove.
- [[apps-econt]] — Econt-specific "Package already in transit" failure mode.

## Open questions

None.
