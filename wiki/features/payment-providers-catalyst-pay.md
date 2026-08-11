---
type: feature
nav_path: "Payment Providers → CatalystPay"
route_name: apps.catalyst_pay.settings
route_path: /admin/payment-providers/catalyst_pay
aliases: ["CatalystPay", "Catalyst Pay", "Catalyst Payments", "Embedded card checkout", "Catalyst hosted Checkout.js"]
tags: [paymentproviders, payment-providers, catalyst-pay, card, embedded, checkout-js, card-brands]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# CatalystPay

## Purpose

**CatalystPay** is an Open Payment Platform (OPPwa)-based card-acquiring gateway used by merchants in Bulgaria and other European markets. The CloudCart integration uses CatalystPay's **embedded Checkout.js module** — the customer enters card details in a CatalystPay-rendered form embedded directly on the CloudCart checkout (rather than being redirected to a hosted page), so the experience feels native to the store. Card data POSTs straight from the browser to CatalystPay (the merchant's server never touches it, minimising PCI scope); CatalystPay completes the charge and returns the result to CloudCart.

The merchant signs a CatalystPay contract, receives an **Entity ID** and an **Authentication Token** for each mode (test + live), and configures which card brands to accept. Charges use `paymentType=DB` (immediate capture); refunds use `paymentType=RF`.

## Where to find it

Sidebar → **Payment Providers** → click **CatalystPay**.

The route is `/admin/payment-providers/catalyst_pay`. The internal provider key is `catalyst_pay`. The settings panel is rendered by the shared `SettingsFormPayments` Vue component.

## What the merchant can do here

- **Install / Uninstall** the CatalystPay payment method.
- **Toggle Active** on / off in the header.
- **Switch between Test and Live mode** — each mode has its own Entity ID + Authentication Token.
- **Enter the Test Entity ID + Test Authentication Token** for the sandbox.
- **Enter the Live Entity ID + Live Authentication Token** for production.
- **Pick the enabled card brands** — the embedded Checkout.js module renders accepted-brand logos based on this list.
- **Override the customer-facing label** — logo, title, description on storefront checkout.
- **Set an amount range** (min / max) and an optional **discount** for the method.
- **Refund a completed CatalystPay payment** from the order page (see [[orders-payment-refund]]).

## Settings & fields

Only one mode's credentials card is visible at a time — the **Live** card shows when `configuration.mode = live`, the **Test** card when `mode = test`; the other locks. The brand multi-select is always visible and the same selection applies to both modes. The credential field labels are "Catalyst Pay ID" (Entity ID) and "Catalyst Pay Authentication Token". The configuration default is `{ mode: 'test', discount_type: 'flat' }`.

| Field / Control | What it does | Default | Validation / message |
|-----------------|--------------|---------|----------------------|
| **Test mode** (`configuration.mode`) | Switches between CatalystPay test (sandbox) and live (production). | `test` | `test` / `live`. |
| **Test Entity ID** (`configuration.entity_id_test`) | Entity identifier for the sandbox. | Empty | `required_if:configuration.mode,test` — "Entity ID is required." |
| **Test Authentication Token** (`configuration.authentication_token_test`) | Bearer token for sandbox API calls. | Empty | `required_if:configuration.mode,test` — "Authentication Token is required." |
| **Live Entity ID** (`configuration.entity_id`) | Entity identifier for production. | Empty | `required_if:configuration.mode,live` — "Entity ID is required." |
| **Live Authentication Token** (`configuration.authentication_token`) | Bearer token for production API calls. | Empty | `required_if:configuration.mode,live` — "Authentication Token is required." |
| **Enabled Brands** (`configuration.enabled_brands`) | Card brands / APMs the Checkout.js module should accept. Searchable multi-select. | Empty | `required` (pick at least one) — "Enabled Brands is required." |
| **Logo / Title / Description** | Standard storefront-label override. | Provider defaults | |
| **Min / Max amount** | Range filter for the method. | Empty | |
| **Discount** | Discount applied when customer picks CatalystPay. | None | |

The brand picker offers a fixed list of ~150 card brands and alternative payment methods. Headline brands: VISA, MASTER, MAESTRO, AMEX, DINERS, DISCOVER, JCB, UNIONPAY, plus wallets (APPLEPAY, GOOGLEPAY, SAMSUNGPAY, CLICK_TO_PAY) and a long tail of regional methods (BANCONTACT, BIZUM, BLIK, KLARNA, PAYPAL, SEPA, TWINT, etc.). A merchant whose CatalystPay contract doesn't accept a chosen brand gets a CatalystPay-side rejection when the customer tries to pay with it.

## Business rules

### Customer flow — embedded Checkout.js, not redirect

The customer **does not leave the store**:

1. On checkout, the platform calls CatalystPay's `/v1/checkouts` endpoint server-side with the order amount, currency (the store's currency — no auto-conversion), locale (matched to the storefront language), `paymentType=DB`, and the Entity ID.
2. CatalystPay returns a `checkoutId` — a one-time-use token tied to that pending transaction.
3. The platform renders a CatalystPay Checkout.js module into the checkout page (via the `checkout` Smarty view) with the checkoutId, the merchant's brand list (joined space-separated), the locale, and a return URL.
4. The customer enters card details directly in the embedded form; the browser POSTs them straight to CatalystPay.
5. CatalystPay processes the transaction and redirects the browser to `/payments.return/catalyst_pay?pid=<payment_id>` with a `resourcePath` query parameter pointing at the result.

The `checkoutId` is **single-use** — once the card form is submitted it is consumed and cannot be reused. If the customer abandons and returns, the platform creates a fresh `checkoutId` server-side. This is why CatalystPay payments don't survive browser-back navigation past the card form — each attempt is a fresh API round-trip and a fresh embedded-module render.

### Two-step status lookup

After the browser returns, the platform does NOT trust the URL parameters — it calls CatalystPay's API for the authoritative result. It queries `getPaymentStatus(<entity_id>, <id>, <resourcePath>)` when a `resourcePath` is present (the typical case) or `getAfterPaymentStatus(<entity_id>, <id>)` as a fallback when none is. The response's `result.code` is matched against the regex-based status grammar below to map to a CloudCart payment status.

### Status code grammar — regex match on `result.code`

CatalystPay's response codes follow OPPwa conventions where each code is a hierarchical dotted number:

| Code pattern | CloudCart status | Meaning |
|--------------|------------------|---------|
| `000.000.` / `000.100.1` / `000.[36]` / `000.400.[110\|120]` | **Completed** | Successful transaction. |
| `000.400.0[^3]` / `000.400.100` | **Requested** | Pending review (risk scoring). |
| `000.200.` | **Requested** | Pending (waiting on customer action). |
| `800.400.5` / `100.400.500` | **Requested** | Soft decline, retry possible. |
| `100.39[765]` | **Requested** | 3DSv2 challenge in progress. |
| `300.100.100` | **Requested** | Other pending state. |
| Anything else | **Failed** | Outright decline / error. |

This rich grammar is why CatalystPay payments may sit at **Requested** longer than other gateways — OPPwa exposes more in-flight states than typical hosted-redirect flows. In particular, a **3DSv2 step-up** (`100.39[765]`) parks the order in Requested until CatalystPay returns a terminal code, at which point the standard mapping applies. The customer sees a pending order page during the step-up window rather than an immediate failure.

### Refunds — strict acknowledgement check

Calling **Refund payment** on a completed CatalystPay order (see [[orders-payment-refund]]) posts a refund with `paymentType=RF`, the full amount, and the original currency. The integration then **strictly validates** the response — `resultDetails.ExtendedDescription` must equal the literal string `"Approved"`; anything else returns "Invalid CatalystPay response after payment". On approval the status flips to **Refunded**. This is unusual — most gateways match a status code; CatalystPay also verifies the human-readable description.

### No authorize-then-capture

Pre-authorisation is **not supported**. Every purchase uses `paymentType=DB` (immediate capture); there is no `PA` (pre-auth) code path, no Capture button, and no Authorize-mode toggle. Merchants who need pre-auth must use a different provider (e.g. [[payment-providers-borica-way4|Borica Way4]] or [[payment-providers-mypos|myPOS]]).

### Plan-tier gating

None — CatalystPay has no `plan_gates` declaration.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where CatalystPay is installed / uninstalled.
- [[orders-payment-refund]] — refund initiation for CatalystPay payments.
- [[payment-provider]] — entity definition.
- [[payment-status]] — Completed / Requested / Refunded / Failed mapping.
- [[checkout-flow]] — concept page on the storefront checkout (CatalystPay surfaces as an embedded module).
- [[payment-providers-mypos]] — comparable card gateway with comparable embedded options.

## Open questions

(none)
