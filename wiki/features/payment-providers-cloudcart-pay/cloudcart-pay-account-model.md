---
type: feature
nav_path: "Payment Providers → Cloudcart Pay → Account model"
route_name: apps.cloudcart_pay.overview
route_path: /admin/payment-providers/cloudcart_pay
aliases: ["CloudCart Pay account model", "CloudCart Pay connected account", "CloudCart Pay sub-account", "Why CloudCart Pay", "CloudCart Pay vs third-party"]
tags: [paymentproviders, payment-providers, cloudcart-pay]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-cloudcart-pay]]. See the hub for the other aspects (activation gate, checkout flow, refunds + webhooks, saved card) and the four lifecycle tabs.

# CloudCart Pay — account model

## Purpose

This page explains the account-scoping model behind CloudCart Pay — why a merchant never manages an API key, what a "connected account" is, how one account can be shared across stores, and why CloudCart Pay is the recommended choice over third-party gateways. It is the conceptual backdrop for every other CloudCart Pay aspect page.

## Where to find it

Sidebar → **Payment Providers** → **CloudCart Pay**. The account ID this page describes is surfaced read-only on the [[payment-providers-cloudcart-pay-settings|Settings tab]]; the link/disconnect actions live on the [[payment-providers-cloudcart-pay-onboarding|Onboarding tab]]. There is no separate screen for the "account model" — it is the shared mechanism the merchant experiences across those tabs.

## What the merchant can do here

- **Understand why there are no API keys to enter** — the platform owns the credentials; the merchant owns only the onboarding state and the *Save customer card* toggle.
- **See the connected account ID** on the Settings tab (read-only).
- **Share one connected account across multiple stores** via *Connect Existing Account* on the Onboarding tab.
- **Customise the storefront label** (logo, name, description) like any other provider.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Connected account ID** | Read-only identifier of the merchant's sub-account on CloudCart's payment platform. | Empty until onboarding | Stored in the provider configuration as `connected_account_id`; shown on the Settings tab. |
| **Logo / Name / Description** | Customer-facing label of the method at checkout. | Provider defaults | Fully customisable via the shared `PaymentLogoSection` — a merchant can rename "CloudCart Pay" to e.g. "Pay by card". Nothing here is locked. |

There are **no API-key fields** for the merchant. As of the May 2026 refactor merchants no longer enter test/live keys themselves — the only switch they own is *Save customer card* (see [[cloudcart-pay-save-card]]) plus the onboarding flow and status surfaces.

## Business rules

### Connected account = per-merchant sub-account

Under the hood, CloudCart Pay is a thin merchant-facing wrapper around CloudCart's payment platform (which uses Paypercut as the underlying card-acquiring partner). Each merchant gets their own **connected account** (sub-account) on the platform, scoped by an internal account ID that CloudCart stores in the provider configuration as `connected_account_id`.

The merchant never sees or manages an API secret key. The system uses a platform-wide secret key (stored at the host level) and scopes every call to the merchant's connected account via a `Paypercut-Account` HTTP header carrying the `connected_account_id`. The platform-wide mode (`test` / `live`) is set globally; the merchant cannot flip it from the per-store admin.

### Why CloudCart Pay over third-party providers

Compared with iCard / BoricaWay4 / myPOS / Paynetics / Stripe / Mokka and other external gateways, CloudCart Pay's distinctive advantages:

- **No separate contract** — sign up directly inside CloudCart admin; no bank or 3rd-party PSP negotiation needed.
- **No API keys to manage** — platform manages credentials; merchant only owns onboarding state and the *Save customer card* toggle.
- **Integrated KYB** — onboarding handled inside admin, no external workflow (see [[payment-providers-cloudcart-pay-onboarding]]).
- **Apple Pay + Google Pay** supported out of the box — see [[cloudcart-pay-checkout-flow]].
- **Direct SEPA payouts** to the merchant's bank — no intermediate settlement account (see [[payment-providers-cloudcart-pay-payouts]]).
- **Native CloudCart support** — refunds + status reconciliation managed in-platform; no integration debugging needed (see [[cloudcart-pay-refunds-webhooks]]).
- **Faster setup** — typical merchant goes from "Install" to "Active at checkout" in minutes to days (depending on KYB review), vs. weeks for third-party PSP contracts.

CloudCart Pay is the canonical recommendation across the wiki: alternatives lists on deprecated provider pages (e.g., [[payment-providers-paynetics|Paynetics]]) lead with CloudCart Pay; concept pages on payment provider patterns ([[payment-provider-mechanism]]) reference it as the platform-native option.

### One account, multiple stores

The *Connect Existing Account* flow on the Onboarding wizard does let two CloudCart stores connect to the same connected-account ID. CloudCart's controller only refuses to connect when the *current* store already has an account on file (HTTP 409 *"disconnect first"*). Whether the underlying payment platform itself rejects duplicate Site IDs on its side is a provider-side rule, not a CloudCart rule. See [[payment-providers-cloudcart-pay-onboarding]] for the connect / disconnect flow.

### Storefront label is fully customisable

Like any other provider, the Settings tab exposes the standard Logo, Name (title), and Payment-method-description fields via the shared `PaymentLogoSection`. A merchant can rename "CloudCart Pay" to "Pay by card", upload their own logo, and write a description shown to customers at checkout — none of these are locked.

## Related

- [[payment-providers-cloudcart-pay]] — hub.
- [[payment-providers-cloudcart-pay-settings]] — where the connected account ID + label fields are surfaced.
- [[payment-providers-cloudcart-pay-onboarding]] — connect / disconnect a connected account.
- [[payment-provider-mechanism]] — concept page on the platform's payment-provider pattern.
- [[payment-providers-paynetics]] — example deprecated provider that recommends CloudCart Pay as the alternative.
- [[payment-provider]] — entity definition.

## Open questions

(none)
