---
type: feature
nav_path: "Payment Providers → Raiffeisen Bank → Setup & credentials"
route_name: apps.raiffeisen.overview
route_path: /admin/payment-providers/kbc
aliases: ["Raiffeisen setup", "Raiffeisen credentials", "Raiffeisen Merchant ID Terminal ID", "Raiffeisen certificate download", "Raiffeisen webhook URL", "Raiffeisen signing algorithm", "KBC Bank environment", "Райфайзен настройка", "Виртуален ПОС Райфайзен настройка"]
tags: [paymentproviders, payment-providers, raiffeisen, kbc, card-gateway, bulgaria, setup]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-raiffeisen]]. See the hub for the other aspects (capture/authorize, save-card, refund/sync/status).

# Raiffeisen Bank — Setup & credentials

## Purpose

This aspect covers how a merchant connects their **Райфайзенбанк** (now KBC Group) e-commerce terminal to CloudCart: entering the Raiffeisen-issued credentials, picking the signing algorithm and currency, downloading the public certificate to register at the bank, and copying the webhook / return URLs back into Raiffeisen's terminal registration. Once these are saved, the provider is ready to take live card payments via Raiffeisen's hosted UPC (Universal Payment Channel) page.

## Where to find it

Sidebar → **Payment Providers** → click **Raiffeisen Bank**.

Route: `/admin/payment-providers/kbc` — the URL path is `/kbc`, **not** `/raiffeisen`. The Vue router registers this provider under the `kbc` URL while keeping the route name `apps.raiffeisen.overview` and the `raiffeisen` provider key. Page renders the standard payment-provider overview; settlement itself lives in Raiffeisen's merchant portal, not here.

## What the merchant can do here

- **Install / Uninstall** the payment method via the standard overview buttons; **Activate / Deactivate** via the header switch.
- **Switch between Test and Live** using the Mode radio.
- **Enter Merchant ID** (Raiffeisen-issued, numeric).
- **Enter Terminal ID** (Raiffeisen-issued, alphanumeric, latin letters + digits only).
- **Pick the signing algorithm** — `sha512` (newer, recommended) or `sha1` (legacy).
- **Pick a currency** — BGN (975) or EUR (978).
- **Download the public certificate** to register at Raiffeisen's side.
- **See the Webhook URL and Return URL** to give Raiffeisen when registering the terminal.
- **Configure standard payment-method options**: Logo / Title / Description, Min / Max amount, optional Discount.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Logo** | Provider logo override on storefront checkout. | Provider default | Standard. |
| **Title / Description** | Customer-facing payment-method label and description. | Provider default | Standard. |
| **Mode** radio | Test or Live. | Test | Switching is unconditional — terminal/merchant IDs alone are enough; the certificate step is bank-side. |
| **Amount from / to** | Order total range where Raiffeisen appears at checkout. | Empty (any amount) | Standard. |
| **Discount** | Optional fixed / percent discount when buyer picks Raiffeisen. | None | Standard. |
| **Merchant ID** | Raiffeisen-issued merchant identifier. | Empty | Required, numeric only. Error: *"Merchant ID is required"* / *"Merchant ID must contain only numbers"*. |
| **Terminal ID** | Raiffeisen-issued terminal identifier. | Empty | Required, latin letters + digits only. Error: *"Terminal ID is required"* / *"Terminal ID must contain only latin letters and numbers"*. |
| **Currency** | BGN (ISO 975) or EUR (ISO 978). | `975` (BGN) | Required. |
| **Signing algorithm** | `sha512` or `sha1` for HMAC signing. | `sha1` (fallback if not set) | Must match Raiffeisen's terminal provisioning. Searchable select. |
| **Download certificate** button | Downloads the platform's public certificate file for the merchant to send to Raiffeisen. | — | Only meaningful after Merchant ID + Terminal ID are saved. |
| **Webhook URL** (notify URL) | Read-only display — the IPN target the merchant gives Raiffeisen. | `<cc_payments_domain>/webhook/kbc` | Path uses `/kbc/` not `/raiffeisen/` — historical naming alias. |
| **Return URL** (success / failure URL) | Read-only display — the customer-return target the merchant gives Raiffeisen. | `<cc_payments_domain>/return/provider/kbc` | Same `/kbc/` path. |

## Business rules

### Bundled CloudCart private keys (security note)

The integration uses a **single CloudCart-issued private key per signing algorithm** bundled with the platform — every merchant on the platform shares the same signing key. Raiffeisen identifies the merchant via the Merchant ID + Terminal ID, **not** via a per-merchant key. The merchant downloads the matching public certificate for Raiffeisen's registration. This is a simpler model than [[payment-providers-borica-way4]]'s per-merchant CSR — the trade-off is that key rotation for Raiffeisen is a platform-wide event, not per-merchant.

### Signing algorithm must match the terminal

Raiffeisen tells the merchant which algorithm (`sha1` or `sha512`) their terminal is provisioned for. A mismatch makes every signature fail. If unset, the platform falls back to `sha1`.

### Currency is single-per-terminal

Raiffeisen terminals are provisioned for a single currency at the bank — typically **BGN** (ISO 975), with **EUR** (ISO 978) also supported. The merchant picks the currency matching their contract.

### Certificate download regenerates against the saved terminal/merchant pair

The *Download certificate* button only appears **after** the Terminal ID has been persisted (the local copy of `terminal_id` must equal the saved one). Clicking it re-saves the settings silently, then auto-downloads the latest certificate file from `/admin/api/payment_providers/raiffeisen/certificate/download`. When the Terminal ID changes after a save, the button hides until the new ID is saved — so the cert regenerates server-side against the new terminal/merchant pair.

### Webhook + return URLs use the `/kbc/` path alias

The merchant copy-pastes these into Raiffeisen's terminal registration:

```
NOTIFY_URL (IPN): <cc_payments_domain>/webhook/kbc
SUCCESS_URL / FAILURE_URL: <cc_payments_domain>/return/provider/kbc
```

The `/kbc/` path is historical — the integration was first built for KBC Group's gateway, and the URL was kept when Raiffeisen joined KBC in 2022. Internally `raiffeisen` and `kbc` map to the same provider key.

### Settings card UI pattern

The Settings page renders **three cards** stacked vertically; the standard rows above them are `['logo', 'mode', 'amount', 'discount', 'auth']` (no description override). Card border colour follows the Mode — `border-color-live` for Live, `border-color-test` for Test.

1. **Save customer card** (`editMethod: inline`, `hideTitle: true`) — one toggle. See [[raiffeisen-save-card]].
2. **KBC Bank environment** (`editMethod: slide`) — Merchant ID, Terminal ID, Currency, Signing algorithm, and the **DownloadCertificate** sub-component.
3. **KBC Bank URL's** (`editMethod: inline`, `hideTitle: true`) — the **Urls** sub-component showing the read-only SUCCESS_URL & FAILURE_URL (`provider.return_url`) and NOTIFY_URL (`provider.webhook_url`).

The **Authorization mode** row sits in the standard rows (`auth`) and gates capture behaviour — see [[raiffeisen-capture-authorize]].

## Related

- [[payment-providers-raiffeisen]] — hub.
- [[payment-providers]] — parent hub.
- [[settings-payment-providers]] — global payment-providers list.
- [[payment-providers-borica-way4]] — per-merchant-CSR card gateway (contrast on key model).
- [[payment-providers-cloudcart-pay]] — CloudCart's own gateway if the merchant has no Raiffeisen e-commerce contract.
- [[payment-provider]] — entity definition.
- [[plan-gates]] — `authorize_payment` gating on the Authorization-mode row.

## Open questions

- ⏸️ Raiffeisen / KBC private-key rotation cadence is a bank-side process not encoded in CloudCart. Keys are bundled with platform code; if the bank rotates, the update ships in a CloudCart release.
