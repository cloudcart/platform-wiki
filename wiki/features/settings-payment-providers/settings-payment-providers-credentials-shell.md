---
type: feature
nav_path: "Settings → Payment methods → Per-gateway credentials (shared shell)"
route_name: admin.payments
route_path: /admin/settings/payment_providers
aliases: ["Payment provider credentials index", "Per-gateway credentials map", "SettingsFormPayments shell", "Shared payment-provider settings layout", "Какво трябва да въведа за платежен метод"]
tags: [settings, payments, providers, credentials, downstream-pages]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-payment-providers]]. See the hub for related aspects (list, Add modal, filtering, activation, uninstall, record fields).

# Payment methods — Per-gateway credentials (shared shell)

## Purpose

When the merchant clicks an installed row in the Payment methods list, the destination is the provider's own `apps.<provider>.settings` page. Most providers share a **common settings shell** — same outer chrome — but the specific credential fields vary wildly per gateway. This aspect catalogues the **6 reusable row slots** the shared shell exposes (`logo`, `mode`, `amount`, `discount`, `description`, `auth`) and the **per-gateway credentials index** (Stripe, myPOS, Borica Way4, CloudCart Pay, Klear, the long tail) with pointers to each provider's deep-dive page. Anchored from this hub because merchants frequently ask *"what do I need to type for gateway X?"* before installing.

## Where to find it

Sidebar → Settings → **Payment methods**. Each provider's actual credentials page is reached by clicking the provider's row (in the installed list — see [[settings-payment-providers-list]]) or clicking the provider's card in the Add modal (see [[settings-payment-providers-add-modal]]). The destination route is `apps.<provider>.settings`.

The shared shell + per-gateway specifics are described below; deep-dive pages exist for the major providers (linked in Related).

## What the merchant can do here

This aspect itself is a **catalogue**, not a screen. From the per-provider settings pages (reached by click-through from this hub), the merchant can: enter API credentials (varies — see the per-gateway table); switch Test ↔ Live mode (most providers; CloudCart Pay is platform-wide); configure shared shell rows (logo, amount min, discount, storefront description, auth); toggle Save Customer Card (where supported); trigger onboarding flows (e.g., **Manage Onboarding** for CloudCart Pay — see [[payment-providers-cloudcart-pay-onboarding]]).

## Settings & fields

### Shared `SettingsFormPayments` shell — the 6 reusable row slots

Most provider settings pages reuse a common shell that exposes 6 row slots. Providers opt into each row via `:rows="[...]"`. The chrome is consistent across providers; credential fields inside vary.

| Slot | What it controls | Where it ends up |
|------|------------------|------------------|
| `logo` | Custom storefront logo for the payment method. | Override of the stock provider logo on the storefront checkout. |
| `mode` | Test / Live environment toggle. | Switches the per-mode credential pair shown below. Most providers expose both modes side-by-side as two cards. |
| `amount` | Minimum-order-value threshold for exposing this payment method to the customer. | Maps to the `min_price` field on the provider record (see [[settings-payment-providers-record-fields]]). |
| `discount` | Per-method discount (%) applied at checkout when the customer picks this provider. | E.g., "-1% if you pay by card transfer". |
| `description` | Customer-facing label / description override. | Maps to the `storefront_name` field on the provider record. |
| `auth` | Per-provider authentication / onboarding link block. | Varies — most providers show the credential pair here; KYC providers (CloudCart Pay) show the onboarding button. |

### Per-gateway credentials index

| Provider | Mode toggle | Credential fields the merchant fills | Deep-dive page |
|----------|-------------|--------------------------------------|----------------|
| **Stripe** | Test / Live | Per-mode pair: **Secret Key**, **Publishable Key**. Two cards ("Live environment setup" / "Test environment setup") gated by the mode toggle. Plus **Save Customer Card** switch per mode. | _(no dedicated page yet)_ |
| **myPOS** | Test / Live | Per-mode **Configuration package** (paste-only base64 the merchant copies from `www.mypos.eu → menu eCommerce → Online stores`). Test pack is pre-populated. The paste is decoded server-side; test info is shown read-only in a JSON viewer. Plus **Save Customer Card** per mode. | _(no dedicated page yet)_ |
| **Borica Way4** | Test / Live | **Step 1 (one-time):** enter **Terminal ID** (TID), click **Generate CSR** to download a CSR for exchange with Borica. **Step 2 (returning):** upload Borica certificate `.zip` per mode; set **MID**, **EGW_SECURITY** (`MAC_GENERAL` / `MAC_ADVANCED`), **Currency** per mode (BGN / EUR). Plus **Save Customer Card**, **Google Pay / Apple Pay**, **EGW_MERCH_BACKREF** terminal-group block. | [[payment-providers-borica-way4]], [[borica-way4-setup-csr]], [[borica-way4-settings-fields]], [[borica-way4-save-card-wallets]] |
| **CloudCart Pay** | Platform-wide | Connected-account flow — no API keys. Shows **Connected Account ID** + a **Manage Onboarding** button that navigates to KYC. Only on-page setting is **Save Customer Card**. | [[payment-providers-cloudcart-pay]], [[payment-providers-cloudcart-pay-settings]], [[payment-providers-cloudcart-pay-onboarding]] |
| **Klear** | Test / Live | Per-mode **Public Api Key** + **Private Api Key**. Plus **Manually confirm a payment**, **Financing program ID**, **Financing program checkout rule** (`Exclusive` / `Inclusive`). | [[payment-providers-klear]] |
| **PayPal / EasyPay / ePay / FusionPay / DSK BNPL / FiBank BNPL / TBI Bank / Iute / Cardlink / EuPlatesc / Paysera / Paynetics / Raiffeisen / NestPay / Sofort / Settle / Braintree / Libra Pay / Mokka / CPay** | Test / Live (most) | Same shared shell, 6 row slots. Credentials vary — most use API key + Merchant ID pair; BNPL providers expose schemes as a sub-tab (e.g., [[payment-providers-dsk-bnpl-promotions]]). | [[payment-providers-fusion-pay]], [[payment-providers-iute]], [[payment-providers-dsk-bnpl]], [[payment-providers-fibank-bnpl]] |

## Business rules

### The shared shell is the chrome; credentials are the variability

The 6-slot shell is the consistent outer chrome (logo upload, environment toggle, min-order-amount, per-method discount, storefront-name override, auth block). The credential fields **inside** the auth block vary wildly: Stripe wants two keys per mode, Borica wants a CSR exchange + certificate upload, CloudCart Pay wants a KYC flow with no on-page keys at all, myPOS wants a single base64 paste. For full mechanics navigate to the provider's deep-dive page.

### Per-mode credentials are isolated

For providers with Test / Live mode, the two modes carry **separate** credential pairs — flipping to Test does not erase the Live credentials and vice versa. CloudCart Pay is the major exception — it's platform-wide (no per-merchant Test / Live toggle); see [[payment-providers-cloudcart-pay-settings]].

### Credentials live on the provider record, not the platform Settings table

Credentials and per-provider settings are stored on the provider's configuration row — see [[settings-payment-providers-record-fields]] for the field shape. So toggling activity, installing, or uninstalling does NOT flush the platform Settings cache, uninstalling destroys all credentials in one DELETE (see [[settings-payment-providers-uninstall]]), and JSON-API v2 reads the row directly.

### Saving credentials is not the same as activating

Saving valid credentials does NOT automatically activate the provider — the merchant must still flip Status to Active on [[settings-payment-providers-list]], and that toggle can run the activation guard which may ping the gateway to verify the credentials. Full flow: install → enter credentials → save → return to Payment methods → toggle Active → optionally pass the gateway's verification.

## Related

- [[settings-payment-providers]] — hub.
- [[settings-payment-providers-list]] — where the click-through to per-provider pages starts.
- [[settings-payment-providers-add-modal]] — where the click-through from new-install starts.
- [[settings-payment-providers-activation]] — credentials may be verified by the activation guard.
- [[settings-payment-providers-record-fields]] — where credentials are stored on the provider configuration row.
- [[payment-providers-cloudcart-pay]] — CloudCart Pay hub.
- [[payment-providers-cloudcart-pay-settings]] — connected-account, Save Customer Card.
- [[payment-providers-cloudcart-pay-onboarding]] — KYC onboarding flow.
- [[payment-providers-borica-way4]] — Borica Way4 hub.
- [[borica-way4-setup-csr]] — Borica CSR + certificate exchange.
- [[borica-way4-settings-fields]] — Borica MID, security, currency, BACKREF.
- [[payment-providers-klear]] — Klear API keys + financing program settings.
- [[payment-providers-dsk-bnpl]] — DSK BNPL.
- [[payment-providers-dsk-bnpl-promotions]] — DSK BNPL Schemes (sub-tab).
- [[payment-providers-fibank-bnpl]] / [[payment-providers-fusion-pay]] / [[payment-providers-iute]] — per-provider configuration pages.

## Open questions

_None._
