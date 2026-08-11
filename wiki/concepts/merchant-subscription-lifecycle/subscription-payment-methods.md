---
type: concept
nav_path: "Concept → Merchant subscription lifecycle → Payment methods (card / iCard / bank transfer)"
aliases: ["Subscription payment methods", "Saved card on file", "Stripe vs Braintree billing", "Card vault", "3D Secure card registration", "iCard SEPA iDEAL", "Manual bank transfer invoicing", "Card validation throttle", "HTTPS required for card", "Delete card support only"]
tags: [billing, subscription, payment, card, stripe, braintree, icard, bank-transfer, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[merchant-subscription-lifecycle]]. See the hub for the other aspects (states, renewal-retry, expiration, cancellation, feature packs, invoices, support flow).

# Subscription payment methods

## Definition

CloudCart charges the merchant for every paid recurring item (plan, feature pack, paid app, expert service, paid theme) via a **single saved card on file** stored in the merchant's billing-side gateway. There is exactly ONE card on file at a time — adding a new card REPLACES the previous one. There is no card-picker, no primary / backup card. The actual saved-card management UI is the side panel documented on [[billing-cards]], opened from the *Payment method* button in the Details area's header OR from the *pencil icon* on [[billing-invoicing]] OR inline in the Checkout panel during any purchase.

Some merchants use alternate payment instruments — **iCard** (SEPA / iDEAL / local methods) or **manual bank transfer** for invoiced enterprise / LTA contract accounts (verify which gateway each instrument routes through). The card on file remains the default for the daily auto-renewal pipeline.

## Scope

What this page covers: the saved card on file (one per account, replacement-only, masked view); the Stripe vs Braintree gateway split + 3DS rules; the 3-attempts-per-24h validation throttle; the HTTPS-required rule; the lack of a Delete-card UI; iCard for SEPA / iDEAL (verify); manual bank transfer for LTA / invoiced accounts (verify).

What it does NOT cover: the retry pipeline that charges the card — see [[subscription-renewal-retry]]; the invoice details printed on each invoice — see [[subscription-invoices]] + [[billing-invoicing]]; the transaction history — see [[details-billing]].

## Contrasts

- **Saved card on file vs storefront payment providers** — the card on file charges the MERCHANT for the platform subscription. The storefront [[payment-providers|payment providers]] accept payments from CUSTOMERS. Two entirely separate gateway integrations.
- **Stripe vs Braintree** — gateway assigned at account provisioning; merchant cannot switch from the UI. Behaviour differs at 3DS (see below).
- **Add a card vs Replace a card** — no difference; saving a new card always replaces. No "primary / backup" concept.
- **No Delete-card UI vs support delete endpoint** — merchant cannot delete from the admin. `/admin/billing/card/delete/{token}` exists for support use only.
- **Card vs iCard** — Card is the standard auto-renewal path; iCard handles SEPA / iDEAL on supported markets (verify availability).
- **Card-on-file vs manual bank transfer** — manual bank transfer is used by LTA-contract / invoiced enterprise accounts (`lta_contract_id` set). These subscriptions do NOT run the daily auto-renewal — the merchant pays the invoice manually and the account manager marks it paid.

## Where it applies

### The saved card on file — key rules

- **Exactly ONE card on file at a time.** Adding a new card REPLACES the previous one. No card-picker, no primary / backup.
- **The merchant cannot view full card numbers** — only brand, masked last 4, expiry month/year, country of issuance.
- **Two gateways**, set at account provisioning: **Stripe** or **Braintree**. Merchant cannot switch from the UI.
- **3D Secure mandatory at card-registration.** Braintree rejects nonces that aren't 3DS-verified; Stripe runs SetupIntent 3DS as part of the card-add.
- **3 card-validation attempts per 24-hour rolling window** — after 3 the merchant is throttled with *"Service temporary disabled. Too many card validations."*. Counts every attempt.
- **HTTPS required on primary domain** to add a card — `http://` primary domains see *"Your primary domain `<host>` uses insecure (http) connection!..."* and the gateway module is not loaded at all.
- **No Delete-card UI** — to "delete" a card the merchant must REPLACE it. `/admin/billing/card/delete/{token}` exists for support use only.

### Where the card is opened

The card-management side panel is reached from three places: (1) Profile dropdown → **Billing / Cards** (owner-only) → `/admin/details/billing` → *Payment method* button in the header; (2) pencil icon on [[billing-invoicing]]; (3) inline within any Checkout side panel. Direct browser navigation to `/admin/billing/card` returns 404 — the panel is always opened via in-app links.

### 3D Secure (3DS) — gateway differences

- **Braintree path** — 3DS runs both at card-registration AND mid-flight for renewal charges. If the bank requires re-authentication for the renewal charge, the merchant sees the issuer's 3DS challenge (OTP / mobile-banking confirmation). On `liabilityShifted: true`, the cart resubmits.
- **Stripe path** — 3DS runs during card registration on [[billing-cards]] via the SetupIntent flow. There's no mid-flight 3DS challenge for Stripe accounts — Stripe handles step-up auth as part of the off-session charge.

### iCard (SEPA / iDEAL) (verify)

On supported markets, some merchant accounts can register an iCard payment method as the card-on-file equivalent (SEPA direct debit, iDEAL, local bank methods). Once registered, the daily auto-renewal pipeline charges the iCard instrument the same way it charges a stored card. (verify markets / merchant types + whether the UI is the same side panel)

### Manual bank transfer (for LTA / invoiced accounts) (verify)

Enterprise merchants with an LTA contract (`lta_contract_id IS NOT NULL` on the subscription) do NOT run the daily auto-renewal — the renew pipeline excludes them. Instead: invoices are issued on the contract's cadence, the merchant pays via bank transfer (IBAN on the invoice), and the account manager marks the invoice paid (`next_billing_date` advanced manually). Contracts past `ends_at` are expired by the daily `expire:subscriptions` sweep, which also creates a penalty invoice — see [[subscription-expiration]]. Non-LTA invoice-only enterprise accounts may also pay via bank transfer against an issued invoice (verify the exact admin surface).

### The card on file across the lifecycle

- **At first plan purchase** — adding the card is part of the Checkout flow. Without a card, the **Pay now** button is disabled.
- **During [[subscription-renewal-retry|the daily retry loop]]** — the next auto-retry uses whatever card is on file at the time. Updating the card mid-loop can rescue a Past due subscription without merchant action.
- **During [[subscription-expiration|the takeover]]** — [[billing-cards]] stays in the allowlist; the merchant can update the card to unblock Renew.
- **Card expired** — the card is NOT auto-replaced. The merchant must manually replace it on [[billing-cards]] before the next retry can succeed.

## Related

- [[merchant-subscription-lifecycle]] — hub.
- [[billing-cards]] — the saved-card management side panel.
- [[billing-invoicing]] — the invoice details printed on each invoice (the OTHER prerequisite at checkout).
- [[details-billing]] — transaction history (charge-by-charge view of attempts against the card).
- [[subscription-renewal-retry]] — the pipeline that charges the card on file.
- [[subscription-expiration]] — the LTA-contract Cancel rejection + the contract penalty invoice.
- [[expired-subscription]] — [[billing-cards]] stays accessible during the takeover.
- [[payment-providers]] — storefront payment providers (NOT the same gateway as the saved card on file).

## Open Questions

- ⏸️ **iCard availability** — verify which markets / merchant types can use iCard as the card-on-file instrument and whether the side panel is reused or a separate route.
- ⏸️ **Manual bank transfer for non-LTA accounts** — verify the exact admin path for enterprise / invoice-only accounts that aren't on an LTA contract but also don't run auto-renewal.
- ⏸️ **Mid-flight 3DS on the Braintree path** — verify the exact `liabilityShifted` resubmit handshake under the modern Vue Checkout panel (the legacy Smarty flow is documented; modern Vue path may differ).
