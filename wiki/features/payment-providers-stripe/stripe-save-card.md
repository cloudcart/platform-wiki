---
type: feature
nav_path: "Payment Providers → Stripe → Save Customer Card"
route_name: apps.stripe.settings
route_path: /admin/payment-providers/stripe
aliases: ["Stripe save card", "Stripe saved card", "Stripe off-session", "Stripe tokenisation", "Stripe setup_future_usage", "Stripe returning customer", "Stripe one-click", "Stripe card on file"]
tags: [paymentproviders, payment-providers, stripe, save-card, off-session, tokenisation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-stripe]]. See the hub for related aspects (settings, checkout flow, refunds/sync).

# Stripe — Save Customer Card

## Purpose

This aspect documents the **Save Customer Card** feature: when it stores a card, exactly what is stored (and what is never stored), the `setup_future_usage = off_session` flag that makes the saved card reusable, and the **returning-customer off-session charge** that skips the hosted-checkout redirect entirely on repeat purchases.

## Where to find it

The two **Save Customer Card** toggles (one for test mode, one for live mode) are on the Stripe settings screen — see [[stripe-settings-fields]]. Saved cards for an individual customer appear on [[customers-details-payments]]. This page documents the behaviour those toggles control; it is otherwise runtime, not a merchant screen.

## What the merchant can do here

- **Turn Save Customer Card on or off**, independently for test and live mode — on [[stripe-settings-fields]].
- **See a customer's saved cards** on the customer's payments panel — see [[customers-details-payments]].
- There is no merchant action to manually charge a saved card; the off-session charge fires automatically on the customer's next purchase.

## Settings & fields

The only fields are the two boolean toggles on [[stripe-settings-fields]]: `configuration.test_save_card` and `configuration.live_save_card` (both default ON). This page does not add its own fields.

## Business rules

### When a card is saved

A card is saved after a successful checkout **only when** Save Customer Card is ON for the active mode **AND** the customer is signed in (not a guest). Guest checkouts never save a card.

### What gets stored — and what never does

After a qualifying successful checkout:

- CloudCart retrieves the `payment_method` ID from Stripe.
- It stores `{customer: <stripe_customer_id>, payment_method: <stripe_pm_id>, card: <card metadata>}` against the CloudCart customer (via the generic `SaveCard` trait).

The actual card number is **never stored in CloudCart** — only Stripe's vault IDs and non-sensitive card metadata (last4, brand, expiry month/year). The real card lives only in Stripe's vault as `Customer` + `PaymentMethod` records.

### `setup_future_usage = off_session`

When Save Card is ON, the Checkout Session is created with `payment_intent_data.setup_future_usage = 'off_session'`. This tells Stripe to make the saved card reusable for merchant-initiated **off-session** charges. Without this flag, the card could not be charged later without the customer present. (The Checkout Session creation itself is documented on [[stripe-checkout-flow]].)

### Returning-customer off-session charge

When Save Customer Card is ON **AND** the customer is signed in (not a guest) **AND** the customer already has a saved Stripe card on this store, the repeat purchase **skips the hosted Checkout Session entirely**:

1. CloudCart calls Stripe's `paymentIntents.create` directly with the saved `customer` ID, the saved `payment_method` ID, and `off_session: true, confirm: true`.
2. If Stripe returns status `requires_confirmation`, CloudCart confirms it via `paymentIntents.confirm`.
3. If Stripe returns status `succeeded` → payment status = `completed`. Otherwise → `cancelled`.

This is a **silent in-place charge** — no redirect and no 3DS step, unless the card requires re-authentication. If the bank challenges, the off-session PaymentIntent goes to `requires_action` and the off-session call fails; the payment is marked `cancelled` and the merchant must contact the customer for a fresh purchase. The status-pull mechanics are on [[stripe-refunds-sync]].

## How it works (verified against backend)

- The save uses the generic `SaveCard` trait shared across providers, so the saved-card storage shape is the same as other tokenising gateways.
- On a repeat purchase the integration checks for an existing saved card for this (customer, store) pair **before** deciding between the redirect flow and the off-session charge — the presence of a saved card is what flips the path.
- The `off_session: true` parameter on the PaymentIntent signals to Stripe that the customer is not present, which changes how Stripe applies issuer authentication rules (and is why a hard 3DS challenge causes the charge to fail rather than prompt).

## Related

- [[payment-providers-stripe]] — hub.
- [[stripe-settings-fields]] — the two Save Customer Card toggles + key configuration.
- [[stripe-checkout-flow]] — the first-purchase flow that stores the card via `setup_future_usage`.
- [[stripe-refunds-sync]] — how the off-session charge's status is resolved; refunds.
- [[customers-details-payments]] — where a customer's saved cards appear.
- [[payment-status]] — the completed / cancelled values produced by the off-session charge.

## Open questions

(none)
