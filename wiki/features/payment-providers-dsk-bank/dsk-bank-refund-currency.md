---
type: feature
nav_path: "Payment Providers → DSK Bank → Refund, currency & limitations"
route_name: apps.dsk_bank.overview
route_path: /admin/payment-providers/dsk_bank
aliases: ["DSK Bank refund", "DSK partial refund", "DSK multi-currency", "DSK RON EUR USD", "DSK no saved cards", "DSK no wallets", "DSK currency conversion"]
tags: [paymentproviders, payment-providers, dsk-bank, card-gateway, refund, currency, bulgaria]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-dsk-bank]]. See the hub for related aspects (settings, payment lifecycle, authorize/capture).

# DSK Bank — Refund, currency & limitations

## Purpose

This aspect documents three related topics: **refunding** a DSK Bank charge (full and partial), the gateway's **multi-currency** support (BGN / EUR / USD / RON) including on-the-fly conversion, and the gateway's **limitations** — no saved cards (tokenisation) and no Google Pay / Apple Pay wallets — plus the alternative providers a merchant should use when those are needed.

## Where to find it

- **Refunds** are initiated from the order details page — see [[orders-payment-refund]].
- **Currency** is configured per environment on the DSK Bank settings page — see [[dsk-bank-settings-fields]].
- The **limitations** are inherent to the integration; there are no toggles to enable saved cards or wallets here.

## What the merchant can do here

- **Refund a payment** (full or partial) from the order details page — see [[orders-payment-refund]].
- **Set the terminal currency** (BGN / EUR / USD / RON) for each environment on [[dsk-bank-settings-fields]].
- **Choose an alternative provider** when saved-card or wallet UX is required (see Business rules).

## Settings & fields

This aspect exposes no settings fields of its own. The relevant configuration is the per-environment **Currency** field documented on [[dsk-bank-settings-fields]] (Test Currency / Live Currency, stored as numeric ISO 975 / 978 / 840 / 946).

## Business rules

### Refund support

Full refund is supported — the platform calls DSK's refund endpoint. Partial refunds work as well (the platform sends the payment amount, but DSK accepts a smaller `amount` if needed). Initiating a refund from [[orders-payment-refund]] flips the payment to `Refunded` after DSK confirms (DSK `orderStatus 4` → platform `Refunded`, per the status table on [[dsk-bank-payment-lifecycle]]).

### Currency support (multi-currency)

DSK Bank's terminal can be provisioned for **BGN, EUR, USD, or RON** (Romanian leu — DSK is part of OTP, which is active across the region). The integration maps the numeric ISO code (975 / 978 / 840 / 946) to the 3-letter currency. If the storefront customer places an order in a currency different from the terminal's currency, the platform **converts the amount on the fly** before sending to DSK — but the merchant should align store currency with terminal currency to avoid rounding drift.

### Save customer card — not supported

DSK Bank's standard integration on CloudCart **does not support tokenisation / saved cards** today. Every purchase requires the customer to enter card details fresh. If the merchant needs saved-card UX they should look at [[payment-providers-borica-way4]] or [[payment-providers-cloudcart-pay]] instead.

### Google Pay / Apple Pay — not configurable here

The standard DSK integration does not expose wallet buttons on storefront checkout. If the merchant wants wallets, the path is Borica Way4 (whose MPay surface supports Google Pay / Apple Pay) or CloudCart Pay.

## How it works (verified against backend)

Built on the `omnipay-dsk-bank` driver.

### Refund

`refund` calls DSK's refund endpoint with the original `orderId`. Partial refunds are supported by the DSK protocol — the platform sends the payment amount by default, but the endpoint accepts a smaller value. On confirmation the status flips to `Refunded`.

### Currency handling (multi-currency)

DSK supports **BGN, EUR, USD, RON** (RON is the Romanian leu). If the storefront's order currency differs from the configured terminal currency, the platform converts the amount on the fly using the store's currency rates before sending — but merchants should align store and terminal currencies to avoid rounding drift.

### No saved cards / no wallets

The standard DSK integration does not implement tokenisation / saved cards and does not expose Google Pay / Apple Pay. Merchants needing these features should use Borica Way4 or CloudCart Pay.

## Related

- [[payment-providers-dsk-bank]] — hub.
- [[dsk-bank-settings-fields]] — where the per-environment Currency field lives.
- [[dsk-bank-payment-lifecycle]] — the `orderStatus 4` → `Refunded` mapping.
- [[orders-payment-refund]] — the order-details refund action.
- [[payment-providers-borica-way4]] — alternative provider with saved cards + Google Pay / Apple Pay.
- [[payment-providers-cloudcart-pay]] — alternative provider with saved-card / wallet support.
- [[payment-status]] — the `Refunded` status this produces.

## Open questions

- ⏸️ Whether a single DSK Bank terminal can be re-provisioned for additional currencies, or whether DSK requires a separate terminal per currency — a DSK Bank commercial / operations decision, not encoded in CloudCart. The merchant should ask their DSK relationship manager.
