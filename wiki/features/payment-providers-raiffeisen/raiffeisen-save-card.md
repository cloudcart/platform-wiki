---
type: feature
nav_path: "Payment Providers → Raiffeisen Bank → Save customer card"
route_name: apps.raiffeisen.overview
route_path: /admin/payment-providers/kbc
aliases: ["Raiffeisen save card", "Raiffeisen saved cards", "Raiffeisen UPCToken", "Raiffeisen tokenisation", "Raiffeisen pay by token", "Raiffeisen one-click", "Райфайзен запазена карта", "Райфайзен токенизация"]
tags: [paymentproviders, payment-providers, raiffeisen, kbc, card-gateway, save-card, tokenisation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-raiffeisen]]. See the hub for the other aspects (setup, capture/authorize, refund/sync/status).

# Raiffeisen Bank — Save customer card

## Purpose

This aspect covers Raiffeisen's **Save customer card** feature: UPCToken-based tokenisation that lets a signed-in customer store their card on the first purchase and pay with one click on later checkouts, without re-entering card details on Raiffeisen's hosted page.

## Where to find it

The **Save customer card** toggle is the first of the three settings cards on the Raiffeisen overview page (Sidebar → **Payment Providers** → **Raiffeisen Bank**, route `/admin/payment-providers/kbc`). The saved cards themselves are managed by the customer in their storefront account panel, and are visible per-customer in the admin under [[customers-details-payments]].

## What the merchant can do here

- **Enable / disable Save customer card** — turns on UPCToken tokenisation for signed-in customers.
- View a customer's saved cards (masked PAN + brand + expiry) under [[customers-details-payments]].

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Save customer card** switch | Enables UPCToken-based tokenisation; signed-in customers see saved cards on subsequent checkouts. | `no` | `yes` / `no`. **Auto-disabled at runtime if Authorize is on** — see [[raiffeisen-capture-authorize]]. |

## Business rules

### Save-card requires a signed-in customer

Tokenisation only runs when **Save customer card** is ON **and** the buyer is signed in (non-guest). Guest checkouts always use the standard hosted-page flow with no token stored.

### The UPCToken flow

1. **First purchase** — Raiffeisen returns a `UPCToken` along with the masked PAN. The platform stores the token + masked PAN + expiry + brand on the customer's saved-card record.
2. **Subsequent purchases** — when the customer picks Raiffeisen again, the platform calls `payByToken` directly with the stored `UPCToken`. Raiffeisen processes the charge server-side without showing the hosted page again, assuming the issuer doesn't trigger a 3-D Secure step-up. (3DS may still be challenged by the issuer — see [[raiffeisen-refund-sync]].)
3. The customer can **remove** a saved card from their storefront account panel.

### Save card and Authorize are mutually exclusive

The runtime forces save-card **OFF** when Authorize is on. So if both toggles are saved as ON in the configuration, the integration disables save-card at request time — Raiffeisen's UPCToken flow doesn't combine with the two-step authorize (`Delay=1`) flow. The merchant should pick one. See [[raiffeisen-capture-authorize]].

### Card data never touches CloudCart

Only the `UPCToken`, masked PAN, brand and expiry are stored. The full card number stays with Raiffeisen / UPC — the platform never sees or stores raw PAN data.

## Related

- [[payment-providers-raiffeisen]] — hub.
- [[customers-details-payments]] — saved-card management per customer.
- [[raiffeisen-capture-authorize]] — the Authorize mode that disables save-card.
- [[payment-provider]] — entity definition.
- [[checkout-flow]] — storefront checkout where saved cards appear.

## Open questions

None.
