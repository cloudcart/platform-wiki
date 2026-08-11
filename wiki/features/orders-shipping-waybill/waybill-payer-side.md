---
type: feature
nav_path: "Orders → Order details → Shipping → Waybill → Payer side"
route_name: admin.internal.change-side
route_path: /admin/orders/action/shipping/:order_id/change-side
aliases: ["Payer side", "Receiver pays", "Sender pays", "Change side", "PAYER_RECEIVER", "PAYER_SENDER", "PAYER_OTHER", "Платец на доставка"]
tags: [orders, shipping, waybill, payer, side, cod]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-shipping-waybill]]. See the hub for other aspects (generate flow, courier specifics, print PDF, remove/void, generic modal, API path).

# Waybill — payer side (sender / recipient / other)

## Purpose

Payer side determines **who's billed for shipping** on the courier waybill:

- **Sender** — merchant pays the courier (typical for free-shipping promotions or absorbing shipping into product price).
- **Recipient** — customer pays courier on delivery (typical with COD).
- **Other** — third party (rarely used; only some couriers support this).

Changing side recalculates the order's totals AND notifies the courier when the waybill is already generated.

## Where to find it

On the waybill form (per-courier or generic) → **Side** dropdown. Also exposed as a standalone action via the `admin.internal.change-side` POST route on existing waybills.

## What the merchant can do here

- Pick a side from the courier's allowed list when generating a waybill.
- Change the side on an existing waybill (recalculates rates AND re-syncs the courier).
- Cannot pick a side outside the courier's allowed set — error: *"Invalid side"*.

## Settings & fields

### Per-courier side support — concrete table (verified)

| Courier | Sender | Receiver | Other (Third Party) | Notes |
|---------|--------|----------|---------------------|-------|
| **Econt** | Yes | Yes | No | Sender or Receiver only |
| **Speedy** | Yes | Yes (only if destination = BG) | No | International destinations DROP receiver |
| **DPD Bulgaria** | Yes | Yes | Yes (Third party) | All three sides supported |
| **DPD Romania** | depends per manager override | — | — | Per-courier definition |
| **BoxNow** | Yes | No | Yes | Locker-only flow |
| **GLS / Cargus / DHL / Berry / AlbanianCourier / Ntclogistics / Tcscourier / Fancourier / EuShipment / ElsLogistic / Sendcloud** | each has its own override | — | Typically Sender + Receiver |

For Speedy specifically: shipping to any destination country other than Bulgaria removes the receiver-pays option entirely — only the sender can pay.

### Allowed-sides filter rules

The platform asks the active shipping manager for its allowed sides (Sender / Receiver / Other) and then filters that list. **PAYER_RECEIVER (recipient pays)** is FILTERED OUT when ANY of these is true:

- Order is `paid` or `completed` (no point in recipient paying after the fact).
- Shipping pricing model is `fixed_price`, `fixed_weight`, `calculator_fixed`, or `price_and_weight` (shipping cost already baked into the order).
- Order has `has_free_shipping` flag (free shipping is by definition sender-paid). See [[marketing-discounts-shipping#free-shipping-discount-marks-the-order-as-has-free-shipping-hides-receiver-pays-option-on-the-waybill|the trigger table on marketing-discounts-shipping]] for all 6 ways this flag flips.
- The payment provider has `is_seller_payer_shipping` set (e.g., some COD payment integrations require sender to pay shipping).
- Free shipping rule met by order subtotal (`getFreeShippingTotal('input')` ≤ order total).
- Speedy-specific: shipping address country is NOT Bulgaria.

So an order that's already paid will only show Sender (or Other if courier supports it). The merchant cannot switch a paid order to recipient-paid shipping without removing the waybill first via [[waybill-remove-void]].

## Business rules

### Default side selection — 3-step fallback

When the merchant opens the waybill modal for a fresh order (no `side` meta saved yet), the platform decides which side to pre-select via:

1. **Order's saved `side` meta** — if the merchant or an integration previously stored a side on this order, that wins. Most newly-created orders have no `side` meta until a waybill is generated.
2. **Courier provider's configured default side** — every courier app has a *"Default payer side"* setting in its admin-panel config (e.g., *Speedy → Settings → Default payer side*). When empty or invalid, the **internal default is `Receiver`** (a leftover from the COD-dominated Bulgarian market where receiver-pays is the cultural norm).
3. **If the side picked in step 1 or 2 is NO LONGER in the filtered allowed list** (one of the filter rules above eliminated it), the platform falls back to **the first key remaining in the filtered allowed list**.

### "First remaining" fallback — concrete table

| Courier | Native order in `getWaybillSides` | If Receiver gets filtered out, fallback side becomes... |
|---|---|---|
| Econt | Receiver → Sender → Other | **Sender** |
| Speedy | Receiver → Sender | **Sender** |
| Cargus / Berry / DPD-style | Sender → Receiver | **Sender** (was already first; no effective change) |
| BoxNow (lockers) | Sender → Other | **Sender** (was already first; no effective change) |
| AlbanianCourier / Rapido / Elslogistic | Sender → Receiver | **Sender** |

**Merchant-visible consequence:** when a merchant has Speedy / Econt configured with *"Default payer side = Receiver"* (the BG-COD default) and one of the filter rules kicks in (free-shipping discount, order already paid, seller-pays-shipping payment provider), the waybill modal opens with **Sender pre-selected** instead of the merchant's configured default. Receiver does not appear in the dropdown at all; the merchant can still pick Other where allowed.

### No silent corruption

The platform never picks a side that the courier doesn't allow. If the filtered list is empty (extreme edge case — courier publishes no allowed sides for this scenario), the side defaults to `null` and the courier-specific waybill form surfaces an error at save time rather than auto-picking something the courier would reject.

### Side change cascades to waybill

When the merchant changes payer side on an existing waybill, the platform calls `changeShipping(provider, false, sideChanged=true)`. This:

1. Recalculates shipping quote with new payer side.
2. Updates `OrderShipping` row.
3. Recalculates order totals.
4. Writes `OrderShippingChange` event → history records the shipping-before / shipping-after states. See [[orders-history]].
5. **Notifies the courier** of the side change.

For couriers that don't support live side-change, the courier-side dispatch may be out of sync after this call. There is NO automatic void+regenerate. The merchant must monitor the courier's dashboard to confirm the change took effect. Toast: *"Shipping provider changed"* (translation reuse — the message isn't side-specific).

### If the merchant wants Receiver to ALWAYS be available

Despite the filters, the workarounds are:

- Don't attach a free-shipping discount (use a [[apps-cart-rules|Cart Rule]] with `value_type=free_shipping` instead — it discounts the shipping line but does NOT set the `has_free_shipping` flag; see [[marketing-discounts-shipping#free-shipping-discount-marks-the-order-as-has-free-shipping-hides-receiver-pays-option-on-the-waybill|the receiver-pays trigger table]]).
- Generate the waybill BEFORE the order is paid (the *paid* / *completed* status filter only kicks in after payment).
- Use a shipping pricing model OTHER than `fixed_price` / `fixed_weight` / `calculator_fixed` / `price_and_weight` (e.g., live-quote from the courier).
- For Speedy specifically: only ship to a Bulgarian address.

## Related

- [[orders-shipping-waybill]] — hub.
- [[marketing-discounts-shipping]] — the `has_free_shipping` trigger table (6 ways the flag flips).
- [[apps-cart-rules]] — the `free_shipping` value-type cart rule (does NOT set `has_free_shipping`).
- [[orders-history]] — `OrderShippingChange` event records side changes.
- [[shipping]] — shipping pricing models referenced in the filter rules.
- [[settings-cart]] — payment provider's `is_seller_payer_shipping` flag.

## Open questions

None.
