---
type: feature
nav_path: "Payment Providers → Stripe → Settings & fields"
route_name: apps.stripe.settings
route_path: /admin/payment-providers/stripe
aliases: ["Stripe settings", "Stripe keys", "Stripe secret key", "Stripe publishable key", "Stripe test mode", "Stripe live mode", "Stripe configuration", "Stripe API key validation"]
tags: [paymentproviders, payment-providers, stripe, settings, validation, api-keys]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-stripe]]. See the hub for related aspects (checkout flow, save card, refunds/sync).

# Stripe — Settings & fields

## Purpose

This aspect documents the Stripe settings screen the merchant configures: the **Test mode ↔ Live mode** switch, the four API-key fields, the Save-Customer-Card toggles, the common storefront options (name, logo, amount range, discount), the per-field server-side validation, and the **live API ping on Save** that makes a broken key impossible to save.

## Where to find it

Payment Providers → **Stripe** → the single **Settings** tab. Route: `/admin/payment-providers/stripe` (`apps.stripe.settings`). The screen is a Vue Single Page App rendering the Stripe-specific edit form.

## What the merchant can do here

- Toggle the provider **Active** (Enable / Disable button in the header status bar).
- Switch between **Test mode** and **Live mode** with the Test mode switch (the "switch.live" toggle).
- Enter the **Test Secret Key** and **Test Publishable Key** for sandbox testing.
- Enter the **Live Secret Key** and **Live Publishable Key** for production.
- Toggle **Save Customer Card** independently for test and live modes (behaviour on [[stripe-save-card]]).
- Configure the storefront name, logo, accepted-amount range (from/to), and an optional discount when paying with Stripe (flat / percent / shipping-free).
- Save: triggers a live API ping to Stripe with the credentials to verify they work.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|---|---|---|---|
| **Test mode** switch | Toggles between Stripe sandbox and live processing. ON: test mode (no real charges). OFF: live mode. | Test mode ON (sandbox) | Stored as `configuration.mode = "test"` or `"live"`. Live toggle text reads "Live mode". |
| **Test Secret Key** | Stripe sandbox API secret key (starts with `sk_test_...`). | empty | Required when mode = test. Must not contain whitespace (`regex:/^\S+$/`). On save, the Stripe API is called with this key — failure returns a Stripe-specific error inline. |
| **Test Publishable Key** | Stripe sandbox publishable key (starts with `pk_test_...`). | empty | Required when mode = test. Must not contain whitespace. Used by Stripe Checkout JS in the customer's browser. |
| **Live Secret Key** | Stripe production API secret key (starts with `sk_live_...`). | empty | Required when mode = live. Must not contain whitespace. Validated against Stripe's live API on save. |
| **Live Publishable Key** | Stripe production publishable key (starts with `pk_live_...`). | empty | Required when mode = live. Must not contain whitespace. |
| **Save Customer Card** (test) | Whether to save card on file for sandbox-mode purchases. | ON | Stored as `configuration.test_save_card` (boolean). See [[stripe-save-card]]. |
| **Save Customer Card** (live) | Whether to save card on file for live-mode purchases. | ON | Stored as `configuration.live_save_card` (boolean). Only saves when the customer is signed in (not a guest). |
| **Storefront name** | Display name customers see at checkout. | "Stripe" | Common to all payment providers. |
| **Logo** | Provider logo image. | Stripe default | Uploaded image. |
| **Amount from / Amount to** | Order-amount range — Stripe is shown only when the cart total falls inside this range. | empty / empty (no limits) | Common gate. |
| **Discount when paying with Stripe** | Flat / percent / free-shipping discount applied when the customer chooses Stripe. | none | Common option. |

### Per-field validation (server-side)

| Field | Rule | Error message |
|---|---|---|
| `configuration.test_secret_key` | `required_if:configuration.mode,test` AND `regex:/^\S+$/` | "Test Secret Key is required" / "Test Secret Key must not contain whitespace" |
| `configuration.test_publishable_key` | `required_if:configuration.mode,test` AND `regex:/^\S+$/` | "Test Publishable Key is required" / "...must not contain whitespace" |
| `configuration.live_secret_key` | `required_if:configuration.mode,live` AND `regex:/^\S+$/` | "Live Secret Key is required" / "...must not contain whitespace" |
| `configuration.live_publishable_key` | `required_if:configuration.mode,live` AND `regex:/^\S+$/` | "Live Publishable Key is required" / "...must not contain whitespace" |

## Business rules

### A broken key cannot be saved (live ping on Save)

When the merchant clicks Save, the configuration-preparation step runs before persisting:

1. Defaults `mode` to `test` if missing.
2. Coerces `test_save_card` / `live_save_card` from the string `"true"` to boolean.
3. Merges the new fields with the existing stored configuration.
4. Validates by immediately making a `stripe.accounts.retrieve` API call against Stripe using the **active mode's** secret key.

If Stripe rejects the call (bad key, network error, etc.), validation fails and the merchant sees the Stripe error message inline on the relevant key field (`configuration.test_secret_key` or `configuration.live_secret_key`); the Save is rejected. So **the merchant cannot save a broken key** — a working key is required before the form will accept. (A separate runtime safeguard, the self-deactivation on a bad key during a live charge, is on [[stripe-refunds-sync]].)

The **publishable key is not validated server-side** — Stripe has no "verify publishable key" endpoint. It is used by the customer's browser when rendering the Stripe Checkout page.

### Test vs live mode behaviour

Test mode uses Stripe's sandbox with test card numbers like `4242 4242 4242 4242`. Live mode processes real cards and real money. Switching mode just changes which key pair is read; no data migration is needed.

### Permission

The settings page is gated behind the standard payment-provider permission (`store.payment_providers`). There is no `PlanFeature` gate on Stripe — see the hub [[payment-providers-stripe]] and [[plan-gates]].

## How it works (verified against backend) — settings UI surfaces

The page layout, top to bottom:

1. **Header — provider status bar**: provider icon, name, mode pill (orange "Test mode" / green "Live mode"), Active badge, **Enable / Disable** button, and the app's `settings_description`. The mode pill appears only when the configuration is valid.
2. **Tabs row**: single tab "Settings" (no extra tabs for Stripe).
3. **Logo + Storefront name section**: edit the `title` (name shown at checkout) and upload/remove a logo image (removal calls `/admin/payment-providers/remove-image/{id}`).
4. **Payment-method description card** (slide-out, rich-text editor): bound to `configuration.payment_description`; the actual API save happens via the bottom Save bar.
5. **Environment mode card**: two stacked radio options — "Test mode" (orange border) / "Live mode" (green border).
6. **Stripe-specific cards** (top to bottom): **Save customer card — Live** (`live_save_card`, locked when `mode === 'test'`), **Save customer card — Test** (`test_save_card`, locked when `mode === 'live'`), **Live environment setup** (`live_secret_key` + `live_publishable_key`, locked when `mode === 'test'`), **Test environment setup** (`test_secret_key` + `test_publishable_key`, locked when `mode === 'live'`).
7. **Common cards**: **Acceptance based on order amount** (`amount_from` / `amount_to`, unit = store currency), and **Discounts** (`discount_type` Fixed / Percent / Free shipping + `discount_amount`; the amount field is hidden when `discount_type === 'shipping'`).
8. **Sticky bottom bar**: Save button + "Cancel changes" link, shown when the form is dirty.

### Conditional UI behaviour

- The card for the **opposite mode** stays visible but is read-only (`lockEditMethod = true`) — the merchant can see the keys for that environment but cannot edit them until they switch mode.
- Save-Card switches are each locked to their mode (the live save-card is read-only when in test mode, and vice-versa).
- Switching `mode` re-locks/unlocks every row in real time (no full re-render).

## Related

- [[payment-providers-stripe]] — hub.
- [[stripe-save-card]] — behaviour of the Save Customer Card toggles configured here.
- [[stripe-refunds-sync]] — the runtime self-deactivation that complements the save-time key ping.
- [[settings-payment-providers]] — global payment-providers list where Stripe is installed / uninstalled.
- [[payment-provider]] — entity definition.
- [[plan-gates]] — Stripe has no plan gate.

## Open questions

(none)
