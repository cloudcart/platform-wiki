---
type: feature
nav_path: "Payment Providers → Stripe"
route_name: apps.stripe.settings
route_path: /admin/payment-providers/stripe
aliases: ["Stripe", "Stripe payment", "Stripe gateway", "Card payments international"]
tags: [paymentproviders, payment-providers, stripe, international, card-gateway]
plan_gates: []
created: 2026-05-22
updated: 2026-06-10
source_count: 2
---

# Stripe

## Purpose

**Stripe** is a global card-payment gateway. With this integration, customers reach a Stripe-hosted Checkout page (a redirect flow), pay with their card, and return to the store with the result. Stripe handles the card form, 3D Secure verification, card-network communication, and storing the saved card on Stripe's vaulted-token infrastructure — so the store never touches raw card data.

The integration uses **Stripe Checkout Sessions** (Stripe's hosted checkout page) for the first-time card flow. If the customer was already saved on Stripe (signed-in customer, not a guest) and **Save Customer Card** is on, repeat purchases skip the redirect and use a server-to-server off-session charge. Stripe is the recommended option for global stores wanting to accept cards from international customers in their local currency.

This hub catalogues the four aspect pages this feature splits into. The Assistant should drill into the aspect that matches the question, not read every page.

## Where to find it

Sidebar → **Payment Providers** → click **Stripe**. Route: `/admin/payment-providers/stripe` (`apps.stripe.settings`).

The page renders the Stripe-specific edit form as a Vue Single Page App. From there the merchant lands on the single **Settings** tab — there are no extra sub-tabs (no Onboarding / Transactions / Payouts surfaces, unlike CloudCart Pay), because Stripe settlement and reporting are done in the merchant's own Stripe Dashboard, not through CloudCart.

## Sub-pages (in this cluster)

This feature is split into 4 aspect pages:

- [[stripe-settings-fields]] — the full settings layout (Test/Live mode switch, the four secret/publishable key fields, Save-Card toggles, storefront name/logo, amount range, discount); per-field server-side validation; the live API ping on Save that blocks a broken key.
- [[stripe-checkout-flow]] — the first-purchase hosted Checkout Session redirect flow; amount in minor units; currency handling; transparent 3D Secure; the localized Checkout page (supported-locale list).
- [[stripe-save-card]] — Save Customer Card storage (what gets stored vs what never does); `setup_future_usage = off_session`; the returning-customer silent off-session charge; signed-in-only requirement.
- [[stripe-refunds-sync]] — refunds (full only); the pull-based (webhook-less) `sync` status verification by reference-ID prefix; auto-capture-only behaviour; no Stripe Subscriptions; self-deactivation on bad credentials; no Stripe Connect.

## Settings & fields

This hub does not expose any fields directly. Field-level documentation lives per aspect:

- **Test mode switch, the four secret/publishable keys, Save Customer Card toggles, storefront name/logo, amount range, discount, and all per-field validation** → [[stripe-settings-fields]].

## What the merchant can do here

The hub itself is navigation only — every concrete action lives on an aspect page. The high-level actions, with their aspect:

- **Toggle the provider Active**, switch **Test mode** ↔ **Live mode**, enter the test/live secret + publishable keys, set storefront name/logo, amount range and discount — see [[stripe-settings-fields]].
- **Toggle Save Customer Card** (independently per test/live mode) — behaviour on [[stripe-save-card]].
- **Refund a payment** from the order's payment record — see [[stripe-refunds-sync]] and [[orders-payment-refund]].

## Business rules (cross-cutting)

The cross-cutting rules that apply to the integration as a whole — each spelled out on the relevant aspect:

- **Hosted-Checkout redirect on first purchase; silent off-session charge on repeat** when Save Card is on and the customer is signed in. See [[stripe-checkout-flow]] and [[stripe-save-card]].
- **3D Secure is handled transparently by Stripe** — the merchant cannot configure it. See [[stripe-checkout-flow]].
- **Webhook-less reconciliation** — status is pulled via `sync` on the customer's return (no Stripe-specific webhook handler is wired). See [[stripe-refunds-sync]].
- **Auto-capture only** — no manual authorize / capture-later mode (capture scaffolding exists in code but is disabled). See [[stripe-refunds-sync]].
- **Card data never touches CloudCart** — only Stripe vault IDs and non-sensitive card metadata (last4, brand, expiry) are stored. See [[stripe-save-card]].
- **A broken API key cannot be saved** — Save triggers a live Stripe API call; failure blocks the save. See [[stripe-settings-fields]].
- **Self-deactivates on invalid credentials** — an init exception flips the provider Active flag OFF and notifies the admin. See [[stripe-refunds-sync]].
- **No plan gate** — any store on any plan can enable Stripe. The settings page is gated behind the standard payment-provider permission (`store.payment_providers`). See [[plan-gates]].

## Why it matters to the merchant

- **Best fit for international card acceptance.** Stripe supports 135+ currencies in its hosted Checkout, so a global store can charge customers in their local currency.
- **One-click repeat purchases** are possible via Save Customer Card + off-session charges — but only for signed-in customers, never guests. See [[stripe-save-card]].
- **No money-flow visibility in CloudCart.** Settlement, payouts and transaction reporting live in the merchant's own Stripe Dashboard — there is no Onboarding / Transactions / Payouts tab here, unlike [[payment-providers-cloudcart-pay|CloudCart Pay]]. Stripe in CloudCart is configuration + reconciliation only.
- **A broken key fails loudly on Save**, and an invalid key in production silently flips the provider off — so a credential problem never leaves customers stuck at a dead checkout for long. See [[stripe-settings-fields]] and [[stripe-refunds-sync]].

## Scope

Covered (across the 4 sub-pages):

- The settings layout, key fields, Save-Card toggles, amount/discount common options, and per-field validation + the save-time credential ping.
- The first-purchase hosted Checkout Session flow, currency, 3DS, locale.
- Save Customer Card storage + the returning-customer off-session charge.
- Refunds, the pull-based sync, auto-capture, recurring limits, self-deactivation, and the absence of Stripe Connect.

Not covered here:

- Settlement money-flow / payouts / Stripe Dashboard reporting — these are Stripe-side; CloudCart does not surface them.
- Storefront checkout-button rendering — see [[checkout-flow]].
- The order-details Refund button itself — see [[orders-payment-refund]].
- The customer's *Cards on file* panel — see [[customers-details-payments]].

## Related

- [[payment-providers]] — parent payment-providers hub.
- [[payment-providers-cloudcart-pay]] — CloudCart's own card gateway alternative.
- [[settings-payment-providers]] — global payment-providers list where Stripe is installed / uninstalled.
- [[orders-payment-refund]] — initiates a refund through Stripe from the order details page (see [[stripe-refunds-sync]]).
- [[orders-payment-capture]] — manual capture flow (not used by Stripe, which is auto-capture).
- [[customers-details-payments]] — where saved customer cards appear (see [[stripe-save-card]]).
- [[payment-provider]] — entity definition.
- [[payment-status]] — requested / completed / cancelled / refunded mapping.
- [[plan-gates]] — Stripe has no plan gate at the provider level.
- [[checkout-flow]] — storefront checkout, where Stripe surfaces as a card payment option.

## Open questions

(none — uncertain claims are flagged with `(verify)` on the aspect pages where they belong.)
