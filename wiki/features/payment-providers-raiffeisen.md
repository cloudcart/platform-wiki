---
type: feature
nav_path: "Payment Providers → Raiffeisen Bank"
route_name: apps.raiffeisen.overview
route_path: /admin/payment-providers/kbc
aliases: ["Raiffeisen", "Raiffeisen Bank", "Райфайзенбанк", "KBC Bank", "ОББ Райфайзен", "Виртуален ПОС Райфайзен", "Плащане с карта - Райфайзен", "RaiffeisenService"]
tags: [paymentproviders, payment-providers, raiffeisen, kbc, card-gateway, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# Raiffeisen Bank

## Purpose

**Raiffeisen Bank** is the bank-card gateway for merchants who hold their e-commerce contract with **Райфайзенбанк** in Bulgaria (now part of the KBC Group after KBC's 2022 acquisition — the admin UI labels environment blocks as *"KBC Bank environment"* internally; the merchant-facing label stays "Raiffeisen Bank"). The customer is redirected to Raiffeisen's hosted UPC (Universal Payment Channel) page, enters their Visa / Mastercard card, completes 3-D Secure, and the funds settle to the merchant's Raiffeisen business account.

The integration uses the **UPC / Bulgarian RBI** protocol with HMAC-signed POST messages. Credentials are: **Merchant ID** (numeric) + **Terminal ID** (alphanumeric) + a CloudCart-bundled private key (per signing algorithm) + a public certificate the merchant sends to Raiffeisen for activation. Supported features: **Save customer card** (UPCToken tokenisation), **Authorize + Capture** (delayed/manual capture), **full refund**, **automatic status sync**, **BGN or EUR currency**, and **SHA-1 or SHA-512 signing**.

This page is the hub for the Raiffeisen cluster. Each aspect below is documented on its own page; drill into the one that matches the question.

## Sub-pages (in this cluster)

- [[raiffeisen-setup]] — credentials (Merchant ID / Terminal ID / signing algorithm / currency), certificate download, webhook + return URLs, the three-card settings UI, and the bundled-private-key model.
- [[raiffeisen-capture-authorize]] — two-phase payment: Authorization mode, the `Delay` flag, the 7-day capture window, capture / cancel from the order, and the `authorize_payment` plan gate.
- [[raiffeisen-save-card]] — UPCToken tokenisation for signed-in customers, the `payByToken` repeat flow, and why it is mutually exclusive with Authorize.
- [[raiffeisen-refund-sync]] — mandatory 3-D Secure, Raiffeisen→platform status mapping, automatic status sync, order-ID format, and full refunds.

## Where to find it

Sidebar → **Payment Providers** → click **Raiffeisen Bank**.

Route: `/admin/payment-providers/kbc` — the URL path is `/kbc`, **not** `/raiffeisen`. The Vue router registers this provider under the `kbc` URL while keeping the route name `apps.raiffeisen.overview` and the `raiffeisen` provider key. Page renders the standard payment-provider overview; there are no sub-tabs — settlement is in Raiffeisen's merchant portal. Detailed field-by-field setup is on [[raiffeisen-setup]].

## What the merchant can do here

- **Install / Uninstall** the payment method; **Activate / Deactivate** via the header switch.
- **Switch between Test and Live** modes.
- **Enter Raiffeisen credentials** and pick signing algorithm + currency — see [[raiffeisen-setup]].
- **Download the public certificate** to register at the bank — see [[raiffeisen-setup]].
- **Enable two-phase Authorize + Capture** — see [[raiffeisen-capture-authorize]].
- **Enable Save customer card** (UPCToken) — see [[raiffeisen-save-card]].
- **Configure standard options** shared with all providers: Logo / Title / Description, Min / Max amount, optional Discount.

## Settings & fields

The full field table (Merchant ID, Terminal ID, Currency, Signing algorithm, certificate, webhook / return URLs) is on [[raiffeisen-setup]]. The **Authorization mode** field is on [[raiffeisen-capture-authorize]], and the **Save customer card** switch is on [[raiffeisen-save-card]]. At a glance:

| Field / Control | Aspect page |
|-----------------|-------------|
| Logo / Title / Description, Mode, Amount, Discount | [[raiffeisen-setup]] |
| Merchant ID, Terminal ID, Currency, Signing algorithm, Download certificate, Webhook / Return URL | [[raiffeisen-setup]] |
| Authorization mode (Auto / Manual capture) | [[raiffeisen-capture-authorize]] |
| Save customer card switch | [[raiffeisen-save-card]] |

## Business rules

- **3-D Secure is mandatory** on every charge — bank-side, cannot be disabled. See [[raiffeisen-refund-sync]].
- **Card networks**: Visa, Mastercard (Maestro / Amex / JCB depend on the merchant's acquiring contract).
- **Currency is single-per-terminal** — BGN (975) or EUR (978), set to match the contract. See [[raiffeisen-setup]].
- **The provider has no plan gate** — any plan that allows payment providers can install Raiffeisen. Only the **Authorize + Capture** toggle is plan-gated via `authorize_payment` (see [[plan-gates]] + [[raiffeisen-capture-authorize]]).
- **Save card and Authorize are mutually exclusive** — the runtime disables save-card when Authorize is on. See [[raiffeisen-save-card]].
- **`/kbc/` path alias** — webhook (`/webhook/kbc`) and return (`/return/provider/kbc`) URLs use `kbc`, not `raiffeisen`, for historical reasons; internally both map to the `raiffeisen` provider key. See [[raiffeisen-setup]].
- **Refunds are full-amount only** — partial refunds are not exposed in the admin UI. See [[raiffeisen-refund-sync]].
- **Shared signing key** — every merchant shares one CloudCart-bundled private key per algorithm; Raiffeisen identifies the merchant by Merchant ID + Terminal ID. Key rotation is platform-wide. See [[raiffeisen-setup]].

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global payment-providers list.
- [[orders-payment-refund]] — initiates a refund through Raiffeisen from the order details page.
- [[orders-payment-capture]] — manual capture of an authorized Raiffeisen payment.
- [[orders-payment-manual]] — manual payment entry (offline / outside Raiffeisen).
- [[customers-details-payments]] — saved-card management for individual customers.
- [[payment-providers-borica-way4]] — multi-bank alternative card gateway.
- [[payment-providers-cloudcart-pay]] — CloudCart's own card gateway if the merchant doesn't have a Raiffeisen e-commerce contract.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Authorized / Completed / Canceled / Refunded / Failed mapping for Raiffeisen charges.
- [[plan-gates]] — concept page on the authorize-payment feature gating.
- [[checkout-flow]] — concept page on storefront checkout.

## Open questions

- ⏸️ Raiffeisen / KBC private-key rotation cadence is a bank-side process not encoded in CloudCart. Keys are bundled with platform code; if the bank rotates, the update ships in a CloudCart release.
