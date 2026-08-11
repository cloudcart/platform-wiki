---
type: feature
nav_path: "Payment Providers → Stripe → Checkout flow & 3DS"
route_name: apps.stripe.settings
route_path: /admin/payment-providers/stripe
aliases: ["Stripe checkout flow", "Stripe Checkout Session", "Stripe redirect", "Stripe 3D Secure", "Stripe currency", "Stripe locale", "Stripe payment intent", "Stripe first purchase"]
tags: [paymentproviders, payment-providers, stripe, checkout, 3ds, currency, locale]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-stripe]]. See the hub for related aspects (settings, save card, refunds/sync).

# Stripe — Checkout flow & 3DS

## Purpose

This aspect documents what happens on the wire when a customer pays with Stripe for the first time: the store creates a Stripe-hosted **Checkout Session**, the customer is redirected to Stripe's page, completes the card form and (if their bank requires it) 3D Secure, then returns to the store where the final status is pulled. It also covers currency handling and the localized Checkout page. The returning-customer fast path (off-session, no redirect) is on [[stripe-save-card]]; status reconciliation on return is on [[stripe-refunds-sync]].

## Where to find it

This aspect is invisible to the merchant — it's the runtime behaviour behind every order paid through Stripe. The customer experiences it as a redirect to Stripe and back. The merchant sees the result on the order in [[orders-details]].

## What the merchant can do here

- **Observe the customer's redirect to Stripe and back** — there is no merchant control over the hosted Checkout page beyond the storefront name and logo set on [[stripe-settings-fields]].
- **Set the amount range** that gates whether Stripe is offered at all — see [[stripe-settings-fields]].
- **Inspect the resulting payment** (reference IDs, status) on the order details page.

## Settings & fields

This aspect does not expose its own fields — the flow is the runtime behaviour determined by the keys and mode on [[stripe-settings-fields]]. 3D Secure is not configurable; the Save-Card branch that bypasses this redirect is documented on [[stripe-save-card]].

## Business rules

### First-purchase customer flow

1. Customer picks Stripe at checkout. CloudCart creates a `Payment` row and calls Stripe's `checkout.sessions.create` API.
2. The request includes: amount in minor units (cents), currency from the payment, customer email, the order ID as `client_reference_id`, locale (if Stripe supports it), success + cancel URLs (both point back to CloudCart's payment-return route), and a single line item named "Order #{id} | {host}".
3. Stripe returns a Checkout Session with `id` (`cs_...`) and a `payment_intent` (`pi_...`). CloudCart stores the payment-intent ID as `provider_reference_id`. Payment status → `requested`.
4. The customer's browser renders an HTML form that auto-submits, redirecting to the Stripe-hosted Checkout page.
5. On Stripe: the customer enters their card and completes 3D Secure if required by their bank.
6. Stripe redirects back to CloudCart's `payments.return` route, where CloudCart calls `sync` to fetch the final status from Stripe — see [[stripe-refunds-sync]].

### Currency

The payment is created in the **customer's payment currency** (the `Payment.currency` value, i.e. the store's currency at checkout time). Stripe supports 135+ currencies in Stripe Checkout — see Stripe docs for the current list. The amount is sent as an integer in the currency's minor unit (cents for USD/EUR, no minor unit for JPY, etc.).

The integration does **not** restrict currencies at the code level — CloudCart sends whatever currency the order is in, and Stripe rejects unsupported currencies at request time. The list a merchant can actually settle in depends on their Stripe account and country.

### 3D Secure

Handled transparently by Stripe. Stripe Checkout (the hosted page) prompts the customer for 3DS when the card issuer requires it; the merchant cannot configure or disable it. For off-session charges with saved cards, 3DS can fail — that case is handled on [[stripe-save-card]].

### Locale

The Stripe Checkout page is localized to the storefront language if Stripe supports it. Current supported list: `bg, cs, da, de, el, en, en-GB, es, es-419, et, fi, fr, fr-CA, hu, id, it, ja, lt, lv, ms, mt, nb, nl, pl, pt, pt-BR, ro, ru, sk, sl, sv, tr, zh, zh-HK, zh-TW`. Other languages fall through to Stripe's auto-detected locale.

### Mode is one-off, not subscription

The Checkout Session is created in `mode: payment` (one-off charge), never `mode: subscription`. There is no scheduled-billing integration at this layer — the one-click repeat-purchase capability comes from saved cards, not Stripe Subscriptions. See [[stripe-refunds-sync]] for the recurring-billing limits and [[stripe-save-card]] for the repeat-purchase fast path.

## How it works (verified against backend)

- **Session creation** calls `checkout.sessions.create`. The line item is a single synthetic entry named `Order #{id} | {host}` — Stripe does not see the individual cart products.
- **`client_reference_id`** carries the CloudCart order ID so the session can be tied back to the order.
- **`provider_reference_id`** on the CloudCart payment is set to the `payment_intent` (`pi_...`) returned with the session; this is the handle used later by `sync` and refunds.
- **Auto-submitting redirect form** — the customer's browser receives a tiny HTML page (template `Stripe.views.checkout3`) that submits itself to the Stripe Checkout URL.
- Every Stripe API call (request + response) is logged to `PaymentLogs` for traceability.

## Related

- [[payment-providers-stripe]] — hub.
- [[stripe-save-card]] — the returning-customer off-session charge that skips this redirect.
- [[stripe-refunds-sync]] — how the final status is pulled when the customer returns; refunds.
- [[stripe-settings-fields]] — storefront name/logo, amount range and keys that drive this flow.
- [[payment-status]] — the requested / completed / cancelled values this flow produces.
- [[orders-details]] — where the resulting payment is surfaced in the admin.
- [[checkout-flow]] — storefront checkout, where the Stripe option triggers this flow.

## Open questions

(none)
