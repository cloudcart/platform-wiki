---
type: feature
nav_path: "Payment Providers → DSK Bank → Settings & fields"
route_name: apps.dsk_bank.overview
route_path: /admin/payment-providers/dsk_bank
aliases: ["DSK Bank settings", "DSK Bank fields", "DSK test credentials", "DSK live credentials", "DSK API version", "DSK terminal currency", "DSK two-card settings"]
tags: [paymentproviders, payment-providers, dsk-bank, card-gateway, settings, bulgaria]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-dsk-bank]]. See the hub for related aspects (payment lifecycle, authorize/capture, refund/currency).

# DSK Bank — Settings & fields

## Purpose

This aspect documents the **Settings page** of the DSK Bank provider: the Test vs Live credential cards, the per-environment fields (Username, Password, API Version, Currency), and the standard shared payment-method options every provider exposes (Logo / Title / Description, amount range, discount, authorization mode). Authentication uses **username + password** (HTTP Basic) issued by DSK — no client certificates to upload.

## Where to find it

Sidebar → **Payment Providers** → **DSK Bank** → the **Settings** tab (the default landing tab on the provider overview). Route: `/admin/payment-providers/dsk_bank`.

## What the merchant can do here

- **Switch between Test and Live** environments using the **Mode** radio.
- **Enter test credentials** — Test Username, Test Password, Test API Version (`2020` or `2022`), Test Currency (BGN / EUR / USD / RON).
- **Enter live credentials** — Live Username, Live Password, Live API Version, Live Currency.
- **Configure standard payment-method options** shared with all providers: Logo / Title / Description, Min / Max amount, optional Discount, Authorization mode (auto / manual capture — see [[dsk-bank-authorize-capture]]).

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Logo** | Provider logo override shown on storefront checkout. | Provider default | Standard logo section. |
| **Title / Description** | Customer-facing payment method label and rich-text description. | Provider default | Standard. |
| **Mode** radio | Test or Live environment. | Test | Switching to Live requires Live credentials to be filled. |
| **Amount from / to** | Order total range in which DSK Bank appears at checkout. | Empty (any amount) | Standard. |
| **Discount** | Optional fixed / percent discount when buyer picks DSK Bank. | None | Standard. |
| **Authorization mode** | Auto-capture vs Manual (Two-Step) capture — see [[dsk-bank-authorize-capture]]. | Auto | Plan gate: server returns *"Your plan does not support authorized payments."* if the plan lacks `authorize_payment`. |
| **Test Username** | DSK-issued username for the test environment (`epgtest.dskbank.bg`). | Empty | Required if mode is Test. Error: *"Test username is required."* |
| **Test Password** | DSK-issued password for the test environment. | Empty | Required if mode is Test. Error: *"Test Password is required."* |
| **Test API Version** | DSK gateway API version — `2020` or `2022`. | `2020` | DSK tells the merchant which version their terminal supports. |
| **Test Currency** | Currency the test terminal is provisioned for. | From global `currencies` list | One of: BGN (975), EUR (978), USD (840), RON (946). |
| **Live Username** | DSK-issued username for live. | Empty | Required if mode is Live. Error: *"Live username is required."* |
| **Live Password** | DSK-issued password for live. | Empty | Required if mode is Live. Error: *"Live Password is required."* |
| **Live API Version** | API version on live terminal. | `2020` | Same options as test. |
| **Live Currency** | Currency the live terminal is provisioned for. | From global `currencies` list | Same options. |

## Business rules

### Live and test credentials are completely separate

There is no shared key. When **Mode = Test**, the platform calls `epgtest.dskbank.bg`; when **Mode = Live**, it calls `epg.dskbank.bg`. DSK provides test username + password pairs on request — they typically allow specific test card numbers documented in their integration manual.

### API Version is per environment

Each environment carries its own API version (`2020` or `2022`). DSK tells the merchant which version their terminal supports; the test and live terminals can be on different versions.

### Currency is per environment

The terminal currency (BGN / EUR / USD / RON) is stored per environment as a numeric ISO code (975 / 978 / 840 / 946) and mapped to the 3-letter currency. For how a mismatched order currency is handled, see [[dsk-bank-refund-currency]].

## How it works (verified against backend)

### Two-card settings layout

The Settings page renders **two cards** stacked vertically. The standard `rows` above the cards are `['logo', 'mode', 'amount', 'discount', 'auth']` (the `auth` row is the Authorize + Capture toggle). Card border colour follows mode.

1. **Test environment setup** — `editMethod: slide`. Visible only when **Mode = Test**. Locked from editing when **Mode = Live** (`lockEditMethod: mode === 'live'`). Card border: `border-color-test`. Fields stacked top-to-bottom:
   - **Test Username** (string, required, error *"Test username is required."*)
   - **Test Password** (password, required, error *"Test Password is required."*)
   - **Test API Version** select (searchable) — `2022` or `2020`. Not strictly required at field-level.
   - **Test Currency** select (searchable) — options come from `provider.currencies` (a server-provided dropdown pulled from the global currency list, typically BGN / EUR / USD / RON for DSK).
2. **Live environment setup** — `editMethod: slide`. Visible only when **Mode = Live**. Locked when **Mode = Test**. Card border: `border-color-live`. Same four fields with `live_username`, `live_password`, `live_api_version`, `live_currency` keys.

Switching Mode immediately swaps which card displays — the other card hides entirely (no greyed-out preview). The unused environment's credentials remain stored but unreachable from the UI until the merchant switches Mode.

### Per-environment configuration keys

Configuration is stored per environment as `username_test|live`, `password_test|live`, `api_version_test|live` (`2020` or `2022`), `currency_test|live` (numeric ISO 975 / 978 / 840 / 946 → mapped to the 3-letter currency). Test endpoint: `epgtest.dskbank.bg`. Live endpoint: `epg.dskbank.bg`.

## Related

- [[payment-providers-dsk-bank]] — hub.
- [[dsk-bank-payment-lifecycle]] — what happens at checkout once these credentials are set.
- [[dsk-bank-authorize-capture]] — the Authorization-mode dropdown's Auto vs Manual semantics.
- [[dsk-bank-refund-currency]] — how the terminal Currency field interacts with the order currency.
- [[payment-providers]] — parent payment-providers hub.
- [[settings-payment-providers]] — global payment-providers list.
- [[plan-gates]] — the `authorize_payment` plan feature gating the Authorization mode.

## Open questions

- None.
