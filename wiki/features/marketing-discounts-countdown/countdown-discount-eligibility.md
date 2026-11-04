---
type: feature
nav_path: "Marketing → Discounts → Countdown → Eligibility"
route_name: discounts-create
route_path: /admin/marketing/discounts/create/countdown
aliases: ["Countdown eligibility", "Countdown validity check", "Countdown discount target", "Countdown order_over threshold", "Countdown only_customer"]
tags: [marketing, discounts, countdown, eligibility, validity-check]
plan_gates: []
created: 2026-06-10
updated: 2026-11-04
source_count: 2
---

> Part of [[marketing-discounts-countdown]]. See the hub for the other aspects (editor, storefront popup + timer, a second Countdown, cart totals + stacking, programmatic access).

# Countdown discount — eligibility (target, customers, dates, validity check)

## Purpose

This page documents the conditions a cart must satisfy for the Countdown popup to fire and the discount to attach: the target (`all` vs `order_over`), the customer-group restriction, the `only_customer` registered-users gate, the calendar `date_start` / `date_end` window, the per-session timer that runs on top, and the silent skip when a fixed amount is larger than the subtotal.

The eligibility chain runs on **every cart-totals computation** (cart view, checkout, order placement) — not only at popup-show time. So a cart that becomes eligible mid-session (e.g., customer adds an item that pushes them over `order_over`) starts seeing the popup on the next checkout visit, provided the calendar window is still open.

## Where to find it

The eligibility chain runs in the storefront cart engine on every cart-totals computation. There's no admin URL for the eligibility check itself — the merchant influences it indirectly via the editor's target, customer-group, `only_customer`, and date fields (see [[countdown-discount-editor]]). The popup endpoint that anchors the per-session timer lives at `/checkout/countdown-discount-popup` (route `checkout.countdown_discount_popup`) — see [[countdown-discount-storefront-popup]].

## What the merchant can do here

- Restrict who is eligible by choosing the target (`all` vs `order_over`) and the `order_over` threshold.
- Set `only_customer` (shown for "Orders over", off by default) so guests get no discount.
- Restrict to specific [[customers-custom-groups]] via `customer_groups[]` when `customer_groups_target = no`.
- Set the calendar `date_start` / `date_end` window during which the Countdown is even considered.
- Configure the per-session timer length (`countdown_minutes`) — see [[countdown-discount-editor]].

The merchant CANNOT bypass the silent "cart too small" skip for flat-type Countdown — when `type_value > cart.subtotal`, the discount doesn't apply and the customer sees nothing.

## Settings & fields

### Discount target

| Value | Means | Companion field |
|-------|-------|-----------------|
| `all` ("For every product in the cart") | Apply to any cart that passes the customer-group + `only_customer` + date-range filters. | — |
| `order_over` ("Orders over") | Products subtotal at or above `order_over`, measured after per-product and line discounts, before whole-order discounts. | `order_over` (amount in store currency). |

The Countdown form's target dropdown only offers these two values — see [[countdown-discount-editor]]. There is NO product / category / vendor / `category_vendor` / `selection` target for Countdown.

### Registered-users gate

`only_customer` defaults to off, and the form shows it only for "Orders over". When ON, guests get no discount row; the popup still shows to them and their timer starts. When OFF, both guests and registered customers get the discount.

### Customer-group filter

The customer-group check runs at cart-time: the cart's customer (or guest group) must match the parent discount's `customer_groups` allow-list:

| Field | Backend key | Effect |
|-------|-------------|--------|
| **All groups** | `customer_groups_target = yes` | No group filtering. |
| **Specific groups** | `customer_groups_target = no` + `customer_groups[]` | Only carts whose customer is in one of the listed [[customers-custom-groups]] qualify. |

No match → no Countdown.

### Date range

| Field | Effect |
|-------|--------|
| `date_start` | Inclusive lower bound for eligibility. |
| `date_end` | Included, up to local midnight. Nullable → no expiration. |

Storefront cart-engine checks use store timezone for the eligibility window, so the customer-visible behaviour stops at the right local time. (The auto-disable sweep runs in UTC — see [[countdown-discount-single-instance]].)

### Per-session timer window

On top of the calendar window, each customer additionally gets their per-session `countdown_minutes` timer that starts the first time they see the popup at checkout. See [[countdown-discount-storefront-popup]] for the meta keys (`countdown_popup_first_showing`, `countdown_discount_popup_was_shown`).

## The validity check chain

On every cart-totals computation (cart view, checkout, order placement) the platform asks:

1. Is there an Active discount with `countdown_minutes` meta set? (Active = `active = yes`; deactivated Countdowns don't apply.)
2. Is `now` within `[date_start, date_end]`?
3. Does the customer's group match?
4. Is the products subtotal at or above `order_over` (if `order_over` is set)?
5. For flat type: is `type_value` ≤ the products subtotal? (See "Fixed amount larger than the subtotal" below.)
6. Take the first popup view from the cart (`countdown_popup_first_showing`), or now if there is none.
7. Is `now` within `countdown_minutes` of that time?

If all yes → the popup can fire. If any fail → the discount silently doesn't apply (no popup, no totals line).

The totals row has further conditions: the popup has been shown, and `only_customer` and `maxused_user` pass. A guest on an `only_customer` Countdown, or a customer at their limit, still gets the popup and their timer starts, but no discount row.

## Business rules

### Fixed amount larger than the subtotal (silent skip)

When the Countdown's inner type is `flat` AND `type_value > cart.subtotal`, the discount silently does NOT apply for that cart. The check compares the single amount, see [[countdown-discount-cart-totals]]. The customer sees no popup, no timer, no animation. The merchant might think the Countdown is broken — it's just that the cart is too small.

This is asymmetric to `percent` (which always produces a sensible amount because it scales with subtotal).

### Per-session deadlines, not a global clock

Two customers landing in checkout 30 minutes apart **each get the full `countdown_minutes` window** — see [[countdown-discount-storefront-popup]] for the per-cart meta that anchors this.

### The popup endpoint is the gate, not the validity check

Steps 1-7 of the validity check above run on every cart recompute, but the popup itself fires only once per cart (at the dedicated endpoint). A cart that becomes eligible later in the session (e.g., adds enough items to clear `order_over`) sees the popup on the next checkout visit, not on the cart view that crossed the threshold.

### Counted statuses for `max_uses` / `maxused_user`

The uses counter increments only on orders that reach the store's configured `discounts_used_statuses` — defaults to `paid`, `completed`, `fulfilled` — see [[settings-statuses]]. An order placed against the Countdown that is later cancelled before reaching a counted status does NOT consume a use.

### Eligibility is independent of plan caps

The plan check runs only when a Countdown is **created** — see [[countdown-discount-single-instance]]. Once created, the cart-time eligibility chain doesn't re-check the plan.

## Related

- [[marketing-discounts-countdown]] — hub.
- [[countdown-discount-editor]] — where the merchant configures target / dates / customer groups / `only_customer`.
- [[countdown-discount-storefront-popup]] — the popup endpoint that anchors the per-session timer.
- [[countdown-discount-cart-totals]] — what happens after eligibility passes.
- [[customers-custom-groups]] — the customer-group entity.
- [[settings-statuses]] — `discounts_used_statuses` setting.

## Open questions

None.
