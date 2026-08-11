---
type: entity
aliases: ["Payment status provider mappings", "Gateway status mapping", "Refund button visibility", "Cancelled vs voided", "Disputed and chargebacked", "Съответствие на платежни статуси по доставчик"]
tags: [orders, payments, payment-providers, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[payment-status]]. See the hub for the other aspects (values, lifecycle, vs order status).

# Payment Status — provider mappings & gating

## Identity

Each [[payment-provider]] speaks its own language of response codes and webhook events; every integration page translates those into the platform's 13-value payment-status enum (see [[payment-status-values]]). This page collects the **provider-mapping behaviour** plus the merchant-visible rules that depend on it: which action buttons show at which status, how the ambiguous final-negative states (`cancelled` vs `voided`, `disputed`, `chargebacked`) are reached and resolved, multi-currency handling, and the multiple-payment-record-per-order rule.

## Aliases

- "Gateway status mapping" — how a provider's codes become a payment status.
- "Refund button visibility" — the gating rule merchants ask about most.
- "Cancelled vs voided" — the two final-negative states.
- Bulgarian: "Съответствие на платежни статуси по доставчик".

## Key Attributes

### Refund button visibility — only on `completed`

The **Refund payment** action on [[orders-details]] is visible only when the payment status is `completed`. For `authorized` payments, the buttons shown are instead **Capture authorization** and **Cancel authorization** — different lifecycle, different action (see [[orders-payment-capture]]). For `refunded`, `failed`, `cancelled`, `voided`, no refund/capture button appears.

### Provider-specific mappings — every provider translates its own codes

Each [[payment-provider]] has its own response codes and webhook events; each integration page documents its provider-specific mapping. Examples:

- **Stripe**: `succeeded` → `completed`; `requires_action` / failure → `cancelled` / `failed`. Pull-based sync. See [[payment-providers-stripe]].
- **Cardlink**: `isSuccessful = true` → `completed`; `isCancelled = true` → `cancelled`; otherwise `failed`. See [[payment-providers-cardlink]].
- **CloudCart Pay**: native event stream — `payment.completed`, `payment.refunded`, etc. See [[payment-providers-cloudcart-pay]].
- **COD** (Cash on Delivery): always starts `pending`; merchant flips to `completed` manually. See [[payment-providers-cod]] (or the cash-on-delivery option in [[settings-payment-providers]]).
- **BNPL providers** (Mokka, Klarna): use the `authorized` flow with a dedicated provider-confirm step. See [[payment-providers-mokka]].
- **Bank-redirect providers** (Borica, DSK, ProCredit, Fibank): redirect-then-sync. See provider-specific pages.

41 payment-provider wiki pages exist, each with a "Status mapping" section. When the AI Assistant fields a "why is my payment showing X?" question, it should cross-reference the provider's mapping page.

### `disputed` lifecycle — manual reconciliation only

There is **no automatic resolution** of `disputed` in code. It's purely a marker the gateway can set (typically via Revolut / PayPal dispute events). The merchant must manually move the payment to its final state — `refunded`, `chargebacked`, or back to `completed` if the dispute resolves in the merchant's favour — usually by reconciliation with the gateway's portal.

### `chargebacked` lifecycle — no automatic stock reversal

The platform does **NOT** automatically reverse stock or fire customer notifications when a payment is set to `chargebacked`. It's a marker that records the bank's action. To reverse stock / record the loss, the merchant must also move the **Order** status to `cancelled` or `refunded` — see [[payment-status-vs-order-status]] for the cascade rules.

### `cancelled` vs `voided` canonical semantics

- **`cancelled`** = customer-side abort OR merchant cancellation of a still-`pending` / `requested` payment (no funds were ever held).
- **`voided`** = explicit cancellation of an already-`authorized` hold (funds were reserved, now released).

Provider mappings sometimes blur the two; the platform treats both as final-negative states (both shown in red, both kept out of revenue).

### Multi-currency mismatch

The platform stores the Order's amount in the Order's currency and uses that for `amount` on the payment record. The gateway is expected to charge in the same currency — there is no in-platform reconciliation step. If the gateway returns a different currency, the status still flips on the gateway's response code, but the merchant sees the gateway's amount in their portal; the Order's record retains the original currency.

### Multiple payment records per order

An order can have **multiple payment records** — failed first attempts, manual top-ups, partial refunds, etc. The order details UI surfaces the **most recent** payment as the headline status, but all of them are kept for audit and visible on the payment row. Sum-of-completed-payments must equal the order total for the order to be considered fully paid.

## Where it appears

- [[orders-details]] — the payment row renders the conditional buttons (Refund / Capture / Cancel authorization / Sync / Manual) based on the current status.
- [[settings-payment-providers]] — where the merchant installs / configures the gateways whose mappings this page describes.
- Every `payment-providers-*` page — carries the provider's own "Status mapping" section.
- [[analytics-full]] — aggregates payments by provider + status for reporting.

## Related

- [[payment-status]] — hub.
- [[payment-status-values]] — the 13 target enum values these mappings resolve to.
- [[payment-status-vs-order-status]] — why `chargebacked` needs a manual ORDER-status move to cascade.
- [[payment-provider]] — the gateway entity that owns the native codes.
- [[settings-payment-providers]] — install / configure gateways.
- [[payment-providers-stripe]] / [[payment-providers-cardlink]] / [[payment-providers-cloudcart-pay]] / [[payment-providers-cod]] / [[payment-providers-mokka]] — example provider mapping pages.
- [[orders-payment-capture]] — the Capture / Cancel authorization buttons shown for `authorized`.
- [[orders-payment-refund]] — the Refund button shown only for `completed`.
- [[analytics-full]] — aggregates by provider + status.

## Open Questions

No outstanding questions.
