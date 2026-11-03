---
type: feature
nav_path: "Payment Providers → BT ePOS"
route_name: apps.btepos.settings
route_path: /admin/payment-providers/btepos
aliases: ["Btepos", "BT ePOS", "BT iPay", "Banca Transilvania ePOS", "BT card gateway", "Romanian Banca Transilvania card payments"]
tags: [paymentproviders, payment-providers, btepos, romania, card, ron, eur, usd, authorize-capture, redirect]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 1
---
# BT ePOS

## Purpose

**BT ePOS** is the ecommerce card-acquiring product of **Banca Transilvania**, Romania's largest bank. CloudCart integrates BT ePOS so merchants with a Banca Transilvania merchant contract can accept Visa / Mastercard charges directly from their CloudCart store. The customer is redirected from the storefront checkout to BT's hosted payment page, completes 3D Secure (mandatory under EU PSD2 rules), and is bounced back to the store after authorisation.

BT ePOS is more flexible than the simpler Romanian gateways: it supports **multiple settlement currencies** (RON, EUR, USD — picked per environment), supports **authorize-then-capture** (reserve funds at checkout, capture on shipment), and forwards rich customer + delivery metadata to BT for risk scoring. It also handles BT's **loyalty programme overlay** — see Business rules below.

## Where to find it

Sidebar → **Payment Providers** → click **BT ePOS**. Route `/admin/payment-providers/btepos`; provider key `btepos`. The panel uses the shared payment-provider settings layout.

## What the merchant can do here

- **Install / Uninstall** the BT ePOS payment method.
- **Toggle Active** on / off in the header.
- **Switch between Test and Live mode** — each mode has its own username, password, and currency.
- **Enter the Test Username + Test Password + Test Currency** for the sandbox.
- **Enter the Live Username + Live Password + Live Currency** for production.
- **Pick the capture mode** — Direct sale (charge immediately) or Authorization + Capture (reserve at checkout, capture later, with manual or automatic capture choice).
- **Override the customer-facing label** — logo, title, description on storefront checkout.
- **Set an amount range** (min / max) and an optional **discount** for the method.
- **Refund a completed BT ePOS payment** from the order page (see [[orders-payment-refund]]).
- **Capture or cancel an authorized BT ePOS payment** from the order page (see [[orders-payment-capture]]).

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode** (`configuration.mode`) | Switches between BT's test environment and production. | `test` | `test` / `live`. |
| **Test Username** (`configuration.test_username`) | BT-issued username for the sandbox. | Empty | Required when mode = test. Error: "Test Username is required" |
| **Test Password** (`configuration.test_password`) | Password matching the Test Username. | Empty | Required when mode = test. Error: "Test Password is required" |
| **Test Currency** (`configuration.test_currency`) | Settlement currency code for sandbox (946=RON, 978=EUR, 840=USD). | Empty | ISO 4217 numeric. |
| **Live Username** (`configuration.live_username`) | BT-issued username for production. | Empty | Required when mode = live. Error: "Username is required" |
| **Live Password** (`configuration.live_password`) | Password matching the Live Username. | Empty | Required when mode = live. Error: "Password is required" |
| **Live Currency** (`configuration.live_currency`) | Settlement currency code for production. | Empty | ISO 4217 numeric (946=RON, 978=EUR, 840=USD). |
| **Authorize payment** (`configuration.authorize_payment`) | Switches between Direct sale and Authorization + Capture. | None (direct sale) | When set, must be `manual` or `auto`. Error: "Your plan does not support authorized payments." if the plan gates this feature. |
| **Logo / Title / Description** | Standard storefront-label override. | Provider defaults | |
| **Min / Max amount** | Range filter for the method. | Empty | |
| **Discount** | Discount applied when customer picks BT ePOS. | None | |

## Business rules

### Multi-currency settlement (RON / EUR / USD)

Settlement is in one of three currencies, picked per mode (test and live can differ, e.g., a sandbox in RON while production is in EUR):

| ISO 4217 numeric | Currency |
|------------------|----------|
| **946** | RON (Romanian Leu) |
| **978** | EUR (Euro) |
| **840** | USD (US Dollar) |

When the order's currency differs from the configured BT currency, the platform auto-converts the payment amount and currency before redirect.

### Customer flow — full redirect with rich metadata

BT ePOS is a **hosted redirect** gateway. The authorize request carries the amount, a description (`Order #<order_id> | <site_host>`), and an order-bundle with the creation date, customer email, name (Romanian diacritics stripped — BT historically mishandled `ă, â, î, ș, ț`), phone (leading `+` removed), and structured delivery + billing info (address, city, postal code, country as ISO numeric). If the order has no billing address, the fallback street `'Str. Caracal, Nr 2'` is sent (BT requires a non-empty street). BT returns a redirect URL; the customer enters card details, completes 3DS, and is bounced back to `/payments.return/btepos`. The return identifies the payment by an `orderId` query parameter, matched against the stored provider reference ID (not the internal payment ID).

### Status mapping — BT's `orderStatus`

The integration reads the BT response's `orderStatus` numeric and maps it to a CloudCart status:

| BT `orderStatus` | CloudCart status |
|------------------|------------------|
| 0, 5 | **Pending** |
| 1 | **Authorized** |
| 2 | **Completed** |
| 3 | **Canceled** |
| 4 | **Refunded** |
| anything else | **Failed** |

### Authorize-then-capture

When **Authorize payment = manual** or **auto**, BT runs the transaction as a two-step authorize. The payment lands in **Authorized** state (orderStatus=1) and the authorized amount is snapshotted. From there:

- **Manual capture** — merchant clicks Capture on the order (see [[orders-payment-capture]]).
- **Automatic capture** — fires when the order's shipping workflow flips to Shipped (only when authorize mode is `auto`).
- **Cancel authorization** — merchant clicks Cancel; on success the payment flips to Canceled.

Authorize-then-capture is plan-gated. If the merchant's plan does not include it, saving raises "Your plan does not support authorized payments." (same gating as Monri and other authorize-capable gateways — see [[plan-gates]]).

### Loyalty programme — dual-order handling

BT ePOS lets Banca Transilvania cardholders pay part of an order with **loyalty points**. When they do, BT records **two separate orders on their side** — one for the loyalty points, one for the card portion. CloudCart then runs each capture / cancel / refund **twice** (once per BT order, card portion = total minus loyalty amount) and logs both for audit. This dual-order handling is unique to BT ePOS.

### Language and failure handling

BT's hosted-page language is `ro` for a Romanian storefront, otherwise `en`. If the authorize call fails, the request/response details are persisted onto the payment and status flips to Failed.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where BT ePOS is installed / uninstalled.
- [[orders-payment-refund]] — refund initiation (with dual-order loyalty handling).
- [[orders-payment-capture]] — manual capture / cancel-authorization for Authorized BT payments.
- [[payment-providers-euplatesc]] — alternative Romanian card gateway (no certificate, RON-only).
- [[payment-providers-mobilpay]] — alternative Romanian card gateway (certificate-based, RON-only).
- [[payment-provider]] — entity definition.
- [[payment-status]] — Pending / Authorized / Completed / Canceled / Refunded / Failed mapping.
- [[checkout-flow]] — concept page on the storefront checkout.
- [[multi-currency]] — context for the RON/EUR/USD switch behaviour.
- [[plan-gates]] — gating of authorize-then-capture.

## Open questions

- ⏸️ BT ePOS may support more settlement currencies than the three (RON / EUR / USD) the integration enumerates. An order in a currency outside this set cannot be sent through BT today; a merchant needing additional currencies on BT ePOS would need to confirm with BT and contact CloudCart support.
