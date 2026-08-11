---
type: feature
nav_path: "Payment Providers → Paynetics"
route_name: apps.paynetics.overview
route_path: /admin/payment-providers/paynetics
aliases: ["Paynetics", "Paynetics BG", "Payoo", "Виртуален ПОС Paynetics", "Плащане с карта - Paynetics", "PayneticsService"]
tags: [paymentproviders, payment-providers, paynetics, card-gateway, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# Paynetics

## Purpose

**Paynetics** is the bank-card gateway from **Paynetics AD** — a licensed Bulgarian payment institution (EMI) operating across the EEA. The customer is redirected to Paynetics's hosted **Payoo** payment page, enters their Visa / Mastercard card, completes 3-D Secure, and the funds settle to the merchant's Paynetics account (Paynetics issues IBAN sub-accounts to merchants and supports SEPA payouts to a withdrawal bank account).

> **Deprecated for new tenants.** The Paynetics route is commented out of the platform's payment-provider router; new stores cannot install Paynetics from the Payments picker. Existing stores with Paynetics already configured continue to work. Merchants looking for a Bulgarian card gateway with an integrated CloudCart experience today should use [[payment-providers-cloudcart-pay|CloudCart Pay]] or [[payment-providers-mypos|myPOS]] instead.

Paynetics is one of the lighter-touch onboarding options for Bulgarian merchants — Paynetics handles the merchant agreement directly (no third-party bank acquiring contract needed) and the CloudCart configuration is just **two fields per environment**: API Key + Secret. The integration uses HMAC-SHA256 signed POST messages to Paynetics's hosted payment service at `pm.payoo.paynetics.digital`.

This hub catalogues the three aspect pages this feature splits into. The Assistant should drill into the aspect that matches the question, not read every page.

## Where to find it

Sidebar → **Settings** → **Payments** → click **Paynetics** (only visible to stores that already have Paynetics configured — new tenants no longer see it in the picker).

Route: `/admin/payment-providers/paynetics`. Route name: `apps.paynetics.overview`. Standard `AppOverview`, no sub-tabs — settlement and merchant management happen in Paynetics's own portal.

## Sub-pages (in this cluster)

This feature is split into 3 aspect pages:

- [[paynetics-setup-ui]] — screen location, the standard settings layout (Logo / Mode / Amount / Discount), the minimal Vue UI that does **not** render credential fields, the four stored credential keys (`test_api_key` / `test_secret` / `api_key` / `secret`), the `enable_iframe` legacy boolean, and the no-plan-gate / deprecated-picker status.
- [[paynetics-payment-lifecycle]] — purchase → base64 `pm` payload → HMAC-SHA256 request signing → `/authenticate/request` → hosted Payoo page → mandatory 3DS → encrypted return URL (status-in-URL, no webhook dependency); binary `success`/`error` → `Completed`/`Failed` mapping; card networks; multi-currency; `reference = payment ID`.
- [[paynetics-gaps]] — the not-implemented surfaces: no Authorize + Capture, `refund` TODO stub, no `sync` reconciliation, no saved cards, no Google Pay / Apple Pay wallets, recurring fields present but commented out — all unlikely to be filled given deprecation.

## What the merchant can do here

The hub itself is navigation only — every concrete action lives on an aspect page:

- **Install / Uninstall / Activate / Deactivate** the payment method — standard payment-provider overview controls. See [[paynetics-setup-ui]].
- **Switch between Test and Live** environments — see [[paynetics-setup-ui]].
- **Configure storefront labels, amount range, discount** — see [[paynetics-setup-ui]].
- **Understand the charge flow** (redirect, 3DS, encrypted return) — see [[paynetics-payment-lifecycle]].
- **Refund a Paynetics order** — must be done in Paynetics's own portal; the integration has no API-driven refund. See [[paynetics-gaps]] and [[orders-payment-refund]].

## Settings & fields

This hub does not expose any fields directly. Field-level documentation lives on the setup aspect:

- **Logo / Title / Description, Mode (Test/Live), Amount range, Discount** → [[paynetics-setup-ui]].
- **Credential keys (`test_api_key` / `test_secret` / `api_key` / `secret`) and the `enable_iframe` legacy boolean** — stored in configuration and read at runtime, but **not rendered as editable fields** in the current Vue UI → [[paynetics-setup-ui]].

## Business rules

The cross-cutting rules that apply to the integration as a whole — each spelled out on the relevant aspect:

- **3-D Secure is mandatory** — every charge routes through 3DS on Paynetics's hosted Payoo page; the merchant cannot disable it. See [[paynetics-payment-lifecycle]].
- **Status-in-URL, no webhook dependency** — the success/error status is encoded into the encrypted `pid` return parameter, making the integration resilient to webhook delivery issues but with no fallback if the customer never reaches the return URL. See [[paynetics-payment-lifecycle]].
- **Binary status mapping** — `success` → `Completed`, anything else → `Failed`; no `Pending` / `Authorized` / nuanced statuses. See [[paynetics-payment-lifecycle]].
- **No plan gate** — any plan that allows payment providers can install Paynetics, but the provider is commented out of the new-tenant picker. See [[paynetics-setup-ui]].
- **Same endpoint URL for test and live** — both point to `https://pm.payoo.paynetics.digital`; the API-key namespace decides the environment. See [[paynetics-payment-lifecycle]].
- **Major feature gaps** — no capture, no API refund, no sync, no saved cards, no wallets, no recurring. See [[paynetics-gaps]].

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global payment-providers list.
- [[orders-payment-refund]] — initiates a refund flag on the order (financial reversal happens in Paynetics's portal — see [[paynetics-gaps]]).
- [[orders-payment-manual]] — manual payment entry (offline / outside Paynetics).
- [[payment-providers-borica-way4]] — multi-bank Bulgarian alternative.
- [[payment-providers-mypos]] — alternative friction-light card gateway for BG merchants without a traditional bank contract.
- [[payment-providers-cloudcart-pay]] — CloudCart's own card gateway.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Failed mapping for Paynetics charges (see [[paynetics-payment-lifecycle]]).
- [[checkout-flow]] — concept page on storefront checkout.

## Open questions

(none — the Paynetics integration is deprecated for new tenants; the capture / refund / sync / recurring / wallet gaps are unlikely to be filled. See [[paynetics-gaps]] and the deprecation note in *Purpose*.)
