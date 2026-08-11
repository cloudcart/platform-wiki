---
type: feature
nav_path: "Payment Providers → Borica Way4 → Settings & fields"
route_name: apps.borica_way4.overview
route_path: /admin/payment-providers/borica_way4
aliases: ["Borica Merchant ID", "Borica MID", "Borica EGW_SECURITY", "Borica MAC_GENERAL", "Borica MAC_ADVANCED", "Borica currency", "Borica BGN", "Borica EUR", "Borica EGW_MERCH_BACKREF", "Borica return URL"]
tags: [paymentproviders, payment-providers, borica-way4, settings, fields, currency]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-borica-way4]]. See the hub for related aspects (setup/CSR, payment lifecycle, authorize/capture, save card, refund/sync).

# Borica Way4 — Settings & fields

## Purpose

Once Phase 1 (CSR + certificate) is complete — see [[borica-way4-setup-csr]] — the page renders the full per-environment settings layout. This aspect catalogues every visible non-certificate field on that layout: Test/Live mode switch, MID, signing algorithm (`EGW_SECURITY`), currency, the storefront-facing labels, the amount range and discount, the authorization mode, and the read-only **EGW_MERCH_BACKREF** return-URL display the merchant copy-pastes into Borica's terminal configuration.

## Where to find it

Sidebar → **Payment Providers** → **Borica Way4** → **Settings** tab. Route: `/admin/payment-providers/borica_way4`. After certificate setup, the settings page renders four cards stacked vertically:

1. **Borica Way4 environment** — the per-environment config card.
2. **Save customer card settings** — toggle described in [[borica-way4-save-card-wallets]].
3. **Google Pay / Apple Pay settings** — toggle described in [[borica-way4-save-card-wallets]].
4. **EGW_MERCH_BACKREF** — read-only return-URL card.

## What the merchant can do here

- **Switch between Test and Live** mode using the radio at the top.
- **Set the Currency** for each environment (BGN or EUR).
- **Set the Merchant ID (MID)** Borica issued alongside the terminal.
- **Pick the security mode** (signing algorithm): `MAC_GENERAL` (newer, SHA-256) or `MAC_ADVANCED` (legacy).
- **Configure the standard payment-method options**: Logo / Title / Description, Min / Max amount, optional Discount, Authorization mode.
- **Copy the EGW_MERCH_BACKREF return URL** the merchant needs to give to Borica.
- **Copy the EGW_TERM_GROUP value** (`SAVE_TOKEN` or `SALE`).

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Logo** | Provider logo override shown on storefront checkout. | Provider default | Standard logo section. |
| **Title / Description** | Customer-facing payment method label and rich-text description. | "Pay with card" | Standard payment-provider settings fields. |
| **Mode** radio | Switches between Test and Live environment. | Test | Cannot switch to live unless live certificates are present — see [[borica-way4-setup-csr]]. |
| **Amount from / to** | Order total range in which Borica appears at checkout. | Empty (any amount) | Standard payment-method gating. |
| **Discount** | Optional fixed / percent discount on this payment method. | None | Standard. |
| **Authorization mode** | Auto-capture (charge immediately) vs Manual capture (authorize now, capture later). | Auto-capture | Server returns *"Your plan does not support authorized payments."* if the current plan lacks the `authorize_payment` feature — see [[plan-gates]] and [[borica-way4-authorize-capture]]. |
| **Merchant ID (MID)** | Borica-issued merchant identifier passed in every transaction. | Empty | If empty, the platform's Site ID is used as fallback. |
| **EGW_SECURITY** dropdown | Signature algorithm: `MAC_GENERAL` (SHA-256, newer) or `MAC_ADVANCED` (older). | `MAC_ADVANCED` | Must match the terminal's provisioning at Borica. No auto-detection. |
| **Currency** (test) | Either BGN or EUR for the test terminal. | `site('currency')` (typically BGN) | Each terminal is provisioned for one currency at Borica. |
| **Currency** (live) | Either BGN or EUR for the live terminal. | `site('currency')` (typically BGN) | Each terminal is provisioned for one currency at Borica. |
| **Save Customer Card** switch | Enables MERCH_TOKEN_ID tokenisation — see [[borica-way4-save-card-wallets]]. | `no` | `yes` / `no` only. |
| **Enable Google Pay / Apple Pay** switch | Adds wallet buttons on checkout — see [[borica-way4-save-card-wallets]]. | `0` (off) | `1` / `0`. Wallets must also be enabled by Borica on the terminal. |
| **EGW_MERCH_BACKREF URL** display | The return URL the merchant copy-pastes into Borica's terminal configuration. | `<cc_payments_domain>/return/provider/borica_way4` | Read-only. |
| **EGW_TERM_GROUP** display | Dynamically reads `SAVE_TOKEN` when **Save Customer Card** is ON, otherwise `SALE`. | `SALE` | Read-only. Merchant copy-pastes this into Borica's terminal form as well. |

The **Currency** fields are duplicated per environment via `dependField: configuration.mode` — only the matching currency input shows for the active mode.

## Business rules

### Currency provisioning is per terminal

Each Borica terminal is provisioned at the bank for **either BGN or EUR**, not both. The merchant picks the matching currency per environment. If a customer places an order in a different storefront currency, the platform converts the amount on the fly using the store's currency rates before sending to Borica. Amounts are sent in **stotinki / cents** (minor units — multiplied by 100). The merchant should still align the storefront currency with the Borica terminal to avoid rounding surprises.

### EGW_SECURITY must match Borica's bank-side configuration

The `EGW_SECURITY` value selects which HMAC algorithm signs the request: `MAC_GENERAL` (SHA-256, newer) or `MAC_ADVANCED` (legacy). There is **no auto-detection** of Borica's bank-side setting. If Borica changes the merchant's MAC algorithm at the bank level, the merchant must update this field manually — otherwise every transaction will fail signature verification.

### Merchant ID (MID) fallback

If the **Merchant ID** field is left empty, the platform falls back to using the store's internal **Site ID** as the `MERCHANT` field in Borica requests. This works for Borica testing but a real production terminal will be tied to a specific Borica MID — leaving this empty in live mode is almost always a misconfiguration.

### Plan-tier gating

The provider itself has no plan gate — any plan that allows installing payment providers can install Borica Way4. The **Authorize + Capture** option in the Authorization-mode dropdown is plan-gated through the `authorize_payment` feature key — lower-tier plans see the dropdown but the server rejects the save with *"Your plan does not support authorized payments."* See [[plan-gates]] and [[borica-way4-authorize-capture]] for details. Save-card and wallets are not separately gated.

### EGW_MERCH_BACKREF + EGW_TERM_GROUP — what the merchant gives Borica

When the merchant's bank registers the terminal, Borica asks for the return URL where the customer is POSTed back after payment and the "TERM_GROUP" identifying which transaction-type group this terminal uses. The merchant copy-pastes both values from this screen:

- **Return URL**: `<cc_payments_domain>/return/provider/borica_way4`. Same URL used for both customer-redirect-back and IPN — see [[borica-way4-payment-lifecycle]].
- **EGW_TERM_GROUP**: `SAVE_TOKEN` when **Save Customer Card** is ON, otherwise `SALE`. Toggling Save Customer Card flips this value and the merchant must re-submit it to Borica if changed.

### Field-card visual mode indication

The Save Customer Card and Google Pay / Apple Pay cards have a border colour that follows the current mode (`border-color-live` when live, `border-color-test` when test) so the merchant always sees which environment they're configuring.

## Related

- [[payment-providers-borica-way4]] — hub.
- [[borica-way4-setup-csr]] — the certificate / Terminal ID prerequisite to this screen.
- [[borica-way4-payment-lifecycle]] — uses the return URL configured here as the IPN destination.
- [[borica-way4-authorize-capture]] — depends on the `authorize_payment` plan-feature gating noted above.
- [[borica-way4-save-card-wallets]] — wallets + Save Customer Card switches that live in the bottom three cards.
- [[plan-gates]] — concept page on the `authorize_payment` feature gating.

## Open questions

(none)
