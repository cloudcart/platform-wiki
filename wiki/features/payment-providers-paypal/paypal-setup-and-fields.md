---
type: feature
nav_path: "Payment Providers → PayPal → Setup & fields"
route_name: apps.paypal.settings
route_path: /admin/payment-providers/paypal
aliases: ["PayPal setup", "PayPal settings", "PayPal configuration", "PayPal fields", "PayPal email field", "PayPal test mode"]
tags: [paymentproviders, payment-providers, paypal, setup, configuration]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-paypal]]. See the hub for the other aspects (payment flow, currency handling).

# PayPal — setup & fields

## Purpose

This aspect covers how the merchant configures PayPal on the CloudCart admin panel: the receiving email, the test/live mode switch, the fallback currency, the common storefront options, and the validation rules behind each field. Setup is intentionally minimal — because CloudCart's own PayPal application credentials are baked into the platform, the merchant only supplies their receiving email and a fallback currency, then toggles the provider active.

## Where to find it

Payment Providers → **PayPal**.

The configuration screen URL is `/admin/payment-providers/paypal` (route `apps.paypal.settings`). It is a Vue SPA that renders the PayPal-specific edit form.

## What the merchant can do here

- Toggle the provider **Active**.
- Switch between **Test mode** (PayPal sandbox) and **Live mode** with the Test mode switch — labels read "Live mode" when active.
- Enter the **PayPal account email** — the receiving merchant's email registered with PayPal.
- Pick a **Fallback currency** — used when the store's currency is not supported by PayPal (e.g., for BGN stores). See [[paypal-currency-handling]] for what the fallback actually does at charge time.
- Configure storefront name, logo, accepted-amount range, and an optional discount when paying with PayPal — see the common payment-provider option group.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|---|---|---|---|
| **Test mode** switch | Toggles between PayPal sandbox and live processing. When ON: sandbox (no real charges). When OFF: live mode. | Test mode OFF (live) — opposite default from most providers | Stored as `configuration.test_mode = "yes"` or `"no"`. Note the inverted semantics: `mode == 'test'` in the form maps to `test_mode = "yes"`. |
| **Email** | The merchant's PayPal account email — where the funds land. | empty | Required, must be a valid email format. Validation messages: "PayPal: merchant email is required." / "PayPal: merchant email is not valid." |
| **Fallback currency** | Currency to use when the store's currency is not in PayPal's supported list. | If store currency is supported → that. Else USD. | Required if store currency is unsupported. Select dropdown of all PayPal-supported currencies. |
| **Storefront name** | Name shown to customers at checkout. | "PayPal" | Common option. |
| **Logo** | Provider logo image. | PayPal default | Common option. |
| **Amount from / Amount to** | Order-amount range when PayPal is available. | empty / empty | Common gate. |
| **Discount when paying with PayPal** | Flat / percent / free-shipping discount when the customer picks PayPal. | none | Common option. |

### Supported currencies

PayPal supports 24 currencies in CloudCart's integration: **AUD, BRL, CAD, CHF, CZK, DKK, EUR, GBP, HKD, HUF, ILS, JPY, MXN, MYR, NOK, NZD, PHP, PLN, RUB, SEK, SGD, THB, TWD, USD**.

Notable absences: **BGN (Bulgarian Lev), RON (Romanian Leu), HRK (Croatian Kuna)** — stores in these currencies must pick a fallback currency. The conversion mechanics live in [[paypal-currency-handling]].

## Business rules

### Plan-gating

No plan-feature gate on PayPal — available on every plan.

### Permission

Settings page: `hasApiPermission:settings,store.payment_providers`.

### Internal CloudCart credentials

CloudCart maintains its **own PayPal app credentials** (client ID + secret) for both sandbox and live modes. The merchant's PayPal email is the payee on each transaction — the technical OAuth handshake uses CloudCart's app. This means the merchant doesn't need to create a PayPal Developer account or register an app; they just need a regular PayPal Business account with the matching email.

### Test mode setup

Test mode uses PayPal's sandbox environment. The merchant should enter a sandbox merchant email (`<something>@business.example.com`) — sandbox emails are created in PayPal's developer dashboard. CloudCart's source-code notes a known sandbox buyer account for internal testing: `buyer@cloudcart.com / cloudcartpaypaltest`.

### Settings UI surfaces (verified 2026-05-27)

The PayPal settings page is the Vue SPA at `apps.paypal.settings`. Layout:

1. **Header — Provider status bar** with mode pill (Test / Live) + Enable/Disable button. PayPal is in the "supports modes" list so the pill shows once the form is valid.
2. **Tabs**: single Settings tab.
3. **Logo + Storefront name** (`PaymentLogoSection`): `title` + logo upload.
4. **Payment-method description** slide-out with TinyMCE editor for `configuration.payment_description`.
5. **Environment mode** radio card: Test mode / Live mode (border color follows the choice).
6. **SettingsBox — PayPal-specific** (single card, key `configuration`, edit method `slide`, always visible). Border color follows mode. Two fields:
   - `configuration.email` — required string. Server validation: `required|email`. Errors: "PayPal: merchant email is required." / "PayPal: merchant email is not valid."
   - `configuration.fallback_currency` — searchable select bound to the list of all currencies returned by the backend, `disableTranslatableOptions: true`, single-choice. Default `"EUR"`.
7. **Common SettingsBox rows**: Amount from/to + Discounts (slide, same shape as Stripe).
8. **SubmitChanges sticky bar** with Save.

`configurationDefault.paypal = { mode: 'test', fallback_currency: 'EUR' }` — `mode` defaults to test, fallback currency defaults to EUR if the merchant has never touched the field.

### Per-field validation

| Field | Rule | Message |
|---|---|---|
| `configuration.email` | `required\|email` | "PayPal: merchant email is required." / "PayPal: merchant email is not valid." |

### Conditional UI behaviour

- The single configuration card stays visible in both modes — PayPal does not split into separate test/live credential cards because the same merchant email is used in both (the test environment is selected by CloudCart's internal sandbox app credentials, not by per-mode merchant input).
- Switching mode just re-paints the card-class border color from live (green) to test (orange) and updates the mode pill in the header.

### `enable_iframe` mode

Legacy / dead code. The configuration loader reads `enable_iframe` on every config read but its value is not used anywhere else in the integration — the active rendering path is full-page redirect to PayPal. The field can be removed in a cleanup; it has no effect today. See [[paypal-payment-flow]] for the live redirect path.

## Related

- [[payment-providers-paypal]] — hub.
- [[payment-providers]] — parent hub.
- [[payment-providers-stripe]] — alternative international card gateway (same common-option shape).
- [[settings-payment-providers]] — settings hub.

## Open questions

(none)
