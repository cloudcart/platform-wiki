---
type: feature
nav_path: "Profile → Billing → Payment method → Stripe flow"
route_name: admin.billing.card
route_path: /admin/billing/card
aliases: ["Stripe card flow", "Stripe SetupIntent", "Stripe CustomerSession", "Stripe Payment Element", "Stripe issuer company"]
tags: [billing, payment-method, stripe, setup-intent, customer-session]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[billing-cards]]. See the hub for the other aspects (Braintree flow, 3DS + security, HTTPS prereqs, replacement, renewal, display summary).

# Payment cards — Stripe flow

## Purpose

Stripe is one of the two billing-side gateways CloudCart uses to tokenise the merchant's card. Stripe accounts are assigned at provisioning time and cannot be switched from the admin UI — see [[billing-cards]]. When the **Payment method** panel detects a Stripe account, it loads the Stripe Payment Element, runs a Stripe-side card registration flow, and stores only the gateway token plus the masked summary — see [[billing-cards-display-summary]].

This aspect documents what the merchant sees during a Stripe-backed card add / replace, the two intent / session objects involved, the wallets the Element surfaces, the issuer-company driver, and how renewals charge the saved card off-session.

## Where to find it

- The **Payment method** panel at `/admin/billing/card` (Profile dropdown → Billing → pencil icon next to the card) renders the Stripe variant when the merchant's account is bound to the Stripe billing provider.
- The same module embeds inline inside the **Checkout** side-panel's *Payment method* card (see [[plans-purchase]]) when the account's `payment_provider` is `stripe`.

## What the merchant can do here

- Enter the card directly into the Stripe Payment Element (card number / expiry / CVC / postal code).
- Use any wallet Stripe defaults expose for the merchant's account / locale — typically **Apple Pay**, **Google Pay**, and **Link** when the browser supports them.
- Save the card with **Save** in the panel header — Stripe runs its SetupIntent flow (3D Secure included), tokenises, and CloudCart stores only the token + masked summary.
- See, save, and remove cards from *inside* the Stripe-hosted module itself (the CustomerSession enables this richer UX).

What the merchant **cannot** do here: switch to Braintree from the UI, edit a saved card's name / address, or save a card whose issuer doesn't support 3D Secure 2.x — see [[billing-cards-3ds-and-security]] and [[billing-cards-replacement-and-deletion]].

## Settings & fields

There are no editable settings on this screen — it is the Stripe Payment Element hosted by Stripe. The panel passes the following from the CloudCart backend to the front-end mount:

| Field | Source | What it does |
|-------|--------|--------------|
| `clientSecret` | Stripe SetupIntent created server-side | Authorises the tokenisation session for this merchant. |
| `customerSessionClientSecret` | Stripe CustomerSession created server-side | Enables `payment_method_redisplay`, `payment_method_save`, `payment_method_save_usage = off_session`, and `payment_method_remove` in the Stripe-hosted Element. |
| `locale` (`lang`) | Merchant's language | Translates Stripe Element field labels. |
| `appearance` | Constant — primary colour `#8d58e0` | Themes the Element to CloudCart's purple primary. |

The Payment Element is configured with `allow_redisplay: 'always'` so the saved method is available to subsequent SetupIntents / PaymentIntents.

## Business rules

### SetupIntent + CustomerSession are both required

The panel creates BOTH objects on every open:

- **SetupIntent** — drives the actual card tokenisation. Tracks 3DS state and returns the saved payment-method ID on success.
- **CustomerSession** — enables the saved-methods management UX *inside* the Stripe Element (so the merchant can see / save / remove cards from the gateway's own UI, without leaving the panel).

The session-secret is what unlocks the Element's saved-method controls. Without it the merchant sees a bare card-entry form. With it, the merchant gets Stripe's full saved-methods experience.

### Issuer company drives the Stripe account

Different issuer companies use different Stripe accounts. The Stripe public / secret keys are loaded by the merchant's `issuer_company_id` — a BG-invoiced merchant connects to one Stripe account, a DE-invoiced merchant to a different one. If a merchant changes invoicing country (via [[billing-invoicing]]) such that their `issuer_company_id` flips, **their saved Stripe customer becomes invalid for the new entity** and they must re-register the card.

### Customer record is auto-created on first card add

When the panel opens for the first time (no Stripe customer yet linked to the merchant), the platform auto-creates a Stripe Customer for the merchant via the gateway API. The Stripe customer ID is then stored on the merchant's user record and reused for every subsequent card replacement. Once created, the customer record persists for the life of the merchant account.

### Renewal charges run off-session

Renewal charges run with `off_session: true` and `confirm: true` — meaning Stripe charges the saved default payment method automatically without merchant intervention. But if 3DS is required by the issuer (re-authentication), the off-session charge **fails** rather than challenging the merchant in real time. The failure surfaces in [[details-billing]] as a transaction with response *"Authentication required"*, which the merchant must clear by re-saving the card so a fresh 3DS handshake runs at registration — see [[billing-cards-renewal-charging]].

### Wallets surface per Stripe defaults

The Stripe module uses Stripe's `payment` Element with **no** `paymentMethodTypes` restriction. Whatever wallet types Stripe's defaults allow for the merchant's Stripe account / locale will appear — typically **card** plus **Apple Pay**, **Google Pay**, and **Link** when the browser supports them. The merchant doesn't configure this from the CloudCart UI.

### Checkout inline variant uses the same backend

The Checkout-embedded variant loads Stripe's JavaScript SDK asynchronously, then builds the Stripe Element with the same `clientSecret`, `customerSessionClientSecret`, `locale`, and `appearance` values, mounts a `payment` Element into the card container, and on Confirm runs Stripe's setup confirmation (redirecting only if required, with `allow_redisplay: 'always'`). When the setup intent reaches the `succeeded` status, it posts the resulting payment-method ID as the `payment_method_nonce` to the same save endpoint the standalone panel uses.

### Stripe panel structure

The Stripe panel has:

- Header — localised *Payment provider* label + **Save** button + close button.
- Body — a yellow 3DS pre-authorisation notice (interpolating the currency into the note text), then an empty payment-element container.
- Bottom — the script that fetches the SetupIntent + CustomerSession secrets and initialises the Stripe Element with locale + appearance + both client secrets.

## Related

- [[billing-cards]] — hub.
- [[billing-cards-braintree-flow]] — the other gateway variant.
- [[billing-cards-3ds-and-security]] — 3DS rules covered there.
- [[billing-cards-replacement-and-deletion]] — how Stripe handles attach-then-detach.
- [[billing-cards-renewal-charging]] — off-session renewal failure mode.
- [[plans-purchase]] — Checkout panel that embeds the inline card form.
- [[billing-invoicing]] — issuer-company is derived from invoicing country.

## Open questions

None.
