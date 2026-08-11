---
type: feature
nav_path: "Payment Providers → Paynetics → Setup & UI"
route_name: apps.paynetics.overview
route_path: /admin/payment-providers/paynetics
aliases: ["Paynetics setup", "Paynetics settings", "Paynetics API Key", "Paynetics Secret", "Paynetics credentials", "Paynetics enable_iframe", "Paynetics settings card", "Настройки Paynetics"]
tags: [paymentproviders, payment-providers, paynetics, setup, credentials, card-gateway]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-paynetics]]. See the hub for related aspects (payment lifecycle, feature gaps).

# Paynetics — Setup & UI

## Purpose

This aspect covers where the Paynetics screen lives, what the admin UI actually renders, the standard payment-method options the merchant configures, and the credential keys Paynetics needs. The headline fact: the Paynetics settings screen is the **shortest** of any payment provider on the platform — it renders only the standard four-row shell and does **not** render input fields for the API Key / Secret credentials, consistent with the provider's deprecated-for-new-tenants status.

## Where to find it

Sidebar → **Settings** → **Payments** → click **Paynetics** (only visible to stores that already have Paynetics configured — new tenants no longer see it in the picker).

Route: `/admin/payment-providers/paynetics`. Route name: `apps.paynetics.overview`. The page renders the standard `AppOverview`, no sub-tabs — settlement and merchant management happen in Paynetics's own portal.

Because the route is commented out of the payment-provider router, **new merchants don't see Paynetics in the picker**. Only stores that already had it configured can navigate to `/admin/payment-providers/paynetics`.

## What the merchant can do here

- **Install / Uninstall** the payment method via the standard overview buttons.
- **Activate / Deactivate** using the header switch.
- **Switch between Test and Live** environments using the radio.
- **Configure standard payment-method options** shared with all providers: Logo / Title / Description, Min / Max amount, optional Discount.

Note: the API Key / Secret credentials are read from stored configuration at runtime, but the current Vue settings UI does **not** render input fields for them — see *Settings & fields* below.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Logo** | Provider logo override on storefront checkout. | Provider default | Standard. |
| **Title / Description** | Customer-facing payment method label. | Provider default | Standard. |
| **Mode** radio | Test or Live. | Test | Switching to Live requires Live API key + secret. |
| **Amount from / to** | Order total range where Paynetics appears at checkout. | Empty (any amount) | Standard. |
| **Discount** | Optional fixed / percent discount when buyer picks Paynetics. | None | Standard. |
| **Test API Key** (`test_api_key`) | Paynetics-issued API identifier for sandbox. | Empty | **No server-side required-validation** — nothing enforces this as required. Read into the `payoo-api-key` HTTP field at runtime. |
| **Test Secret** (`test_secret`) | Paynetics-issued HMAC signing secret for sandbox. | Empty | No required-validation. Used as the HMAC-SHA256 signing secret for request signing — see [[paynetics-payment-lifecycle]]. |
| **Live API Key** (`api_key`) | Paynetics-issued API identifier for production. | Empty | No required-validation. |
| **Live Secret** (`secret`) | Paynetics-issued HMAC signing secret for production. | Empty | No required-validation. |
| **iframe option** (`enable_iframe`) | Legacy boolean — embed Paynetics's page in an iframe vs full redirect. | `false` | Not exposed in the current Vue UI; stored in the configuration for forward compatibility. |

The Vue settings file is minimal — it renders ONLY the standard `SettingsFormPayments` shell with the four rows `['logo', 'mode', 'amount', 'discount']`, and **no provider-specific credential card**. In other words, the current Vue UI surfaces logo, mode, amount range and discount, but does **not** render input fields for the API Key / Secret. The credential keys (`test_api_key` / `test_secret` / `api_key` / `secret`) exist in the stored configuration and are read at runtime, but there is no editing surface for them in the current admin UI.

## Business rules

### UI mechanics — the shortest settings card on the platform

The `Settings.vue` is a 30-line file that just renders `SettingsFormPayments` with `rows: ['logo', 'mode', 'amount', 'discount']`. There is **no custom `#settings` slot**, no `SettingsBox` cards, no environment-specific layouts. This means:

- **No per-environment card splitting** — test/live credentials are NOT split into two cards like Borica / Fibank / DSK; there is no credential card at all.
- **No file uploads, no certificate UI** — Paynetics uses plain API Key + Secret, not certificates.
- **No sub-modals, no JSON certificate viewer.**
- Activate / Deactivate / Mode radio still work through the shared `SettingsFormPayments` shell.

### No required-validation on credentials

Paynetics has no `ConfigurationValidator` — `ConfigurationPreparation` only defaults `mode` and merges; nothing enforces the API Key / Secret as required. A misconfigured (blank-credential) install will not be blocked at save time.

### Plan-tier gating

The provider has **no plan gate**. Any plan that allows payment providers can install Paynetics — but the provider is commented out of the new-tenant picker, so in practice no new store can install it.

## Related

- [[payment-providers-paynetics]] — hub.
- [[settings-payment-providers]] — global payment-providers list where Paynetics is installed / uninstalled.
- [[payment-provider]] — entity definition.

## Open questions

_None._
