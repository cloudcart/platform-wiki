---
type: feature
nav_path: "Orders → COD sync → Eligibility"
route_name: admin.orders.sync.cod
route_path: /admin/orders/sync/cod
aliases: ["COD sync eligibility", "COD sync polling conditions", "COD sync retry cap", "When a COD order is polled", "COD sync 3-month cut-off"]
tags: [orders, cod, sync, eligibility, courier-integration]
plan_gates: ["shipping_payment_sync"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---
# COD sync — eligibility

> Part of [[orders-sync-cod]]. See the hub for related aspects (log view, polling job, status flip, errors, quota, manual alternatives).

## Purpose

Defines **which COD orders the platform actually polls** against the courier's system. Not every COD order is checked — an order must meet a strict set of conditions, and there is a hard cap on how many times any one order is retried. This is the page to consult when a merchant asks *"why isn't this COD order syncing?"*.

## Where to find it

There is no dedicated screen for eligibility — it is enforced inside the background COD-sync job. The merchant observes the result on [[orders-sync-cod-log-view]] (orders that pass appear in the log; orders that fail eligibility never appear).

## What the merchant can do here

Indirectly, the merchant controls eligibility by:
- Marking the shipment fulfilled (adding a waybill) so the order qualifies.
- Keeping the order in `pending` status until the courier reports payment.
- Using a courier whose payment provider is recognised as COD.

The merchant cannot override eligibility — it is fixed by the platform.

## Settings & fields

### The 7 conditions — an order is polled only when ALL are true

1. **Status fulfillment = `fulfilled`** — the merchant has marked the shipment as fulfilled (typically by adding a waybill / `bol_id`). Orders awaiting shipment are NOT polled.
2. **Order status = `pending`** — already-completed, refunded, or cancelled orders are skipped.
3. **Order created within the last 3 months** — older orders are excluded from polling entirely, even if still pending. Pre-3-month COD orders must be reconciled manually (see [[orders-sync-cod-manual]]).
4. **Order has a `bol_id` meta value** — the courier's waybill / parcel tracking number must exist. Without it the COD-status lookup can't be made.
5. **Order's payment provider = `cod`** — the platform-internal payment provider type must be COD. Cash-on-delivery via custom offline providers does NOT trigger this sync.
6. **Expected delivery date is more than ~3 days in the past OR not set** — if the courier's expected delivery date is in the recent future (within 24h), the order is skipped this cycle and revisited later. This prevents pinging the courier before the package even arrives.
7. **More than 24h since the last sync attempt** — the same order is NOT re-checked within 24h.

### Hard retry cap — 15 attempts per order

The platform tracks a per-order counter (`sync_payment` meta). Each failed sync attempt increments it. When the counter reaches **15**, the order is dropped from the polling pool permanently — no more attempts. From this point the merchant must reconcile manually.

Some courier errors immediately jump the counter straight to **15** to avoid burning quota on configuration problems — specifically when the courier error message contains `is not authorized to access`, `There is not enough quantity for`, or `Няма достатъчно количество за`. The full error catalogue is on [[orders-sync-cod-errors]].

## Business rules

- **Eligibility is re-evaluated every job run** — an order that fails one condition today (e.g., not yet fulfilled) becomes eligible automatically once the condition is met, with no merchant action beyond fulfilling/waybilling it.
- **The 3-month cut-off is on order creation date, not last activity** — an old order that is still pending will silently stop being polled at the 3-month mark.
- **Missing waybill is the most common "not syncing" cause** — if the courier integration didn't write a `bol_id` to the order, condition 4 fails and the order is invisible to the job. Check the waybill on [[orders-shipping-waybill]].
- **The 24h spacing means status changes can lag** — a customer who paid an hour ago won't show as paid until the next eligible cycle (and the courier itself must have reported it).
- Once an eligible order passes all checks and the courier reports collection, the platform flips it to `completed` — see [[orders-sync-cod-status-flip]].

## Related

- [[orders-sync-cod]] — hub.
- [[orders-shipping-waybill]] — where the `bol_id` waybill is set (condition 4).
- [[payment-providers-cod]] — the COD payment provider that satisfies condition 5.
- [[orders-history]] — per-order timeline showing sync attempts.

## Open questions

- Exact tolerance window on condition 6 (expected-delivery date) is approximate (~3 days). (verify)
