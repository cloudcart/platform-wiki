---
type: feature
nav_path: "Payment Providers → PayPal → Payment flow"
route_name: apps.paypal.settings
route_path: /admin/payment-providers/paypal
aliases: ["PayPal payment flow", "PayPal checkout flow", "PayPal redirect", "PayPal refund", "PayPal sync", "PayPal capture", "PayPal 3D Secure", "PayPal Pay Later"]
tags: [paymentproviders, payment-providers, paypal, checkout, refund, redirect]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-paypal]]. See the hub for the other aspects (setup & fields, currency handling).

# PayPal — payment flow

## Purpose

This aspect covers what happens at runtime once a customer picks PayPal: the redirect-and-return checkout sequence, how the transaction is captured, how the merchant issues refunds and runs a status Sync, and which PayPal capabilities are (and are not) wired into CloudCart's integration — 3D Secure, recurring billing, saved cards, Pay Later, and the iframe path.

## Where to find it

The flow is driven from the storefront checkout and the order's payment record; there is no separate admin screen beyond the provider settings at `/admin/payment-providers/paypal`. Refund and Sync controls appear on the order's payment row — see [[orders-payment-refund]].

## What the merchant can do here

- Receive payments via the redirect-and-return PayPal flow (no merchant action needed once active).
- Issue a **full refund** from the order's payment row.
- Run a **Sync** to pull the latest transaction status from PayPal.

## Settings & fields

This aspect has no dedicated configuration fields — runtime behaviour is fixed by the integration. The provider-level fields (email, mode, fallback currency) live on [[paypal-setup-and-fields]]. The runtime behaviours below are not merchant-configurable.

## Business rules

### Customer flow at checkout

1. Customer picks PayPal at checkout. CloudCart creates a `Payment` row.
2. CloudCart calls PayPal REST API (`/v1/payments/payment`) with: currency (store currency or fallback), order line with name "Order #{id} | {host}", price total, return URL, cancel URL, payee email, and the referrer code `CloudCart_SP_PayPal_BT`.
3. PayPal returns an approval URL. CloudCart stores the transaction reference on `Payment.provider_reference_id`. Payment status → `requested`.
4. Customer is redirected to PayPal (full-page redirect).
5. On PayPal: customer logs in or pays as guest with a card.
6. PayPal redirects to CloudCart's `site.payment.return` route, passing `PayerID` in the query string.
7. CloudCart calls PayPal's "execute payment" endpoint (`completePurchase`) with the `PayerID` to finalize the transaction.
8. Status is set from PayPal's transaction state.

### Referrer code

Every API call includes `CloudCart_SP_PayPal_BT` as the referrer (PayPal's partner-attribution code). This identifies CloudCart as the platform initiating the API call — used by PayPal for partner reporting.

### 3D Secure

Handled by PayPal (when paying with a card through PayPal's guest-card flow). For PayPal-wallet payments (account login), 3DS is not used — the wallet itself acts as authentication.

### Capture mode

Auto-capture (default). The integration uses PayPal's standard payment flow (`mode: payment`), not the authorize-then-capture flow. Funds are captured immediately on successful payment.

### Refunds

Supported. Clicking Refund triggers `refund` which calls PayPal's refund endpoint with the saved transaction reference. The refund amount is read from the original transaction's currency + total (preserving the actual charged amount in case of currency conversion — see [[paypal-currency-handling]]). Full refund only — partial-refund control is not exposed in the UI.

### Sync — pull-based status check

When the merchant clicks Sync on a payment (or the platform polls), CloudCart fetches the transaction state from PayPal:

- If `provider_reference_id` starts with `PAY` → call `fetchPurchase`.
- Otherwise → call `fetchTransaction`.

The status returned by PayPal (`approved`, `failed`, etc.) is mapped to CloudCart's `Payments` statuses.

### Recurring / subscriptions

Not implemented at this layer. PayPal supports recurring billing through `BillingAgreements`, but CloudCart's PayPal integration is one-off purchase only. For recurring needs, the store would need a different setup.

### Saved cards

Not supported for PayPal in this integration. PayPal handles wallet-level recognition itself — returning customers see their saved PayPal account on the PayPal side, but CloudCart doesn't store any payment-method tokens locally for PayPal.

### PayPal Pay Later / PayPal Credit (BNPL)

Not surfaced through this integration. The standard CloudCart PayPal flow uses PayPal's classic Express Checkout (`mode: payment`), which does not include the Pay Later branding. PayPal merchants who want Pay Later must configure it on the PayPal side — it may then appear automatically on PayPal's hosted page for eligible customers, which is a PayPal-side render decision, not a CloudCart one.

### iframe mode

The configuration loader reads `enable_iframe` from settings, but the standard flow is a full-page redirect. iframe-mode is legacy / inactive; redirect is the supported pattern. The dead-field detail is documented on [[paypal-setup-and-fields]].

### Mid-transaction PayPal email change

Changing the merchant's PayPal email on the settings tab does NOT break in-flight payments. The integration's purchase / sync / refund calls all use the **saved `provider_reference_id`** (the original PayPal payment / transaction ID), not the merchant's current email. The new email only affects payments that haven't been initiated yet.

## Related

- [[payment-providers-paypal]] — hub.
- [[payment-providers]] — parent hub.
- [[orders-payment-refund]] — how to issue refunds from the order.
- [[payment-providers-stripe]] — alternative international card gateway.

## Open questions

(none)
