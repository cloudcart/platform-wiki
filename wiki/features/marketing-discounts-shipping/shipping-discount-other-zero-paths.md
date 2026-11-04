---
type: feature
nav_path: "Marketing → Discounts → Shipping → Other zero-paths"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Free shipping other paths", "Has free shipping flag", "Receiver pays hidden", "Cross-sell free shipping", "Payment shipping discount", "Order modification free shipping", "Cart rule free_shipping action"]
tags: [marketing, discounts, shipping, cross-sell, payment, waybill, cart-rule]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 4
---

> Part of [[marketing-discounts-shipping]]. See the hub for the other aspects (eligibility, value mechanics, stacking, force-save, plan gates / API, examples).

# Shipping discount — other paths that zero the shipping line

## Purpose

A merchant-configured Free-shipping discount is only **one of several** mechanisms that can zero the shipping line on a cart / order. This page catalogues them, plus a condition table for **why the waybill sometimes hides the "receiver pays" option**.

Tickets that land here: *"my order has free shipping but I didn't set a discount"*, *"why is receiver-pays missing on this waybill"*.

## Where to find it

These mechanisms are NOT configured from the Free-shipping discount form. Each lives on a different surface: Cross-Sell injection (cross-sell admin), payment-provider waive (per-provider promo bundle), order modification (manually on [[orders-details]] `(verify)`), Cart Rule with `free_shipping` action ([[apps-cart-rules]]). The receiver-pays-hidden behaviour is read on the [[orders-shipping-waybill|waybill]] picker.

## What the merchant can do here

- Recognise that several different mechanisms can produce a zeroed shipping line.
- Pick the right one (the discount form is one option; a Cart Rule gives free shipping on its own conditions, and an order modification covers a single order).
- Understand which mechanisms set the **"has free shipping"** flag (and hide receiver-pays on the waybill) vs which don't.

## Settings & fields

There are no shipping-discount-specific fields on this page — each path is configured on its own surface. The shared **"has free shipping"** flag is a computed read-only flag on the order; it is not directly editable.

## Business rules

### The mechanisms that zero the shipping line

Beyond the merchant-configured Free shipping discount, **these other mechanisms** can independently zero the shipping line on a cart / order:

1. **Cross-Sell injection** — a cart line triggered by a Cross-Sell configured with `free_shipping > 0` injects a synthetic in-memory shipping discount. The cart's discount-lookup returns a synthetic Discount object (constructed in-memory, not saved to the database) named after the cross-sell. This auto-applies free shipping for that cart even if no Free-shipping discount is configured by the merchant. The merchant doesn't see this discount in the Discounts list — it's a hidden cross-sell side-effect.

2. **Payment-provider-driven shipping waive** — certain payment-provider promo bundles (e.g., specific BNPL or CloudCart Pay configurations) attach a `payment-shipping-*` discount type to the order, which adds a free-shipping row to the totals. This is independent of the merchant-configured Free shipping discount.

3. **Order modification** — an admin can manually attach an order modification of type `discount` and value-type `free_shipping` to an existing order `(verify)`, which adds a free-shipping row to the totals. Used when staff want to comp shipping on a single order without affecting other carts.

4. **Cart Rule with `free_shipping` action** — a Cart Rule that fires a free-shipping action zeroes the shipping line via a separate cart-rule modification. See [[apps-cart-rules]] for the differences. **Key one:** the Cart Rule mechanism does NOT set the *"has free shipping"* flag, so the waybill picker keeps the receiver-pays option visible — see the next section.

Only one free-shipping row ever shows. The first that applies takes it, in this order: no-code discount or Cross-Sell, then code, then payment method, then Cart Rule.

### Free shipping discount marks the order as "has free shipping" (hides receiver-pays on the waybill)

When a Free shipping discount (`type=shipping`) attaches to an order and its `order_over` condition is met (or `order_over` is empty), the order is internally flagged as **"has free shipping"** — a computed flag the platform reads when deciding what shipping-side-of-pay options to show on the courier waybill.

Concrete merchant-visible side-effect: every courier that supports a **receiver-pays-the-shipping** option (the "PAYER_RECEIVER" side on the waybill — DPD, Speedy, Econt, GLS, Omniship-integrated couriers, Sendcloud, Eushipment, etc.) **HIDES the receiver-pays choice** when this flag is true. The merchant then sees only "sender pays" on the waybill side selector — because there is no shipping cost left for the receiver to pay.

### All triggers that hide receiver-pays on the waybill (independent of this discount)

Other actions that ALSO trigger this hide (independent of the free-shipping discount flag) — useful when troubleshooting why "receiver pays" is missing on a waybill:

| Trigger | Side-effect |
|---|---|
| Free shipping discount attached AND `order_over` met (this discount) | "has free shipping" flag becomes true |
| Payment provider with seller-pays-shipping promotion attached (specific `payment-shipping-*` discount types — e.g., certain BNPL or CloudCart Pay promo bundles) | "has free shipping" flag becomes true |
| Shipping provider's per-method **Free shipping threshold** setting is reached by the order total | Receiver-pays is hidden directly (no flag toggle — checked at waybill time) |
| Order status is `paid` or `completed` | Receiver-pays is hidden (the shipping side is already committed) |
| Shipping pricing model is `fixed_price`, `fixed_weight`, `calculator_fixed`, or `price_and_weight` | Receiver-pays is hidden (these pricing models don't support per-side payer split) |
| Payment provider's `seller_payer_shipping` flag is on (provider-level promo, e.g., select CloudCart Pay configurations) | Receiver-pays is hidden |
| The shipping method has no pricing type | Receiver-pays is hidden |
| The order was paid partly from the wallet | Receiver-pays is hidden |

**[[apps-cart-rules|Cart Rules]] with a `free_shipping` action do NOT trigger this flag** — they zero the shipping line through a separate mechanism that doesn't surface as a `type=shipping` discount on the order. A Cart Rule's free shipping also makes sender the default payer, but the waybill picker keeps showing both sides.

### When to use which mechanism — decision guide

- **Native Free-shipping discount** — store-wide, condition-based, customer-visible. Use for "Free shipping over X EUR" / "Free shipping for VIPs" / a code limited to one region. Sets the flag.
- **Cross-Sell free_shipping** — bundle promo ("buy this, get free shipping"). Synthetic; not in the Discounts list. Sets the flag.
- **Payment-provider waive** — payment-method-specific promo (e.g., pay with BNPL → free shipping). Sets the flag.
- **Order modification** — one-off staff comp on a single existing order `(verify)`. Does NOT set the flag.
- **Cart Rule with `free_shipping` action** — free shipping on conditions the Discounts form doesn't have (cart contents, customer history). It zeroes the whole line; there is no partial shipping action. **Does NOT set the flag** — waybill keeps both sides, sender by default.

### What the free-shipping row shows

A no-code discount or Cross-Sell row shows its `name` only. A code row shows the `name` and the code. A payment-method or Cart Rule row shows *"Free Shipping"* with its name beside it. See [[shipping-discount-stacking]] for which one takes the row.

## Related

- [[marketing-discounts-shipping]] — hub.
- [[apps-cart-rules]] — Cart Rules with `free_shipping` action (does NOT set the "has free shipping" flag).
- [[orders-shipping-waybill]] — the waybill picker that hides receiver-pays when the flag is true.
- [[orders-details]] — admin order screen where order modifications are added `(verify)`.
- [[shipping]] — store's shipping providers; per-method *"Free shipping threshold"* is an independent trigger.
- [[settings-shipping]] — per-method shipping settings, including the threshold.

## Open questions

None.
