---
type: feature
nav_path: "Payment Providers → Raiffeisen Bank → Capture & authorize"
route_name: apps.raiffeisen.overview
route_path: /admin/payment-providers/kbc
aliases: ["Raiffeisen authorize", "Raiffeisen capture", "Raiffeisen manual capture", "Raiffeisen two-phase payment", "Raiffeisen Delay flag", "Raiffeisen authorized payment", "Райфайзен отложено плащане", "Райфайзен авторизация"]
tags: [paymentproviders, payment-providers, raiffeisen, kbc, card-gateway, authorize, capture]
plan_gates: [authorize_payment]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[payment-providers-raiffeisen]]. See the hub for the other aspects (setup, save-card, refund/sync/status).

# Raiffeisen Bank — Capture & authorize

## Purpose

This aspect covers Raiffeisen's **two-phase payment** (Authorize + Capture). When enabled, a purchase only *reserves* funds on the customer's card; the merchant later captures (charges) or cancels (releases) the reservation. This is used for stores that confirm stock or fulfilment before taking money. When disabled, every purchase captures immediately.

## Where to find it

The **Authorization mode** control sits on the Raiffeisen overview page (Sidebar → **Payment Providers** → **Raiffeisen Bank**) in the standard settings rows. Route: `/admin/payment-providers/kbc`. The capture / cancel actions themselves are triggered later from the order, not from this screen — see [[orders-payment-capture]].

## What the merchant can do here

- **Pick Authorization mode** — Auto-capture (default) or Manual capture.
- After a Manual-mode order is placed and `Authorized`, **Capture** the held funds from the order's payment panel (see [[orders-payment-capture]]).
- Alternatively **Cancel** the authorization to release the hold (also from [[orders-payment-capture]]).

## Settings & fields

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Authorization mode** | Auto-capture vs Manual capture. | Auto | Plan gate: server returns *"Your plan does not support authorized payments."* if the plan lacks `authorize_payment`. When Authorize is on, **Save customer card is forcibly disabled** at runtime — see [[raiffeisen-save-card]]. |

## Business rules

### The Delay flag drives the two-phase behaviour

- **Manual** mode → the platform sends `Delay=1` on every purchase. Raiffeisen reserves the funds without capturing. The order is marked `Authorized` (see [[payment-status]]).
- **Auto** mode → the platform sends `Delay=0` and the purchase is captured immediately, landing the payment at `Completed`.

### Capture window — 7 days

After a Manual-mode authorization, the merchant has up to **7 days** (Raiffeisen's standard hold window) to capture or cancel. After that the hold expires bank-side.

### Capture

Triggered from [[orders-payment-capture]]. The platform calls Raiffeisen's `capture` endpoint with `Rrn` (retrieval reference number) and `PostauthorizationAmount` from the original authorization. Raiffeisen response code `507` ("already captured") is treated as a **non-error** — the payment is simply confirmed as `Completed`.

### Cancel

Triggered from [[orders-payment-capture]]. To release a hold, the platform internally calls `refund` against the authorization and then flips the platform status to `Canceled`. (There is no separate "void" call — cancel reuses the refund path.)

### Plan-tier gating

The Raiffeisen provider itself has no plan gate — any plan that allows payment providers can install it. **Only** the Authorize + Capture toggle is plan-gated, via the `authorize_payment` feature (see [[plan-gates]]). On a plan without it, saving Authorize returns *"Your plan does not support authorized payments."*

### Mutually exclusive with Save customer card

Save-card (UPCToken) and Authorize cannot run together. If both flags are saved as ON, the integration disables save-card at request time — Raiffeisen's tokenisation flow does not combine with two-step authorize. The merchant should pick one. Full mechanics in [[raiffeisen-save-card]].

## Related

- [[payment-providers-raiffeisen]] — hub.
- [[orders-payment-capture]] — where the merchant captures / cancels an authorized Raiffeisen payment.
- [[payment-status]] — `Authorized` → `Completed` / `Canceled` transitions for Raiffeisen.
- [[plan-gates]] — the `authorize_payment` feature gate.
- [[payment-provider]] — entity definition.

## Open questions

None.
