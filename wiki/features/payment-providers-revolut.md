---
type: feature
nav_path: "Payment Providers → Revolut"
route_name: ""
route_path: ""
aliases: ["Revolut", "Revolut Pay", "Revolut Merchant", "Revolut Business"]
tags: [paymentproviders, payment-providers, revolut, not-integrated]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 1
---
# Revolut

## Status: NOT integrated in CloudCart

**There is no Revolut payment-provider integration in CloudCart.** A code audit (2026-05-28) found:

- **No backend integration** — there is no the theme templates directory, no `RevolutService`, no `RevolutClient`, and no `Revolut/ConfigurationValidator.php`.
- **No Vue settings component** — there is no `vuejs-sitecp/.../Providers/revolut/Settings.vue`.
- **No route** — `revolut` is **not** in the Vue payment-providers router's provider list, so there is no `apps.revolut.settings` (or `.overview`) route and no `/admin/payment-providers/revolut` page.
- **Not in the provider registry** — `revolut` does not appear in the platform's payment-provider list (the `cc_gateway.payment_providers` table), so it never shows in the merchant's "Add payment method" picker.

So a merchant **cannot** select, install, or configure Revolut as a payment method in CloudCart today. Any earlier description of a Revolut Merchant API integration (capture modes, webhook secrets, embed.js popup, API version pinning, etc.) did not reflect the actual codebase.

## What to use instead

For international card acceptance, point the merchant at an integration that actually exists:

- [[payment-providers-stripe|Stripe]] — global hosted-checkout card gateway.
- [[payment-providers-cloudcart-pay|CloudCart Pay]] — CloudCart's own card gateway.
- [[payment-providers-mollie|Mollie]] — EU multi-method gateway.

If a merchant specifically asks for Revolut, the honest answer is that CloudCart has no Revolut integration; they would need to use one of the supported gateways above (or request the integration as a feature).

## Related

- [[payment-providers]] — parent hub (lists the providers that DO exist).
- [[settings-payment-providers]] — settings hub.

## Open questions

- ⏸️ Whether a Revolut integration is on CloudCart's roadmap is a product decision, not encoded in the codebase. As of this audit there is no Revolut code in the platform.

## Purpose

Documents that **Revolut is NOT integrated in CloudCart** so the merchant-support AI Assistant does not invent a configuration flow that does not exist.

## Where to find it

Nowhere — the merchant cannot reach a Revolut configuration screen because there is no Revolut entry in the payment-provider registry, no Vue route, and no backend integration.

## What the merchant can do here

Nothing on a Revolut-specific surface. To accept card payments, the merchant picks one of the actually-integrated gateways listed under "What to use instead" above.

## Settings & fields

Not applicable — no settings exist.

## Business rules

Not applicable — no integration exists.
