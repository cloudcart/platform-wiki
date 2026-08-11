---
type: feature
nav_path: "Orders → Order details → Payment → Refund"
route_name: admin.orders.payment.refund
route_path: /admin/orders/action/payment/refund/:payment_id
aliases: ["Refund order", "Refund payment", "Issue refund", "Order refund", "Възстановяване на плащане", "Реверсиране"]
tags: [orders, payment, refund, gateway, smarty]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 14
---

# Payment refund

## Purpose

The **Refund payment** action reverses a completed payment through the payment provider's own API. The merchant clicks the red **Refund payment** button on the order details page; the platform calls the configured payment gateway (Stripe / CloudCart Pay / PayPal / Mokka / Klear / Borica WAY4 / etc.) with the refund request. On success, the customer is credited at the gateway, the local payment record flips to `refunded`, the order may auto-flip to `refunded`, stock is auto-restored, and an entry lands in [[orders-history]].

This is the canonical way to reverse a **charged** payment. It is NOT the same as cancelling an order (cancellation might occur without any money having moved — e.g., a Cash-on-Delivery order). Authorized-but-not-captured payments use Cancel Authorization instead — see [[orders-payment-capture]].

This page is the **hub** for the refund flow. Each provider's exact wire-call, each side-effect, and each business rule lives on a dedicated aspect page below — the Assistant should drill into the aspect that matches the merchant's question.

## Sub-pages (in this cluster)

The refund flow is split into 7 aspect pages. Drill into the one that matches the question.

- [[orders-payment-refund-visibility]] — when the **Refund payment** button appears (payment status, provider capability, `orders.refund` permission grant); two surfaces (primary red button + cog-dropdown); terminal-state hiding.
- [[orders-payment-refund-provider-matrix]] — provider-by-provider matrix of refund support (Stripe / CloudCart Pay / PayPal / Mollie / PayU / Borica WAY4 / DSK Bank / iBank / Monri / CIB Bank / Mokka / Klear / etc. supported; COD / bwt / EasyPay / Iute / FusionPay unsupported).
- [[orders-payment-refund-gateway-quirks]] — per-provider quirks: Mokka's always-throws-error pattern, Klear's email-to-staff manual flow, Stripe's `pi_*` vs `ch_*` handling, Borica WAY4's idle-retry helper, network-failure 504 + log entry, no auto-retry.
- [[orders-payment-refund-side-effects]] — what fires when a refund succeeds: payment flips to `refunded`, stock auto-restore via PaymentSync, customer income aggregate decrement, `order.updated` webhook, history action 20, NO customer email by default.
- [[orders-payment-refund-partial-refunds]] — full-amount only via this UI; gateway-dashboard partial path; action 21 (`order_payment_partially_refunded`) is webhook-driven; manual reconciliation guidance.
- [[orders-payment-refund-status-flip-rules]] — order auto-flips to `refunded` only when no other completed / authorized / pending payments remain; manual status override (via [[orders-status-change]]) blocks auto-flip; multi-payment / split-deposit orders need each payment refunded individually.
- [[orders-payment-refund-api-access]] — JSON-API v2 is read-only for payments; no mutate endpoint exposes refund; chargebacks (action 44) are gateway-initiated via webhook, NOT the Refund button.

## Where to find it

From [[orders-details]] → in the **Payment action row** under the order summary, when the payment is in `completed` state, the provider supports programmatic refunds, and the staff member has the `orders.refund` grant.

Route: `/admin/orders/action/payment/refund/{payment_id}` (GET — the action runs on click). The button appears in **two surfaces**: a primary red **Refund payment** button (`payment/action.tpl`) and a cog-dropdown secondary action (`payment/details_action.tpl`) next to the payment status badge. Both call the same route. The cog dropdown also lists **Sync payment** for gateways that support it. See [[orders-payment-refund-visibility]] for the full visibility matrix.

## What the merchant can do here

### Click Refund payment

A browser-style confirmation dialog appears (*"Refund payment?"* — translation key `order.payment.confirm.refund`). On accept, the platform looks up the payment, resolves the gateway by `provider`, calls the gateway's refund API with the full payment amount, and reports back to the merchant via toast — *"Refund successful"* or the gateway's error message.

For per-provider behaviour, see [[orders-payment-refund-provider-matrix]] and [[orders-payment-refund-gateway-quirks]].

### What the merchant CANNOT do here

- Specify a partial refund amount via this UI — the button always sends the **full payment amount**. For partial refunds, see [[orders-payment-refund-partial-refunds]].
- Refund a non-completed payment — the button is hidden for Pending / Failed / Authorized states. Authorized payments use Cancel Authorization (see [[orders-payment-capture]]).
- Refund a payment from an unsupported provider (Cash on Delivery, manual bank transfer, EasyPay, Iute, FusionPay). The merchant records the refund offline and uses [[orders-credit]] to issue a credit note for tax compliance.
- Refund without the `orders.refund` permission grant (see [[settings-staff]]).
- Bulk-refund multiple orders — refund is strictly per-order. Batch refunds (e.g., a product recall) must process each order individually.

## Settings & fields

This page documents an **action**, not a configuration form — there are no merchant-editable fields. The relevant configuration lives elsewhere:

- **Refund-support flag per provider** — read-only; set internally by each gateway's class. See [[orders-payment-refund-provider-matrix]].
- **Permission grant** — `orders.refund` on [[settings-staff]]. Defense-in-depth alongside the general `orders` grant.
- **Stock auto-restore behaviour** — not gated by `settings-cart` flags; the platform always restores stock on refund via the PaymentSync event listener. See [[orders-payment-refund-side-effects]].
- **Customer email on refund** — currently disabled in this flow. To notify the customer, the merchant issues + sends a credit note via [[orders-credit]].

## Business rules

The full business-rule set is distributed across the aspect pages. The cross-cutting rules in one place:

- **Full payment amount only** from this UI — see [[orders-payment-refund-partial-refunds]].
- **`orders.refund` permission** is required at BOTH button-render and route-handler — direct URL access is also denied without the grant.
- **No customer email** is sent by the refund flow itself. The credit-note flow ([[orders-credit]]) has its own email action.
- **Stock is auto-restored** regardless of `settings-cart` stock-restore flags — always on. See [[orders-payment-refund-side-effects]].
- **Order auto-flips to `refunded`** only when no other completed / authorized / pending payments exist on the order. Multi-payment orders need each refunded. See [[orders-payment-refund-status-flip-rules]].
- **Manual status override blocks auto-flip** — if the merchant manually changed the order's status via [[orders-status-change]], the auto-recalc is skipped.
- **Refund is irrevocable on the gateway side** — once Stripe / PayPal / etc. accept the refund, the merchant cannot recall it from CloudCart.
- **Chargebacks are separate** — gateway-initiated via webhook (action 44 `chargebacked`), NOT triggered by this button. See [[orders-payment-refund-api-access]].

## Related

- [[orders-details]] — parent page (button lives in the payment action row).
- [[orders-payment-capture]] — Authorize-related flows (for orders in Authorized status).
- [[orders-payment-mark-paid]] — for offline payments without programmatic refund support.
- [[orders-credit]] — credit note flow (typically issued alongside / after a refund for tax compliance).
- [[orders-invoice]] — original invoice that the refund / credit note references.
- [[orders-history]] — refund actions land here (action codes 20, 21, 43, 44).
- [[orders-status-change]] — manual status override (blocks the refund-driven auto-flip).
- [[settings-payment-providers]] — payment provider list + refund-support indicators.
- [[settings-staff]] — `orders.refund` permission grant.
- [[settings-cart]] — stock auto-restore on refund.
- [[settings-hooks]] — `order.updated` webhook on refund.
- [[api-order-payment]] — read-only JSON-API v2 resource.
- [[json-api-v2]] — API overview.
- [[orders]] — parent list (refunded orders appear with Refunded status badge).
- [[order-processing-pipeline]] — refund triggers the negative-status side-effects (stock restock, auth cancel, discount counter decrement).

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
