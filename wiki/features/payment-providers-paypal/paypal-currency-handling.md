---
type: feature
nav_path: "Payment Providers → PayPal → Currency handling"
route_name: apps.paypal.settings
route_path: /admin/payment-providers/paypal
aliases: ["PayPal currency", "PayPal fallback currency", "PayPal currency conversion", "PayPal BGN", "PayPal unsupported currency", "PayPal account country"]
tags: [paymentproviders, payment-providers, paypal, currency, conversion]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-paypal]]. See the hub for the other aspects (setup & fields, payment flow).

# PayPal — currency handling

## Purpose

This aspect covers how CloudCart bridges the store's selling currency to a currency PayPal can charge in. It matters most for stores whose currency PayPal does not support — notably **BGN, RON, HRK** — where the merchant must pick a fallback currency and accept that customers see converted prices on PayPal's page. It also covers the account-country / account-currency rules that surprise merchants and how to minimise triangular conversions.

## Where to find it

The **Fallback currency** dropdown lives on the PayPal settings screen at `/admin/payment-providers/paypal` — see [[paypal-setup-and-fields]] for the field details. There is no separate currency screen; the conversion behaviour described here is automatic at checkout time.

## What the merchant can do here

- Pick the **Fallback currency** PayPal charges in when the store's currency is unsupported.
- Align their PayPal account's primary currency with that fallback to reduce conversion overhead.

## Settings & fields

The only field is the **Fallback currency** select (documented fully on [[paypal-setup-and-fields]]). Default: if the store currency is in PayPal's supported list → that currency; otherwise USD. The stored key is `configuration.fallback_currency` (default `"EUR"` until the merchant touches it).

## Business rules

### Currency conversion

If the store's currency differs from the currency PayPal will charge in (the fallback currency, when the store currency is unsupported):

1. CloudCart converts the order total using its internal currency-conversion helper.
2. The converted price (rounded to 2 decimals) is sent to PayPal.
3. PayPal charges in the fallback currency. The customer sees the converted amount on PayPal's page.

When the store's currency IS supported by PayPal, no conversion happens — PayPal is called in the native currency.

### Supported vs unsupported store currencies

PayPal supports 24 currencies in CloudCart's integration (full list on [[paypal-setup-and-fields]]). The notable absences are **BGN (Bulgarian Lev), RON (Romanian Leu), HRK (Croatian Kuna)**. Stores in these currencies must pick a fallback currency, and PayPal converts prices into that fallback at checkout time. CloudCart converts amounts internally using its currency tables before sending to PayPal.

### Refund amount preservation

Refunds read the amount from the **original transaction's currency + total**, not from a fresh conversion at refund time. This preserves the exact charged amount even when the order went through a conversion. The refund mechanics live on [[paypal-payment-flow]].

### Account-country and account-currency edge cases (verified against backend)

PayPal's account rules can surprise merchants:

- A PayPal Business account is registered in **one country** with a **primary currency**. The merchant can hold balances in multiple currencies, but the account's primary currency drives the conversion rules.
- If the store sells in EUR but the merchant's PayPal account is USD-based, the merchant chooses USD as the fallback — orders are converted to USD before PayPal sees them.
- PayPal may convert again (USD → merchant's withdrawal currency) when transferring to the bank. PayPal exposes its conversion rate to the merchant in their PayPal dashboard.

### Minimising conversion overhead

For the lowest currency-conversion overhead, the merchant should:

1. Set their PayPal account's primary currency to match the store's selling currency (if supported).
2. Set the **Fallback currency** to that same currency.
3. Avoid unnecessary triangular conversions.

For unsupported store currencies (BGN, RON, HRK, etc.), the merchant must accept that customers see converted prices at PayPal — there's no way around this until PayPal adds those currencies.

## Related

- [[payment-providers-paypal]] — hub.
- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — settings hub.

## Open questions

(none)
