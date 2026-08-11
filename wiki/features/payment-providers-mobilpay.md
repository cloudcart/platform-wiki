---
type: feature
nav_path: "Payment Providers → MobilPay"
route_name: apps.mobilpay.settings
route_path: /admin/payment-providers/mobilpay
aliases: ["MobilPay", "Mobilpay", "NETOPIA Payments", "NETOPIA", "Romanian card gateway", "MobilPay RON"]
tags: [paymentproviders, payment-providers, mobilpay, romania, card, ron, redirect, certificate]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 2
---
# MobilPay

## Purpose

**MobilPay** (now known as NETOPIA Payments) is the legacy Romanian card-acquiring gateway integrated into CloudCart. Like [[payment-providers-euplatesc|EuPlatesc]], it lets the merchant accept Visa / Mastercard charges in **Romanian Leu (RON)** through a hosted redirect — the customer is bounced to MobilPay, enters card details there, and is returned to the store after authorisation. Unlike EuPlatesc, the security model is **certificate-based**: every request is encrypted with MobilPay's public key and every response is decrypted with the merchant's private key. The merchant pastes both the public certificate (`.cer`) and the private key (`.key`) here, for both test and live modes.

This is a Romanian-market-only integration; it hard-codes RON as the settlement currency and converts other-currency orders before redirecting.

## Where to find it

Sidebar → **Payment Providers** → click **MobilPay**.

The route is `/admin/payment-providers/mobilpay`. The internal provider key is `mobilpay`.

## What the merchant can do here

- **Install / Uninstall** the method and **toggle Active** to control whether it appears on the storefront checkout.
- **Switch between Test and Live mode** — each mode has its own certificate pair, so test credentials can stay configured alongside live ones.
- **Enter the MobilPay Merchant ID** — the personal merchant code, formatted like `XXXX-XXXX-XXXX-XXXX-XXXX`.
- **Paste the public certificate (`.cer`) and private key (`.key`)** for the test environment and, separately, for the live environment.
- **Override the customer-facing label** (logo, title, description) and set an **amount range** (min / max) plus an optional **discount**.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode** (`configuration.mode`) | Switches between MobilPay's test environment and live processing; each mode uses its own certificate pair. | Test | Values `test` / `live`. |
| **MobilPay Merchant ID** (`configuration.merchant_id`) | Personal merchant code from MobilPay. | Empty | Required. Helper: "This is your personal merchant code, looking something like this: XXXX-XXXX-XXXX-XXXX-XXXX" |
| **Test Public Certificate** (`configuration.certificate_test`) | MobilPay `.cer` for the sandbox — encrypts outgoing test requests. | Empty | Helper: "This is the public certificate (Ending with.cer)" |
| **Test Private Key** (`configuration.certificate_private_test`) | Merchant's matching `.key` for the sandbox — decrypts test responses. | Empty | Helper: "This is the private key (Ending with.key)" |
| **Real Public Certificate** (`configuration.certificate_live`) | MobilPay `.cer` for live mode. | Empty | Required in live mode. |
| **Real Private Key** (`configuration.certificate_private_live`) | Merchant's matching `.key` for live mode. | Empty | Required in live mode. |
| **Logo / Title / Description** | Standard label override for the storefront. | Provider defaults | |
| **Min / Max amount** | Range filter for when the method shows up. | Empty | |
| **Discount** | Discount applied when customer picks MobilPay. | None | |

## Business rules

### Forced currency: RON

MobilPay only settles in **Romanian Leu (RON)**. If the order is in another currency, the platform converts the payment amount to RON at the platform exchange rate **before** building the redirect — the amount and currency are updated and persisted, and the customer sees the RON total on MobilPay's page.

### Customer flow — full redirect with encrypted POST

MobilPay is a **hosted redirect** gateway with an extra encryption step: the purchase request is signed and encrypted with the public certificate, returned to the browser as an auto-submitting form, and the customer completes payment on MobilPay's hosted page (card entry, 3DS if required). MobilPay then POSTs back on two paths — `payments.webhook/mobilpay?pid=<payment_id>` for the IPN and `site.payment.return/<payment_id>` for the visible customer return.

### Two callbacks: IPN (truth) and Return (UX)

MobilPay has two return paths, handled differently:

- **IPN** — server-to-server confirmation. The platform decrypts the payload with the merchant's private key, maps the MobilPay transaction state to a CloudCart [[payment-status]], and responds with an XML acknowledgement (`Content-Type: application/xml`) — MobilPay requires this exact shape. This callback is the source of truth.
- **Return** — the customer-facing browser-bounce. The platform flips the payment Requested → Pending here (so the order-confirmation page reflects "processing"), then waits for the IPN to deliver the final status.

### Transaction state mapping

The MobilPay IPN response maps to CloudCart statuses as:

| MobilPay state | CloudCart status |
|----------------|------------------|
| Successful | **Completed** |
| Pending | **Pending** |
| Cancelled | **Failed** (note: not Canceled — the integration explicitly maps cancellation to Failed) |
| Refunded | **Refunded** |
| Anything else | **Requested** (stays in flight) |

### Certificate handling on disk

For every request the integration writes each certificate string to a temporary file, passes the **file paths** (not the contents) to the payment client, then deletes both temp files when the request ends — even on a fatal error. No certificate sits on disk between requests; this matters because the merchant's **private key** material must never leak to the host filesystem.

### Billing-address payload

The platform sends a structured `billingAddress` block with the order's billing data (name, country, state, city, postal code, address line, email, mobile phone), distinguishing **person** vs **company** by the order's company flag. If the order has no billing address (digital goods, guest checkout without an address step), it falls back to a stub where most fields equal the country code — MobilPay still accepts the request, with thin metadata.

### Refunds

Refunds are not implemented end-to-end — a payment flips to **Refunded** only via an IPN where MobilPay indicates a refund occurred on their side. There is no admin button that initiates a MobilPay refund from CloudCart.

### Plan-tier gating

None — MobilPay has no `plan_gates` declaration.

### Save-time validation (verified 2026-05-27)

The merchant **cannot** save an empty configuration. On save the backend enforces:

- **Merchant ID** — if empty, save fails with "Enter your merchant ID here".
- **Certificate pair for the active mode** — both the public certificate and the private key are required for the selected mode. If a field is empty and no value was previously stored, save fails with "Certificate file is required". (The opposite mode's pair is not validated until the merchant switches to it.)
- **Certificate validity** — an unparseable certificate or key fails with "Invalid certificate file".

Certificate files are stored as their string contents; on a later save an existing stored value satisfies the requirement without re-uploading. The default mode is `test`.

In the UI, the **test environment** card is always visible (locks for editing in live mode), the **live environment** card is hidden entirely in test mode, and the **Merchant ID** card always shows — the merchant code is the same in both modes; only the certificate pair differs.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where MobilPay is installed / uninstalled.
- [[payment-providers-euplatesc]] — the other Romanian card gateway integrated in CloudCart (simpler MID + KEY auth, no certificate files).
- [[orders-payment-refund]] — refund flow (note: MobilPay refunds only flow IN from IPN; no outbound refund call).
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Pending / Failed / Refunded mapping.
- [[checkout-flow]] — concept page on the storefront checkout.
- [[multi-currency]] — context for the RON auto-conversion behaviour.
- [[notification-delivery]] — admin notifications surface for payment-provider issues.

## Open questions

_None._
