---
type: feature
nav_path: "Payment Providers → myPOS"
route_name: apps.mypos.overview
route_path: /admin/payment-providers/mypos
aliases: ["myPOS", "MyPOS", "Mypos", "myPOS Europe", "myPOS Virtual Checkout", "Виртуален ПОС myPOS", "Плащане с карта - myPOS", "MyposService"]
tags: [paymentproviders, payment-providers, mypos, card-gateway, bulgaria, cross-border, popular]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# myPOS

## Purpose

**myPOS** is one of the most popular card-acceptance products for Bulgarian and pan-European e-commerce — operated by **myPOS Europe** (a Bulgarian fintech with a UK / EU passport, offering merchant accounts to small businesses without traditional bank-acquiring contracts). The customer is redirected to myPOS's hosted **Virtual Checkout** page, enters their Visa / Mastercard / Maestro / VPay / JCB card, completes 3-D Secure, and the funds settle to the merchant's **myPOS wallet** (the merchant can then withdraw to their bank account or use the funds via myPOS's debit card).

myPOS is **friction-light onboarding** compared to traditional bank gateways — no e-commerce contract with a Bulgarian bank is required; sign-up is online through myPOS's web portal. The CloudCart setup is also light: the merchant generates a **Configuration Pack** from myPOS, pastes it into CloudCart, and the integration is live. Supported features: **Save customer card** (CardToken tokenisation), **automatic status sync**, **full refund**, **multi-currency**, mandatory **3DS**, and Visa / Visa Electron / VPay / Mastercard / Maestro / JCB card brands.

This hub catalogues the four aspect pages this feature splits into. The Assistant should drill into the aspect that matches the question, not read every page.

## Where to find it

Sidebar → **Payment Providers** → click **myPOS**.

Route: `/admin/payment-providers/mypos`. Route name: `apps.mypos.overview`. The page renders the standard `AppOverview`. There are no sub-tabs — wallet management, payouts, and transactions are in myPOS's own merchant portal at `www.mypos.eu`.

## Sub-pages (in this cluster)

This feature is split into 4 aspect pages:

- [[mypos-setup-config-pack]] — the screen location, full settings layout, and the base64 **Configuration Pack** onboarding (Store ID / Wallet / Key Index / RSA key); the bundled pre-populated test pack; IPC `1.4` version + key-rotation; the four-card UI mechanics; no plan gate.
- [[mypos-payment-lifecycle]] — purchase → Virtual Checkout redirect → mandatory 3DS → return + IPN webhook (`<storefront_domain>/payment/webhook/<payment_id>`); status mapping (`IPCPurchaseNotify` → `Completed`); card networks; multi-currency; OrderID format; address handling.
- [[mypos-save-card]] — CardToken save-card flow (`CARD_TOKEN_REQUEST_PAY_AND_STORE` → `IAPurchase`); the per-environment `test_save_card` / `save_card` switches (myPOS is the only gateway with separate per-environment switches).
- [[mypos-refund-sync]] — full refund via myPOS's `Refund` API (`Trnref`); auto-capture-only (no two-phase capture); periodic `GetPaymentStatus` reconciliation for stranded Pending payments.

## What the merchant can do here

The hub itself is navigation only — every concrete action lives on an aspect page:

- **Install / Uninstall / Activate / Deactivate** the payment method — standard payment-provider overview controls.
- **Switch Test / Live and paste the Configuration Pack** — see [[mypos-setup-config-pack]].
- **Configure storefront labels, amount range, discount** — see [[mypos-setup-config-pack]].
- **Enable Save customer card (per environment)** — see [[mypos-save-card]].
- **Refund a payment, or wait for automatic reconciliation of a stranded Pending payment** — see [[mypos-refund-sync]].

## Settings & fields

This hub does not expose any fields directly. Field-level documentation lives per aspect:

- **Configuration Pack (test + live), Mode, Logo / Title / Description, Amount range, Discount, JSON view of decoded credentials** → [[mypos-setup-config-pack]].
- **Test / Live Save customer card switches** → [[mypos-save-card]].

## Business rules

The cross-cutting rules that apply to the integration as a whole — each spelled out on the relevant aspect:

- **3-D Secure is mandatory** — every Virtual Checkout charge routes through 3DS on myPOS's hosted page; the merchant cannot disable it. See [[mypos-payment-lifecycle]].
- **No bank contract needed** — onboarding is online through myPOS's portal; the only CloudCart-side step is pasting the Configuration Pack. See [[mypos-setup-config-pack]].
- **No plan gate** — any plan that allows payment providers can install myPOS.
- **Per-environment save-card switches** — `test_save_card` and `save_card` are independent flags; myPOS is the only CloudCart card gateway with this split. See [[mypos-save-card]].
- **Auto-capture only** — single-message capture; no pre-authorize / delayed-capture surface, which is why the settings page has no Authorization row. See [[mypos-refund-sync]].
- **Full refunds only** — refunds use the full payment amount (partial refunds are protocol-supported but not exposed in the admin UI). See [[mypos-refund-sync]].
- **Self-healing Pending payments** — a periodic `GetPaymentStatus` sync settles any payment whose IPN didn't arrive, within a few minutes. See [[mypos-refund-sync]].

## Scope

Covered (across the 4 sub-pages):

- Screen location, settings layout, and the Configuration Pack onboarding mechanism.
- Payment lifecycle: purchase, 3DS, redirect, return + IPN, signature verification, status mapping, OrderID + address handling.
- Save Customer Card (CardToken) tokenisation with per-environment switches.
- Full refund and the periodic sync reconciliation loop; auto-capture-only.

Not covered here:

- Wallet balance, payouts, and transaction reporting — these are in myPOS's own portal (`www.mypos.eu`), not in CloudCart.
- The order details Refund button itself — see [[orders-payment-refund]].
- The customer's saved-cards panel — see [[customers-details-payments]].
- Storefront rendering of the checkout button — see [[checkout-flow]].

## Related

- [[payment-providers]] — parent payment-providers hub.
- [[settings-payment-providers]] — global payment-providers list where myPOS is installed / uninstalled.
- [[orders-payment-refund]] — initiates a refund through myPOS from the order details page (see [[mypos-refund-sync]]).
- [[orders-payment-manual]] — manual payment entry (offline / outside myPOS).
- [[customers-details-payments]] — saved-card management for individual customers (see [[mypos-save-card]]).
- [[payment-providers-borica-way4]] — alternative for merchants with a traditional Bulgarian bank contract.
- [[payment-providers-cloudcart-pay]] — CloudCart's own card gateway.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Pending / Canceled / Refunded mapping for myPOS charges (see [[mypos-payment-lifecycle]]).
- [[checkout-flow]] — concept page on storefront checkout.

## Open questions

_None._
