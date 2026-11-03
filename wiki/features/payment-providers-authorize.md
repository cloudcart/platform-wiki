---
type: feature
nav_path: "Payment Providers → Authorize.net"
route_name: apps.autorize.settings
route_path: /admin/payment-providers/autorize
aliases: ["Authorize.net", "Authorize Net", "AuthorizeNet", "autorize", "autorize_net"]
tags: [paymentproviders, payment-providers, authorize, international, us, card-gateway]
plan_gates: ["autorize_net"]
created: 2026-05-22
updated: 2026-05-27
source_count: 2
---
# Authorize.net

## Purpose

Authorize.net is one of the oldest and most-established **US card-payment gateways**, owned by Visa. It supports US-based merchants accepting Visa, Mastercard, Discover, American Express, JCB, and Diners Club cards through their own merchant-acquirer relationship.

Authorize.net is the standard choice for **US merchants** who already have a merchant-account with a US bank/processor and need a gateway to connect that account to e-commerce. The merchant signs up for an Authorize.net account, gets API credentials (an App Login Key and Transaction Key), and configures them here.

This is a more "traditional" gateway than newer entrants like Stripe — primarily used by US-focused stores where Stripe alternatives are preferred or where the merchant has existing Authorize.net history.

## Where to find it

Settings → Payments → **Authorize.net**.

URL: `/admin/payment-providers/autorize` (note the spelling — internal key is `autorize` without the "h", a legacy convention). Route name: `apps.autorize.settings`.

## What the merchant can do here

- Toggle the provider **Active**.
- Switch between **Test mode** (Authorize.net sandbox) and **Live mode** with the Live mode switch.
- Enter the **App Login Key** (also called API Login ID) from the Authorize.net merchant portal.
- Enter the **Transaction Key** from the Authorize.net merchant portal (Account → Security Settings → API Credentials).
- Configure storefront name, logo, accepted-amount range, and an optional discount when paying with Authorize.net.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|---|---|---|---|
| **Test mode** switch | Toggles between Authorize.net sandbox and live processing. | Test mode ON (`mode = "test"` when unchecked) | Stored as `configuration.mode = "live"` if checked, else `"test"`. |
| **App Login Key** (API Login ID) | The Authorize.net API Login ID — uniquely identifies your Authorize.net merchant account in API calls. | empty | Required. Validation message: "Authorize: app login key is required." Help: "Authorize.net app login key". |
| **Transaction Key** | The Authorize.net Transaction Key — the secret used to authenticate API calls. | empty | Required. Validation message: "Authorize: transaction key is required." Help: "Authorize.net transaction key". Treat as secret. |
| **Storefront name** | Display name on storefront. | "Authorize.net" | Common option. |
| **Logo** | Provider logo. | Authorize.net default | Common option. |
| **Amount from / Amount to** | Order-amount range when Authorize.net is available. | empty / empty | Common gate. |
| **Discount when paying with Authorize.net** | Flat / percent / shipping-free discount. | none | Common option. |

## Business rules

### Dormant / configuration-only integration

The Authorize.net integration on CloudCart is **dormant** — it only ships a validator for App Login Key + Transaction Key and a settings template. There is **no purchase, sync, capture, refund, or webhook handler** in the codebase for `autorize`. A merchant who enables the provider can save credentials but the runtime flow that would actually charge a card via Authorize.net is not wired. This is effectively a legacy slot kept for plan-gating; merchants who need US card processing today are pointed at [[payment-providers-stripe]] or [[payment-providers-cloudcart-pay]].

### Currency, 3DS, refunds, recurring, saved cards, AVS / CVV

Because no charge flow exists in the CloudCart codebase, none of Authorize.net's runtime features (currency selection, 3DS / Cardholder Authentication, refundTransaction, Automated Recurring Billing, Customer Information Manager / vaulted cards, AVS / CVV checks) are wired in. If the integration is ever brought back to life, all of these will need to be implemented against Authorize.net's APIs.

### Plan-gating

Authorize.net is plan-gated via the feature key `autorize_net` (mapped internally to the provider key `autorize` — the spelling without the "h" is the legacy internal key). The CloudCart plan must include the `autorize_net` feature for the merchant to see / install it. The mapping `autorize_net → autorize` keeps the marketing-facing plan key recognizable while the internal provider slug stays short.

### Permission

Requires the standard payment-providers permission (`settings` / `settings.payment_providers`).

## How it works (verified against backend) — config storage

The configuration storage flow:

1. The merchant submits the form. The `mode` checkbox value is interpreted: if the checkbox is checked, mode is `live`; otherwise `test`.
2. Configuration preparation merges the new fields with the existing stored configuration so unchanged values are preserved.
3. The provider is saved without any pre-flight API ping. **Credentials are NOT validated against the live Authorize.net API on save**, and since there is no purchase flow, a typo in either key is also never caught at transaction time — there is no transaction time.

## Deep audit: settings UI surfaces (verified 2026-05-27)

Like [[payment-providers-skrill|Skrill]] and [[payment-providers-instamojo|Instamojo]], **Authorize.net still uses a legacy Smarty edit form** — there is no modern Vue settings screen. The UI is the older "box / box-section" Smarty layout.

Sections rendered top-to-bottom:

1. **Provider dependency notice** (shared include).
2. **Title + Logo** (shared include).
3. **Mode box**: a single "switch" checkbox labelled with the `payment_provider.label.authorize.mode` translation. Checked → `live`, unchecked → `test`. The toggle is rendered as a Bootstrap-like switch with the `payment_provider.switch.live` off-state label.
4. **Global settings box**: two-column row with **App Login Key** (`configuration[app_login_key]`) and **Transaction Key** (`configuration[transaction_key]`) text inputs.
5. **From-To** shared include (`amount_from` / `amount_to`).
6. **Discount** shared include (`discount_type` / `discount_amount`).

### Per-field validation

| Field | Rule | Message |
|---|---|---|
| `configuration.app_login_key` | `required` | "Authorize: app login key is required." |
| `configuration.transaction_key` | `required` | "Authorize: transaction key is required." |

On save, the mode checkbox is coerced to `'live'` if present, `'test'` if missing, then merged with the existing configuration.

### Conditional UI behaviour

- The mode switch toggles the saved `mode` value but **does not change which fields are visible** — App Login Key and Transaction Key apply to whichever mode is active (the Authorize.net sandbox accepts the same credentials shape as production; the live URL is different).
- No conditional `required_if` — both keys are required regardless of mode.

## Related

- [[payment-providers]] — parent hub.
- [[payment-providers-stripe]] — alternative US/global card gateway (newer, more modern).
- [[payment-providers-cloudcart-pay]] — CloudCart's own card gateway.
- [[orders-payment-refund]] — refund flow.
- [[settings-payment-providers]] — settings hub.

## Open questions

_None._
