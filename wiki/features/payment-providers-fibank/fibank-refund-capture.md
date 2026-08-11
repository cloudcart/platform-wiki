---
type: feature
nav_path: "Payment Providers → Fibank → Refunds & capture"
route_name: apps.fibank.overview
route_path: /admin/payment-providers/fibank
aliases: ["Fibank refund", "Fibank status mapping", "Fibank capture", "Fibank no saved cards", "Fibank wallets", "Fibank iframe", "Възстановяване Fibank", "Fibank статус на плащане"]
tags: [paymentproviders, payment-providers, fibank, card-gateway, bulgaria, refund]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# Fibank — Refunds & capture

> Part of [[payment-providers-fibank]]. See the hub for the other aspects (setup & certificates, payment lifecycle).

## Purpose

This page covers what Fibank can and cannot do **after** a successful charge: full refunds, how Fibank's `RESULT` field maps to the platform payment status, and the capabilities Fibank's CloudCart integration deliberately does **not** implement — Authorize + Capture, saved cards, and wallets. It also documents the legacy iframe flag. A merchant deciding between gateways should read the contrasts here.

## Where to find it

Sidebar → **Payment Providers** → **Fibank**. Route: `/admin/payment-providers/fibank`. Refunds are initiated from the order details page (see [[orders-payment-refund]]); the capability limits below are inherent to the Fibank integration, not toggles on this screen.

## What the merchant can do here

- **Issue a full refund** for a Fibank payment from the order details page.
- **See the resulting payment status** mapped from Fibank's `RESULT`.
- The merchant **cannot** do partial refunds in the admin UI, cannot Authorize-then-Capture, and cannot offer saved cards or wallets through Fibank.

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Refund** | Initiated from the order, not this screen. Calls Fibank's refund-transaction endpoint for the **full** payment amount. | — | No partial-amount input exposed in the admin UI. |
| **`enable_iframe`** (legacy) | Boolean read from configuration; historically embedded Fibank's Ecomm page in an iframe. | Off | **Not exposed** in the current Vue settings UI — legacy carryover. |

## Business rules

### Refund support

Full refund is supported — the platform calls Fibank's refund-transaction endpoint with the original `TRANSACTION_ID`. On success the platform stores Fibank's returned `REFUND_TRANS_ID` on the payment's `provider_data.refund` field for audit and flips the status to `Refunded`. Partial refunds are protocol-supported but **no amount input is exposed** in the admin UI today — refunds use the full payment amount.

### Status code mapping

The Fibank `RESULT` field maps to the platform's [[payment-status]] as follows:

| Fibank RESULT | Mapped status |
|---------------|---------------|
| `OK` (no refund) | `Completed` |
| `OK` (with `REFUND_TRANS_ID` set) | `Refunded` |
| `PENDING`, `CREATED`, `AUTOREVERSED` | `Pending` |
| `TIMEOUT` | `Expired` (the customer didn't complete payment in Fibank's session window) |
| `FAILED`, `REVERSED`, `DECLINED` | `Canceled` |
| (anything else) | `Requested` |

This mapping is applied both on the return callback and on the periodic sync — see [[fibank-payment-lifecycle]].

### No Authorize + Capture flow

Fibank's standard Ecomm protocol on CloudCart is **single-message capture only** — there's no pre-authorize / delayed-capture surface. If the merchant needs delayed capture (e.g., for pre-orders or backorder fulfilment), they should use [[payment-providers-borica-way4]] or [[payment-providers-dsk-bank]] instead.

### No saved cards / no wallets

Fibank's CloudCart integration does not implement tokenisation / saved cards (no `SaveCard` trait). Every purchase requires the customer to enter card details on Fibank's page. Google Pay / Apple Pay wallets are also not exposed here — those merchants should look at Borica Way4 (MPay) or CloudCart Pay.

### iframe option (legacy)

The configuration stores an `enable_iframe` boolean — historically Fibank could be embedded in an iframe on storefront checkout instead of redirecting fully. This flag is **not exposed** in the Vue settings UI today; it's a legacy carryover.

## Related

- [[payment-providers-fibank]] — hub.
- [[orders-payment-refund]] — initiates a refund through Fibank from the order details page.
- [[payment-status]] — Completed / Pending / Expired / Canceled / Refunded statuses.
- [[payment-providers-borica-way4]] — alternative with saved cards / Authorize + Capture / wallets.
- [[payment-providers-dsk-bank]] — alternative card gateway with delayed-capture support.

## Open questions

- None.
