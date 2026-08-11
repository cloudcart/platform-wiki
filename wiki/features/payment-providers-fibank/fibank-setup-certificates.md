---
type: feature
nav_path: "Payment Providers → Fibank → Setup & certificates"
route_name: apps.fibank.overview
route_path: /admin/payment-providers/fibank
aliases: ["Fibank certificate", "Fibank PKCS12", "Fibank.p12", "Fibank test environment", "Fibank live environment", "Fibank currency", "Fibank EGate setup", "Сертификат Fibank", "Настройка Fibank"]
tags: [paymentproviders, payment-providers, fibank, card-gateway, bulgaria, certificate]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Fibank — Setup & certificates

> Part of [[payment-providers-fibank]]. See the hub for the other aspects (payment lifecycle, refund / capture).

## Purpose

This page covers how the merchant connects a **Fibank Ecomm (EGate)** terminal to CloudCart: uploading the **PKCS#12 (.p12) client certificate** Fibank issues, entering its password, picking the terminal currency, and switching between Test and Live. Unlike DSK Bank's username/password flow, Fibank authenticates with a mutual-TLS client certificate, so the certificate upload is the central setup step. Get this right and purchases work; leave the live environment empty and every live charge fails Fibank-side.

## Where to find it

Sidebar → **Payment Providers** → **Fibank**. Route: `/admin/payment-providers/fibank`. The setup fields live on the same `AppOverview` settings page — there are no sub-tabs.

## What the merchant can do here

- **Upload the test PKCS#12 certificate** (`.p12`) Fibank provides for the test environment, plus its password.
- **Upload the live PKCS#12 certificate** plus its password.
- **Pick a currency per environment** — BGN (975) or EUR (978).
- **Switch Mode** between Test and Live (reactively toggles which environment card shows).

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Mode** radio | Test or Live. | Test | Live requires the live certificate uploaded. |
| **Test certificate** | PKCS#12 (.p12) file Fibank provides for the test environment. | Empty | Required if mode is Test. MIME must be `application/octet-stream`. Validated with the password — error *"Invalid certificate and/or password"* if either is wrong. Auto-converted to PEM internally. |
| **Test certificate password** | Password Fibank gave alongside the test PKCS#12. | Empty | Required when uploading. Error: *"Certificate password is required"*. Stored in configuration (re-displayed obscured). |
| **Test Currency** | BGN (975) or EUR (978). | None | Required. |
| **Live certificate** | PKCS#12 (.p12) file for live. | Empty | Required when mode is Live. Same validation. |
| **Live certificate password** | Password for the live certificate. | Empty | Required. |
| **Live Currency** | BGN (975) or EUR (978). | None | Required. |

## Business rules

### PKCS#12 certificate handling

Fibank sends the merchant a `.p12` file (binary mutual-TLS client certificate + private key + Fibank CA chain) and a separate password. The merchant uploads the `.p12` to either **Test certificate** or **Live certificate**, types the password, and on save the platform:

1. Reads the `.p12` bundle with the supplied password.
2. Concatenates the private key + certificate into a single PEM block.
3. Stores the PEM in `certificate_test` / `certificate_live`.
4. Stores the filename in `certificate_test_name` / `certificate_live_name` for display.
5. Stores the password (`password_test` / `password_live`) so subsequent saves don't need a re-upload.

Validation errors the merchant may see:

- Wrong password → *"Invalid certificate and/or password"*.
- File isn't a valid PKCS#12 → *"Invalid certificate file"*.
- File missing on first save → *"Certificate file is required"*.

The integration can also convert `.jks` (Java Keystore) → PKCS#12 → PEM if Fibank ever issues a JKS instead, but the UI exposes **only** the `.p12` upload path.

### Currency support

Each Fibank Ecomm terminal is provisioned for **one currency** — **BGN (ISO 975)** or **EUR (ISO 978)**. The merchant picks the currency per environment. The platform reads `currency_test` / `currency_live` and sends it verbatim on every Fibank request. The amount is **NOT auto-converted** by the platform if the storefront currency differs from the terminal currency — the merchant must align them or implement a currency-conversion strategy at checkout level. See [[fibank-payment-lifecycle]] for how the currency is sent on `registerOrder`.

### Mutual-TLS connection

The stored PEM authenticates the merchant to Fibank's Ecomm endpoint over mutual TLS. Connections use a **5-second timeout** and **`ssl_verify=false`** — the PKCS#12 client-cert auth is treated as sufficient.

## UI mechanics (settings card pattern)

The Settings page renders **three cards** stacked vertically. Standard `rows` above: `['logo', 'mode', 'amount', 'discount']` (no description, no auth — Fibank doesn't support two-phase capture).

1. **Fibank test environment** — `editMethod: slide`. Visible only when **Mode = Test** (`isVisible: mode === 'test'`). Locked from editing while Mode = Live. Card border: `border-color-test`. Fields:
   - **Test certificate** (file upload, help block: *"Select PKCS12 certificate, provided by Fibank"*).
   - **Certificate password** (password input, placeholder: *"Enter secret key for test environment"*, multiLine, 12-col width).
   - **Currency** select (required) — `975` (BGN) or `978` (EUR).
2. **Fibank live environment** — `editMethod: slide`. Visible only when **Mode = Live**. Locked while Mode = Test. Card border: `border-color-live`. Same three fields as the test card but with `certificate_live` and `password_live` keys + a *"Enter secret key for live environment"* placeholder.
3. **Return URL** — `editMethod: inline`, `hideTitle: true`, always visible. Renders a single read-only `title` field showing `provider.return_url` — the URL the merchant gives Fibank's onboarding team (see [[fibank-payment-lifecycle]]).

Switching Mode reactively toggles which environment card displays — switching to Live without uploading a live PKCS#12 leaves the live card empty and any purchase will fail with a Fibank-side error.

## Related

- [[payment-providers-fibank]] — hub.
- [[payment-providers]] — payment providers parent hub.
- [[settings-payment-providers]] — global payment-providers list.
- [[payment-provider]] — entity definition.

## Open questions

- ⏸️ Whether Fibank supports multi-currency on a single terminal (BGN + EUR together) — a Fibank commercial decision, not encoded in CloudCart. Workaround for multiple per-currency terminals: install Fibank twice (one per terminal).
