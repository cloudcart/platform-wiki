---
type: feature
nav_path: "Payment Providers → myPOS → Save customer card"
route_name: apps.mypos.overview
route_path: /admin/payment-providers/mypos
aliases: ["myPOS save card", "myPOS CardToken", "myPOS tokenisation", "myPOS saved cards", "myPOS IAPurchase", "myPOS per-environment save switches", "Запазена карта myPOS"]
tags: [paymentproviders, payment-providers, mypos, save-card, tokenisation, cardtoken]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-mypos]]. See the hub for related aspects (setup & config pack, payment lifecycle, refund & sync).

# myPOS — Save customer card

## Purpose

This aspect documents myPOS's **CardToken-based tokenisation** — the "Save customer card" feature that lets signed-in (non-guest) customers store a card on their first myPOS purchase and re-use it on later checkouts without re-entering the number. myPOS is the **only card gateway on CloudCart with separate save-card switches per environment**, so a merchant can test the saved-card flow without touching live behaviour.

## Where to find it

The two switches live on the myPOS Settings page — **Test Save customer card** (visible when Mode = Test) and **Live Save customer card** (visible when Mode = Live). Both are documented field-by-field on [[mypos-setup-config-pack]]. The customer manages their stored cards from their storefront account panel (see [[customers-details-payments]] for the admin-side view).

## What the merchant can do here

- **Enable Save customer card per environment** — turn on CardToken-based tokenisation independently for test and live.
- **Confirm a stored card** exists on a customer from [[customers-details-payments]].
- **Understand the saved-card failure message** the customer sees so support can guide them to remove a stale token.

## Settings & fields

Two independent boolean switches (no other fields specific to this aspect):

| Switch | Stored key | Default | Notes |
|--------|-----------|---------|-------|
| **Test Save customer card** | `test_save_card` | `no` | Visible when Mode = Test. Independent of the live switch. |
| **Live Save customer card** | `save_card` | `no` | Visible when Mode = Live. Independent of the test switch. |

Full field layout and the card-rendering mechanics are on [[mypos-setup-config-pack]].

## Business rules

### Save customer card flow (CardToken)

When **Save customer card** is ON AND the buyer is signed in (non-guest), the platform:

1. **First purchase** — the platform sends `CardTokenRequest = CARD_TOKEN_REQUEST_PAY_AND_STORE` on the purchase. The customer enters their card on myPOS's page, completes 3DS, and on success myPOS returns `CardToken`, `PAN` (masked), `ExpDate`, and `CardType`. The platform stores these on the customer's `CustomerCard` record.
2. **Subsequent purchases** — when the customer picks myPOS again, the platform calls `IAPurchase` (Initial-Auth Purchase) directly with the stored `CardToken` — myPOS processes the charge server-side without showing the hosted page (3DS step-up may still happen depending on the issuer).
3. If a saved-card charge fails, the merchant-facing error reads: *"Payment failed. Please remove the saved card and try again."* — the customer is encouraged to delete the stale token from their account panel.
4. The customer can remove a saved card from their storefront account panel.

Guest checkouts never tokenise — save-card requires a signed-in customer with an account to attach the `CustomerCard` to.

### Separate save-card switches per environment

myPOS is the **only card gateway on CloudCart with separate save-card switches per environment** — `test_save_card` and `save_card` are independent boolean flags. Most other providers (Borica, Raiffeisen) have a single switch. This makes test runs easier without affecting live behaviour. See [[payment-providers-borica-way4]] for the single-switch contrast.

### Card brand labelling

The platform's save-card helper maps each myPOS card network to a brand label that the customer sees next to their stored card: VISA → "Visa", VPAY / Visa Electron → "Visa", Mastercard → "MasterCard", Maestro → "Maestro", JCB → "JCB". The masked `PAN` and `ExpDate` returned by myPOS are stored alongside the token for display.

### Interaction with capture mode

The saved-card path uses myPOS's single-message `IAPurchase` — there is no delayed-capture variant for tokenised charges, consistent with the auto-capture-only rule on [[mypos-refund-sync]].

## Related

- [[payment-providers-mypos]] — hub.
- [[customers-details-payments]] — saved-card management for individual customers.
- [[payment-providers-borica-way4]] — alternative card gateway with a single (not per-environment) save-card switch.
- [[customer]] — the entity the `CustomerCard` token attaches to.

## Open questions

_None._
