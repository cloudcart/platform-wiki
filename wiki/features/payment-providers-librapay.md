---
type: feature
nav_path: "Payment Providers → LibraPay"
route_name: apps.libra_pay.overview
route_path: /admin/payment-providers/libra_pay
aliases: ["LibraPay", "Libra Pay", "LibraBank", "Libra Internet Bank", "Romanian card gateway", "Плащане с карта - Romania", "LibraPayService"]
tags: [paymentproviders, payment-providers, librapay, card-gateway, romania, cross-border]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# LibraPay

## Purpose

**LibraPay** is the **Romanian** bank-card gateway from **Libra Internet Bank** — the standard card-acceptance product for merchants who have, or want, a Romanian merchant account for **RON-denominated** card payments. The customer is redirected to LibraPay's hosted payment page, enters their Visa / Mastercard card, completes 3-D Secure, and the funds settle to the merchant's Libra Internet Bank account in Romania.

LibraPay suits merchants who **operate in Romania directly** (Romanian legal entity + bank account) or run a **cross-border Bulgarian → Romanian operation** that wants RON acceptance for Romanian customers without FX surcharges. The integration is built on the third-party Omnipay LibraPay driver.

Supported: **redirect to a hosted page**, **3DS mandatory**, **status reconciliation via return-url + webhook callback**, **RON currency only**. Not supported: saved cards, Authorize + Capture, Google Pay / Apple Pay wallets, automated refunds.

## Where to find it

Sidebar → **Payment Providers** → click **LibraPay**.

Route: `/admin/payment-providers/libra_pay`. Route name: `apps.libra_pay.overview`. Renders the standard payment-provider overview. No sub-tabs.

## What the merchant can do here

- **Install / Uninstall** via the standard overview buttons.
- **Activate / Deactivate** using the header switch.
- **Switch between Test and Live** environments using the Mode radio.
- **Enter test credentials** (six fields — see below) — all required when Mode is Test.
- **Enter live credentials** — same six fields, all required when Mode is Live.
- **Configure standard payment-method options** shared with all providers: Logo / Title / Description, Min / Max amount, optional Discount.

## Settings & fields

The Settings page stacks two cards — **Live** and **Test** (both `editMethod: slide`). Only the card matching the current Mode is editable; the other is locked. There is no card-border colour cue (no `border-color-live` / `border-color-test`); the active environment is signalled by the Mode radio row. Standard rows above the cards: `['logo', 'mode', 'amount', 'discount']` (no auth row — single-message capture only).

Each environment exposes the **same six fields** (`live_`-prefixed on the Live card, `test_`-prefixed on the Test card), all issued by Libra Internet Bank and all required when that environment is active:

| Field | Key (live / test) | What it is | Validation error string |
|-------|-------------------|------------|-------------------------|
| **Merchant name** | `live_merchant_name` / `test_merchant_name` | LibraPay-issued business name. | "The test merchant name field is required." |
| **Merchant email** | `live_merchant_email` / `test_merchant_email` | LibraPay-issued contact email. | "The test merchant email field is required." |
| **Merchant url** | `live_merchant_url` / `test_merchant_url` | Storefront URL on file with LibraPay. | "The test merchant url field is required." |
| **Merchant** | `live_merchant` / `test_merchant` | Numeric merchant code from the bank. | "The test merchant field is required." |
| **Terminal** | `live_terminal` / `test_terminal` | Terminal code from the bank. | "The test terminal field is required." |
| **Key** | `live_key` / `test_key` | Signing key from the bank. | "The test key field is required." |

Standard provider controls: **Logo** (storefront checkout logo override), **Title / Description** (customer-facing label), **Mode** radio (Test default; switching to Live requires Live credentials filled), **Amount from / to** (order-total range where LibraPay appears at checkout), **Discount** (optional fixed / percent discount when the buyer picks LibraPay). The underlying Omnipay driver picks the correct live or test endpoint URL from the current Mode — the merchant never sees two different URLs.

## Business rules

All mechanics below are verified against the backend integration (Omnipay LibraPay driver).

### 3-D Secure is mandatory

Every charge runs through 3DS on Libra Internet Bank's hosted page. The merchant cannot disable 3DS — bank policy.

### Card networks

Visa, Mastercard. (Maestro depends on the bank's per-merchant acquiring contract.)

### Currency — RON only

The integration **forces the request currency to `RON`**, regardless of storefront currency. If the storefront is denominated in something other than EUR / RON, the platform converts the order total to RON using the configured exchange rate before sending. A merchant displaying BGN-priced products through LibraPay will see the customer **charged in RON** at the moment of payment — the conversion happens at platform level. See [[multi-currency]].

### Payment lifecycle

1. **Purchase** builds a signed POST payload for LibraPay's hosted page, including: the order ID (see *Order ID format*), `description = <site_url> - Order #<order_id>`, the amount in RON, the customer's first name / last name / email / phone, the return + notify URLs, and a signature derived from the merchant's Key.
2. **Redirect**: the customer is sent to LibraPay's hosted page on the bank's domain.
3. **3DS** happens on that hosted page.
4. **Return + webhook**: LibraPay POSTs back to both the return URL and the notify URL with `RC` (Response Code) and `RRN` (Retrieval Reference Number). The platform reads `RC` and maps it to a [[payment-status]].

### Per-payment URLs

These are constructed per-payment and sent on every transaction — no merchant configuration in the LibraPay portal beyond terminal registration:

```
Return URL: <cc_payments_domain>/return/provider/libra_pay?pid=<payment_id>
Notify URL: <cc_payments_domain>/webhook/libra_pay?pid=<payment_id>
```

### Status code mapping

| LibraPay `RC` | Mapped [[payment-status]] |
|---|---|
| `00` | `Completed` |
| `-19`, `54` | `Failed` |
| anything else | `Requested` (the customer hasn't completed yet) |

### Order ID format

The platform sends `orderId = str_pad(<order_id>, 6, '1', STR_PAD_LEFT)` — LibraPay's order-reference field requires **exactly 6 digits**, so the platform left-pads the order ID with the digit `1` (not zeros — a quirk of the integration) when it's shorter.

### Customer information sent on each transaction

First name, last name, email, and phone (from the storefront's shipping address, falling back to billing if no shipping). Required by LibraPay's anti-fraud rules for Romanian regulators.

### Refunds — not API-implemented

There is no automated refund flow in CloudCart for LibraPay. Refunds must be initiated from Libra Internet Bank's merchant portal directly. The order can still be flagged as refunded in the admin UI via [[orders-payment-refund]], but the financial reversal happens at the bank.

### Not supported

- **Authorize + Capture** — single-message capture only, no delayed-capture surface.
- **Saved cards / wallets** — no tokenisation; no Google Pay / Apple Pay.
- **Periodic reconciliation poll** — the platform relies on the return + webhook callbacks. If both are missed (webhook drop + customer never returns), the order remains in the pre-payment state.

### Plan-tier gating

No plan gate. Any plan that allows payment providers can install LibraPay.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global payment-providers list.
- [[orders-payment-refund]] — initiates a refund flag on the order (financial reversal happens in LibraPay's portal).
- [[orders-payment-manual]] — manual payment entry (offline / outside LibraPay).
- [[payment-providers-borica-way4]] — Bulgarian multi-bank alternative.
- [[payment-providers-cloudcart-pay]] — CloudCart's own card gateway (EUR / BGN focus).
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Failed / Requested mapping for LibraPay charges.
- [[multi-currency]] — storefront-side currency handling (LibraPay always charges in RON).
- [[checkout-flow]] — storefront checkout.

## Open questions

_None._
