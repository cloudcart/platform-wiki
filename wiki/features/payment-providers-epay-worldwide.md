---
type: feature
nav_path: "Payment Providers → ePay Worldwide"
route_name: apps.epay_worldwide.settings
route_path: /admin/payment-providers/epay_worldwide
aliases: ["ePay Worldwide", "EpayWorldwide", "Borica Paycenter", "ePay International", "Paycenter", "ePay Card"]
tags: [paymentproviders, payment-providers, epay-worldwide, paycenter, borica, card, online]
plan_gates: []
created: 2026-05-22
updated: 2026-05-22
source_count: 0
---
# ePay Worldwide

## Purpose

A configuration screen for **ePay Worldwide** — the international card-processing brand associated with Borica's Paycenter Redirect platform, marketed in Bulgaria under the ePay umbrella. Unlike base [[payment-providers-epay]] (which is the BGN-only Bulgarian e-wallet), ePay Worldwide accepts payments in **48 currencies** including USD, EUR, GBP, RON, RUB, PLN, JPY, CNY, and many more.

The merchant enters six credentials (AcquirerID, MerchantID, PosID, Username, Password) plus picks a settlement currency. Customers choose ePay Worldwide at checkout and are redirected to the Borica Paycenter Redirect-hosted card-entry page. The merchant typically uses this provider to accept cards from international customers shipping to Bulgaria, or for stores selling cross-border out of Bulgaria.

## Where to find it

Payment Providers → **ePay Worldwide**. Provider key: `epay_worldwide`. Route name `apps.epay_worldwide.settings`, path `/admin/payment-providers/epay_worldwide/settings`.

## What the merchant can do here

- **Toggle Test / Live mode** — selects Paycenter sandbox vs. production endpoint.
- **Enter six credentials**: AcquirerID, MerchantID (Borica merchant ID), PosID, Username, Password.
- **Pick the live-account settlement currency** from 48 ISO-4217 currency codes.
- **See the read-only Return URL** that doubles as SUCCESS_URL, FAILURE_URL, and BACKLINK_URL — paste this into the merchant's Paycenter dashboard.
- **Customer-facing title** override.
- **Logo override**.
- **Per-provider discount / fee** ([[discount]]).
- **From / To availability window**.
- **Active toggle**.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode** switch | Test → Paycenter sandbox URL. Live → Paycenter production URL. | test after install | Stored as `configuration.mode`. |
| **Acquirer ID** | Borica-assigned acquirer identifier. | required | Stored as `configuration.AcquirerID`. Validation error: "AcquirerID is required." |
| **Merchant ID** | Borica-assigned merchant identifier. | required | Stored as `configuration.MerchantID`. Validation error: "MerchantID is required." |
| **Pos ID** | Borica-assigned POS terminal identifier. | required | Stored as `configuration.PosID`. Validation error: "PosID is required." |
| **Username** | Paycenter API username. | required | Stored as `configuration.Username`. Validation error: "Username is required." |
| **Password** | Paycenter API password. Stored as plaintext (Paycenter's protocol requires it to compute a fresh MD5 hash per request) and masked in the field. | required | Stored as `configuration.Password`. Treated as sensitive — rotate it if a CloudCart staff role is compromised. Validation error: "Password is required." |
| **Live Account Currency** | Settlement currency for the live account — picks from 48 supported ISO-4217 codes. | 978 (EUR) | Required. Stored as `configuration.currency` (numeric ISO-4217 code). Validation error: "Currency is required." |
| **Return URL** (read-only) | SUCCESS_URL / FAILURE_URL / BACKLINK_URL — the same URL serves all three Paycenter callback purposes. | `<cc_payments-domain>/return/provider/epay_worldwide` | Auto-generated. Card label clarifies: "SUCCESS_URL / FAILURE_URL / BACKLINK_URL". |

## Business rules

### Currency support — 48 currencies via numeric ISO-4217

The integration ships a static map of ISO-4217 numeric codes → human label, including:

| Code | Label |
|------|-------|
| 008 | ALBANIAN LEK (ALL) |
| 036 | AUSTRALIAN DOLLAR (AUD) |
| 124 | CANADIAN DOLLAR (CAD) |
| 156 | CHINESE YUAN (CNY) |
| 203 | CZECH KORUNA (CZK) |
| 208 | DANISH KRONE (DKK) |
| 392 | YEN (JPY) |
| 643 | RUSSIAN ROUBLE (RUB) |
| 826 | POUND STERLING (GBP) |
| 840 | US DOLLAR (USD) |
| 946 | ROMANIAN LEU (RON) |
| 975 | BULGARIAN LEV (BGN) |
| 978 | EURO (EUR) |
| 980 | UKRAINIAN HRYVNIA (UAH) |
| 985 | POLISH ZLOTY (PLN) |

The full list of 48 codes is rendered in the currency dropdown.

### Currency conversion at checkout

If the cart currency doesn't match the provider's configured `currency`, the integration auto-converts using the platform's live exchange rates from the configured FX provider — see [[settings-general]]. The converted amount is sent to Paycenter and the payment row is updated with the new amount and currency.

Important: the customer is charged in the merchant's configured live-account currency, NOT the original cart currency. Cart displays one number, the customer's card statement may show another.

### Checkout flow

Unlike base ePay (URL redirect), ePay Worldwide uses an HTML auto-submit form: the storefront automatically POSTs the customer to Paycenter's card-entry page. This pattern matches Borica BGN gateways and many BG bank-acquired card processors.

### Return URL serves three purposes

Paycenter requires three configured URLs (SUCCESS, FAILURE, BACKLINK). All three point to the same CloudCart URL — `<cc_payments>/return/provider/epay_worldwide`. CloudCart reads the returned `pid` parameter (sent back as either POST form-data or a GET query string) to find the right payment row, determine the outcome, and finalize the payment.

### Test vs. live endpoint

The **Test mode** switch flips the gateway between Paycenter's sandbox and production endpoints. Payment outcome (`completed` / `failed` / `cancelled`) is mapped from Paycenter's response codes — typically `00` = success, others = failure.

### Refund

Not supported through CloudCart. As with base ePay, refunds happen via the merchant's Paycenter / ePay merchant interface, then are marked Refunded in CloudCart manually.

There is no periodic status-sync; payment outcome is determined entirely from the return-URL request.

### Order-ID format

The reference sent to Paycenter is the customer-facing order ID (either the increment hash or the raw order ID, depending on the store's Order ID display setting). It appears in the merchant's Paycenter transaction list, making it easy to cross-reference with the order in CloudCart.

### Availability

ePay Worldwide is not BG-restricted — it is offered to stores in multiple operation countries (see [[settings-general]]). Onboarding is offline through Borica / ePay's commercial team; there is no in-platform onboarding wizard (in contrast to [[payment-providers-cloudcart-pay|CloudCart Pay]]). Managing the provider requires the `store.payment_providers` permission. For test mode, Borica Paycenter ships standard 3DS and non-3DS test card numbers; merchants get the exact numbers when registering a test account with Borica/ePay.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-epay]] — the BG e-wallet (BGN-only, different gateway).
- [[payment-providers-epay-one-touch]] — one-click variant for returning customers.
- [[payment-providers-borica-way4]] — Borica's main BG card gateway (separate provider).
- [[settings-payment-providers]] — install/uninstall.
- [[settings-general]] — `operation_country` + `currency` defaults influence which providers are visible.
- [[discount]] — per-provider fee/discount.
- [[orders-payment-refund]] — Refund flow.
- [[payment-providers]] — the `payments` row gets `provider=epay_worldwide`; advances `requested → completed`.

## Open questions

(none)
