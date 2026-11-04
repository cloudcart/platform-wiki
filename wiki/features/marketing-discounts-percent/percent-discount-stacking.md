---
type: feature
nav_path: "Marketing → Discounts → Percent → Stacking"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/global
aliases: ["Percent discount stacking", "code_apply", "apply_regular_price"]
tags: [marketing, discounts, percent, stacking]
plan_gates: ["discount_global", "discount_coupon"]
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

> Part of [[marketing-discounts-percent]]. See the hub for the other aspects (editor, fields, targeting, validity, plan gates, programmatic access).

# Percent discount — stacking with other discounts + Cart Rules

## Purpose

This page documents how a Percent discount combines with other discounts and Cart Rules at checkout: when they stack, which no-code `order_over` discount wins when several qualify, when a code is refused on an already-discounted cart, and the `code_apply` / `apply_regular_price` interaction.

## Where to find it

Stacking behaviour runs in the storefront cart engine on every cart-totals computation. There's no admin URL for it — the merchant influences it indirectly via the `code_apply` and `apply_regular_price` toggles on a code-based Percent ([[percent-discount-editor]]), and via the broader `discounts_used_statuses` setting (see [[settings-statuses]]). The cross-type stacking ladder lives on [[discount-stacking]].

## What the merchant can do here

- Toggle `code_apply` (default OFF) on a code-based Percent to allow it on carts that already have a per-product discount.
- Toggle `apply_regular_price` (visible only when `code_apply = 1`) so the code is worked out on the regular price and replaces the product discount when its price is lower.
- Plan several no-code `order_over` discounts knowing only the highest threshold the subtotal passes applies.
- Layer Percent with Cart Rules knowing their conditions see the total after product discounts and line-level codes, before order-level discounts.

## Settings & fields

### Stacking-related fields (code-based Percent only)

| Field | Backend key | What it does |
|---|---|---|
| **The discount is applied even when the cart contains discounted products** | `code_apply` | Defaults OFF. When ON, the code is not refused on `order_over` carts with already-discounted lines, and does not skip those lines. |
| **Apply to the regular price of products, if this discount is greater** | `apply_regular_price` | Visible only when `code_apply = 1`. The code is worked out on the regular price; if that price is lower than the current discounted price it replaces the product discount, otherwise the line keeps the product discount and no code. |

Full validation strings + the other code-only fields live on [[percent-discount-fields]].

## Default-off stacking (`code_apply = 0`)

For code-based Percent discounts, the default `code_apply = 0` means the code does not stack on a line that already holds a product discount (e.g., a [[marketing-discounts-fixed]] on one of the items). The merchant must explicitly enable **"The discount is applied even when the cart contains discounted products"** to stack.

No-code Percent discounts have no such switch. A no-code `order_over` applies on the subtotal after product discounts. A no-code Percent on `all` or a specific target is itself a product discount (see *Other combinations DO stack* below).

What happens depends on the target. A Percent code with target `order_over` is refused at entry when any cart line holds a product discount, with *"This discount code can not be applied because you already have a discounted products at your cart"*. A Percent code on `all` or on specific products / categories / vendors / selections is accepted and skips those lines; if all are discounted, nothing comes off and no message shows. Free-shipping codes have their own rules — see [[marketing-discounts-shipping]].

## Apply-regular-price comparison

With `code_apply = 1` AND `apply_regular_price = 1`, the code is worked out on the line's **regular** price and compared with the current discounted price. If the code's price is lower, it replaces the product discount; otherwise the line keeps the product discount and no code. Never both. Regular price 100 EUR, Fixed 80 EUR: with a 10% code the customer pays 80 EUR; with a 30% code they pay 70 EUR and the Fixed no longer applies.

## Several no-code `order_over` discounts — highest threshold wins

When several no-code `order_over` discounts qualify, flat or percent, **they do NOT stack — only the one with the highest threshold the subtotal passes applies, whatever it saves**. If that one cannot apply (a flat larger than the subtotal), none does. Examples on a 150 EUR cart:

- "20% off over 100 EUR" vs "10 EUR off over 50 EUR" → **the 20% wins** (threshold 100).
- "50 EUR off over 50 EUR" vs "5% off over 100 EUR" → **the 5% wins** (threshold 100), saving 7.50 EUR.
- Equal thresholds → undefined which wins; the merchant should avoid them.

## Other combinations DO stack

These live in independent slots in the engine:

- A no-code Percent (`order_over`) + a Code-based Percent → both apply.
- A no-code Percent (`order_over`) + a per-product Fixed → both apply.
- A no-code Percent (`order_over`) + a Quantity tier → both apply.
- A no-code Percent + a Countdown discount → both apply.
- A no-code Percent + a Free-shipping discount → both apply.
- A no-code Percent + a Cart Rule (cart-level or product-level) → both apply (see *Cart Rules vs Percent discount ordering* below).

Product-level discounts on one line never add up. Among Fixed and no-code Flat or Percent on `all` or a specific target, the lowest final price wins; a Quantity tier is used instead of them.

A subscription line whose plan option has **Combine with other discounts** off takes none of these line discounts ([[apps-subscriptions-plans]]).

## Cart Rules vs Percent discount ordering

[[apps-cart-rules]] conditions see the total after product discounts and line-level codes, before order-level discounts. So a Percent on `all` or a specific target lowers the total a rule's condition sees; a Percent on `order_over` does not. A product-level Cart Rule's reduction is already in the subtotal that `order_over` is checked against.

## Stacking with other code-based Percent

Two code-based Percent discounts cannot apply on the same cart — the cart stores ONE code at a time. Switching codes overwrites the previous. The same holds for a [[marketing-discounts-code-pro]] code.

## Quantity-discount interaction — separate engine slots

When a Percent code with `code_apply = 1` lands on a cart line that already qualifies for a Quantity-discount tier (see [[marketing-discounts-quantity]]), the engine applies them in **separate slots**: the Quantity tier acts on the line first (line-level price drop), then the Percent code's allocation acts on the discounted line subtotal. There is no special "subtract the tier save" step at the Percent allocation stage — the Percent is simply computed against whatever per-unit price remains after the Quantity tier has applied.

Merchant-visible outcome: both savings show inside the product line's price, with no separate row in the totals. Total saving = Quantity-tier saving + (Percent × post-tier-price). Without `code_apply = 1`, the Percent code skips any line already on a Quantity tier (per the "Default-off stacking" rule).

## Business rules

- **Per-customer cap auto-clears the code** — if a logged-in customer hits the `maxused_user` cap for this Percent code, the platform doesn't merely fail to apply — it **wipes the code off the cart** and returns: *"You have used this discount code the maximum number of times"*. They'd need to enter a different code.
- **Cart Rule conditions run before order-level discounts** — a Percent on `order_over` is not yet taken off when a rule's condition is checked; a Percent on `all` or a specific target is.

## Related

- [[marketing-discounts-percent]] — hub.
- [[marketing-discounts-flat]] — sister type that shares the no-code `order_over` pool.
- [[marketing-discounts-fixed]] — per-product Fixed; the type that triggers `code_apply = 0` rejection on `order_over` Percent codes.
- [[marketing-discounts-quantity]] — Quantity tiers; separate engine slot.
- [[marketing-discounts-countdown]] — Countdown discount; stacks freely.
- [[marketing-discounts-shipping]] — Free shipping; stacks freely + has its own `code_apply = 0` exception for target=`all`.
- [[marketing-discounts-code-pro]] — multi-code campaigns.
- [[apps-cart-rules]] — conditions see the total after product discounts and line-level codes.
- [[discount-stacking]] — cross-type stacking ladder.
- [[percent-discount-validity]] — strictly-greater `order_over` rule and per-customer cap mechanics.

## Open questions

None.
