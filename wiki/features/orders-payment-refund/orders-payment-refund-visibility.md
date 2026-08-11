---
type: feature
nav_path: "Orders → Order details → Payment → Refund → Visibility"
route_name: admin.orders.payment.refund
route_path: /admin/orders/action/payment/refund/:payment_id
aliases: ["Refund button visibility", "When refund appears", "Refund permission gate", "Refund button surfaces"]
tags: [orders, payment, refund, permissions, smarty]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[orders-payment-refund]]. See the hub for the other aspects (provider matrix, gateway quirks, side effects, partial refunds, status-flip rules, API access).

# Payment refund — button visibility

## Purpose

Defines **when** the **Refund payment** button is rendered on the order details page and **where** it appears. Three independent conditions gate visibility; failing any one hides the button. The gate is enforced at both the Smarty template render AND the route handler — direct URL access without permission is denied.

## Where to find it

From [[orders-details]] → **Payment action row** (under the order summary). When visible, the button appears in **two surfaces** on the same page:

1. **Primary action row** — large red **Refund payment** button under the payment row, rendered from the `payment/action.tpl` template.
2. **Cog-dropdown secondary action** — a small settings icon (`<i class="fal fa-cog">`) next to the payment status badge, rendered from `payment/details_action.tpl`. Opens a menu containing a **Refund payment** item with a red undo icon (`fa fa-undo notification-red`). For gateways that also support `sync`, the same dropdown lists a **Sync payment** entry alongside Refund.

Both surfaces call the same route: `/admin/orders/action/payment/refund/{payment_id}` (GET — the action runs on click).

## What the merchant can do here

This page documents the **visibility logic**, not actions. The merchant interacts with the button per the hub page; this page explains why the button is or isn't present.

## Settings & fields

### Visibility conditions (all three must be true)

| Condition | What it checks | If false |
|-----------|---------------|----------|
| Payment status is `completed` | The customer has actually paid (not Authorized, not Pending, not Failed). | Button hidden. Authorized payments use Cancel Authorization instead — see [[orders-payment-capture]]. |
| Provider supports programmatic refunds | The payment gateway's class reports refund capability. | Button hidden. See [[orders-payment-refund-provider-matrix]] for the supported / unsupported provider list. |
| Staff has `orders.refund` grant | Both `orders` (general orders access) AND `orders.refund` (specific) on [[settings-staff]]. | Button hidden. Direct URL access also returns access-denied at the route handler. |

### Terminal-state hiding

The Refund button only appears when the payment status is `completed`. Once the merchant has clicked Refund and the payment is now `refunded` / `cancelled` / `voided`, the button is **gone**. The platform does NOT allow a "second refund" attempt via this UI surface — for any further partial-refund-then-additional-refund flow, the merchant uses the provider's dashboard (and the resulting state syncs back via webhook; see [[orders-payment-refund-partial-refunds]]).

## Business rules

### Permission gate — defense in depth

Both surfaces (primary button + cog dropdown) AND the route handler check the platform code. So:

- A staff member with `orders` alone can SEE the order details page but the Refund button is hidden.
- The route URL is protected — typing it into the browser returns access-denied.
- A merchant who wants to restrict who can issue refunds removes the `orders.refund` grant from less-trusted staff; financially impactful actions stay with senior operators.

### Provider capability is read-only

The "does this provider support refunds?" check is set internally by each gateway integration — there is no merchant-editable switch. Whether the Refund button appears for a Borica WAY4 vs an EasyPay payment is fixed by the platform code, not by a setting. See [[orders-payment-refund-provider-matrix]] for the matrix.

### Cog dropdown also lists Sync payment

For gateways that implement `sync` (most BNPL + bank gateways), the cog dropdown lists **Sync payment** **alongside** **Refund payment** when the payment is in `completed` state. The merchant can choose either action from the same menu — Sync re-fetches the payment's current state from the gateway; Refund initiates a reversal.

### Confirmation dialog

Clicking the button (either surface) triggers a browser-style confirmation (`data-confirm`) with the translated message *"Refund payment?"* (`order.payment.confirm.refund`). Only on Accept does the AJAX call fire — `modal: false` in the action config, so there is no platform modal layered on top of the browser confirm.

### Smarty + jQuery + AJAX

- Button uses the `js-payment-action` class.
- Click handler: AJAX call to the refund URL.
- Success / error toast via the platform's standard `toastr` library.

## Related

- [[orders-payment-refund]] — hub.
- [[orders-payment-refund-provider-matrix]] — which providers expose the button.
- [[orders-details]] — parent page where the button lives.
- [[orders-payment-capture]] — Cancel Authorization (alternate flow for Authorized payments).
- [[settings-staff]] — `orders.refund` permission grant.
- [[settings-payment-providers]] — provider list with refund-support indicators.

## Open questions

None.
