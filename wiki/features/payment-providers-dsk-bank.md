---
type: feature
nav_path: "Payment Providers → DSK Bank"
route_name: apps.dsk_bank.overview
route_path: /admin/payment-providers/dsk_bank
aliases: ["DSK Bank", "DSK Bank card gateway", "Виртуален ПОС DSK", "ПОС терминал ДСК", "Плащане с карта - ДСК", "DskBank"]
tags: [paymentproviders, payment-providers, dsk-bank, card-gateway, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---

# DSK Bank

## Purpose

**DSK Bank** is the standard bank-card gateway for merchants with an e-commerce contract directly through **Банка ДСК** (DSK Bank, part of OTP Group). The customer is redirected to DSK Bank's hosted Way4-based 3-D Secure page (`epg.dskbank.bg`), enters their Visa / Mastercard / Maestro / Amex card, and on success the money settles to the merchant's DSK Bank account by the next business day. Unlike Borica Way4 (which is a national multi-bank switch — see [[payment-providers-borica-way4]]), this provider is a **DSK-only direct integration** — the merchant must have a DSK Bank business account and e-commerce contract.

Authentication uses **username + password** (HTTP Basic auth credentials) issued by DSK alongside the e-commerce contract — no client certificates to upload, much simpler setup than Borica Way4 or Fibank. Supported features: **Authorize + Capture** (delayed / manual capture), **full and partial refund**, **automatic payment status sync**, **multi-currency** (BGN, EUR, USD, RON). 3DS is mandatory.

This hub catalogues the four aspect pages this feature splits into. The Assistant should drill into the aspect that matches the question, not read every page.

## Where to find it

Sidebar → **Payment Providers** → click **DSK Bank**.

Route: `/admin/payment-providers/dsk_bank`. Route name: `apps.dsk_bank.overview`. The page renders the standard payment-provider overview. No sub-tabs — settlement, payouts and transactions are managed inside DSK's own merchant portal, not in CloudCart.

## Sub-pages (in this cluster)

This feature is split into 4 aspect pages:

- [[dsk-bank-settings-fields]] — the Settings page layout; Test vs Live credential cards (Username, Password, API Version `2020`/`2022`, Currency); the two-card UI pattern that swaps with Mode; standard shared fields (Logo, Title, Amount range, Discount, Authorization mode).
- [[dsk-bank-payment-lifecycle]] — purchase → redirect → mandatory 3DS → return → periodic sync; the `orderNumber = <internal_order_id>-<site_id>` ID format; DSK `orderStatus` → platform [[payment-status]] mapping; the return / webhook URL; provider-side error handling.
- [[dsk-bank-authorize-capture]] — the two-phase Authorize + Capture (manual capture) flow; the 7-day DSK authorization window; Capture vs Cancel from the order details page; the `authorize_payment` plan gate.
- [[dsk-bank-refund-currency]] — full and partial refund; multi-currency (BGN / EUR / USD / RON) terminal provisioning and on-the-fly conversion; the no-saved-cards / no-wallets limitations and the alternative providers.

## What the merchant can do here

The hub itself is navigation only — every concrete action lives on an aspect page. The high-level actions, with their aspect:

- **Install / Uninstall / Activate / Deactivate** the payment method — standard payment-provider overview controls.
- **Switch between Test and Live** environments and **enter credentials** for each — see [[dsk-bank-settings-fields]].
- **Configure standard payment-method options** (Logo / Title / Description, Min / Max amount, Discount) — see [[dsk-bank-settings-fields]].
- **Pick Auto vs Manual capture** (and later Capture / Cancel an authorization) — see [[dsk-bank-authorize-capture]].
- **Refund a payment** — see [[dsk-bank-refund-currency]].

## Settings & fields

This hub does not expose any fields directly. Field-level documentation lives per aspect:

- **Mode, Test/Live Username, Password, API Version, Currency, Logo / Title / Description, Amount range, Discount, Authorization mode** → [[dsk-bank-settings-fields]].
- **Authorization mode dropdown semantics (Auto vs Manual capture)** → [[dsk-bank-authorize-capture]].

## Business rules

The cross-cutting rules that apply to the whole provider; per-aspect rules live on each sub-page:

- **3-D Secure is mandatory.** Every charge runs through the bank's 3DS flow on `epg.dskbank.bg` (live) or `epgtest.dskbank.bg` (test). The merchant cannot disable 3DS — it is the bank's policy. See [[dsk-bank-payment-lifecycle]].
- **Card networks supported:** Visa, Mastercard, Maestro, American Express, Diners — depending on which networks DSK has enabled on the merchant's terminal (Amex is often a separate contract addendum).
- **The provider itself has no plan gate** — any plan that allows payment providers can install DSK Bank. Only the Authorize + Capture toggle is plan-gated, through the `authorize_payment` feature flag — see [[dsk-bank-authorize-capture]] and [[plan-gates]].
- **Live and test credentials are completely separate** — there is no shared key. Test mode calls `epgtest.dskbank.bg`; DSK provides test username + password pairs on request. See [[dsk-bank-settings-fields]].

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global payment-providers list.
- [[orders-payment-refund]] — initiates a refund through DSK Bank from the order details page.
- [[orders-payment-capture]] — manual capture of a Two-Step DSK Bank pre-authorization.
- [[orders-payment-manual]] — manual payment entry (offline / outside DSK Bank).
- [[payment-providers-dsk-bnpl]] — separate DSK installment / buy-now-pay-later product, different gateway and configuration.
- [[payment-providers-dsk-zero]] — DSK 0% interest schemes (Zora-only product, not relevant here).
- [[payment-providers-borica-way4]] — multi-bank alternative if the merchant changes acquiring bank.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Authorized / Completed / Canceled / Refunded / Failed mapping for DSK Bank charges.
- [[plan-gates]] — concept page on the `authorize_payment` feature gating.
- [[checkout-flow]] — concept page on storefront checkout.

## Open questions

- ⏸️ Whether a single DSK Bank terminal can be re-provisioned for additional currencies, or whether DSK requires a separate terminal per currency — a DSK Bank commercial / operations decision, not encoded in CloudCart. The merchant should ask their DSK relationship manager. See [[dsk-bank-refund-currency]].
