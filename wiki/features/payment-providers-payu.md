---
type: feature
nav_path: "Payment Providers → PayU"
route_name: apps.pay_u.settings
route_path: /admin/payment-providers/pay_u
aliases: ["PayU", "pay_u", "PayU Romania", "PayU EU", "PayU global"]
tags: [paymentproviders, payment-providers, payu, international, eu, romania, card-gateway]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# PayU

## Purpose

PayU is a global payment gateway with strong presence in Romania, Poland, Czech Republic, Slovakia, Hungary, Turkey, India, and Latin America, accepting cards (Visa, Mastercard, Maestro, JCB) plus local methods. CloudCart's integration uses the **PayU Romania API v4** (`secure.payu.ro` live / `sandbox.payu.ro` test), making it a **Romania-focused integration** in practice.

The merchant signs up with PayU Romania, gets a merchant code + secret key, and enters them here. Customers are redirected to PayU's hosted payment page to pay by card or a local method enabled in the merchant's PayU dashboard.

## Where to find it

Payment Providers → **PayU**.

URL: `/admin/payment-providers/pay_u` (note the underscore). Route name: `apps.pay_u.settings`. Renders the standard PayU edit form.

## What the merchant can do here

- Toggle the provider **Active**.
- Switch between **Test mode** (`sandbox.payu.ro`) and **Live mode** (`secure.payu.ro`) with the Test mode switch.
- Enter the **Test Secret Key** and **Test Merchant Code** for sandbox.
- Enter the **Live Secret Key** and **Live Merchant Code** for production.
- Pick the **Payment Method** for live mode from the 13 Romanian PayU method codes (live-only — not shown in test mode).
- Configure storefront name, logo, accepted-amount range, and an optional discount when paying with PayU.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|---|---|---|---|
| **Test mode** switch | Toggles between PayU sandbox (`sandbox.payu.ro`) and live (`secure.payu.ro`). | Test mode ON | Stored as `configuration.mode = "test"` or `"live"`. |
| **Test Secret Key** | Sandbox secret key from the PayU Romania dashboard. | empty | `required_if:configuration.mode,==,test`. Message: "The test secret key is required". |
| **Test Merchant Code** | Sandbox merchant code. | empty | `required_if:configuration.mode,==,test`. Message: "The test merchant code is required". |
| **Live Secret Key** | Production secret key. | empty | `required_if:configuration.mode,==,live`. Message: "The live secret key is required". Treat as secret. |
| **Live Merchant Code** | Production merchant code (label "Merchant Integration Code"). | empty | `required_if:configuration.mode,==,live`. Message: "The live merchant code is required". |
| **Payment Method** | The PayU method code sent on each transaction. The picker hardcodes 13 Romanian options (see Business rules). | empty | `required_if:configuration.mode,==,live`. Message: "The payment method is required". Live-only. |
| **Storefront name** | Display name on storefront. | "PayU" | Common option. |
| **Logo** | Provider logo. | PayU default | Common option. |
| **Amount from / Amount to** | Order-amount range when PayU is available. | empty / empty | Common gate. |
| **Discount when paying with PayU** | Flat / percent / shipping-free discount. | none | Common option. Default `discount_type: 'flat'`. |

Defaults: `configurationDefault.pay_u = { mode: 'test', discount_type: 'flat' }`.

### Conditional UI

The settings UI shows two credential cards (keys `live` and `test`, slide-edit), with **exactly one visible based on mode** — switching mode swaps cards and locks the other. The **Live** card additionally carries the `payment_method` selector; the **Test** card has no `payment_method` field (payment method is configurable for live only). Each credential is required only when its mode is selected, so a merchant can save with just live credentials and add test credentials later. Layout: header/tabs/logo, environment-mode radio, the active credential card, common Amount + Discount rows, sticky SubmitChanges bar.

## Business rules

### Payment-method codes (Romania-specific picker)

PayU's API requires a method code on every transaction. The picker hardcodes these **13 Romanian options**: `CARD_AVANTAJ` (Card Avantaj), `STAR_BT` (Star BT), `UNICREDIT` (Unicredit), `BRD_INSTALLMENTS` (BRD Finance), `RAIFFEISEN` (Raiffeisen), `GARANTI_RO` (Garanti BBVA), `PAYOUT`, `BCR_INSTALLMENTS` (BCR), `ALPHABANK_INSTALLMENTS` (Alpha Bank), `OPTIMO` (Optimo Card), `CARD_EMAG` (eMAG Card), `ITRANSFER_BT` (BT24 Internet Banking), `WIRE` (Bank Wire). The merchant picks whichever method is on their PayU contract. There is **no `CCVISAMC` code** in this integration. Methods outside this list (PayU Poland's BLIK, India's UPI, etc.) are not selectable because the integration is Romania-only.

### Country / region scope

PayU Romania only. Endpoint constants point at `sandbox.payu.ro` (test) and `secure.payu.ro` (live). RON and EUR are the dominant pairs. A merchant with a PayU Poland, Czech, India, or LATAM account **cannot** use this integration with that account — the endpoints differ.

### Customer flow at checkout

1. Customer picks PayU; CloudCart creates a payment row.
2. CloudCart calls PayU's `POST /api/v4/payments/authorize` with: merchant payment reference (the payment ID), currency, return URL, billing data, shipping data, communication language (storefront locale), and a single product item (`name: "Order #{id}"`).
3. The request is HMAC-signed with the secret key (see below).
4. PayU returns a payment URL; CloudCart stores PayU's `payuPaymentReference` as `provider_reference_id`.
5. Customer is redirected to PayU's hosted page (Romanian-domain endpoints), pays, and is redirected back to CloudCart's `payments.return` route.
6. PayU also POSTs an IPN to CloudCart's webhook URL; CloudCart re-syncs the payment status at that point.

### Status mapping

PayU response statuses map to CloudCart payment statuses:

- `PAYMENT_AUTHORIZED`, `COMPLETE` → `completed`
- `REFUND` → `refunded`
- `CANCELED`, `EXPIRED` → `cancelled`
- `FAILED` → `failed`
- Other → `pending`

### Signature signing

Every API request is HMAC-SHA256-signed with the merchant's secret key over `HTTP_METHOD + "\n" + URI_PATH + "\n" + DATE_UTC + "\n" + JSON_BODY` (date format `Y-m-d\TH:i:s\Z`). Headers sent on every request: `X-Header-Date` (UTC timestamp), `X-Header-Merchant` (merchant code), `X-Header-Signature` (the HMAC). This prevents replay (the date is signed), tampering (any body change invalidates the signature), and credential theft from traffic capture (only the HMAC transits, not the secret). The integration uses separate `{mode}_merchant_code` / `{mode}_secret_key` pairs for test and live; the active mode selects which pair is read.

### Currency

The order's native currency is sent to PayU. PayU Romania supports RON, EUR, USD, BGN, HUF, PLN, GBP (and possibly more). The merchant's PayU account must accept the currency or PayU rejects the transaction.

### Capture, 3DS, refunds, recurring

- **Capture mode**: the flow calls PayU's `authorize` endpoint but treats the response as final (auto-capture-like). No manual-authorize / capture-later flow is exposed at the settings level.
- **3D Secure**: handled by PayU on their hosted page. Cards requiring 3DS prompt for issuer authentication; others go through transparently.
- **Refunds**: supported. CloudCart calls PayU's refund endpoint with the saved `payuPaymentReference`. Refunds take 3–7 business days to reach the customer's bank.
- **Recurring / subscriptions** and **saved cards / tokenization**: not wired here (PayU supports recurring in their API, but this integration does not use it).

### Gating & permissions

No plan-feature gate. Requires the standard payment-providers permission (`store.payment_providers`).

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-stripe]] — alternative international card gateway.
- [[payment-providers-cloudcart-pay]] — CloudCart's own card gateway.
- [[orders-payment-refund]] — refund flow.
- [[settings-payment-providers]] — settings hub.

## Open questions

(none)
