---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Transactions → Status & amount"
route_name: apps.cloudcart_pay.transactions
route_path: /admin/payment-providers/cloudcart_pay/transactions
aliases: ["CloudCart Pay transactions status pill", "Refund detection client-side", "partially_refunded transactions", "Transactions amount formatting", "Minor unit scale formatting", "Status pill colours"]
tags: [paymentproviders, payment-providers, cloudcart-pay, transactions, payments, refunds]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay-transactions]]. See the hub for the other aspects (list & filters UI, live read + scoping).

# Transactions — status & amount

## Purpose

Two columns on the Transactions list carry display logic that surprises merchants if taken literally: the **Status** pill and the **Amount**. This aspect documents both. The Status pill is **derived client-side** — Paypercut never changes a payment's `status` when a refund happens, so the page infers `refunded` / `partially_refunded` from the refund amount. The Amount is reconstructed from a minor-unit integer plus a currency `scale`, so `1995` becomes `€19.95`. This is the page to cite for "why does this still say succeeded after I refunded it?" and "why is the amount 100× too big?".

## Where to find it

Payment Providers → CloudCart Pay → **Transactions** tab — the **Status** and **Amount** columns of the [[cloudcart-pay-transactions-list-filters|transactions table]], and the **Captured / Refunded / Fee** fields of the expanded row.

The route is `/admin/payment-providers/cloudcart_pay/transactions`.

## What the merchant can do here

- **Read the status pill** — a colour-coded, human-readable status that reflects refunds even when the underlying payment is still `succeeded` upstream.
- **Read formatted amounts** — Amount, Captured, Refunded, and Fee, each rendered in the transaction's own currency.
- These are read-only display fields; there are no editable controls on this aspect.

## Settings & fields

| Field | What it shows | Derivation |
|-------|---------------|------------|
| **Status** pill | Human-readable status (`succeeded`, `pending`, `failed`, `refunded`, `partially_refunded`, …). | Derived client-side from `tx.status` + refund amount — see Business rules. |
| **Amount** | The payment total in transaction currency. | `formatted_amount` if present; otherwise minor-unit integer ÷ `10^scale`, run through `Intl.NumberFormat`. |
| **Captured / Refunded / Fee** | `amount_captured`, `amount_refunded`, `tx.fee` in transaction currency. | Same minor-unit + scale formatting as Amount. |

## Business rules

### Refund detection is client-side

Paypercut's `status` enum is only `failed | pending | succeeded` — **a refund never changes `status`** on the underlying payment intent; it adds an `amount_refunded` and a refund operation marker. To surface refunds, the page derives the displayed status from the refund amount:

```
amount, refunded = numeric tx.amount, tx.amount_refunded
if tx.refunded OR (amount > 0 AND refunded >= amount) → "refunded"
else if refunded > 0 → "partially_refunded"
else → tx.status (or "-")
```

This is the single source of truth for the `refunded` / `partially_refunded` pills in the Status column. It is also why the Status **filter** maps `refunded` to the upstream `operation=refund` rather than a `status` value (see [[cloudcart-pay-transactions-live-read]]). The practical consequence for support: a fully refunded payment is genuinely still `succeeded` at the payment-processor level — the refund is a separate operation against it — so the "refunded" label here is CloudCart's interpretation, not a Paypercut status.

### Status pill colours

The status badge uses the same pill design system as the account billing list:

| Status | Colour intent |
|--------|---------------|
| `succeeded`, `completed`, `captured`, `paid` | Green (success). |
| `processing`, `requires_action`, `pending` | Amber (in-progress). |
| `failed` | Red. |
| `canceled`, `cancelled`, `expired` | Grey. |
| `refunded`, `partially_refunded`, `disputed` | Blue. |
| (anything else) | Neutral default. |

### Amount formatting reads Paypercut's minor-unit + scale

Paypercut returns amounts as integers in the currency's smallest unit, plus a `scale` field on the currency object (e.g., `EUR` returns `scale=2`, so an amount of `1995` is €19.95). The page divides by `10^scale` and runs the result through `Intl.NumberFormat` with `style=currency`. If `Intl` cannot format the currency (browser fallback), the value is formatted as `value.toFixed(scale) + " " + code` manually. The Paypercut-pre-formatted `formatted_amount` field is **preferred when present**. The same rule applies to the Captured, Refunded, and Fee fields in the expanded row.

### Permission

The page is under `hasApiPermission:settings,store.payment_providers`. A staff member without that grant cannot reach the page or its API endpoint.

## Related

- [[payment-providers-cloudcart-pay-transactions]] — hub.
- [[orders-payment-refund]] — the refund flow that produces the `amount_refunded` this derivation reads.
- [[orders-payment-capture]] — automatic-capture context for the `amount_captured` field.
- [[payment-status]] — platform-level payment status mapping (distinct from this client-side derivation).

## Open questions

_None._
