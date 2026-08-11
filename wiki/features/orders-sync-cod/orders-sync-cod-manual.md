---
type: feature
nav_path: "Orders → COD sync → Manual alternatives"
route_name: admin.orders.sync.cod
route_path: /admin/orders/sync/cod
aliases: ["COD sync manual override", "COD sync no per-order button", "Manually mark COD paid", "Force COD sync", "COD sync workarounds"]
tags: [orders, cod, sync, manual, courier-integration]
plan_gates: ["shipping_payment_sync"]
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---
# COD sync — manual alternatives

> Part of [[orders-sync-cod]]. See the hub for related aspects (log view, eligibility, polling job, status flip, errors, quota).

## Purpose

Explains that there is **no per-order Sync button** on the COD sync page and documents the manual alternatives a merchant has when they don't want to wait for the automatic poll — plus the caveats of each. This is the page to consult when a merchant asks *"how do I force a COD order to sync right now?"*.

## Where to find it

The COD sync page itself (`/admin/orders/sync/cod`) has no manual trigger. The alternatives live on other surfaces — the order's payment row ([[orders-payment-mark-paid]]) and the background-queue trigger ([[settings-queue-view]]).

## What the merchant can do here

- Manually mark a COD payment as paid from the order detail page.
- Fire the global COD-sync job from the queue surface (affects all eligible orders, not one).
- Wait for the next scheduled run.

## Settings & fields

### No per-order Sync button

There is no per-order Sync control on the COD sync page. To trigger a one-off sync the merchant must either:

1. Use the queue-trigger surface ([[settings-queue-view]]) to fire the platform's COD-sync job. This applies **globally** — the merchant cannot pick a single order; it runs the normal eligibility filter over the whole pool. See [[orders-sync-cod-eligibility]].
2. Or wait for the next scheduled run (typically several hours between runs — see [[orders-sync-cod-polling-job]]).

### Manual override — Mark as paid

If the merchant is impatient or the courier hasn't reported back, they can manually mark the COD payment as paid via [[orders-payment-mark-paid]] on the order detail page. This sets the payment to `completed` with the merchant's provided reference.

## Business rules

### Manual mark-paid can still race the auto-sync

The background COD-sync job queries by waybill, not by payment status. The job's first check ("is the order already completed?") skips orders already `completed`. But if the merchant marked the order `paid` (not `completed`), the order may still be in the polling pool — so the auto-sync can later fire for the same order. To be safe, the merchant should mark it in a way that lands the order at `completed`, or accept that a later sync may overwrite the recorded amount with the courier-reported figure (see [[orders-sync-cod-status-flip]]).

### Global trigger, not surgical

Firing the job from [[settings-queue-view]] processes up to 100 eligible orders across the whole store — it is not a way to sync one specific order ahead of the others. An order that fails eligibility won't sync no matter how often the job is fired; check [[orders-sync-cod-eligibility]] first.

### Pre-3-month orders are manual-only

Orders older than 3 months are excluded from polling entirely (eligibility condition 3). For those, manual Mark as paid via [[orders-payment-mark-paid]] is the only option — the auto-sync will never pick them up.

### Exhausted quota forces manual reconciliation

When the COD-sync quota is exhausted, manual Mark as paid is the merchant's interim path until they upgrade or buy capacity. See [[orders-sync-cod-quota]].

## Related

- [[orders-sync-cod]] — hub.
- [[orders-payment-mark-paid]] — the manual Mark-as-paid action on the order detail page.
- [[settings-queue-view]] — the only way to fire the COD-sync job on demand (globally).
- [[orders-sync-cod-eligibility]] — the eligibility filter that a manual job run still applies.
- [[orders-sync-cod-status-flip]] — what a later auto-sync writes if it races a manual mark-paid.

## Open questions

None.
