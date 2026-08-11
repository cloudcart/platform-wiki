---
type: feature
nav_path: "Payment Providers → Instamojo"
route_name: apps.instamojo.settings
route_path: /admin/payment-providers/instamojo
aliases: ["Instamojo", "Indian payment gateway", "INR payments", "Instamojo iframe", "Instamojo redirect"]
tags: [paymentproviders, payment-providers, instamojo, india, inr, deprecated, redirect, iframe]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---
# Instamojo

## Purpose

**Instamojo** is an Indian payment aggregator that lets merchants accept cards, UPI, net banking, and wallets (Paytm, etc.) in **Indian Rupees (INR)**. CloudCart's integration uses Instamojo's hosted **Payment Request** flow: the platform creates a payment request server-side, the customer is sent to the Instamojo-hosted checkout (full-page redirect, or an iframe overlay if `enable_iframe` is set) to pick a method and pay, and after payment Instamojo redirects the customer back and sends a webhook to confirm the final state.

**Instamojo is deprecated.** It is excluded from the storefront payment-method picker, so **new merchants cannot install it**. Existing installations keep working (active payments, refunds, syncs, and webhooks all function). This page is retained for merchants with a grandfathered configuration.

## Where to find it

Sidebar → **Payment Providers** → **Instamojo**, at route `/admin/payment-providers/instamojo`. The internal provider key is `instamojo`. The screen is **only visible to merchants who already have it installed** — it is not listed for new installs.

Instamojo still ships the older settings form (the legacy box / box-section layout), not the modern Vue settings UI used by current providers.

## What the merchant can do here

- **View / Uninstall** the Instamojo method (install is blocked for new tenants — see *Deprecated*).
- **Toggle Active** on / off in the header.
- **Switch between Test and Live mode** — each mode has its own API Key + Auth Token + Salt set.
- **Enter Test credentials**: Test API Key, Test Auth Token, Test Salt (sandbox).
- **Enter Live credentials**: Live API Key, Live Auth Token, Live Salt (production).
- **Override the customer-facing label** — logo, title, description on the storefront.
- **Set an amount range** (min / max) and an optional **discount** for the method.
- **Refund a completed Instamojo payment** from the order page — see [[orders-payment-refund]].

Iframe-overlay mode exists as a runtime flag (`enable_iframe`) but has **no toggle in the settings form** — see *Settings & fields*.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Mode** (`configuration.mode`) | Switches between Instamojo test (sandbox) and live (production). One checkbox: checked → `live`, unchecked → `test`. | `test` | `test` / `live`. |
| **Test API Key** (`configuration.test_api_key`) | Instamojo API key for the sandbox. | Empty | `required`, label "Test Api Key". |
| **Test Auth Token** (`configuration.test_auth_token`) | Instamojo auth token for the sandbox. | Empty | `required`, label "Test Auth Token". |
| **Test Salt** (`configuration.test_salt`) | HMAC salt for signing requests in test mode. | Empty | `required`, label "Test Salt". |
| **Live API Key** (`configuration.live_api_key`) | Instamojo API key for production. | Empty | `required`, label "Live Api Key". |
| **Live Auth Token** (`configuration.live_auth_token`) | Instamojo auth token for production. | Empty | `required`, label "Live Auth Token". |
| **Live Salt** (`configuration.live_salt`) | HMAC salt for signing requests in production. | Empty | `required`, label "Live Salt". |
| **Enable iframe** (`configuration.enable_iframe`) | When set, renders the Instamojo checkout inside an iframe overlay instead of a full-page redirect. | OFF | **Runtime-only flag — NOT in the settings form.** Honoured only if a previously-stored config already carries it; the merchant cannot turn it on from the current admin UI. |
| **Logo / Title / Description** | Standard storefront-label override. | Provider defaults | |
| **Min / Max amount** | Range filter for the method. | Empty | |
| **Discount** | Discount applied when the customer picks Instamojo. | None | |

All six credential fields are visible at once (no conditional show/hide), and **all six are required regardless of which mode is active** — there is no per-mode conditional rule. In practice merchants paste sandbox values into the test fields and production values into the live fields before going live. The mode switch only controls which credential set is used at runtime. The form also shows a read-only **webhook URL** for reference (`/webhook/instamojo`).

## Business rules

### Deprecated — no new installs

Instamojo is on CloudCart's deprecated-provider list, which removes it from the storefront payment-method picker. Merchants with an **existing** installation keep full functionality (refunds, syncs, webhook handling); **new tenants cannot install it**. There is **no deprecation banner** in the UI — existing merchants see a normal settings page. (Sofort is deprecated the same way: the code is kept for historical-payment reconciliation, but onboarding is closed.)

### Customer flow — redirect (or iframe overlay)

The standard flow is a **hosted redirect**:

1. The platform creates an Instamojo payment request server-side with the amount (in INR, rounded to 2 decimal places, e.g. `123.45`), a purpose string (`Payment #<payment_id>`), the buyer's email and full name (when a billing address exists), a return URL of `/payments.return/instamojo`, and a webhook URL of `/payments.webhook/instamojo`.
2. Instamojo returns a hosted-checkout URL.
3. The platform sends the storefront a `redirect` action with that URL; the browser navigates to Instamojo.
4. The customer picks a method (UPI, card, net banking, etc.) and completes the transaction on Instamojo's page.
5. Instamojo posts a webhook to `/payments.webhook/instamojo` (server-to-server, source of truth) and also redirects the customer to `/payments.return/instamojo` (customer-facing).

When **iframe mode is ON**, the storefront renders the Instamojo URL inside an iframe overlay rather than navigating away — the customer never visually leaves CloudCart.

### Two return paths

- **Customer return** (`/payments.return/instamojo`) — the browser bounce-back. Reads the payment id from the return query string, fetches the latest state from Instamojo, and persists the status.
- **Webhook** (`/payments.webhook/instamojo`) — the server-side notification. Validates the signature, then persists the final status. This is **the source of truth**: even if the customer closes the browser, loses network, or is blocked by an ad-blocker before redirect, the webhook delivers the final state.

Instamojo's response status (`Credit`, `Pending`, `Failed`, etc.) is mapped to a CloudCart payment status — see [[payment-status]] for the canonical set.

### Refunds

Calling **Refund payment** on a completed Instamojo order (see [[orders-payment-refund]]) issues a refund request to Instamojo against the stored provider reference. Only **full refunds** are supported — partial refunds are not exposed. On success the payment flips to Refunded.

### Sync handles two reference flavours

Instamojo issues two kinds of reference: **MOJO**-prefixed payment IDs (the final transaction ID) and **payment-request IDs** (the pre-transaction reference). Sync detects which is stored and queries the matching Instamojo endpoint, so reconciliation works whether the order recorded a completed payment or only the pending request.

### Plan-tier gating

None at the integration level. The deprecation flag is the only access control — new tenants cannot install.

## Related

- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global list where Instamojo is installed / uninstalled (existing tenants only).
- [[orders-payment-refund]] — refund initiation for Instamojo payments.
- [[payment-provider]] — entity definition.
- [[payment-status]] — status mapping.
- [[checkout-flow]] — storefront checkout concept.

## Open questions

_None._
