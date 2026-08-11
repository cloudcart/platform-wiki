---
type: feature
nav_path: "Payment Providers → Borica Way4 → Authorize & Capture"
route_name: apps.borica_way4.overview
route_path: /admin/payment-providers/borica_way4
aliases: ["Borica manual capture", "Borica authorize", "Borica pre-authorize", "Borica TRTYPE 12", "Borica TRTYPE 21", "Borica TRTYPE 22", "Borica two-phase", "authorize_payment plan gate"]
tags: [paymentproviders, payment-providers, borica-way4, authorize, capture, manual-capture]
plan_gates: [authorize_payment]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-borica-way4]]. See the hub for related aspects (setup/CSR, settings, payment lifecycle, save card, refund/sync).

# Borica Way4 — Authorize & Capture (manual capture)

## Purpose

This aspect documents the **two-phase** card-payment flow: the platform first **authorises** the card (reserves funds without charging), then **captures** the funds later — typically after the merchant confirms the order can ship. Useful for pre-orders, partial stock confirmation, or any flow where the merchant wants to avoid charging cards for orders they'll cancel. This is gated by the `authorize_payment` plan feature.

## Where to find it

- The **Authorization mode** dropdown lives on the Borica Way4 settings page — see [[borica-way4-settings-fields]].
- The **Capture** + **Cancel authorization** actions live on the order details page — see [[orders-payment-capture]].

## What the merchant can do here

- **Switch the provider to Manual capture** by setting Authorization mode = Manual (if the plan supports `authorize_payment`).
- **Capture an authorized payment** from the order details page — see [[orders-payment-capture]].
- **Cancel an authorization** from the order details page (releases the hold without charging).
- **Switch back to Auto capture** at any time — only future orders use the new mode; existing authorised orders retain their mode.

## Settings & fields

The Authorization-mode dropdown is the only field that belongs to this aspect; it lives on the main Borica settings page and is documented as a row in the field table on [[borica-way4-settings-fields]]:

| Field / Control | What it does | Default | Validation / notes |
|-----------------|--------------|---------|--------------------|
| **Authorization mode** | Auto-capture (charge immediately, `TRTYPE=1`) vs Manual capture (authorize now via `TRTYPE=12`, capture later via `TRTYPE=21`). | Auto-capture | Server returns *"Your plan does not support authorized payments."* if the current plan lacks the `authorize_payment` feature — see [[plan-gates]]. |

The Capture / Cancel-authorization actions themselves are not on the Borica settings page — they live on the order details page; see [[orders-payment-capture]].

## Business rules

### Two TRTYPE values gate the flow

The flow is identified by Borica's `TRTYPE` (transaction type) values:

| TRTYPE | Meaning | When used |
|--------|---------|-----------|
| `1` | Purchase (auto-capture) | Authorization mode = Auto. Funds captured immediately at the same time as authorization. |
| `12` | Pre-authorize | Authorization mode = Manual. Funds reserved on the card without charging. Order moves to `Authorized`. |
| `21` | Capture | Triggered later from the order details page for an Authorized payment. Sends the stored payment amount. |
| `22` | Cancel authorization | Triggered later from the order details page. Releases the hold without charging. |

When **Authorization mode = Auto** (default), `TRTYPE=1` is sent and capture is immediate. Manual capture and cancel-authorization are no-ops in this mode.

### Plan gate — `authorize_payment`

The Authorization-mode dropdown is **plan-gated** through the `authorize_payment` feature key. Lower-tier plans see the dropdown but the server rejects the save with the verbatim error:

> *"Your plan does not support authorized payments."*

See [[plan-gates]] for the cross-cutting plan-feature concept.

### Capture window

Borica's default authorization window is typically **7 days**. After that the authorization expires bank-side and the funds are released automatically — a subsequent `TRTYPE=21` capture will fail. The merchant should capture before the window closes.

> `(verify)` — the exact 7-day default may vary by issuer / card scheme. Borica documents it as bank-configurable; CloudCart does not surface a countdown in the admin.

### Capture amount

The platform sends the **payment row's stored amount** as the capture amount. Borica also accepts a smaller amount in the `TRTYPE=21` request, but the CloudCart admin does not surface an editable capture-amount input today — partial captures from the UI are not possible. `(verify)`

### Save card + Authorize — pick one

When both **Save Customer Card** is ON and **Authorization mode = Manual**, the runtime picks the **authorize** branch — the token-save branch is skipped on the authorize call. The two flags can coexist in configuration but the merchant should pick one for clarity. Auto-capture + Save Customer Card is the most common pairing. See [[borica-way4-save-card-wallets]].

### Sync still reconciles authorized payments

A still-pending `Authorized` payment is reconciled by the platform's 5-minute sync — see [[borica-way4-refund-sync]] for the cadence. The `-24` "transaction not found" auto-cancel rule applies to the authorize phase too.

## How it works (verified against backend)

### Authorization mode = Manual

1. The customer pays at checkout. The platform sends the purchase form with `TRTYPE=12` (pre-authorize) — see [[borica-way4-payment-lifecycle]] for the full purchase request shape.
2. Borica reserves funds on the card. The customer sees a successful payment; the issuer holds the amount.
3. The order moves to `Authorized` in CloudCart (per the status-code mapping in [[borica-way4-payment-lifecycle]]).
4. The merchant later opens the order details page and either:
   - **Captures** — clicks the Capture action; the platform sends `TRTYPE=21` with the stored `RRN` + `INT_REF` and the payment row's amount. On `RC=00`, payment status becomes `Completed`.
   - **Cancels** — clicks the Cancel-authorization action; the platform sends `TRTYPE=22` with the stored `RRN` + `INT_REF`. On `RC=00`, payment status becomes `Canceled`.

### Authorization mode = Auto

1. The customer pays at checkout. The platform sends `TRTYPE=1` (purchase).
2. On `RC=00`, the payment is `Completed` immediately. There is no later capture step.
3. The Capture / Cancel-authorization actions on the order details page are not available for this payment.

### Refund vs Cancel authorization

The two are distinct. Cancel authorization (`TRTYPE=22`) only applies before capture — it releases the hold. After capture, only **refund** (`TRTYPE=24`) is possible — see [[borica-way4-refund-sync]].

## Related

- [[payment-providers-borica-way4]] — hub.
- [[borica-way4-settings-fields]] — where the Authorization-mode dropdown lives.
- [[borica-way4-payment-lifecycle]] — base purchase flow that this aspect extends with TRTYPE 12 / 21 / 22.
- [[borica-way4-refund-sync]] — refund vs cancel-authorization distinction.
- [[orders-payment-capture]] — the order-details action that triggers `TRTYPE=21`.
- [[orders-payment-refund]] — the order-details refund action (for already-captured payments).
- [[payment-status]] — Authorized → Completed / Canceled state transitions.
- [[plan-gates]] — the `authorize_payment` plan feature gating this aspect.

## Open questions

- ⏸️ Whether the 7-day authorization window is bank-fixed or merchant-tunable on Borica's side. CloudCart does not surface a countdown today. `(verify)`
- ⏸️ Whether partial capture (smaller amount than the original authorization) is exposed in any admin surface. Not in the order-details UI today; the platform always sends the full stored amount. `(verify)`
