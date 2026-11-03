---
type: feature
nav_path: "Profile → Billing → Payment method → Braintree flow"
route_name: admin.billing.card
route_path: /admin/billing/card
aliases: ["Braintree card flow", "Braintree Drop-in UI", "Braintree nonce", "Braintree 3D Secure", "Payment method nonce"]
tags: [billing, payment-method, braintree, drop-in, nonce]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[billing-cards]]. See the hub for the other aspects (Stripe flow, 3DS + security, HTTPS prereqs, replacement, renewal, display summary).

# Payment cards — Braintree flow

## Purpose

Braintree is the second of CloudCart's two billing-side gateways. It is the **default for legacy accounts** and remains active for any merchant whose account was not provisioned on Stripe. Braintree accounts cannot be switched to Stripe (or vice versa) from the admin UI — gateway assignment is a CloudCart-support operation — see [[billing-cards]].

This aspect documents what the merchant sees during a Braintree-backed card add / replace, the Drop-in UI + nonce flow, the `makeDefault=true` semantics, the duplicate-customer race recovery, and how the same module embeds inline inside Checkout.

## Where to find it

- The **Payment method** panel at `/admin/billing/card` (Profile dropdown → Billing → pencil icon next to the card) renders the Braintree variant when the merchant's account is bound to anything **other** than the Stripe billing provider (i.e. the default).
- The same module also embeds inline inside the **Checkout** side-panel's *Payment method* card (see [[plans-purchase]]) when the account is not on Stripe.

## What the merchant can do here

- Enter the card directly into the Braintree Drop-in UI inside the panel.
- Save the card with **Save** — Braintree runs its `payment-method` create call, performs 3D Secure on the card, and returns a payment-method nonce. CloudCart attaches the nonce as the customer's default and stores the masked summary — see [[billing-cards-display-summary]].

What the merchant **cannot** do here: switch gateway from the UI, save a card whose nonce is not 3D-Secured (`liabilityShifted: true`), or store multiple cards — see [[billing-cards-3ds-and-security]] and [[billing-cards-replacement-and-deletion]].

## Settings & fields

There are no editable settings on this screen — it is the Braintree Drop-in UI hosted by Braintree. The panel renders:

- Header — same localised *Payment provider* label + **Save** button + close button as the Stripe variant.
- Body — a yellow 3DS pre-authorisation notice, then the container where the Drop-in UI mounts.
- A hidden form — carries the `payment_method_nonce` value that the Drop-in UI fills before submit.
- Bottom — the script that wires up the Braintree client + the 3D Secure flow on save.

Verbatim 3DS pre-authorisation notice shown above the Drop-in UI:

> *"In connection with PSD2 SCA regulatory requirements, we will validate your card with 3D Secure validation for the amount of 1 `<currency>`, which will not be debited from the card. After successful validation, the selected card will be charged automatically for all your subscriptions."*

## Business rules

### Card register = client token + nonce + 3DS check

The flow is:

1. The Drop-in UI mounts and Braintree issues a client token to it.
2. The merchant types card details inside the Drop-in.
3. On Save, the Drop-in tokenises the card directly to Braintree and returns a payment-method nonce to the page.
4. The nonce + `verificationAmount: 1` are posted to the CloudCart backend.
5. The platform calls Braintree's `payment-method` create API with `makeDefault: true`. Braintree runs 3D Secure as part of this — see [[billing-cards-3ds-and-security]].
6. On success, the masked summary returned by Braintree is stored locally (see [[billing-cards-display-summary]]).

### `makeDefault=true` replaces the previous default

Every successful save sets the new payment method as the customer's default. The previously attached method is removed in the same step — only one card is kept per Braintree customer at a time. See [[billing-cards-replacement-and-deletion]].

### Verification amount: 1 currency-equivalent

Braintree's card verification runs a real 3DS check against a **1 USD-equivalent** authorisation amount (`verificationAmount: 1`). The hold is released immediately and never settles. The merchant may briefly see a `$1` pending hold on their bank statement that disappears within hours.

### `liabilityShifted: true` is mandatory

If the issuer's `threeDSecureInfo.liabilityShifted` flag is **not** true after the 3DS challenge, the save throws *"3D Secure validation error"* and no card is stored. The merchant must retry on a card whose issuer supports 3DS, or contact their bank — see [[billing-cards-3ds-and-security]].

### First-time-customer creation is idempotent

When the merchant opens the panel for the first time (no Braintree customer linked yet), the platform auto-creates a Braintree Customer for the merchant. The Braintree customer ID is stored on the user record and reused on every subsequent card replacement.

### Duplicate-customer race is handled

If a duplicate Braintree customer creation is attempted (because the customer ID has already been claimed on the gateway side, e.g. from a previous failed creation), the code catches the *"Customer ID has already been taken"* error and assigns the merchant's `unique_id` to the **existing** customer, recovering gracefully. The merchant never sees this race — the panel loads normally.

### Braintree customer deletion sweeps all cards

When a Braintree customer record is deleted on the gateway side (e.g. account termination), all payment methods are removed in a single sweep. A daily background job also deletes cards that have expired (past their expiry month). After expiry, the merchant must re-register a card or the next renewal will fail — see [[billing-cards-renewal-charging]].

### Checkout inline variant uses the same backend

The Checkout-embedded variant loads Braintree's Drop-in UI + 3D Secure SDK, opens the same module as the standalone panel but inline, and saves the nonce + 3DS-verified payment method via the same backend. After save, the inline panel collapses back to the read-only summary (brand + last 4 + expiry) and the parent Checkout panel can submit Pay-now.

### Per-charge 3DS challenge UI is Braintree's, not CloudCart's

When a renewal or Pay-now triggers a 3DS challenge mid-flight (Braintree path), the merchant sees the issuer's bank-controlled 3DS challenge modal — typically OTP input or mobile-banking confirmation. This is the gateway's UI, not CloudCart's. After `liabilityShifted: true`, the original cart submits with the verified nonce. After failure, the merchant sees an inline error and the charge is not retried.

## Related

- [[billing-cards]] — hub.
- [[billing-cards-stripe-flow]] — the other gateway variant.
- [[billing-cards-3ds-and-security]] — 3DS rules covered there.
- [[billing-cards-replacement-and-deletion]] — how Braintree handles attach-then-detach.
- [[billing-cards-renewal-charging]] — Braintree retry / refund flow.
- [[plans-purchase]] — Checkout panel that embeds the inline card form.

## Open questions

None.
