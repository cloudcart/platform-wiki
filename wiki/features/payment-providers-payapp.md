---
type: feature
nav_path: "Payment Providers → Payapp"
route_name: apps.payapp.settings
route_path: /admin/payment-providers/payapp
aliases: ["Payapp", "Pay App", "Payapp redirect gateway", "Generic redirect provider"]
tags: [paymentproviders, payment-providers, payapp, redirect, signed-payload, generic]
plan_gates: []
created: 2026-05-22
updated: 2026-05-27
source_count: 2
---
# Payapp

## Purpose

**Payapp** is a generic redirect-style payment gateway integration in CloudCart that uses a **signed-payload protocol** to exchange data with an external payment service. The merchant configures a **redirect URL** (the destination Payapp service) and a **secret key** (used to sign every payload and verify every callback). At checkout, CloudCart serialises the order payment data, base64-encodes it, signs it with the secret key, and POSTs the result to the configured Payapp URL. The customer completes the payment on the Payapp side, and Payapp posts a signed callback back to CloudCart to update the order.

This is the simplest of CloudCart's redirect-style gateways — there's no per-provider API, no card-brand handling, no currency conversion. It's effectively a programmable "send the customer here, listen for a signed reply" channel. It can be used as a bridge to any payment service that supports a signed POST + signed callback contract.

## Where to find it

Sidebar → **Payment Providers** → click **Payapp**.

The route is `/admin/payment-providers/payapp`. The internal provider key is `payapp`. The settings panel uses the shared payment-provider settings shell.

## What the merchant can do here

- **Install / Uninstall** the Payapp payment method.
- **Toggle Active** on / off in the header.
- **Enter the Secret Key** — used to sign outgoing payloads and verify incoming callbacks.
- **Enter the Redirect URL** — the Payapp service endpoint where the customer is redirected to complete payment.
- **Override the customer-facing label** — logo, title, description on storefront checkout.
- **Set an amount range** (min / max) and an optional **discount** for the method.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Secret Key** (`configuration.secret_key`) | Used to sign every payload sent to Payapp and verify every signed callback. | Empty | Required. Minimum 32 characters. Error: "Secret Key is required." |
| **Redirect URL** (`configuration.redirect_url`) | Destination URL where the customer is POSTed at checkout. | Empty | Required. Must be a valid URL. |
| **Logo / Title / Description** | Standard storefront-label override. | Provider defaults | |
| **Min / Max amount** | Range filter for the method. | Empty | |
| **Discount** | Discount applied when customer picks Payapp. | None | |

## Business rules

### Customer flow — signed POST redirect

Payapp is a **hosted redirect** gateway with a custom signed-payload contract:

1. On checkout, the platform builds an array containing the internal Payment ID and the full payment row data.
2. The integration serialises this to JSON, base64-encodes the JSON, signs it with the merchant's secret key (HMAC-style), and renders an auto-submitting HTML form back to the browser.
3. The browser auto-submits to the configured `redirect_url` — this is the Payapp service that handles the actual card / payment processing.
4. The customer completes the payment on the Payapp side.
5. Payapp posts back to CloudCart with two fields: `payload` (the response payload, base64-encoded JSON) and `signature` (HMAC signature of the payload).

### Two return paths — return + IPN

Like most CloudCart redirect gateways, Payapp has both:

- **Return URL** — the customer-facing browser-bounce after Payapp. Verifies the signature and payload, then updates the payment status.
- **IPN** — the server-side callback. Same signature check, same status update, but returns the literal text `OK` so Payapp stops retrying.

### Payload validation — strict signature + required fields

The platform enforces three checks before trusting any return:

1. **Both `payload` and `signature` query parameters must be present** — otherwise it returns "Bad Request: invalid payload" or "Bad Request: invalid signature".
2. **The decoded JSON must contain** `payment_id`, `provider_name`, `provider_reference_id`, and `status` keys — missing any returns "Bad Request: invalid <field>".
3. **The signature must match** the platform's reconstruction with the configured secret key. Mismatch returns "Bad Request: invalid signature".

A signed return that fails any of these checks does NOT update the payment — the order stays in its pre-callback state.

### Status mapping

Payapp's callback contains a `status` field that maps to CloudCart's status set:

| Payapp `status` value | CloudCart status |
|-----------------------|------------------|
| `approved` | **Completed** |
| `pending` | **Pending** |
| `declined` | **Failed** |
| `canceled` | **Canceled** |
| anything else | **Requested** (stays in flight) |

### Payment-identifier lookup

The platform identifies which CloudCart payment a callback refers to by decoding the base64 `payload` parameter, parsing the JSON, and looking up `payment_id`. If the payload is malformed (not base64, not JSON, missing `payment_id`), the platform returns "Bad Request" without touching any payment.

### No built-in test mode

Payapp has no `test_mode` toggle — the URL the merchant configures is the URL the platform uses. To test, point the URL at a Payapp sandbox; for production, change it to the live URL. There's no integration-level switch.

### Currency handling

The platform does **not auto-convert** the order amount for Payapp — it sends whatever currency the order is in. The Payapp service receiving the POST is expected to handle (or reject) the currency itself.

### Plan-tier gating

None — Payapp has no `plan_gates` declaration.

## How it works (verified against backend)

- **Secret Key**: minimum 32 characters (256 bits of entropy from a random string), the defence against weak signing. The merchant should generate a long random string and paste the identical value into the Payapp service's matching configuration — they must match exactly for signatures to verify.
- **Signing algorithm**: HMAC-SHA512 over secret key + payload. Fixed in code, not exposed in the admin UI; the Payapp service must use the same algorithm.
- **Refunds**: not supported. To refund a Payapp-charged order, the merchant marks the order Refunded in CloudCart manually after coordinating with the external Payapp service.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where Payapp is installed / uninstalled.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Pending / Failed / Canceled / Requested mapping (Payapp uses all five).
- [[checkout-flow]] — concept page on the storefront checkout.
- [[settings-api-keys]] — concept comparison: Payapp's secret key is the same pattern as platform API keys for webhook signing.

## Open questions

_None._

## Deep audit: settings UI surfaces (verified 2026-05-27)

Route `apps.payapp.settings`. No environment-mode radio — the field set is `logo`, `amount`, `discount` (no `mode`). Three Payapp-specific cards:

- **Pay App settings** (key `configuration`): two required fields — `configuration.secret_key` ("Secret Key", rule `required|min:32`, error "Secret Key is required.") and `configuration.redirect_url` ("Redirect URL", rule `required|url`, must be a valid URL).
- **Pay App Return URL** (key `payapp_return_url`): read-only `provider.return_url`. Description: "You MUST redirect the customer to this url with POST request after the payment is processed on your redirect url page."
- **Pay App Webhook URL** (key `payapp_webhook_url`): read-only `provider.webhook_url`. Description: "You CAN use this url to POST the payment status update at later time."

The two read-only URL cards exist purely for the merchant to copy/paste — the values come from the backend. `mode` defaults to `live` but is set programmatically (no UI radio).
