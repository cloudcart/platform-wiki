---
type: concept
nav_path: "Concept → Checkout flow → Order lifecycle overview"
aliases: ["Order initial state", "Positive lifecycle", "Negative branch", "Payment status shapes", "Direct charge", "Authorize-then-capture", "Manual offline", "authorized status", "order_complete setting"]
tags: [orders, checkout, lifecycle, status, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[checkout-flow]]. See the hub for the other aspects (cart entity, abandoned detection, submit-to-order, guest vs registered, discounts & rules, events & webhooks).

# Checkout flow — Order lifecycle overview

## Definition

This aspect documents the **initial post-creation state** of the order produced by [[checkout-flow-submit-order-creation]], and the high-level shape of what comes next: the positive flow (`pending → paid → completed`), the seven negative-branch statuses (`failed`, `cancelled`, `voided`, `timeouted`, `refunded`, `chargebacked`, `disputed`), and the three payment-status lifecycle shapes (direct charge / authorize-then-capture / manual offline). The detailed state-machine rules live in [[order-status-workflow]] + [[payment-status]] — this page is the checkout-flow-side **summary** of where the order goes once it leaves the checkout.

## Scope

Covered:

- The initial `status = pending`, `status_fulfillment = not_fulfilled` state.
- The positive flow + the `order_complete` setting that gates auto-promotion to `completed`.
- The `authorized` pre-auth state.
- The seven negative-branch statuses + their recovery patterns.
- The three payment-status lifecycle shapes (high-level — full enum in [[payment-status]]).

Not covered here:

- Per-status transition rules — see [[order-status-workflow]].
- Full `payment.status` enum (13 values) — see [[payment-status]].
- Manual status changes from the admin — see [[orders-status-change]].
- Side-effects fired at each transition — see [[checkout-flow-events-and-webhooks]] + [[order-processing-pipeline]].

## Contrasts

- **Order `status` vs payment `status`** — independent fields. An order can be `completed` while its payment is `refunded`. The order's status answers *"where is this order in the workflow?"*. The payment's status answers *"where is the money?"*.
- **`order_complete = 1` (auto) vs `0` (manual)** — when set to 1 (default), the order auto-promotes to `completed` the instant `status = paid` AND `status_fulfillment = fulfilled` (via the `saving` hook). When set to 0, the merchant must mark `completed` manually from [[orders-status-change]]. (verify default)
- **`failed` vs `cancelled` vs `voided` vs `timeouted`** — all "did not succeed" outcomes but with different causes: payment failed at gateway / customer abandoned at provider page / pre-auth cancelled before capture / provider didn't respond in time.
- **`refunded` vs `chargebacked` vs `disputed`** — all post-capture money-back states but bank-side vs merchant-side: refunded = merchant-initiated; chargebacked = bank-initiated against captured payment; disputed = pre-chargeback investigation.

## Where it applies

### Order initial state and positive lifecycle

A newly-created order is `status = pending`, `status_fulfillment = not_fulfilled`. The positive flow is:

```
pending → paid → (status_fulfillment: fulfilled by courier) → completed
                  ↘ (digital order, no fulfillment needed) → completed
```

The transition to `completed` is automatic when `status = paid` AND `status_fulfillment = fulfilled` AND the store setting `order_complete = 1` ([[settings-cart]]). With `order_complete = 0`, the merchant must mark the order `completed` manually.

For pre-auth payment providers, there's an additional `authorized` step before `paid` — the funds are reserved on the customer's card but not yet captured. The merchant captures via [[orders-payment-capture]] (auth → paid) or cancels the authorisation (auth → voided).

### Negative branch — what happens when things go wrong

The order can land in any of seven negative statuses, depending on what failed:

| Status | When | Recovery |
|--------|------|----------|
| `failed` | Payment failed at the gateway (declined, insufficient funds). | Merchant can retry via [[orders-payment-mark-paid]] / manual / capture flow. Customer-side retry is provider-dependent: many providers (Stripe, Borica, Adyen) display a *Try again* button on the failure page that re-initiates the same payment session; others (typically bank-redirect methods) require the customer to start a new checkout. CloudCart does not generate a universal retry URL — what the customer sees after `failed` is the provider's own UI. |
| `cancelled` | Customer abandoned at the provider page; merchant clicked cancel; banned-IP auto-cancel ([[settings-banned-ip]]); merchant cancelled via [[orders-status-change]]. | Returns stock if applicable — see [[inventory-restock]]. |
| `voided` | Pre-auth was cancelled before capture (merchant clicked *Cancel authorization*). | No money ever charged. |
| `timeouted` | Payment provider timed out without confirming. | Sync from provider may flip to `paid` or `failed`. |
| `refunded` | Money returned to customer via [[orders-payment-refund]]. | Issue a credit note ([[orders-credit]]) for accounting. |
| `chargebacked` | Bank-initiated chargeback against the captured payment. | Dispute via gateway tools; not editable from the admin. |
| `disputed` | Pre-chargeback dispute / investigation. | Awaiting resolution. |

Orders in `NEGATIVE_STATUS` are excluded from revenue analytics, do NOT count toward discount-usage counters (see [[discount-stacking]]), and do NOT count toward the free-plan `orders_amount` / `orders_revenue` quotas ([[plan-gates]]).

### The three payment-status lifecycle shapes

Independent of the order's `status`, the payment record's `payment.status` has 13 possible values that walk one of three lifecycle shapes — see [[payment-status]] for the full state breakdown:

- **Direct charge** (most card-on-file, redirect-then-capture providers): `initiated` → `requested` → `pending` → `completed`.
- **Authorize-then-capture** (pre-auth providers like Klarna, some Stripe flows): `initiated` → `requested` → `authorized` → `completed` (or → `voided`).
- **Manual / offline** (cash on delivery, bank transfer): `initiated` → `requested` → `pending` (merchant manually flips to `completed` via [[orders-payment-mark-paid]]).

The order's `status` typically tracks the payment's `status` (paid → paid, completed → completed) but they're separate fields — the merchant can mark an order `paid` even before the payment is actually captured at the gateway (via [[orders-payment-manual]]).

### Stock decrement runs on `authorized` orders under default config

The **Reduce items on Paid order** setting (`order_status_for_quantity_decrease = paid`, the default) actually decrements stock when an order reaches ANY of `paid`, `authorized`, OR `completed`. So pre-auth providers (Klarna, Stripe pre-auth, Borica Way4) that move orders straight to `authorized` reserve stock at the auth step, not just at the eventual capture. Merchants using these providers should treat *"auth received"* as *"stock gone"* for inventory-availability purposes. See [[inventory-decrement-timing]] for the full matrix.

## Related

- [[checkout-flow]] — hub.
- [[checkout-flow-submit-order-creation]] — what created the `pending` order this page picks up from.
- [[checkout-flow-events-and-webhooks]] — the side-effects fired at each status transition.
- [[order-status-workflow]] — the per-status state-machine details.
- [[payment-status]] — the full 13-value `payment.status` enum.
- [[order-processing-pipeline]] — the post-creation pipeline side-effects.
- [[inventory-decrement-timing]] — `authorized` + `paid` + `completed` decrement matrix.
- [[inventory-restock]] — re-credit on negative-branch transitions.
- [[discount-stacking]] — discount-usage counter rules across positive / negative statuses.
- [[settings-cart]] — `order_complete` setting.
- [[settings-banned-ip]] — banned-IP auto-cancel source.
- [[orders-status-change]] — manual status transitions.
- [[orders-payment-mark-paid]] / [[orders-payment-capture]] / [[orders-payment-refund]] / [[orders-payment-manual]] — payment actions that move orders along the lifecycle.
- [[orders-credit]] — credit note for `refunded` orders.
- [[plan-gates]] — `orders_amount` / `orders_revenue` quotas excluding negative statuses.

## Open Questions

- Confirm `order_complete` default value in the platform code / `settings` table (verify).
- Confirm which providers actually emit `authorized` vs going straight to `paid` (Klarna, Stripe pre-auth, Borica Way4 listed — others?) (verify).
