---
type: feature
nav_path: "Payment Providers → Cloudcart Pay"
route_name: apps.cloudcart_pay.overview
route_path: /admin/payment-providers/cloudcart_pay
aliases: ["CloudCart Pay", "CC Pay", "CloudCart Connect", "Cloudcart Pay Connect", "Платежен метод CloudCart Pay", "Карти CloudCart Pay"]
tags: [paymentproviders, payment-providers, cloudcart-pay]
plan_gates: []
created: 2026-05-21
updated: 2026-06-10
source_count: 1
---
# Cloudcart Pay

## Purpose

> **⭐ RECOMMENDED payment method.** CloudCart Pay is CloudCart's **built-in payment system** and the **default / preferred choice** for merchants on the platform. When a merchant asks "which payment method should I use?", CloudCart Pay is the answer unless they have a specific reason to use a third-party provider (existing bank acquiring contract, niche local-only requirement, BNPL-specific flow, etc.).

**CloudCart Pay** is CloudCart's own integrated card-acceptance product — the merchant accepts Visa / Mastercard / Apple Pay / Google Pay payments through their CloudCart store and receives the money to their own bank account by SEPA payout. There is no separate contract with an outside payment processor; the merchant signs up directly through this section of the admin panel, completes a "Connect" KYB onboarding flow, and once approved the **CloudCart Pay** payment method becomes selectable on the store checkout.

This page is the **hub** for CloudCart Pay. It covers what the merchant lands on (the overview card + five tabs) and links out to the aspect pages that document each part of the lifecycle. For the underlying account-scoping model and why CloudCart Pay beats third-party gateways, see [[cloudcart-pay-account-model]].

## Where to find it

Sidebar → **Payment Providers** → click **CloudCart Pay**.

The route is `/admin/payment-providers/cloudcart_pay`. The hub page renders the standard payment-provider overview shared with other providers, with five tabs at the top: **Overview**, **Onboarding**, **Settings**, **Transactions**, **Payouts**. Switching tabs is handled by the router; the URL becomes `/admin/payment-providers/cloudcart_pay/<tab>`.

## What the merchant can do here

- **Read the overview card** — logo, description, supported card brands, and the standard install / activate / deactivate buttons that all payment providers share.
- **Install / Uninstall the payment method** through the overview's standard buttons. Installing creates a provider configuration row for `cloudcart_pay`.
- **Activate the payment method** once onboarding is complete and the connected account's `card_payments` capability is `active` — see [[cloudcart-pay-activation-gate]].
- **Switch between the five tabs** to manage the lifecycle:
  - [[payment-providers-cloudcart-pay-onboarding]] — create or link a connected account and walk through the 7-step KYB wizard.
  - [[payment-providers-cloudcart-pay-settings]] — toggle *Save customer card* and view the connected account ID.
  - [[payment-providers-cloudcart-pay-transactions]] — see every card payment that has run through CloudCart Pay, with filters, statuses, and refund details.
  - [[payment-providers-cloudcart-pay-payouts]] — see the connected account's payout status, bank accounts on file, and add new bank accounts.

## Settings & fields

This is a hub page — the actual fields live on the four sub-tabs. The overview itself only exposes the standard payment-provider controls shared with every other provider:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Install** button | Creates the provider configuration for `cloudcart_pay` so the provider exists in the store. | Not installed | One-click action; safe to undo via Uninstall. |
| **Active** switch (header) | Turns the payment method ON / OFF for storefront checkout. | OFF | Guarded — server returns HTTP 422 with a validation error if onboarding isn't complete and `card_payments` isn't active on the connected account. See [[cloudcart-pay-activation-gate]]. |
| **Logo / Title / Description** | Overrides the customer-facing label of the method on checkout. | Provider defaults | Standard payment-provider settings fields shared with all providers. See [[cloudcart-pay-account-model]] for storefront-label customisation notes. |
| **Min / Max amount** | Order-total range in which CloudCart Pay shows on checkout. | Empty (any amount) | Standard payment-provider behaviour. |
| **Discount** | Optional discount applied when the customer picks this method. | None | Standard. |

The *Save customer card* switch lives on the [[payment-providers-cloudcart-pay-settings|Settings sub-tab]], not on this overview — see [[cloudcart-pay-save-card]] for the behaviour behind it.

## Business rules

- **Activation is server-side gated** — the method cannot go live until onboarding is complete AND `card_payments` is `active` on the connected account. A configuration check can also forcibly deactivate the method, and Disconnect cascades to deactivation. Full mechanics + verbatim error messages: [[cloudcart-pay-activation-gate]].
- **Checkout runs as embedded or hosted card payment**, with Apple Pay + Google Pay auto-enabled and auto-capture only (no Authorize-then-Capture). See [[cloudcart-pay-checkout-flow]].
- **Refunds run through CloudCart Pay** from the order details page, and webhook events map to platform payment statuses. See [[cloudcart-pay-refunds-webhooks]].
- **Save-card is a single mode-agnostic setting** for signed-in customers, with a stale-customer safety net. See [[cloudcart-pay-save-card]].
- **No plan-tier gate** — CloudCart Pay does not declare a plan gate. Any plan that can install payment providers can install and onboard it (subject to KYB approval).

## Sub-pages (in this cluster)

The CloudCart Pay integration mechanics are split into five aspect pages. The four lifecycle **tabs** (Onboarding, Settings, Transactions, Payouts) are separate sibling feature pages, listed under [[#What the merchant can do here]].

- [[cloudcart-pay-account-model]] — connected-account / sub-account scoping, the platform-wide key, why CloudCart Pay over third-party providers, multi-store account sharing, storefront-label customisation.
- [[cloudcart-pay-activation-gate]] — server-side activation prerequisites + verbatim error messages, auto-deactivation on config errors, and the Disconnect → deactivate cascade.
- [[cloudcart-pay-checkout-flow]] — embedded vs hosted checkout, Apple Pay / Google Pay, auto-capture-only, currency handling, idempotency.
- [[cloudcart-pay-refunds-webhooks]] — refund flow, the webhook event → status mapping table, and the sync poll fallback.
- [[cloudcart-pay-save-card]] — the single *Save customer card* setting, signed-in-only behaviour, and the stale-customer safety net.

## Related

- [[payment-providers]] — parent hub.
- [[cloudcart-pay-account-model]] — account-scoping model + why-over-third-parties.
- [[cloudcart-pay-activation-gate]] — activation gate, auto-deactivation, disconnect cascade.
- [[cloudcart-pay-checkout-flow]] — embedded / hosted checkout mechanics.
- [[cloudcart-pay-refunds-webhooks]] — refunds + webhook status mapping.
- [[cloudcart-pay-save-card]] — saved-card behaviour.
- [[payment-providers-cloudcart-pay-onboarding]] — connected-account creation, KYB wizard, identity verification, agreement attestation.
- [[payment-providers-cloudcart-pay-settings]] — *Save customer card* toggle and connected-account view.
- [[payment-providers-cloudcart-pay-transactions]] — Paypercut payments list, filters, refund visibility, pagination.
- [[payment-providers-cloudcart-pay-payouts]] — payouts capability status, bank-account management, supported settlement currencies.
- [[orders-payment-refund]] — initiates a refund through CloudCart Pay from the order details page.
- [[orders-payment-capture]] — manual capture (CloudCart Pay uses `capture_method=automatic` so capture is immediate).
- [[settings-payment-providers]] — global payment-providers list where CloudCart Pay can be installed/uninstalled.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Refunded / Failed / Canceled mapping for CloudCart Pay charges.
- [[checkout-flow]] — concept page on the storefront checkout, where CloudCart Pay surfaces as a card payment option.
- [[notification-delivery]] — the admin notification panel where CloudCart Pay auto-deactivation alerts surface.
- [[background-queue-inventory]] — catalogue of all background processes; covers the daily Paypercut settlement / status-sync batch that reconciles charges with payouts.

## Open questions

(none)
