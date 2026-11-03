---
type: feature
nav_path: "Settings → Payment providers → PayPal Credit & Debit Cards"
route_name: apps.paypal_acdc.settings
route_path: /admin/payment-providers/paypal_acdc
aliases: ["PayPal ACDC", "PayPal Advanced Cards", "PayPal Credit & Debit Cards", "PayPal Advanced Checkout", "PayPal card fields", "PayPal Apple Pay", "PayPal Google Pay", "paypal_acdc"]
tags: [payment, providers, paypal, cards, apple-pay, google-pay]
plan_gates: []
created: 2026-06-18
updated: 2026-06-18
source_count: 1
---
# PayPal Credit & Debit Cards (Advanced Checkout)

## Purpose

A payment provider that accepts **credit / debit card payments directly on the checkout page** — PayPal-hosted card fields with built-in 3-D Secure — plus **Apple Pay** and **Google Pay** buttons, all powered by the merchant's own PayPal Business account through PayPal's Advanced Checkout (Orders v2) API. In-product name: *"PayPal Credit & Debit Cards"*; description: *"PayPal Advanced Checkout — accept credit and debit card payments directly on your checkout page, powered by PayPal."*

It is a **separate provider** from the legacy [[payment-providers-paypal|PayPal]] wallet (redirect) integration — the two can run side by side. ACDC requires the merchant's **own PayPal REST app credentials** and an Advanced-Cards-eligible PayPal Business account.

## Where to find it

Sidebar → Settings → **Payment providers** → **PayPal Credit & Debit Cards** (`paypal_acdc`). Provider key `paypal_acdc`, payment category.

## What the merchant can do here

- Switch between **Test (sandbox)** and **Live** mode.
- Enter their PayPal **REST app credentials** per mode (Client ID + Client Secret + optional Webhook ID).
- Pick a **fallback currency** for when the store currency isn't supported by PayPal.
- Choose the **card-form display** — inline on the checkout page, or in a popup after "Complete order".
- Toggle the **cardholder-name** field, **saved cards**, **Apple Pay**, and **Google Pay**.

### What the merchant CANNOT do here

- Use it without an Advanced-Cards-eligible PayPal Business account + their own REST app.
- Treat it as a replacement for the legacy PayPal wallet — ACDC is additional, not a migration.

## Settings & fields

| Field | Key | Notes |
|---|---|---|
| Environment mode | `mode` | `test` / `live`. *"Use test mode to test your connection. Live mode is for the actual payment processing."* |
| Sandbox Client ID / Secret | `test_client_id` / `test_client_secret` | Required when `mode=test`. No whitespace. |
| Sandbox Webhook ID | `test_webhook_id` | Optional. |
| Live Client ID / Secret | `live_client_id` / `live_client_secret` | Required when `mode=live`. |
| Live Webhook ID | `live_webhook_id` | Optional. |
| Currency (fallback) | `fallback_currency` | **Required.** *"Currency used to charge the card when the store currency is not supported by PayPal."* |
| Card form display | `display_mode` | `inline` (fields render in the checkout page) or `popup` (fields open in a popup after the complete-order button). |
| Show cardholder name field | `show_cardholder_name` | `yes` / `no`. |
| Save card | `save_card` | `yes` / `no` — lets signed-in customers vault a card for reuse. |
| Apple Pay | `apple_pay` | `yes` / `no`. |
| Google Pay | `google_pay` | `yes` / `no`. |

Help text (verbatim): live-credentials box — *"REST app credentials used to process live payments through your PayPal Business account."*; card-display box — *"Choose whether the card fields render directly in the checkout page or in a popup after clicking the complete order button."*. Credentials are validated against PayPal on save.

## Checkout behaviour

- **Card fields** — PayPal-hosted, on-site; 3-D Secure handled automatically. Two-phase: create the order server-side → customer enters the card (+ 3DS) → server-side capture.
- **Inline vs popup** — `display_mode`: inline renders the fields in the checkout payment accordion; popup opens the card form in a modal after "Complete order".
- **Apple Pay** — button shows when `apple_pay=yes` **and** the device / browser supports it (Safari / iOS / macOS) **and** the PayPal account is eligible. Requires the Apple Pay domain-association file (see below).
- **Google Pay** — button shows when `google_pay=yes` **and** the PayPal account is eligible; works on any platform.
- **Saved cards (vaulting)** — when `save_card=yes`, a **signed-in** customer can save a card to the PayPal vault and reuse it; a saved card is then charged entirely server-side. Guests cannot save cards.
- **Refunds** — full / partial refunds via the payment actions on [[orders-details]] (PayPal capture refund). See [[orders-payment-refund]].
- **Webhooks** — PayPal webhook events keep the order status in sync (order approved + capture completed / denied / pending / refunded / reversed). The merchant sets the webhook URL + ID in their PayPal developer dashboard; the optional `*_webhook_id` settings hold it.

## Currency handling

PayPal Advanced Cards supports a fixed currency set (AUD, BRL, CAD, CHF, CZK, DKK, EUR, GBP, HKD, HUF, ILS, JPY, MXN, MYR, NOK, NZD, PHP, PLN, SEK, SGD, THB, TWD, USD). When the store currency isn't in that set, the card is charged in the configured **`fallback_currency`**. Zero-decimal currencies (HUF, JPY, TWD) are sent without decimals.

## Business rules

- **Separate from legacy PayPal.** [[payment-providers-paypal]] is the older wallet / redirect flow on the merchant's PayPal email + platform credentials; PayPal ACDC is on-site card fields on the merchant's own REST app. Both can be active at once.
- **No plan gate.** Registered as visible, non-beta, non-dev — available on all plans.
- **Apple Pay domain registration.** To show the Apple Pay button the merchant enables `apple_pay` **and** registers their store domain with PayPal; the sandbox domain-association file ships bundled, while the **live** file is downloaded from the PayPal dashboard per merchant. See Open questions for the exact live-hosting step.

## Related

- [[payment-providers-paypal]] — the legacy PayPal wallet provider (separate integration; can coexist).
- [[settings-payment-providers]] — the payment-providers list where this is enabled.
- [[orders-payment-refund]] — refunding an ACDC payment.
- [[checkout-step-payment]] — the storefront checkout step where the card fields / wallet buttons render.

## Open questions

- The exact hosting step for the **live** Apple Pay domain-association file (the sandbox file ships bundled; the live file is downloaded per merchant from the PayPal dashboard). (verify)
- Whether a dedicated Vue settings screen has fully shipped or the provider is configured via the generic payment-provider settings surface. (verify)
