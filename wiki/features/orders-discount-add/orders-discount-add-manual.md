---
type: feature
nav_path: "Orders → Order details → Discount → Add → Manual discount"
route_name: admin.orders.discount.add
route_path: /admin/orders/action/discount/:order_id/add
aliases: ["Manual order discount", "One-off discount", "Flat discount", "Percent discount", "Manual discount label", "Courtesy discount"]
tags: [orders, discount, manual-discount, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 3
---

> Part of [[orders-discount-add]]. See the hub for the other aspects (form fields, existing-discount eligibility, delete, recalculation, API).

# Order-level discount — manual discounts

## Purpose

The **one-off manual discount path** of the Add Discount flow — a flat-currency amount OR a percentage typed directly on the order, applied right now to this order only. Unlike existing discounts, a manual discount has no master record in [[marketing-discounts]] and does not appear in discount reports, including the Order discounts box in analytics ([[analytics-top-order-discounts]]).

The merchant uses this for negotiated courtesy discounts ("10% off for the inconvenience") that don't correspond to a defined campaign.

## Where to find it

[[orders-details]] → **Add Discount** → primary dropdown → **Manual discount**. Reveals a type + amount sub-form (field shapes on [[orders-discount-add-form]]).

## What the merchant can do here

- Choose **Flat** (currency amount off) or **Percent** (% off) — defaults to **Percent**.
- Type the amount and save.

What the merchant CANNOT do:
- Enter a custom label / reason — the label is fixed (see below).
- Go above the subtotal — a flat amount or a percent that would take the subtotal below zero is refused (see below).

## Settings & fields

| Field | Type | Notes |
|-------|------|-------|
| **Type** | Select (Flat / Percent) | Defaults to **Percent**. Drives the amount input's mask. |
| **Amount** | Input (`type_value`) | Currency or percent depending on type. |

## Business rules

### Flat discount cannot exceed the order subtotal

A flat amount above the order's subtotal is refused with *"The value of the rebate can not exceed the subtotal of the order"*. An amount equal to the subtotal is accepted and zeroes the products.

### Percent discount above 100 is refused

The form accepts a percentage above 100, but saving it is refused with the same error, *"The value of the rebate can not exceed the subtotal of the order"*. The value must be numeric. An empty amount saves a zero-value discount, which deducts nothing and blocks adding another until it is removed.

### Default type is PERCENT, not Flat

The manual-discount type dropdown defaults to **Percent** (selected). The merchant must explicitly switch to Flat for currency-amount discounts; the amount input's mask switches accordingly (currency vs percent) on type change.

### The label is fixed — "Manual discount"

The created discount record is locked to the translation key `order.Manual_discount` — English *"Manual discount"*, Bulgarian *"Ръчна отстъпка"*. The merchant cannot type a custom label or note in this form; the customer sees only this generic label on the invoice ([[orders-invoice]]). For a custom-labelled discount, the merchant must create a one-off discount in [[marketing-discounts]] and then apply it via the existing-discount path ([[orders-discount-add-existing-eligibility]]).

### No master record to restore on delete

Because a manual discount has no master record in [[marketing-discounts]], removing it ([[orders-discount-add-delete]]) does NOT restore any uses-left counter — there is nothing to restore. This contrasts with existing discounts, which DO restore on delete.

### Save still triggers the full recalculation cascade

Like existing discounts, saving a manual discount recalculates subtotal, tax, and shipping in one transaction and fires `order.updated`. See [[orders-discount-add-recalculation]].

## Related

- [[orders-discount-add]] — hub.
- [[orders-discount-add-form]] — the manual sub-form field shapes + mask switching.
- [[marketing-discounts]] — the alternative for custom-labelled discounts.
- [[orders-invoice]] — where the fixed "Manual discount" label appears.
- [[orders-products]] — per-line manual discount (different scope).
- [[discount]] — entity page.

## Open questions

None.
