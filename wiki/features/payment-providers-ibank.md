---
type: feature
nav_path: "Payment Providers → iBank"
route_name: apps.ibank.settings
route_path: /admin/payment-providers/ibank
aliases: ["Ibank", "iBank", "iBank Simplify", "Simplify Commerce", "Mastercard Simplify", "popup card payment"]
tags: [paymentproviders, payment-providers, ibank, simplify, card, eur, popup, hosted-form]
plan_gates: []
created: 2026-05-22
updated: 2026-05-28
source_count: 1
---
# iBank

## Purpose

**iBank** is a card-acquiring integration based on **Mastercard Simplify Commerce**. The merchant accepts Visa / Mastercard charges through a **Simplify hosted-payment popup** that opens on top of the CloudCart checkout — the customer enters card details in the Simplify-rendered form (so the merchant never touches card data) and the popup closes on success. Settlement is in **Euro (EUR)**.

Each mode (test / live) has two key pairs — an **API key pair** (server-to-server refunds and status sync) and a **hosted-payment key pair** (authenticates the popup module and verifies its return signature). The merchant pastes all four values per mode and is good to go. iBank is one of the few CloudCart payment integrations that uses a popup flow instead of a full redirect.

## Where to find it

Sidebar → **Payment Providers** → click **iBank**. The route is `/admin/payment-providers/ibank`; the provider key is `ibank`.

## What the merchant can do here

- **Install / Uninstall** the method and **toggle Active** in the header.
- **Switch between Test and Live mode** — each mode has its own four-key set (API pair + hosted pair; see the table below).
- **Override the customer-facing label** — logo, title, description on checkout.
- **Set an amount range** (min / max) and an optional **discount**.
- **Refund a completed iBank payment** from the order page (see [[orders-payment-refund]]).

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Test mode** (`configuration.mode`) | Switches between iBank test (sandbox) and live (production). | `test` | Empty/test treated as test, `live` for production. |
| **Public key** (`configuration.public_key`) | Server-side API public key for live mode. | Empty | Required when mode = live. |
| **Private key** (`configuration.private_key`) | Server-side API private key for live mode (matched with `public_key`). | Empty | Required when mode = live. |
| **Public key (hosted)** (`configuration.public_key_hosted`) | Popup module public key for live mode. | Empty | Required when mode = live. |
| **Private key (hosted)** (`configuration.private_key_hosted`) | Popup module private key for live mode (used for signature verification). | Empty | Required when mode = live. |
| **Public key (test)** (`configuration.public_key_test`) | Server-side API public key for sandbox. | Empty | See validator quirk below. |
| **Private key (test)** (`configuration.private_key_test`) | Server-side API private key for sandbox. | Empty | See validator quirk below. |
| **Public key (hosted, test)** (`configuration.public_key_hosted_test`) | Popup module public key for sandbox. | Empty | See validator quirk below. |
| **Private key (hosted, test)** (`configuration.private_key_hosted_test`) | Popup module private key for sandbox. | Empty | See validator quirk below. |
| **Logo / Title / Description** | Standard storefront-label override. | Provider defaults | |
| **Min / Max amount** | Range filter for the method. | Empty | |
| **Discount** | Discount applied when customer picks iBank. | None | |

> **Validator quirk:** the live keys are correctly required when `mode` = `live`. The four test keys are guarded by `required_if:configuration.mode,==,""` (empty-string comparison), but the form defaults `mode` to the literal `"test"` — so in practice the test keys are **not** enforced as required on save.

## Business rules

### Forced currency: EUR

iBank settles in **Euro (EUR)** only. When the order is in another currency, the platform converts the amount to EUR at the configured exchange rate **before** rendering the popup — the customer sees the EUR amount on the Simplify card form.

### Customer flow — popup overlay (Simplify module)

iBank is a **popup-overlay** gateway, not a full redirect:

1. On checkout the storefront shows a button initialised with the hosted public key, the amount, the customer name/email, and an order description.
2. Clicking it opens the Simplify popup over the checkout; the customer enters card details (3DS challenge if required).
3. On approval Simplify closes the popup and returns the browser to the payment-return URL with the outcome parameters `paymentId`, `paymentDate`, `paymentStatus`, and `signature`.
4. The platform verifies the signature, stores `paymentId` as the provider reference, then fetches the authoritative status via the server-side API.

### Two key pairs — why?

Simplify issues the keys in two pairs for different trust zones. The **API keys** drive server-to-server calls (refunds, status sync) and must never leak to the client. The **hosted keys** drive the popup module — the public key identifies the merchant inside the module, the private key verifies the return-URL signature. The merchant copies all four (per mode) from the Simplify dashboard.

### Signature verification on return

On return, the platform recomputes a signature from the payment amount, the internal reference, Simplify's `paymentId`, `paymentDate`, `paymentStatus`, and the hosted private key. If it doesn't match the `signature` query parameter, the platform returns "Bad Request - signature do not match" and aborts — without this check, an attacker could spoof a return URL and mark an unpaid order as completed.

### Status mapping

After the signature is verified, the platform fetches the authoritative status via the server-side API (so a forged return cannot bypass the real charge state):

| Simplify `paymentStatus` | CloudCart status |
|--------------------------|------------------|
| `APPROVED` | **Completed** |
| `APPROVED_REFUNDED` (synthesised after a successful refund call) | **Refunded** |
| Anything else | **Failed** |

### Refunds — full only

Calling **Refund payment** on a completed iBank order (see [[orders-payment-refund]]) refunds the **full payment amount** through Simplify; partial refunds are not exposed here. On success the payment moves to **Refunded** (`APPROVED_REFUNDED`); on a Simplify error the underlying message is surfaced to the merchant and recorded for audit.

### Plan-tier gating

None — iBank has no plan gates.

## How it works (verified against backend)

CloudCart talks to Simplify through the official Mastercard Simplify Commerce client. Every server-side call (refund, status sync) uses the **API key pair** for the current mode — test keys in Test, live keys in Live — so a sandbox setup never reaches the production acquirer.

## UI mechanics (settings card pattern)

Above the keys sit the standard rows: logo, mode, amount, discount. The keys live in **two stacked cards** — **Test environment setup** (shown only when Mode = Test, holds the four test keys) and **Live environment setup** (shown only when Mode = Live, holds the four live keys).

All eight key inputs are plaintext **string** fields (no password-masking — the merchant copies them straight from the Simplify dashboard). Validation messages read "Public key test is required", "Private key test is required", "Public key hosted test is required", etc.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where iBank is installed / uninstalled.
- [[orders-payment-refund]] — refund initiation for iBank payments.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Refunded / Failed mapping.
- [[checkout-flow]] — concept page on the storefront checkout.
- [[multi-currency]] — context for the EUR auto-conversion behaviour.

## Open questions

- ⏸️ The underlying acquirer (the bank that settles funds) depends on the merchant's commercial contract with iBank, not encoded in CloudCart.
