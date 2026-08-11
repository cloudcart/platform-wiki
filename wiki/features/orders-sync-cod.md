---
type: feature
nav_path: "Orders → COD sync"
route_name: admin.orders.sync.cod
route_path: /admin/orders/sync/cod
aliases: ["COD sync", "Cash on delivery sync", "COD synchronization log", "Синхронизация на наложен платеж", "COD статус"]
tags: [orders, cod, sync, courier-integration, smarty]
plan_gates: ["shipping_payment_sync"]
created: 2026-05-21
updated: 2026-06-10
source_count: 8
---
# COD sync

## Purpose

The merchant's **Cash-on-Delivery sync log** — shows when each COD order was checked against the courier's system and what the result was (paid / unchanged / error). Used by stores running couriers that mirror COD payment status back to CloudCart (typically Bulgarian couriers Econt, Speedy, etc.). Each row is a sync event for one order, not the order itself.

The platform polls participating courier APIs on a schedule; when a courier reports the customer has paid a COD package, the platform records the event here and flips the order straight to `completed`. The page is the **audit / debug surface** for that automatic sync activity, plus the **plan-gated capacity meter** (period / used / remaining).

This page documents a multi-part flow. It is split into a hub (this page) plus seven aspect sub-pages — see **Sub-pages** below. Drill into the aspect that matches the question rather than reading every page.

## Where to find it

Sidebar → Orders → **COD sync** (or directly via `/admin/orders/sync/cod`).

Route: `/admin/orders/sync/cod`. Method: GET (initial render) / POST (AJAX grid).

## What the merchant can do here

- **Read the sync log** — one row per COD order synced this calendar month, showing datetime, order ID, action result, and courier. See [[orders-sync-cod-log-view]].
- **Filter by courier provider** — narrow the log to one shipping provider. See [[orders-sync-cod-log-view]].
- **Preview an order** — click an Order ID to open a slide-from-right side panel without leaving the log. See [[orders-sync-cod-log-view]].
- **Watch capacity** — the usage banner shows period / used / remaining and a *"Add more COD"* link when exhausted. See [[orders-sync-cod-quota]].

What the merchant **cannot** do here:
- Manually trigger a sync for one order — see [[orders-sync-cod-manual]] for the workarounds.
- Edit / delete sync records — they are an audit trail.
- See sync events for orders placed in previous months — the view is scoped to the current calendar month.
- Configure which couriers participate — that is done by enabling COD-sync on the courier in [[apps]] / [[shipping]].

## Settings & fields

The page itself has only a Provider filter and the read-only log grid; the full field-level breakdown is on [[orders-sync-cod-log-view]]. The behaviours that produce the rows live on the aspect pages:

- **Eligibility** — the 7 conditions an order must meet to be polled. See [[orders-sync-cod-eligibility]].
- **The polling job** — schedule, throughput caps, job-level pre-checks. See [[orders-sync-cod-polling-job]].
- **The status flip** — what a successful sync writes to the order. See [[orders-sync-cod-status-flip]].
- **Error handling** — how courier errors are bucketed and shown. See [[orders-sync-cod-errors]].

## Business rules

- COD sync is **fully automatic** — the merchant never triggers it from this page. The platform's background-job system polls courier APIs on a schedule. See [[orders-sync-cod-polling-job]].
- A successful sync flips the order **directly to `completed`** (not `paid`) and overwrites the payment amount with the courier-reported sum. See [[orders-sync-cod-status-flip]].
- The feature is **plan-gated with metered capacity** (`shipping_payment_sync`). Quota exhaustion stops new sync events. See [[orders-sync-cod-quota]].
- An order must meet **all 7 eligibility rules** (fulfilled, pending, < 3 months old, has waybill, COD provider, delivery-date window, < 24h since last attempt) to be polled. See [[orders-sync-cod-eligibility]].
- Sync events are visible **only for the current calendar month**; older history lives on each order's own page. See [[orders-sync-cod-log-view]].

## Sub-pages (in this cluster)

- [[orders-sync-cod-log-view]] — the page UI: usage banner, list grid (one row per order, latest sync only), Provider filter, side-panel preview, empty state, current-month scope.
- [[orders-sync-cod-eligibility]] — the 7 conditions an order must satisfy to be polled, the 3-month cut-off, and the 15-attempt hard retry cap.
- [[orders-sync-cod-polling-job]] — the background polling job: schedule, queue, 100-orders-per-run cap, Rapido 1.1s throttle, and the job-level site/plan pre-checks.
- [[orders-sync-cod-status-flip]] — what a successful sync writes: direct flip to `completed`, courier-amount override, payment-record changes, downstream notification pipeline.
- [[orders-sync-cod-errors]] — courier-error categorisation (ignore / continue / search / restart buckets), verbatim error fragments, and quota-burn protection.
- [[orders-sync-cod-quota]] — the `shipping_payment_sync` plan gate: per-store metered capacity, period display, exhaustion behaviour, and the *"Add more COD"* upgrade path.
- [[orders-sync-cod-manual]] — why there is no per-order Sync button and the manual alternatives (Mark as paid, global queue trigger) plus their caveats.

## Related

- [[orders]] — parent orders list.
- [[orders-details]] — clicking an order ID opens its detail in a side panel.
- [[shipping]] — courier integrations + COD-sync activation.
- [[apps]] — courier apps (Econt, Speedy, etc.) that implement COD sync.
- [[settings-statuses]] — payment status transitions triggered by sync events.
- [[settings-queue-view]] — the background-job system that runs the COD-sync polls.
- [[plan]] — plan tier governs base COD-sync quota.
- [[plan-gates]] — concept page on plan-based feature gating.

## Open questions

None.
