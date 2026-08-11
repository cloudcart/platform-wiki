---
type: feature
nav_path: "Payment Providers → Borica Way4 → Refund & Sync"
route_name: apps.borica_way4.overview
route_path: /admin/payment-providers/borica_way4
aliases: ["Borica refund", "Borica TRTYPE 24", "Borica reversal", "Borica sync", "Borica reconciliation", "Borica -24", "Borica idle timeout", "Borica retry", "Borica partial refund"]
tags: [paymentproviders, payment-providers, borica-way4, refund, sync, reconciliation]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[payment-providers-borica-way4]]. See the hub for related aspects (setup/CSR, settings, payment lifecycle, authorize/capture, save card).

# Borica Way4 — Refund & Sync

## Purpose

This aspect documents two backend-only flows that finalise the state of every Borica payment after the customer leaves the checkout: **refund** (the merchant-initiated reversal of a captured payment) and **sync** (the platform-initiated reconciliation of payments still in `Pending` after the customer drop-off). Together they ensure no Borica payment stays in an indeterminate state for more than 5 minutes.

## Where to find it

- **Refund** — Order details page → Payments → **Refund** action, which calls into the Borica refund flow. See [[orders-payment-refund]].
- **Sync** — Order details page → Payments → **Sync status** action (manual single-payment sync), plus the automatic platform-wide reconciliation job that runs every 5 minutes.

## What the merchant can do here

- **Refund a Completed Borica payment** from the order details page — see [[orders-payment-refund]].
- **Manually re-sync a Pending Borica payment** from the order details page if the IPN was missed or the customer never returned.

## Settings & fields

This aspect does not expose its own fields — refund and sync are backend flows triggered from the order details page. The settings that affect this aspect are on [[borica-way4-settings-fields]] (Mode, EGW_SECURITY for signature verification on the sync response). The refund and sync actions themselves live on the order details page; see [[orders-payment-refund]] and [[orders-details]].

## Business rules

### Refund — full vs partial

Full refunds are fully supported via Borica's `TRTYPE=24` (reversal). The platform marks the payment as `Refunded` on `RC=00`.

**Partial refunds are protocol-allowed but not exposed in the admin UI today**:

- The platform always sends the **payment row's stored amount** as the refund amount.
- The refund button on the order details page does **not** surface an editable amount input.
- Borica's protocol accepts a smaller amount in the `TRTYPE=24` request — partial refunds via API integration would work — but a merchant cannot trigger a partial refund from the UI. `(verify)`

If the response is flagged as a reversal and `RC=00`, the platform flips the payment to `Refunded`.

### Refund vs Cancel authorization — different stages

- **Cancel authorization** (`TRTYPE=22`) applies before capture — releases a hold without charging. See [[borica-way4-authorize-capture]].
- **Refund** (`TRTYPE=24`) applies after capture — reverses a completed charge.

The order details page surfaces whichever action is appropriate for the current payment state. An `Authorized` payment can only be cancelled, not refunded. A `Completed` payment can only be refunded.

### Sync — what it does

The sync flow calls Borica's transaction-fetch endpoint with the stored `INT_REF` to reconcile the platform's payment status with Borica's view. It is called in two ways:

1. **Manual sync** — from the order details page, the merchant clicks *Sync status* and the platform calls Borica directly.
2. **Automatic platform-wide sync** — the platform-wide reconciliation job (`borica_way4_status` → `SyncStatus`) runs every **5 minutes** (interval 300 s, single-flighted on the `cc-system8` queue) and polls Borica for the status of every Pending Borica payment platform-wide.

So a customer who closes the browser mid-payment (and never hits the return URL) will have their stranded order's final status — `paid` or `canceled` — settled within at most 5 minutes by this polling loop, without merchant intervention. See [[borica-way4-payment-lifecycle]] for the status-code mapping.

### Sync — retry behaviour

The HTTP client used for sync calls has these timeouts:

- **5-second connection timeout**.
- **10-second max duration**.
- Up to **3 retries** on idle / read timeouts.

If Borica is briefly unreachable, the sync queue retries up to 3 times before giving up for this cycle. The next 5-minute tick picks the payment up again.

### Sync — `-24` auto-cancel

If Borica returns response code `-24` (transaction not found) for a still-pending payment, the platform auto-marks it as `Canceled`. This clears stale checkout drop-offs where the customer started a payment but Borica never received the transaction (e.g., customer closed the page before submitting the card).

> This is the most common terminal-state for abandoned Borica checkouts and is **expected behaviour** — not a sign of a misconfigured terminal.

### Idempotency on IPN

Borica IPNs (see [[borica-way4-payment-lifecycle]]) can fire multiple times. The platform locates the payment by `NONCE=<provider_reference_id>` and re-evaluates status. Re-applying the same status is a no-op. Refunds are tracked by the `isReversal` flag so a re-delivered IPN does not double-refund. `(verify)`

## How it works (verified against backend)

### Refund call

The refund call sends `TRTYPE=24` (reversal) with the original `RRN` + `INT_REF` stored on the payment row. Response code `00` flips the payment to `Refunded`. Refund amount used is the payment row's stored amount.

### Sync call

The sync call calls Borica's transaction-fetch endpoint with the stored `INT_REF` to retrieve the latest status. The HTTP client uses 5 s connection + 10 s max duration, retried up to 3 times on idle / read timeouts. The response code maps to the platform's payment status using the same table as the IPN path — see [[borica-way4-payment-lifecycle]].

### Reconciliation job cadence

- Runs every **300 seconds** (5 minutes).
- Single-flighted on the `cc-system8` queue so two ticks cannot run concurrently.
- Polls every Borica payment in `Pending` state platform-wide (not per-store).
- Each polled payment is run through the same sync call described above.

## Related

- [[payment-providers-borica-way4]] — hub.
- [[borica-way4-payment-lifecycle]] — status-code mapping shared between IPN and sync paths.
- [[borica-way4-authorize-capture]] — cancel-authorization (`TRTYPE=22`) is the pre-capture analogue of refund.
- [[orders-payment-refund]] — the order-details action that triggers `TRTYPE=24`.
- [[orders-details]] — where the manual *Sync status* action lives.
- [[payment-status]] — Refunded / Canceled / Pending state values.

## Open questions

- ⏸️ Whether the order-details refund flow will ever expose an editable amount input for partial refunds. Today it always sends the full stored amount. `(verify)`
- ⏸️ Exact idempotency guarantees on re-delivered IPNs (whether the platform suppresses re-firing the `payment.refunded` webhook on a duplicate Borica reversal IPN). `(verify)`
