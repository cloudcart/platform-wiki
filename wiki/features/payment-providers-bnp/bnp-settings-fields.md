---
type: feature
nav_path: "Payment Providers → BNP Paribas Personal Finance → Settings & fields"
route_name: apps.bnp.settings
route_path: /admin/payment-providers/bnp
aliases: ["BNP settings", "BNP fields", "BNP configuration", "BNP validation", "BNP POS ID", "BNP merchant code", "BNP eCom credentials", "BNP no test mode", "BNP live-only UI"]
tags: [paymentproviders, payment-providers, bnp, bulgaria, credit, settings, validation, postbank]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-bnp]]. See the hub for the other aspects (credit flow, eligibility & promotions, market positioning).

# BNP — settings & fields

## Purpose

This page is the complete reference for the BNP settings panel — every configurable field, its default and validation rule, the live-only UI layout (there is no test card), and the "no actual test mode" runtime behaviour. It is the page to read for "what do I enter where?" and "why is my BNP setting rejected?".

## Where to find it

Sidebar → **Payment Providers** → **BNP Paribas Personal Finance**. The route is `apps.bnp.settings` (`/admin/payment-providers/bnp`). The panel is rendered by the shared `SettingsFormPayments` Vue component.

## What the merchant can do here

- **Enter the credentials Postbank issues** — Merchant Code, POS ID (live), optional POS ID 2, contact email.
- **Configure the eCom API** — toggle it on, enter client ID / secret, upload the certificate and enter its password.
- **Toggle the record-keeping email** (`send_email_after_checkout`).
- **Set the storefront-label overrides** (Logo / Title / Description) and the standard Min / Max amount + Discount.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Email** (`configuration.email`) | Where Postbank receives the request emails. | `the provider's support address` | Required, must be valid email. |
| **Merchant code** (`configuration.code`) | 10-character merchant code issued by BNP/Postbank. | Empty | Required. Exactly 10 chars. |
| **Test POS ID** (`configuration.merchant_id_test`) | POS ID for sandbox. | Empty | Required when mode = test. Error: "POS ID is required" |
| **Live POS ID** (`configuration.merchant_id_live`) | POS ID for live. | Empty | Required when mode = live. Error: "POS ID is required" |
| **POS ID 2 (test/live)** (`configuration.pos_id2_test`, `pos_id2_live`) | Separate POS for BNP-branded card products — see [[bnp-eligibility-promotions]]. | Empty | Optional. |
| **Minimum price** (`configuration.min_price`) | Hide BNP if order total is below this amount — see [[bnp-eligibility-promotions]]. | 75 BGN | Required. Error: "Minimum price is required" |
| **eCom enabled** (`configuration.ecom_enabled`) | When ON, use the online API instead of email-only flow — see [[bnp-credit-flow]]. | OFF | |
| **eCom Client ID** (`configuration.ecom_client_id`) | OAuth client ID for BNP eCom API. | Empty | Required when ecom_enabled = 1. |
| **eCom Client Secret** (`configuration.ecom_client_secret`) | OAuth client secret for BNP eCom API. | Empty | Required when ecom_enabled = 1. |
| **eCom certificate (test/live)** (`configuration.ecom_certificate_test`, `_live`) | Client certificate for the eCom API (mutual TLS). | Empty | |
| **eCom password (test/live)** (`configuration.ecom_password_test`, `_live`) | Certificate password. | Empty | |
| **Send request email after checkout** (`configuration.send_email_after_checkout`) | Even with eCom on, send the legacy email too. | OFF | |
| **Logo / Title / Description** | Standard storefront-label override. | Provider defaults | |
| **Min / Max amount** | Standard amount-range filter (separate from `min_price`). | Empty | |
| **Discount** | Discount applied when customer picks BNP. | None | |

## Business rules

### No actual test mode

The integration's `loadConfig` **hard-codes `test_mode = false` and `postfix = '_live'`** regardless of the merchant's mode setting. This means test credentials cannot currently be used through the standard switch — the merchant can configure live BNP and that's it. To test, the merchant must arrange a sandbox merchant code with Postbank and configure that as their live values. (The mode switch in the UI remains for backward compatibility but doesn't affect runtime behaviour.)

### Settings UI layout (verified 2026-05-27)

Layout of route `apps.bnp.settings` (no environment-mode radio — `bnp` is in the `is-modes: false` list in `Index.vue`):

1. **Header + Tabs + Logo** (`no-description: true`). `rows: ['logo']` — no mode, no amount-from-to, no discount.
2. **SettingsBox — BNP-specific** (three cards):
   - **Live environment** (key `live`, edit method `panel`, **`isVisible: mode === 'live'`**, lock when `mode === 'test'`, border-color-live). Six fields rendered inline:
     - `configuration.code` — required string. Label "Merchant Code in BNP Paribas PF".
     - `configuration.min_price` — required number. Label "Minimum amount". Unit: store currency sign. Help: "Minimum order value".
     - `configuration.merchant_id_live` — required string, full-width. Label "POS ID for Live environment". Placeholder "This POS ID is provided from BNP Paribas".
     - `configuration.pos_id2_live` — optional string, full-width. Label "POS ID 2 (for BNP cards) for Live Environment".
     - Separator line.
     - **ViewCert component** — read-only display of the parsed certificate metadata in `settings.configuration.cert` (subject, issuer, expiry).
   - **Ecom API** (key `ecom`, edit method `panel`, **`isVisible: mode === 'live'`**, lock when `mode === 'test'`, border-color-live). Fields:
     - `configuration.ecom_enabled` — switch (`trueValue: 1`, `falseValue: 0`).
     - `configuration.ecom_client_id` — string, full-width. Placeholder "Enter API key". Required when `ecom_enabled === 1` (backend validator).
     - `configuration.ecom_client_secret` — string, full-width. Placeholder "Enter API secret". Required when `ecom_enabled === 1`.
     - `configuration.ecom_certificate_live` — file upload. Help: "Choose the certificate provided by BNP Paribas for Live Environment".
     - `configuration.ecom_password_live` — password, full-width. Placeholder "Enter the password provided by BNP Paribas for Live Environment".
     - Separator line.
     - **ViewCert component** — displays parsed Ecom certificate metadata from `settings.configuration.cert_ecom`.
   - **PB Personal Finance settings** (key `settings`, edit method `panel`, always visible). Two fields:
     - `configuration.send_email_after_checkout` — switch (`trueValue: 1`, `falseValue: 0`). Label "Send an inquiry immediately after completing an order".
     - `configuration.email` — required string. Help: "Please enter a valid Email of the leasing institution you have chosen".
3. **SubmitChanges** sticky bar.

### Per-field validation (`Bnp/ConfigurationValidator.php`)

| Field | Rule | Message |
|---|---|---|
| `configuration.email` | `required\|email` | "Email is required" / "Email is not valid" |
| `configuration.code` | `required\|string\|min:10\|max:10` | (the application framework defaults) |
| `configuration.min_price` | `required` | "Minimum price is required" |
| `configuration.merchant_id_test` | `required_if:configuration.mode,test` | "POS ID is required" |
| `configuration.merchant_id_live` | `required_if:configuration.mode,live` | "POS ID is required" |
| `configuration.ecom_client_id` | `required_if:configuration.ecom_enabled,1` | (default) |
| `configuration.ecom_client_secret` | `required_if:configuration.ecom_enabled,1` | (default) |

`configurationDefault.bnp = { min_price: 75, mode: 'live', ecom_enabled: 0 }`. Additional defaults arrive in `provider.meta` (server-supplied) and are spread into `configuration` if not already set.

### Conditional UI behaviour

- The Live and Ecom cards are only rendered when `mode === 'live'`. There is **no Test card defined in the Vue file** (despite the backend validator handling `merchant_id_test`) — the form has been simplified to live-only since BNP's test environment is not exposed to merchants.
- Within the Ecom card, the secret/cert/password fields are always rendered but are validated only when `ecom_enabled === 1`.
- The PB Personal Finance settings card (email + send_email switch) is always visible regardless of mode.

## Related

- [[payment-providers-bnp]] — hub.
- [[bnp-credit-flow]] — how the `ecom_enabled` / `send_email_after_checkout` switches change the runtime flow.
- [[bnp-eligibility-promotions]] — `min_price` and the two POS IDs whose fields live in this panel.
- [[payment-provider]] — entity definition.
- [[settings-payment-providers]] — global list where BNP is installed / uninstalled.

## Open questions

(none)
