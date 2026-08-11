---
type: feature
nav_path: "Payment Providers → Paynetics → Feature gaps"
route_name: apps.paynetics.overview
route_path: /admin/payment-providers/paynetics
aliases: ["Paynetics refund", "Paynetics capture", "Paynetics sync", "Paynetics recurring", "Paynetics saved cards", "Paynetics wallets", "Paynetics not implemented", "Paynetics feature gaps", "Възстановяване Paynetics"]
tags: [paymentproviders, payment-providers, paynetics, refund, capture, sync, deprecated, card-gateway]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-paynetics]]. See the hub for related aspects (setup & UI, payment lifecycle).

# Paynetics — Feature gaps

## Purpose

This aspect catalogues what the Paynetics integration does **not** do: no two-phase capture, no API-driven refund, no periodic status sync, no saved cards, no Google Pay / Apple Pay wallets, and recurring fields that exist in the payload schema but are not exposed. Because the integration is **deprecated for new tenants**, these gaps are unlikely to be filled — this page exists so support can confirm "no, that's not supported" quickly rather than hunting for a non-existent control.

## Where to find it

These are absences, not screens — there is nothing to navigate to. A refund must be initiated from Paynetics's own merchant portal, not from CloudCart. The merchant can still flag an order as refunded in the admin via [[orders-payment-refund]], but the actual money movement happens at Paynetics.

## What the merchant can do here

- **Refund a Paynetics order** — only from Paynetics's own merchant portal. CloudCart can flag the order as refunded (see [[orders-payment-refund]]), but the financial reversal happens at Paynetics.
- **Recognise the limits** — no delayed-capture, no saved-card reuse, no wallet buttons, no recurring billing through Paynetics today.
- **Choose an alternative** if these features are needed — see [[payment-providers-borica-way4]] or [[payment-providers-cloudcart-pay]].

## Settings & fields

This aspect exposes no settings — every item below is a missing surface, not a configurable field. The configurable fields live on [[paynetics-setup-ui]].

## Business rules

### Refund support — not implemented

The refund hook is a TODO stub — no automated refund surface is implemented for Paynetics today. Refunds must be initiated from Paynetics's own merchant portal. The merchant can still mark the order as refunded in the admin UI via [[orders-payment-refund]], but the financial reversal happens at Paynetics.

### No Authorize + Capture

Paynetics's CloudCart integration is **single-message capture only** — there is no pre-authorize / delayed-capture surface.

### Status sync — not implemented

There is no periodic sync — the platform doesn't poll Paynetics for status changes (the status is settled on the return URL; see [[paynetics-payment-lifecycle]]). If a customer's payment is interrupted before they hit the return URL (network drop, browser crash), the platform's order status stays `Pending` until manually reconciled.

### No saved cards, no wallets

- Tokenisation / saved cards not implemented.
- Google Pay / Apple Pay not exposed in the storefront (even though Paynetics supports them bank-side).

If the merchant needs these features, they should consider [[payment-providers-borica-way4]] or [[payment-providers-cloudcart-pay]].

### Recurring billing — code exists, not exposed

The integration's payload type supports `recurring`, `recurringPeriod`, `recurringStart`, `recurringEnd`, and `user` token fields (for subscription billing scenarios), but the storefront integration does NOT expose these. They're commented out in the request output and aren't surfaced in the admin UI. Subscription billing through Paynetics is not a supported flow today.

### Why these gaps won't be filled

The Paynetics route is commented out of the payment-provider router (deprecated for new tenants — see the hub's *Purpose*). The capture / refund / sync / recurring / wallet gaps are therefore unlikely to be addressed. Merchants needing those capabilities should migrate to [[payment-providers-cloudcart-pay|CloudCart Pay]] or [[payment-providers-mypos|myPOS]].

## Related

- [[payment-providers-paynetics]] — hub.
- [[orders-payment-refund]] — flags a refund on the order (financial reversal happens in Paynetics's portal).
- [[orders-payment-manual]] — manual payment entry (offline / outside Paynetics).
- [[payment-providers-borica-way4]] — alternative supporting Authorize + Capture and wallets.
- [[payment-providers-cloudcart-pay]] — CloudCart's own card gateway with the broader feature set.

## Open questions

_None — the gaps above are by design for a deprecated integration._
