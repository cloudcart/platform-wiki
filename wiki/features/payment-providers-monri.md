---
type: feature
nav_path: "Payment Providers → Monri"
route_name: apps.monri.settings
route_path: /admin/payment-providers/monri
aliases: ["Monri", "Monri Payments", "Balkans card gateway", "Croatian card payments", "Slovenian card payments", "Bosnian card payments"]
tags: [paymentproviders, payment-providers, monri, balkans, croatia, slovenia, bosnia, card, redirect, save-card, authorize-capture]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# Monri

## Purpose

**Monri Payments** is a regional card-acquiring gateway used mainly by merchants in **Croatia, Slovenia, and Bosnia & Herzegovina** (and other South-East European markets). CloudCart integrates Monri's hosted payment page: the customer is redirected from checkout to Monri's secure page, enters card details there (so the merchant never touches PAN data), and is bounced back to the store after authorisation. Monri also supports CloudCart's **save-card** flow (returning customers pay with a tokenised card) and the **authorize-then-capture** flow (reserve funds at checkout, capture later — e.g. on shipment).

The merchant signs a Monri contract, receives a **Merchant Key** and an **Authenticity Token**, and pastes those in here. Test and Live endpoints switch via a single Test-mode field.

## Where to find it

Sidebar → **Payment Providers** → click **Monri**. Route `/admin/payment-providers/monri`; internal provider key `monri`. The panel is rendered by the shared `SettingsFormPayments` component.

## What the merchant can do here

- **Install / Uninstall** the method, and **Toggle Active** in the header (controls storefront visibility).
- **Switch Test / Live mode** (points the client at Monri's sandbox vs production).
- **Enter Merchant Key + Authenticity Token** — both required before any transaction is attempted.
- **Enable Save customer card** — when ON and the customer is signed in, Monri tokenises the card for one-tap future checkouts.
- **Pick the capture mode** — Direct sale, or Authorization + capture (Automatic = capture on shipment; Manual = capture from the order page).
- **Override the storefront label** (logo / title / description), **set an amount range** (min / max), and an optional **discount** for paying by Monri.
- From the order page: **Refund** a completed payment (see [[orders-payment-refund]]) and **Capture / cancel** an authorized one (see [[orders-payment-capture]]).

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode** (`configuration.mode`) | Sandbox vs production endpoint. | `test` | `test` or `live`. |
| **Merchant Key** (`configuration.merchant_key`) | Public merchant identifier from Monri. | Empty | `required`. Attribute "Merchant Key". |
| **Authenticity Token** (`configuration.authenticity_token`) | Secret token authenticating every API call. | Empty | `required`. Attribute "Authenticity Token". |
| **Authorize payment** (`configuration.authorize_payment`) | Immediate charge vs reserve-now / capture-later. | `0` (direct sale) | When set, `manual` or `auto`. Plan-gated — error: "Your plan does not support authorized payments." |
| **Save customer card** (`configuration.save_card`) | When `yes` + signed-in customer, tokenises the card for future charges. | `yes`* | `trueValue: 'yes'` / `falseValue: 'no'`. Global (same for test + live). |
| **Logo / Title / Description** | Storefront-label override. | Provider defaults | |
| **Min / Max amount** | Range filter for the method. | Empty | |
| **Discount** (`discount_type`) | Discount when customer picks Monri. | `flat` | |

\* Shipped default `save_card: 'yes'`; no card is actually saved until a token exists. Both credential fields are always shown (no mode-conditional lock) — Monri selects test vs live from the credential's environment.

## Business rules

### Country & currency support

Monri serves the Balkans — Croatia (EUR, HRK retired post-Eurozone), Slovenia (EUR), Bosnia & Herzegovina (BAM, EUR), and other SEE countries. The integration does **not hard-code a currency**: the customer pays in the store's currency and Monri accepts whatever its contract allows, rejecting the rest at request time. (Contrast [[payment-providers-euplatesc|EuPlatesc]] / [[payment-providers-mobilpay|MobilPay]], which hard-code RON.)

### Customer flow — full redirect

The platform builds the checkout request server-side and renders an auto-submitting form. The customer is redirected to Monri's hosted page, enters card details (3DS challenge if required), and is bounced back to one of three configured URLs:

- **`success_url_override`** → `/site.payment.return/<payment_id>` — return after a successful charge.
- **`cancel_url_override`** → `/site.payment.cancel/<payment_id>` — return after a cancelled / failed charge.
- **`callback_url_override`** → `/site.payment.webhook/<payment_id>` — server-to-server IPN confirming the final state.

The IPN (handler at `payments.webhook/monri`) is the **source of truth**. It validates the payment is in an IPN-accepting state (Initiated / Requested / Pending — anything else returns the literal `OK` immediately so Monri stops retrying), verifies Monri's signature, applies the status mapping below, persists the IPN `reference_number` as `provider_reference_id` plus the full payload in `provider_data`, triggers save-card persistence when a `pan_token` is present for a non-guest, and replies with the literal text **`OK`** (the exact ack string Monri retries on if absent). Payments already in a final state are not re-processed (Monri can deliver the same IPN multiple times). The customer-facing return updates the UI but defers to the IPN; `response_code=0000` on that path also means success.

### Status mapping

| Monri response | CloudCart status |
|----------------|------------------|
| `status=approved` (no authorize) | **Completed** |
| `status=approved` + `authorize_payment` set | **Authorized** |
| anything else (incl. 3DS-failed, customer abort, hard decline) | **Failed** |
| refund call returns `approved` | **Refunded** |
| void / cancel-authorization returns `approved` | **Canceled** |

There is no separate Canceled state for 3DS step-up failures — a declined 3DS challenge, a customer-aborted form, and a hard decline all look identical to the merchant: a **Failed** payment.

### Save customer card flow

When **Save customer card = yes**:

- If the signed-in customer already has a Monri card on file, the platform **bypasses the hosted page** and pays directly with the saved token (`pan_token`); status flips to Completed (or Authorized) immediately.
- If no saved card exists, the request adds `tokenize_pan_offered=true` so Monri's page asks the customer whether to save the card.
- On success, the platform reads `pan_token`, `masked_pan`, `expiration_date` from the IPN, infers the brand from the BIN ([[customers-details-payments]]), and stores the token against the customer. Guests are skipped — only signed-in shoppers get cards saved.
- If a saved-card auto-charge errors, a generic "Monri saved card error" is logged and the order falls back to the standard redirect next attempt.

### Authorize-then-capture workflow

When **Authorize payment = manual** or **auto**, the request sets `transaction_type=authorize` (not `purchase`); on approval the payment goes to **Authorized** with `authorize_amount` snapshotted. Then: **Manual capture** = merchant clicks Capture on the order page → Completed; **Automatic capture** = fires when the order is marked Shipped; **Cancel authorization** = void call → Canceled. Plan-gated (see [[plan-gates]]).

### Refunds & customer metadata

Refund on a completed payment (see [[orders-payment-refund]]) calls Monri's refund endpoint with the stored `order_number`, `currency`, and amount; on `status=approved` the payment flips to Refunded, logged to the order's payment log. The checkout request forwards the customer's email, country (ISO display region), and — when available — name, phone, address, city, and postal code. With no billing address (e.g. digital goods), only email + country reach Monri.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where Monri is installed / uninstalled.
- [[orders-payment-refund]] — refund initiation for Monri payments.
- [[orders-payment-capture]] — manual capture / cancel-authorization for Authorized Monri payments.
- [[customers-details-payments]] — saved customer cards on the customer profile.
- [[payment-provider]] — entity definition.
- [[payment-status]] — status mapping (Completed / Authorized / Canceled / Refunded / Failed).
- [[checkout-flow]] — storefront checkout concept.
- [[plan-gates]] — gating of authorize-then-capture.
- [[notification-delivery]] — admin alerts surface for payment-provider failures.

## Open questions

- ⏸️ The exact list of Monri-accepted currencies is per-contract (typical SEE merchants: EUR primary, BAM / RSD per agreement; HRK retired post-Eurozone-adoption). CloudCart sends whatever currency the order is in; Monri rejects unsupported currencies at request time.
