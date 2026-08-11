---
type: feature
nav_path: "Marketing → Discounts → Countdown → Cart totals + stacking"
route_name: discounts-create
route_path: /admin/marketing-new/discounts/create/countdown
aliases: ["Countdown cart totals", "Countdown stacking", "Countdown discount group", "Countdown per-product attachment", "Countdown order rows"]
tags: [marketing, discounts, countdown, cart-totals, stacking]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[marketing-discounts-countdown]]. See the hub for the other aspects (editor, storefront popup + timer, eligibility, single-instance rule, programmatic access).

# Countdown discount — cart totals, stacking, order rows

## Purpose

This page documents what happens to the cart and the placed order once the Countdown discount passes eligibility: how the totals line is computed, which discount group it lives in, why it stacks freely with code-based and order-over discounts, why per-product "was X / now Y" pricing is NOT shown on listings, and what rows the platform writes when the order is placed.

The crisp summary: Countdown is a **whole-order** discount (single subtraction at totals time, no per-product attachment), in its own **`countdown` discount group**, that **coexists** with every other group at checkout.

## Where to find it

The math runs in the storefront cart engine on every cart-totals computation. The result is visible to the customer in the checkout summary's totals area. On order placement, an `OrderDiscount` row is written; the row drives downstream analytics and webhook payloads. There is no admin URL for the totals math itself — the merchant influences it indirectly via the inner type (`flat` vs `percent`) and `type_value` in the [[countdown-discount-editor]].

## What the merchant can do here

- Watch the Countdown apply at checkout as a separate `countdown` discount-group totals line, stacking on top of any `order_over` discount and any code-based discount the customer enters.
- Confirm the negative amount math: for `percent`, `subtotal × (percent / 100)` (split per VAT group on multi-VAT carts); for `flat`, the stored `type_value` (capped at subtotal).
- See an `OrderDiscount` row on the placed order with `is_countdown = 1` and `discount_group = countdown` — used downstream by [[analytics-top-order-discounts]].

The merchant CANNOT make Countdown render "was X / now Y" pricing on product listings — Countdown skips per-product attachment entirely.

## Settings & fields

### Cart totals math

When the Countdown discount is attached, the totals chain (specifically `DiscountBeforeShipping`) adds a negative totals line **before** the shipping is added:

| Inner type | Formula |
|------------|---------|
| `percent` | `discount_amount = subtotal × (percent / 100)`. When the cart has multiple VAT rates, the platform also computes per-VAT-group amounts (one negative per VAT group present in the cart). |
| `flat` | `discount_amount = type_value` (capped at subtotal — see [[countdown-discount-eligibility]] for the "cart too small" silent skip). |

The totals line is keyed `discount.before.countdown.<discount_id>`. Its `value` is set to the timer's expiry timestamp (`popupFirstShowDate + countdown_minutes`) so the storefront timer module knows when to stop ticking — see [[countdown-discount-storefront-popup]].

### Order rows attached at checkout

When the customer places an order with an active Countdown discount:

- An `OrderDiscount` row is created with `is_countdown = 1`, `discount_group = countdown`.
- The order's discount-meta carries `parameter = countdown, value = countdown` so reports can identify which orders were Countdown-driven.
- The discount's `uses` counter increments when the order reaches one of the counted statuses (see [[settings-statuses]]).

### Discount groups Countdown coexists with

| Group | What's in it | Stacks with Countdown? |
|-------|--------------|------------------------|
| `countdown` | The Countdown discount. | — |
| `order_over` | Regular Flat / Percent over-amount discounts. | YES — two separate negative totals lines. |
| Per-line code (Promo / Container / Code PRO) | Code-based discount applied per cart line. | YES — codes and Countdown never see each other. |
| Fixed (per-product overrides) | Per-product `product_to_discount` rows. | YES — Countdown skips per-product attachment entirely. |

## Business rules

### Excluded from per-product attachment regeneration

Unlike `flat` and `percent` discounts which create per-product attachment rows (`product_to_discount`), **Countdown discounts DO NOT generate per-product attachment rows**. The regeneration step returns early when `countdown_minutes` meta is present. So Countdown:

- Does NOT show "was X / now Y" pricing on product cards / listings.
- Does NOT inject "On sale" smart-collection memberships.
- Shows its effect ONLY via the checkout-summary totals line + timer module.

### Countdown fetched separately from order-over collection

The cart's `getDiscountsOver` query EXCLUDES Countdown (filters with `!isCountDown`). Countdown is fetched separately via `getCountdownDiscount` and added to its own `countdown` discount group. A cart can simultaneously have:

- A standard flat / percent over-amount discount (in the `order_over` group).
- A Countdown discount (in the `countdown` group).

Both lines coexist — merchants can stack a regular sale with the Countdown urgency.

### Stacking with code-based discounts (Promo, Container, Code PRO)

Code-based discounts coexist with Countdown:

- The customer can enter a code on top of an active Countdown — both apply at separate stages.
- The `code_apply` flag on the code controls whether the CODE can stack on per-product discounts (Fixed) — it does NOT block Countdown.
- A code's "stacking on discounted items" check looks at per-line discounts, not at Countdown's order-level subtraction.

The per-line code-apply check happens in the line-discount path; Countdown happens in the order-totals path. They never see each other — see [[marketing-discounts-code-pro]] and [[marketing-discounts-codes]].

### Multi-VAT carts produce one negative line per VAT group (percent only)

When the cart has multiple VAT rates, the percent-type Countdown produces one negative totals line per VAT group present in the cart. This keeps the VAT-correct math intact — each line's VAT base is reduced proportionally. (Flat-type Countdown produces a single negative line regardless of VAT mix `(verify)`.)

### Per-cart timer survives navigation, resets on cookie clearing

The `countdown_popup_first_showing` timestamp is stored on the cart meta. As long as the customer keeps the same cart (same session / customer account), navigating away and returning doesn't reset the timer — the deadline keeps ticking. But clearing cookies / logging out / starting a new cart resets the meta, and the timer restarts on the next checkout visit — see [[countdown-discount-storefront-popup]].

### `force_save` only meaningful for `order_over`

The `force_save` flag is meaningful only when the Countdown's target is `order_over`. For target `all`, the flag is stored but unused — there are no `order_over` conditions to "force save" past.

When `force_save` is ON and the target is `order_over`, an admin-edited order keeps the Countdown discount even if the edited cart drops below the threshold. Without `force_save`, an admin edit that drops the cart below `order_over` removes the Countdown line on next recompute.

### FastOrder bypass

The [[apps-fast-order]] integration explicitly excludes Countdown discounts from cart evaluation when the order is submitted through the fast-order route — no popup, no timer, no totals line. See [[countdown-discount-storefront-popup]] for the per-cart meta keys that don't get written on this path.

## Related

- [[marketing-discounts-countdown]] — hub.
- [[countdown-discount-eligibility]] — what must pass before the totals math runs.
- [[countdown-discount-storefront-popup]] — the timer's expiry timestamp travels on the totals line `value`.
- [[discount-stacking]] — the cross-cutting stacking ladder; Countdown is in its own group.
- [[marketing-discounts-code-pro]] — Code PRO codes stack on top of Countdown.
- [[marketing-discounts-codes]] — Container codes stack on top of Countdown.
- [[marketing-discounts-fixed]] — Fixed per-product overrides; Countdown's per-product attachment is skipped, so Fixed and Countdown apply at separate stages.
- [[apps-fast-order]] — bypasses Countdown.
- [[analytics-top-order-discounts]] — surfaces Countdown redemptions via `is_countdown = 1` on the `OrderDiscount` row.

## Open questions

- Verify whether flat-type Countdown produces a single negative line on multi-VAT carts or splits per VAT group like percent does `(verify)`.
