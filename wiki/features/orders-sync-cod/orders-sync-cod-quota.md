---
type: feature
nav_path: "Orders → COD sync → Quota"
route_name: admin.orders.sync.cod
route_path: /admin/orders/sync/cod
aliases: ["COD sync quota", "COD sync capacity", "COD sync subscription", "Add more COD", "shipping_payment_sync plan gate", "COD sync period", "COD sync pack", "Синхронизация на наложени платежи лимит"]
tags: [orders, cod, sync, plan-gate, billing]
plan_gates: ["shipping_payment_sync"]
created: 2026-06-10
updated: 2026-11-09
source_count: 4
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

COD sync is a plan-gated feature with **explicit usage metering** — distinct from on/off plan gates because the merchant can buy add-on packs.

**One unit = one order the sync marked as paid in the current calendar month.** The count is the orders whose payout the sync recorded with a last sync date in this month. Polls that find nothing, and failed attempts, use nothing.

**The monthly limit** is the plan's own value plus the value of every active paid pack for this feature. A pack therefore raises the limit in every month while it is active; unused units do not carry over. The plan's own value and the pack prices are in the plan and billing catalog, not in the code.

### Period — calendar month, not billing month

The "Period" line shows the **calendar month** range as `d.m.Y - d.m.Y` (e.g., `01.05.2026 - 31.05.2026`), derived from start-of-month / end-of-month. This is the same window used for the quota count and the list query, so usage stats, the log view, and quota all align on calendar months. Merchants whose plan billing cycle differs from the calendar month still see the COD quota reset at month-end (00:00 on day 1).

### Per-store quota — no shared pool

The plan usage / remaining lookups are scoped to the **current store (site)**. Merchants running multiple stores via the Stores app get a separate COD-sync quota per store; there is no shared cross-store pool.

### "Add more COD" link target

The link routes to the plan-feature upgrade page for `shipping_payment_sync` (per [[plan-gates]]). Depending on the merchant's current plan tier, this is either:
- A "Buy more COD-sync events" purchase form (if the plan supports buying packs), OR
- A plan-upgrade prompt (if the plan is the baseline and doesn't allow add-on packs).

The merchant lands on the standard plan-upgrade UI; resolution happens there, not on the COD sync page. Buying a pack restarts the store's COD-sync job; it does not install or subscribe to any courier app.

## Business rules

### Quota exhaustion stops sync

When the `shipping_payment_sync` quota is exhausted for the period, the background-job system **stops recording new sync events** for COD orders. The merchant misses status updates until they upgrade or buy capacity — and must reconcile COD payments manually via the courier's own dashboard in the meantime (see [[orders-sync-cod-manual]]).

### Job-level capacity pre-check

Before doing any work, each run of the polling job checks that plan capacity is available; if not, the run stops with an access-denied-by-plan condition. So an exhausted quota blocks the whole run, not just individual orders. See [[orders-sync-cod-polling-job]].

### Plan-expired / suspended sites get no sync

The same job-level pre-checks also bail out on a plan-expired, suspended, or in-maintenance site (see [[orders-sync-cod-polling-job]]). A merchant whose plan has lapsed will see zero sync events even with quota nominally remaining.

### Quota-burn protection

Failed attempts never use quota (only an order marked paid counts). The platform also caps retries per order and jumps the attempt counter to 15 on permanent configuration errors, which stops polling that order — see [[orders-sync-cod-errors]] and [[orders-sync-cod-eligibility]].

### Couriers that can sync

COD sync works for couriers whose integration can read their cash-on-delivery payouts: [[apps-econt|Econt]], [[apps-dpdbulgaria-speedy|DPD Bulgaria (Speedy)]], [[apps-dpdromania|DPD Romania]], [[apps-pigeonexpress|Pigeon Express]], MPL, [[apps-nextlevel|Next Level]] and [[apps-berry|Berry]], plus the retired Speedy and Rapido apps. Each waybill keeps the courier login it was made with, and the sync uses that login.

## Related

- [[orders-sync-cod]] — hub.
- [[plan-gates]] — concept page on plan-based feature gating; `shipping_payment_sync` is one such gate.
- [[plan]] — the merchant's plan tier governs base quota and pack availability.
- [[orders-sync-cod-log-view]] — the usage banner that renders these figures.
- [[orders-sync-cod-polling-job]] — the run-level capacity pre-check.

## Open questions

None.
