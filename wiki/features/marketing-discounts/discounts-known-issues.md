---
type: feature
nav_path: "Marketing → Discounts → Known issues"
route_name: ""
route_path: ""
aliases: ["Discount gotchas", "Discount edge cases", "Discount validation messages", "Container codes reusable", "Order_over strict greater", "Free shipping tie-break", "Highest threshold wins", "Negative discount total", "Грешки при отстъпки"]
tags: [marketing, discounts, promotions, known-issues, edge-cases, validation]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 4
---

# Discount known issues & merchant gotchas

> Part of [[marketing-discounts]]. See the hub for the other cross-cutting aspects (lifecycle, eligibility, storefront display, audit trail) plus per-type details.

## Purpose

This aspect catalogues the **by-design surprises** the support agent should look up first when a merchant reports unexpected behaviour. Each item is either: (a) a validation rule that rejects something the merchant thought should work, or (b) a cart-engine resolution rule that picks a different winner. The **first page to read** for "the discount doesn't apply / the wrong discount applied / I got an error I don't understand" tickets.

## Where to find it

These surface at three points: **save-time validation errors** (conflicting fields), **checkout-time messages** (code can't apply), and **silent cart-engine choices** (no error, but a different total than expected).

## What the merchant can do here

- Set `order_over` thresholds 0.01 below the intended minimum to dodge the strict-greater rule.
- Know that with two overlapping no-code Free Shipping discounts, which name shows is unspecified (free shipping applies either way).
- Subscribe to webhooks for audit (no internal log exists — see [[discounts-audit-trail]]).

## Settings & fields

This page introduces no new fields; it documents corner-case behaviour of fields on the other aspects.

## Business rules

### Countdown — checkout uses one

A second Countdown discount can be saved. Checkout uses the first active one it finds and tries no other.

### Quantity — one Quantity discount per product

A product can be in only one Quantity discount, active or not. A second create on the same product returns `"Product is already in use"`. For different tiers per customer group, use [[apps-cart-rules]] instead.

### Promo code uniqueness

A promo code is unique across `discounts.code` per store. Code PRO codes live in a separate table (`discounts_code_pro.code`) and don't collide with regular codes — see [[marketing-discounts-code-pro]]. Container codes are one store-wide pool in which each string is unique — see [[marketing-discounts-codes]].

### Strict-greater rules — `order_over` and `max_uses`

`order_over`: for a no-code Flat / Percent discount or a code, the cart subtotal must be **strictly greater than** the threshold; equal does NOT qualify. A 50 EUR threshold rejects 50 EUR with `"The discount could not be applied because the minimum total price of the products has not been reached."`. Workaround: set threshold slightly below (e.g., 49.99). At-or-above applies to no-code **Free shipping** (on the total before shipping, after order-level discounts), a free-shipping code once it is accepted, **Countdown** (on the products subtotal) and **Code PRO** Orders-over conditions (on the subtotal of the lines). See [[marketing-discounts-shipping]].

`max_uses > uses`: a discount with `max_uses = 100` is still active at `uses = 99` and becomes inactive at `uses = 100`. The 100th order consumes the last slot when its status hits a counted status — see [[discounts-lifecycle]].

### `order_over` resolution + shipping tie-break

Several **no-code `order_over`** Flat / Percent discounts: the highest threshold the subtotal passes wins, whatever it saves, flat or percent. If that one cannot apply, no other is tried. Largest saving applies only among several Orders-over conditions inside one Code PRO code. See [[discounts-eligibility]].

**Shipping discounts use a SEPARATE path** (not the `order_over` pool). The engine tries every discount and returns the **first that qualifies**, with no threshold sort: free shipping applies either way, and which name shows is unspecified when two qualify. The "left to free shipping" amount uses the closest threshold. See [[shipping-discount-stacking]].

### Amount larger than what it comes off

A flat amount is not capped at the subtotal. A code with an Orders-over target checks only the threshold, and a code on every product or a specific target has no lower limit once accepted, so a line and the total can go below zero. See [[discount-stacking-amount-by-target]].

### Container codes

Container codes are one store-wide pool attached to no Container, and an order does not use a code up: it stays reusable until turned off or deleted. All active Containers for the customer's region try the entered codes and the highest total wins; a code applies only if it fits what remains of that Container's value. A Container code is never refused for `code_apply`: the Container's default is on and its form has no such switch. See [[marketing-discounts-codes]].

### Code lookup

A typed code is looked up among promo codes, barcode matches (EAN-13 / EAN-8 + optional store prefix) and Code PRO codes together, with no set priority. Container codes are tried only if none of those match.

### Per-customer cap auto-clears the code

When a logged-in customer hits `maxused_user`, the platform **clears the code from the cart entirely** (not just blocks redemption) and returns *"You have used this discount code the maximum number of times"*. See [[discounts-eligibility]].

### JSON-API v2

- **HTTP 402 Payment Required** when a plan quota is exceeded, on create only, comparing usage with `discount_global`, `discount_fixed` or `discount_coupon`. The admin form's create check returns HTTP 403 instead (see the hub's Plan-gates note).
- **Quantity and Countdown not creatable via JSON-API v2.** The JSON-API v2 allowlist is 5 types: `percent`, `flat`, `fixed`, `shipping`, `code-pro`. See [[api-discounts]].
- **No audit log.** No internal audit log exists for discount changes, only webhooks; the payload does not distinguish API from admin. See [[discounts-audit-trail]].

## Related

- [[marketing-discounts]] — hub.
- [[apps-cart-rules]] — workaround engine when a single Quantity discount isn't flexible enough.
- [[json-api-v2]] / [[api-discounts]] — programmatic CRUD with the 5-type allowlist + HTTP 402 on plan quota.

## Open questions

None.
