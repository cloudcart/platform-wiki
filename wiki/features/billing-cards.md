---
type: feature
nav_path: "Profile → Billing → Payment method"
route_name: admin.billing.card
route_path: /admin/billing/card
aliases: ["Payment method", "Payment cards", "Billing card", "Credit card", "Card on file", "Платежен метод", "Платежна карта", "Карта"]
tags: [billing, payment-method, card, subscription-billing, stripe, braintree]
plan_gates: []
created: 2026-05-23
updated: 2026-06-10
source_count: 6
---

# Payment cards (billing)

## Purpose

The **Payment method** screen is where the merchant registers (and replaces) the credit card that CloudCart charges for **subscriptions** the merchant owes to CloudCart — the store plan, paid apps, paid feature packs, paid services. This is the merchant's "card on file" for billing CloudCart, **not** a tool for accepting customer payments on the storefront (that lives under [[settings-payment-providers]]).

The screen is a slide-in side panel hosting an external card-tokenisation module (Stripe Payment Element or Braintree Drop-in UI). The merchant types card details directly into the gateway's module — the data never touches CloudCart servers — the gateway returns a token, and the platform stores only the token plus masked metadata. The store is **not** in PCI-DSS scope for cardholder data.

Once a card is on file, CloudCart automatically charges it on each renewal of every active subscription. If the card is missing, expired, or the renewal fails repeatedly, the merchant's subscriptions enter the expired-subscription flow — see [[expired-subscription]] and [[billing-cards-renewal-charging]].

## Where to find it

- **Profile dropdown** (top-right user-account menu) → **Billing**.
- The same panel opens automatically from several other places the merchant might be in:
  - The **Invoicing details** screen at `/admin/billing/invoicing` shows the current card alongside the invoicing block; the pencil icon opens this panel to replace the card. If no card is on file, an **Add payment method** button opens this same panel.
  - The **Subscriptions** list shows a payment-method link in the header bar that opens this panel.
  - The **Services purchase** flow (see [[services]]) renders this panel inline when the merchant has no card on file.

URL pattern: `/admin/billing/card` (panel-only — the merchant cannot navigate to this URL directly; the link is always opened via AJAX as a side panel, see [[billing-cards-https-throttle-prereqs]]).

## Sub-pages (in this cluster)

This feature is split into 7 aspect pages. The Assistant should drill into the aspect that matches the question, not read every page.

- [[billing-cards-stripe-flow]] — Stripe accounts: SetupIntent + CustomerSession + Payment Element; Stripe panel + Checkout variant; issuer-company picks the Stripe account; off-session renewal charges.
- [[billing-cards-braintree-flow]] — Braintree accounts: Drop-in UI + payment-method nonce; Braintree panel + Checkout variant; `makeDefault=true`; first-time-customer duplicate-ID race recovery.
- [[billing-cards-3ds-and-security]] — 3D Secure mandatory at registration on both gateways; PCI-DSS scope (tokenisation only); the gateway-hosted challenge UI; the "Authentication required" off-session failure mode.
- [[billing-cards-https-throttle-prereqs]] — HTTPS-on-primary-domain hard block + insecure-warning template; the 3-attempts-per-24-hours throttle (success or failure); AJAX-only route access.
- [[billing-cards-replacement-and-deletion]] — one-card-per-merchant model; replacement attaches new then detaches old; no Delete UI; the internal `card/delete/{token}` route; auto-clear on expiry.
- [[billing-cards-renewal-charging]] — saved cards driving subscription renewals; retry schedule (2/3/4/5 days, max 5 attempts); PAST_DUE → EXPIRED daily sweep; refund flow on the same gateway.
- [[billing-cards-display-summary]] — the read-only card summary string format (`VISA **** 1234 Exp. 05/27`) + everywhere it's shown + the metadata stored locally (brand / last 4 / expiry / country / logo URL / token).

## What the merchant can do here

- **Add a card** when none is on file — the gateway module opens inside the side panel.
- **Replace the current card** — the merchant enters new card details and saves; the new card becomes the active card on file. The previously stored card is removed in the same operation — see [[billing-cards-replacement-and-deletion]].
- See a warning on the [[settings-domains]] / [[settings-general]] screens when the store's primary domain is `http://`, blocking card entry until the merchant moves to a secure (`https://`) primary domain or installs an SSL certificate — see [[billing-cards-https-throttle-prereqs]].

What the merchant **cannot** do here:

- View full card numbers — only brand, last four, expiry, country of issuance are stored anywhere — see [[billing-cards-display-summary]].
- Store multiple cards — adding a new card replaces the previous one — see [[billing-cards-replacement-and-deletion]].
- Delete the on-file card from the UI — there is no Delete control; change by replacing — see [[billing-cards-replacement-and-deletion]].
- Bypass 3D Secure — both gateways require a 3DS-validated card at registration — see [[billing-cards-3ds-and-security]].
- Enter card details from a domain that does not use HTTPS — see [[billing-cards-https-throttle-prereqs]].

## Settings & fields

There are no editable settings on this screen — it is a card-entry module hosted by an external payment provider. Three variants are possible depending on the merchant's gateway + domain state:

| Variant | When shown | Aspect |
|---------|------------|--------|
| **Stripe module** | Account set to the Stripe billing provider. | [[billing-cards-stripe-flow]] |
| **Braintree module** | Account set to the Braintree billing provider (default for legacy accounts). | [[billing-cards-braintree-flow]] |
| **Insecure-domain warning** | The store's primary domain is `http://` (no SSL). | [[billing-cards-https-throttle-prereqs]] |

All variants show a 3D Secure pre-authorisation notice above the module — *"In connection with PSD2 SCA regulatory requirements, we will validate your card with 3D Secure validation for the amount of 1 `<currency>`..."* — see [[billing-cards-3ds-and-security]] for the full notice text and the validation-amount semantics.

## Business rules (cluster-wide)

The cluster's rules live on the aspect pages. The headline rules:

- **Card data never touches CloudCart.** All entry happens inside the gateway-hosted module; CloudCart receives only a token + masked summary. See [[billing-cards-3ds-and-security]].
- **One card per merchant, replacement-only.** No multi-card list, no Delete button — the merchant replaces by entering a new card. See [[billing-cards-replacement-and-deletion]].
- **3D Secure is mandatory at registration on both gateways.** Issuers without 3DS 2.x support cannot be saved. See [[billing-cards-3ds-and-security]].
- **HTTPS on the primary domain is required.** `http://` primary domains see the warning template only; the module is not loaded. See [[billing-cards-https-throttle-prereqs]].
- **Card-add throttle: 3 attempts per 24 hours** — counts every attempt regardless of success. After the limit: *"Service temporary disabled. Too many card validations."*. See [[billing-cards-https-throttle-prereqs]].
- **Two billing-side gateways: Stripe and Braintree.** Assigned by CloudCart at account provisioning; the merchant cannot switch from the admin UI. Token migration between gateways is support-driven. See [[billing-cards-stripe-flow]] and [[billing-cards-braintree-flow]].
- **Renewal failure escalation.** Renewal retries (2/3/4/5 days), PAST_DUE on first failure, EXPIRED via the daily sweep about 1 month past `next_billing_date`. See [[billing-cards-renewal-charging]] and [[expired-subscription]].

## Related

- [[settings-domains]] — SSL prerequisite for entering card details.
- [[billing-invoicing]] — sibling screen; the merchant's invoicing details for the same CloudCart bill.
- [[plans]] — store plan paid by this card.
- [[subscriptions]] — every recurring item charged against this card.
- [[services]] — paid services purchased with this card.
- [[apps]] — paid apps charged against this card.
- [[expired-subscription]] — what the merchant sees when the card fails.
- [[merchant-subscription-lifecycle]] — merchant-question hub: "where do I see my payment methods / what happens if my card fails / how do I update my card?".
- [[settings-payment-providers]] — completely different surface: payment providers for the merchant's customers on the storefront (Stripe / PayPal / iCard / Borica etc. for accepting payments, not paying CloudCart).
- [[details-billing]] — subscription detail Billing log where charge / refund transactions appear.

## Open questions

None — all previously-flagged items resolved or distributed to sub-pages.
