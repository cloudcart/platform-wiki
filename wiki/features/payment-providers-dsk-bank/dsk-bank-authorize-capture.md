---
type: feature
nav_path: "Payment Providers → DSK Bank → Authorize & Capture"
route_name: apps.dsk_bank.overview
route_path: /admin/payment-providers/dsk_bank
aliases: ["DSK Bank authorize", "DSK Bank manual capture", "DSK Two-Step", "DSK pre-authorize", "DSK capture window", "DSK registerPreAuth", "DSK deposit reverse"]
tags: [paymentproviders, payment-providers, dsk-bank, card-gateway, authorize, capture, manual-capture]
plan_gates: [authorize_payment]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-dsk-bank]]. See the hub for related aspects (settings, payment lifecycle, refund/currency).

# DSK Bank — Authorize & Capture (manual capture)

## Purpose

This aspect documents the **two-phase** card-payment flow for DSK Bank: the platform first **authorises** the card (reserves funds without charging), then **captures** the funds later — typically after the merchant confirms the order can ship. Useful for pre-orders, partial stock confirmation, or any flow where the merchant wants to avoid charging cards for orders they may cancel. This is gated by the `authorize_payment` plan feature.

## Where to find it

- The **Authorization mode** dropdown lives on the DSK Bank settings page — see [[dsk-bank-settings-fields]].
- The **Capture** + **Cancel authorization** actions live on the order details page — see [[orders-payment-capture]].

## What the merchant can do here

- **Switch the provider to Manual capture** by setting Authorization mode = Manual (if the plan supports `authorize_payment`).
- **Capture an authorized payment** from the order details page — see [[orders-payment-capture]].
- **Cancel an authorization** from the order details page (releases the hold without charging) — see [[orders-payment-capture]].
- **Switch back to Auto capture** at any time — only future orders use the new mode.

## Settings & fields

The Authorization-mode dropdown is the only field that belongs to this aspect; it lives on the main DSK Bank settings page and is documented as a row in the field table on [[dsk-bank-settings-fields]]:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Authorization mode** | Auto-capture (full purchase in a single message) vs Manual (Two-Step) capture: authorize now, capture later. | Auto | Server returns *"Your plan does not support authorized payments."* if the current plan lacks the `authorize_payment` feature — see [[plan-gates]]. |

The Capture / Cancel-authorization actions themselves are not on the DSK settings page — they live on the order details page; see [[orders-payment-capture]].

## Business rules

### Capture mode — auto-capture vs Two-Step

When **Authorization mode** is **Auto**, the platform issues a 1-step authorize request (DSK Way4 jargon — actually a full purchase in single-message mode). The funds are reserved + captured in one call.

When **Authorization mode** is **Manual**, the platform issues a Two-Step authorize (TRTYPE 12). The order is marked `Authorized`. The merchant has up to **7 days** (DSK's standard auth window) to either:

- **Capture** the held funds via [[orders-payment-capture]] — calls DSK's deposit endpoint.
- **Cancel** the authorization via [[orders-payment-capture]] (release) — calls DSK's reverse endpoint.

### Capture window

DSK's standard authorization window is **7 days**. After that the authorization expires bank-side and the funds are released automatically — a subsequent capture will fail. The merchant should capture before the window closes. `(verify)` — the exact 7-day default may vary by issuer / card scheme; CloudCart does not surface a countdown in the admin.

### Capture amount

The platform sends the held authorization amount on capture. DSK's protocol supports a smaller (partial) capture amount, but the CloudCart admin does not surface an editable capture-amount input today. `(verify)`

### Plan gate — `authorize_payment`

The **Authorize** option is only enabled on plans with the `authorize_payment` feature. Lower-tier plans that lack it get the verbatim server error on save:

> *"Your plan does not support authorized payments."*

See [[plan-gates]] for the cross-cutting plan-feature concept.

### Status while authorized

A successful Two-Step pre-auth maps DSK `orderStatus 1` → platform `Authorized` — see the status-code table on [[dsk-bank-payment-lifecycle]]. A still-pending authorized payment is reconciled by the periodic sync described there.

## How it works (verified against backend)

Supported via DSK Way4's Two-Step Auth flow. Built on the `omnipay-dsk-bank` driver.

### Authorization mode = Manual

1. The customer pays at checkout. The platform calls `registerPreAuth` (instead of `registerOrder`) — see [[dsk-bank-payment-lifecycle]] for the base purchase request shape.
2. DSK reserves funds on the card. The order moves to `Authorized`.
3. The merchant later opens the order details page and either:
   - **Captures** — `captureAuthorization` calls DSK's `deposit` endpoint with the held amount (partial capture supported if a smaller amount is sent).
   - **Cancels** — `cancelAuthorization` calls DSK's `reverse` endpoint to release the hold.

### Authorization mode = Auto

The platform calls `registerOrder` (full purchase, single message). Funds are reserved + captured in one call; there is no later capture step.

### Authorization window

DSK's standard 7 days. Plan-gated by `authorize_payment`.

## Related

- [[payment-providers-dsk-bank]] — hub.
- [[dsk-bank-settings-fields]] — where the Authorization-mode dropdown lives.
- [[dsk-bank-payment-lifecycle]] — the base purchase flow this aspect extends with the pre-auth variant + the `Authorized` status mapping.
- [[orders-payment-capture]] — the order-details action that captures or cancels an authorization.
- [[orders-payment-refund]] — refund of an already-captured payment.
- [[payment-status]] — Authorized → Completed / Canceled state transitions.
- [[plan-gates]] — the `authorize_payment` plan feature gating this aspect.

## Open questions

- ⏸️ Whether the 7-day authorization window is bank-fixed or merchant-tunable on DSK's side. CloudCart does not surface a countdown today. `(verify)`
- ⏸️ Whether partial capture (smaller amount than the original authorization) is exposed in any admin surface. Not in the order-details UI today. `(verify)`
