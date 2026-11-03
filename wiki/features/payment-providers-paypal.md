---
type: feature
nav_path: "Payment Providers → PayPal"
route_name: apps.paypal.settings
route_path: /admin/payment-providers/paypal
aliases: ["PayPal", "Paypal", "PayPal wallet", "PayPal Express"]
tags: [paymentproviders, payment-providers, paypal, international, wallet, card-gateway]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# PayPal

## Purpose

PayPal is a global wallet + card-payment gateway. Customers redirect to PayPal, log in with their PayPal account (or enter a card via PayPal's guest-card form), and approve the payment. PayPal then redirects back to CloudCart with the result.

This is the most-recognized payment method internationally — particularly strong in the US, UK, Western Europe, and many Asian markets. CloudCart's integration uses the **PayPal REST API** with the merchant's PayPal email as the payee, and pre-configured CloudCart application credentials baked into the platform — the merchant only needs to supply their receiving email and a fallback currency.

This hub is split into 3 aspect pages because the topic spans configuration, runtime flow, and currency bridging — each is a distinct concern the Assistant should be able to reach without reading the others.

## Sub-pages (in this cluster)

- [[paypal-setup-and-fields]] — the config screen: email, test/live mode switch, fallback currency, common storefront options, per-field validation, plan-gating, permission, and the settings-UI deep audit.
- [[paypal-payment-flow]] — the redirect-and-return checkout sequence, capture mode, refunds, Sync, and which PayPal capabilities (3DS, recurring, saved cards, Pay Later, iframe) are or aren't wired in.
- [[paypal-currency-handling]] — fallback-currency mechanics, conversion at checkout, the BGN/RON/HRK unsupported-currency case, and account-country edge cases.

## Where to find it

Payment Providers → **PayPal**. The configuration screen URL is `/admin/payment-providers/paypal` (route `apps.paypal.settings`). It renders the PayPal-specific edit form as a Vue SPA. Field-level detail is on [[paypal-setup-and-fields]].

## What the merchant can do here

- Toggle the provider **Active** and switch between **Test mode** (sandbox) and **Live mode**.
- Enter the **PayPal account email** (where funds land) and pick a **Fallback currency**.
- Configure storefront name, logo, accepted-amount range, and an optional PayPal-payment discount.
- Receive payments via the redirect flow, issue **full refunds**, and **Sync** transaction status — see [[paypal-payment-flow]].

## Settings & fields

The PayPal settings screen has two PayPal-specific fields — the **Email** (`required|email`) and the **Fallback currency** select — plus the common storefront-name / logo / amount-range / discount options shared with other providers. The **Test mode** switch has inverted semantics versus most providers (default is Live). Full field table, defaults, validation messages, and the settings-UI layout are documented on [[paypal-setup-and-fields]]. The 24 supported currencies and the BGN/RON/HRK gap are on [[paypal-currency-handling]].

## Business rules

- **No plan-gate** — PayPal is available on every plan. Settings permission: `hasApiPermission:settings,store.payment_providers`.
- **CloudCart owns the app credentials** — the merchant needs only a PayPal Business account with the matching email; no PayPal Developer app registration. See [[paypal-setup-and-fields]].
- **Redirect-and-return flow** with auto-capture (`mode: payment`); full refunds and pull-based Sync are supported; recurring, saved cards, and Pay Later are not wired in. See [[paypal-payment-flow]].
- **Currency bridging** — supported store currencies are charged natively; unsupported ones (BGN, RON, HRK) convert to the fallback currency at checkout. See [[paypal-currency-handling]].
- **Mid-transaction email change is safe** — in-flight payments use the saved transaction reference, not the current email. See [[paypal-payment-flow]].

## Related

- [[paypal-setup-and-fields]] — configuration aspect.
- [[paypal-payment-flow]] — runtime checkout / refund / sync aspect.
- [[paypal-currency-handling]] — currency-conversion aspect.
- [[payment-providers]] — parent hub.
- [[payment-providers-stripe]] — alternative international card gateway.
- [[payment-providers-paypal-acdc]] — PayPal's on-site card-fields provider (Advanced Checkout — cards + Apple Pay + Google Pay); separate from this wallet integration, can run alongside it.
- [[payment-providers-cloudcart-pay]] — CloudCart's own card gateway.
- [[orders-payment-refund]] — how to issue refunds.
- [[settings-payment-providers]] — settings hub.

## Open questions

(none)
