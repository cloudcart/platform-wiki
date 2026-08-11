---
type: feature
nav_path: "Payment Providers → Fibank"
route_name: apps.fibank.overview
route_path: /admin/payment-providers/fibank
aliases: ["Fibank", "First Investment Bank", "Първа Инвестиционна Банка", "FIB", "Виртуален ПОС Fibank", "Плащане с карта - Fibank", "FibankService"]
tags: [paymentproviders, payment-providers, fibank, card-gateway, bulgaria]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# Fibank

## Purpose

**Fibank** (First Investment Bank / Първа Инвестиционна Банка) is the bank-card gateway for merchants with an e-commerce contract through **First Investment Bank Bulgaria**. The customer is redirected to Fibank's hosted "Ecomm" payment page, enters their Visa / Mastercard / Maestro card, and on a successful 3DS challenge the money settles to the merchant's Fibank business account. The integration uses the older **EGate** / Ecomm protocol (XML over mutual-TLS with a PKCS#12 client certificate) — set-up is more involved than DSK Bank's username/password flow, but lighter than Borica Way4's CSR-and-certificate dance.

This is the **card-acquiring** Fibank product — distinct from [[payment-providers-fibank-bnpl]] which is Fibank's installment / buy-now-pay-later loan product (different gateway, different contract).

Supported features: **redirect to Fibank's hosted page**, **automatic status sync**, **full refund**, **multi-currency** (BGN or EUR). No saved cards. No Authorize + Capture. No wallets.

## Where to find it

Sidebar → **Payment Providers** → click **Fibank**.

Route: `/admin/payment-providers/fibank`. Route name: `apps.fibank.overview`. Page renders standard `AppOverview`. No sub-tabs — settlement is in Fibank's merchant portal.

## What the merchant can do here

- **Install / Uninstall** the payment method via the standard overview buttons.
- **Activate / Deactivate** using the header switch.
- **Switch between Test and Live** environments using the radio.
- **Upload the test PKCS#12 certificate** (`.p12` file) that Fibank issues for the test environment, plus the certificate password.
- **Upload the live PKCS#12 certificate** plus its password.
- **Pick a currency** for each environment (BGN = 975 or EUR = 978).
- **See the Return URL** the merchant must give Fibank when registering the terminal.
- **Configure standard payment-method options** shared with all providers: Logo / Title / Description, Min / Max amount, optional Discount.

For the full certificate upload + environment card mechanics, see [[fibank-setup-certificates]].

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Logo** | Provider logo override on storefront checkout. | Provider default | Standard `PaymentLogoSection`. |
| **Title / Description** | Customer-facing label. Storefront default reads "Pay with card" (`payment_provider.name_fibank`). | "Pay with card" | Standard. |
| **Mode** radio | Test or Live. | Test | Live requires live certificate uploaded. |
| **Amount from / to** | Order total range where Fibank appears at checkout. | Empty (any amount) | Standard. |
| **Discount** | Optional fixed / percent discount when buyer picks Fibank. | None | Standard. |
| **Test / Live certificate** | PKCS#12 (.p12) file Fibank provides per environment. | Empty | See [[fibank-setup-certificates]] for upload + validation rules. |
| **Test / Live certificate password** | Password Fibank gave alongside the PKCS#12. | Empty | Required when uploading certificate. |
| **Test / Live Currency** | BGN (975) or EUR (978). | None | Required. One currency per terminal — see [[fibank-payment-lifecycle]]. |
| **Return URL** | Read-only display of the URL the merchant tells Fibank to send the customer back to. | `<cc_payments_domain>/return/provider/fibank` | Copy-paste into Fibank's terminal configuration. |

## Business rules

- **3-D Secure is mandatory.** Every charge goes through 3DS on Fibank's hosted page; the merchant cannot disable it. See [[fibank-payment-lifecycle]].
- **Card networks:** Visa, Mastercard, Maestro. (Amex / JCB / Diners are not typically activated on Fibank Ecomm terminals — confirm per contract.)
- **One currency per terminal** (BGN 975 or EUR 978); the platform does **not** auto-convert if the storefront currency differs. See [[fibank-setup-certificates]].
- **Full refund only** — no partial-refund amount input in the admin UI. No Authorize + Capture (single-message capture only). See [[fibank-refund-capture]].
- **No saved cards / no wallets** — every purchase requires the customer to enter card details on Fibank's page. See [[fibank-refund-capture]].
- **No plan gate** — any plan that allows payment providers can install Fibank.

## Sub-pages (in this cluster)

- [[fibank-setup-certificates]] — PKCS#12 (.p12) certificate upload, password validation, PEM conversion, per-environment currency, and the three-card settings UI.
- [[fibank-payment-lifecycle]] — purchase → redirect → return → sync flow, mandatory 3DS, order-ID format, connection timeout, and the Return URL the merchant gives Fibank.
- [[fibank-refund-capture]] — full-refund flow, status-code mapping, no Authorize+Capture, no saved cards / wallets, and the legacy iframe flag.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global payment-providers list.
- [[orders-payment-refund]] — initiates a refund through Fibank from the order details page.
- [[orders-payment-manual]] — manual payment entry (offline / outside Fibank).
- [[payment-providers-fibank-bnpl]] — separate Fibank installment / BNPL product (different gateway, different contract).
- [[payment-providers-borica-way4]] — multi-bank alternative if the merchant wants saved cards / Authorize + Capture / wallets.
- [[payment-providers-dsk-bank]] — alternative DSK-only card gateway.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Pending / Expired / Canceled / Refunded mapping for Fibank charges.
- [[checkout-flow]] — concept page on storefront checkout.

## Open questions

- ⏸️ Whether Fibank supports multi-currency on a single terminal (e.g., BGN + EUR together) — a Fibank commercial decision, not encoded in CloudCart. If the merchant holds multiple per-currency terminals, the typical workaround is to install Fibank twice (one per terminal) at the platform level.
