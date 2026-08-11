---
type: feature
nav_path: "Settings → Payments (provider directory)"
route_name: admin.payments
route_path: /admin/settings/payment_providers
aliases: ["Payment providers directory", "Payment methods catalogue", "Платежни доставчици", "Каталог на платежни методи"]
tags: [payment-providers, directory, hub]
plan_gates: []
created: 2026-05-21
updated: 2026-05-27
source_count: 1
---
# Payment Providers

## Purpose

This page is the **directory of every payment provider** CloudCart supports, so the merchant (or the support Assistant) can jump straight to the right provider's configuration page. The **Payments screen itself** — where providers are installed, activated, ordered, and uninstalled — is documented at [[settings-payment-providers]] (the canonical Settings → Payment methods screen). Use this page to *find* a provider; use [[settings-payment-providers]] to learn how the *screen* works.

> **💡 Recommended payment method: [[payment-providers-cloudcart-pay|CloudCart Pay]]** — CloudCart's own built-in payment system. No separate contract with a third-party processor, in-admin onboarding, Apple Pay / Google Pay / Visa / Mastercard supported, SEPA payouts direct to the merchant's bank account. This is the canonical / default choice for merchants who don't already have a bank-side card acquiring contract.

## Where to find it

Sidebar → **Settings** → **Payment methods** ([[settings-payment-providers]], `/admin/settings/payment_providers`). Add a provider from the **+ Add payment method** modal (or **View more Payment methods** → the App Store, Payments category) → install → open its settings. Each provider below links to its own configuration page.

## What the merchant can do here

- Browse the supported providers in `## Related` and open the one they need.
- Install / activate / order / uninstall a provider on [[settings-payment-providers]].
- Pick **CloudCart Pay** as the primary payment method (recommended), or browse the third-party providers (iCard, BoricaWay4, myPOS, Stripe, Mokka, etc.) if they already hold an acquiring contract with one of those providers.

## Settings & fields

This is a directory — it has no settings of its own. All payment configuration lives on [[settings-payment-providers]] and its sub-pages (list, add modal, activation, uninstall, filtering, credentials shell, record fields).

## Business rules

- The Payments link is visible to a staff member only if their role grants `settings` or `settings.payment_providers` permission.

## Programmatic access

Installed payment providers can be **read** via **JSON-API v2** — see [[api-payment-providers]] for the endpoint and field map. The API surface is **read-only**: integrations enumerate the merchant's enabled providers, but cannot install, uninstall, configure, or activate them through the API. Those operations live in each provider's dedicated sub-screen under this hub.

See [[json-api-v2]] for authentication, rate limit, and the side-effects principle.

## Related

- [[settings-payment-providers]] — the canonical Payment methods screen (install / activate / order / uninstall providers).
- [[api-payment-providers]] — read-only JSON-API v2 enumeration of installed providers.
- [[payment-provider-mechanism]] — the integration model every provider here instantiates (configuration, checkout visibility, confirmation, refunds, tokenization / 3DS).
- [[checkout-flow]] — how an activated provider reaches the customer at checkout.
- [[multi-currency]] — the store currency constrains which providers can process payments.

### Provider directory

- [[payment-providers-borica-way4]]
- [[payment-providers-cloudcart-pay]]
- [[payment-providers-cloudcart-pay-onboarding]]
- [[payment-providers-cloudcart-pay-payouts]]
- [[payment-providers-cloudcart-pay-settings]]
- [[payment-providers-cloudcart-pay-transactions]]
- [[payment-providers-cod]]
- [[payment-providers-cpay]]
- [[payment-providers-dsk-bank]]
- [[payment-providers-dsk-bnpl]]
- [[payment-providers-dsk-bnpl-promotions]]
- [[payment-providers-dsk-bnpl-settings]]
- [[payment-providers-dsk-zero]]
- [[payment-providers-dsk-zero-schemes]]
- [[payment-providers-dsk-zero-settings]]
- [[payment-providers-easypay]]
- [[payment-providers-epay]]
- [[payment-providers-epay-one-touch]]
- [[payment-providers-epay-worldwide]]
- [[payment-providers-fibank]]
- [[payment-providers-fibank-bnpl]]
- [[payment-providers-fibank-bnpl-promotions]]
- [[payment-providers-fibank-bnpl-settings]]
- [[payment-providers-fusion-pay]]
- [[payment-providers-fusion-pay-schemes]]
- [[payment-providers-fusion-pay-settings]]
- [[payment-providers-icard]]
- [[payment-providers-iute]]
- [[payment-providers-iute-schemes]]
- [[payment-providers-iute-settings]]
- [[payment-providers-klear]]
- [[payment-providers-klear-settings]]
- [[payment-providers-librapay]]
- [[payment-providers-mokka]]
- [[payment-providers-mypos]]
- [[payment-providers-newpay]]
- [[payment-providers-paynetics]]
- [[payment-providers-pop]]
- [[payment-providers-raiffeisen]]
- [[payment-providers-tbi]]
- [[payment-providers-tbi-bank]]
- [[payment-providers-plati-posle]]
- [[payment-providers-stripe]]
- [[payment-providers-paypal]]
- [[payment-providers-paypal-acdc]]
- [[payment-providers-mollie]]
- [[payment-providers-braintree]]
- [[payment-providers-skrill]]
- [[payment-providers-sofort]]
- [[payment-providers-revolut]]
- [[payment-providers-paysera]]
- [[payment-providers-authorize]]
- [[payment-providers-payu]]
- [[payment-providers-everypay]]
- [[payment-providers-settle]]
- [[payment-providers-euplatesc]]
- [[payment-providers-mobilpay]]
- [[payment-providers-monri]]
- [[payment-providers-nestpay]]
- [[payment-providers-cardlink]]
- [[payment-providers-cib-bank]]
- [[payment-providers-instamojo]]
- [[payment-providers-catalyst-pay]]
- [[payment-providers-payapp]]
- [[payment-providers-btepos]]
- [[payment-providers-bnp]]
- [[payment-providers-bwt]]
- [[payment-providers-ibank]]
- [[payment-providers-smart-ucf]]
- [[payment-providers-ubb]]
- [[payment-providers-ucf]]
- [[payment-providers-voucher]]

## Open questions

(none)
