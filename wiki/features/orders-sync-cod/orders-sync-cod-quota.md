---
type: feature
nav_path: "Orders → COD sync → Quota"
route_name: admin.orders.sync.cod
route_path: /admin/orders/sync/cod
aliases: ["COD sync quota", "COD sync capacity", "COD sync subscription", "Add more COD", "shipping_payment_sync plan gate", "COD sync period"]
tags: [orders, cod, sync, plan-gate, billing]
plan_gates: ["shipping_payment_sync"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---
# COD sync — quota

> Part of [[orders-sync-cod]]. See the hub for related aspects (log view, eligibility, polling job, status flip, errors, manual alternatives).

## Purpose

Describes the **plan-gated, metered capacity** behind COD sync: how many sync events the merchant gets per period, what happens when that runs out, and the *"Add more COD"* upgrade path. This is the page to consult when a merchant asks *"why did my COD orders stop syncing mid-month?"*.

## Where to find it

The usage banner at the top of the COD sync page (`/admin/orders/sync/cod`) — see [[orders-sync-cod-log-view]] for the banner layout. The upgrade flow opens from the *"Add more COD"* link.

## What the merchant can do here

- See the current period, events used, and events remaining.
- Click *"Add more COD"* (when remaining = 0) to reach the upgrade / pack-purchase flow.
- The merchant cannot reset or extend the quota except by upgrading / buying packs.

## Settings & fields

### Metered plan gate — `shipping_payment_sync`

COD sync is a plan-gated feature with **explicit usage metering** — distinct from on/off plan gates because the merchant can buy add-on packs. The merchant consumes one sync event each time the platform polls and registers a status change for a COD order.

### Period — calendar month, not billing month

The "Period" line shows the **calendar month** range as `d.m.Y - d.m.Y` (e.g., `01.05.2026 - 31.05.2026`), derived from start-of-month / end-of-month. This is the same window used for the quota count and the list query, so usage stats, the log view, and quota all align on calendar months. Merchants whose plan billing cycle differs from the calendar month still see the COD quota reset at month-end (00:00 on day 1).

### Per-store quota — no shared pool

The plan usage / remaining lookups are scoped to the **current store (site)**. Merchants running multiple stores via the Stores app get a separate COD-sync quota per store; there is no shared cross-store pool.

### "Add more COD" link target

The link routes to the plan-feature upgrade page for `shipping_payment_sync` (per [[plan-gates]]). Depending on the merchant's current plan tier, this is either:
- A "Buy more COD-sync events" purchase form (if the plan supports buying packs), OR
- A plan-upgrade prompt (if the plan is the baseline and doesn't allow add-on packs).

The merchant lands on the standard plan-upgrade UI; resolution happens there, not on the COD sync page.

## Business rules

### Quota exhaustion stops sync

When the `shipping_payment_sync` quota is exhausted for the period, the background-job system **stops recording new sync events** for COD orders. The merchant misses status updates until they upgrade or buy capacity — and must reconcile COD payments manually via the courier's own dashboard in the meantime (see [[orders-sync-cod-manual]]).

### Job-level capacity pre-check

Before doing any work, each run of the polling job checks that plan capacity is available; if not, the run stops with an access-denied-by-plan condition. So an exhausted quota blocks the whole run, not just individual orders. See [[orders-sync-cod-polling-job]].

### Plan-expired / suspended sites get no sync

The same job-level pre-checks also bail out on a plan-expired, suspended, or in-maintenance site (see [[orders-sync-cod-polling-job]]). A merchant whose plan has lapsed will see zero sync events even with quota nominally remaining.

### Quota-burn protection

The platform caps retries per order and jumps the attempt counter to 15 on permanent configuration errors specifically to avoid wasting quota — see [[orders-sync-cod-errors]] and [[orders-sync-cod-eligibility]].

## Related

- [[orders-sync-cod]] — hub.
- [[plan-gates]] — concept page on plan-based feature gating; `shipping_payment_sync` is one such gate.
- [[plan]] — the merchant's plan tier governs base quota and pack availability.
- [[orders-sync-cod-log-view]] — the usage banner that renders these figures.
- [[orders-sync-cod-polling-job]] — the run-level capacity pre-check.

## Open questions

None.
