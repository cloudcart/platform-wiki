---
type: feature
nav_path: "Orders → Order details → Payment → Refund → Provider matrix"
route_name: admin.orders.payment.refund
route_path: /admin/orders/action/payment/refund/:payment_id
aliases: ["Refund provider matrix", "Refund supported gateways", "Refund unsupported gateways", "Which providers support refund"]
tags: [orders, payment, refund, providers, gateway]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[orders-payment-refund]]. See the hub for the other aspects (visibility, gateway quirks, side effects, partial refunds, status-flip rules, API access).

# Payment refund — provider matrix

## Purpose

A per-provider catalogue of refund support: which payment gateways expose programmatic refund (Refund button visible), which don't, and which sit in a middle ground (provider-dependent, partial-only, or excluded from the regular flow). The merchant uses this matrix to decide whether to expect a one-click refund or to fall back to the gateway's own dashboard + [[orders-credit]].

## Where to find it

From [[orders-details]] → the Refund button is conditionally rendered based on the provider's refund capability. The capability is read-only per provider — see [[orders-payment-refund-visibility]] for the gating logic.

## What the merchant can do here

For each provider the merchant has configured on [[settings-payment-providers]], this page lets the merchant predict whether the Refund button will appear on a completed payment of that provider.

## Settings & fields

### Refund-supported providers (Refund button visible)

| Provider | Refund call | Notes |
|----------|-------------|-------|
| **Stripe** | Stripe Refunds API on original PaymentIntent (`pi_*`) or Charge (`ch_*`) ID. | Full charge only via this button; partial via gateway dashboard. Refund window typically ~180 days on Stripe's side. Appears on the customer's card statement within ~5-10 business days. |
| **CloudCart Pay** | Platform's own refund endpoint with PaymentIntent ID. | Full refund only. |
| **PayPal** | PayPal Refunds API. | Refund amount sent in the original transaction's currency; Sandbox vs Live based on configuration. |
| **Mollie** | Mollie refund API. | Full payment amount only. |
| **PayU** | PayU refund API. | Full payment amount only. |
| **Mokka** (BNPL) | Sends `return` if Mokka considers order `finished`; otherwise `cancel`. Always sends full `price_total_input`. | Has an "always throws error" quirk — see [[orders-payment-refund-gateway-quirks]]. |
| **Klear** (BNPL) | NOT an API call — sends an email to `the provider's support address` with merchant's public API key + order ID + amount. | Manual processing at Klear; see [[orders-payment-refund-gateway-quirks]]. |
| **Borica WAY4** | Borica's API with the order's reference. | Full amount only; uses the same idle-retry helper as capture/cancel — see [[orders-payment-refund-gateway-quirks]]. |
| **DSK Bank** | DSK gateway API. | Full amount only. |
| **Btepos** | Btepos API. | Full amount only. |
| **Monri** | Monri API with stored `order_number` + `currency`. | Full amount only; response logged to payment log. On `status=approved` the platform flips to Refunded. |
| **Raiffeisen** | Raiffeisen gateway API. | Full amount only. |
| **TBI Bank** | TBI API. | Full amount only. |
| **Fibank** | Fibank API. | Full amount only. |
| **iBank** | iBank (Simplify) API with original payment ID. | Full amount only; partial not exposed. |
| **CIB Bank** | CIB API with retransfer auto-fallback. | Full amount only. |
| **Icard** | Icard API. | Full amount only. |
| **EveryPay** | EveryPay API. | Full amount only. |
| **Settle** | Settle API. | Full amount only. |
| **Instamojo** | Instamojo API. | Full amount only. |
| **Catalyst Pay** | Catalyst Pay API. | Full amount only. |
| **MyPOS** | MyPOS API. | Full amount only. |
| **Braintree** | Braintree refund API. | Full amount only. |
| **Revolut** | Revolut API. | Full amount only. |
| **Nestpay** | Nestpay API. | Full amount only. |
| **Cardlink** | Cardlink API. | Full amount only. |

All of these implement a `refund` method in their gateway class. Most send the full charged amount; specific provider rules apply (refund window, currency, etc.).

### Refund-NOT-supported providers (Refund button hidden)

| Provider | Why no programmatic refund |
|----------|---------------------------|
| **Cash on Delivery** (cod) | No money moved through the platform — refund is offline (merchant returns the cash). |
| **Bank transfer manual** (bwt) | Refund is a separate bank-side action initiated by the merchant. |
| **EasyPay** (epay) | No programmatic refund flow available. |
| **Iute** (BNPL) | No programmatic refund flow available. |
| **FusionPay** | Excluded from the regular refund flow ("lease" exclusion). |
| **Paynetics** | Refund hook is a TODO stub — no automated refund surface. Refunds initiate from Paynetics's own merchant portal; the merchant may still mark the order as refunded via [[orders-payment-refund]]. |

For all of the above, the merchant handles the refund offline (returns the cash, initiates a bank transfer back, requests reversal in the provider's portal, etc.) and uses [[orders-credit]] to issue the credit note for tax compliance.

### Provider-dependent (case-by-case)

| Provider | Status |
|----------|--------|
| **Mokka / Iute / Klear** | Some BNPL providers don't support programmatic refund. Mokka and Klear are supported with quirks; Iute is not. |
| **Sofort** | Refunds typically handled at Klarna's portal, not via the Refund button. |

## Business rules

- **Refund-support is determined per gateway class** — no merchant-editable switch. To change which providers expose the Refund button, the platform code changes; the merchant cannot opt out per provider.
- **Unsupported-provider workflow** — the merchant refunds offline AND uses [[orders-credit]] to document for tax purposes; the credit note's "send" action notifies the customer.
- **Provider-specific refund windows** vary — Stripe ~180 days, others differ. The platform doesn't surface refund windows in the UI; if the gateway rejects, the merchant sees the gateway's error message.

## Related

- [[orders-payment-refund]] — hub.
- [[orders-payment-refund-visibility]] — provider-capability check (gate).
- [[orders-payment-refund-gateway-quirks]] — per-provider edge cases (Mokka, Klear, Stripe, Borica WAY4).
- [[settings-payment-providers]] — provider list + refund-support indicators.
- [[orders-credit]] — fallback flow for unsupported providers.

## Open questions

None.
