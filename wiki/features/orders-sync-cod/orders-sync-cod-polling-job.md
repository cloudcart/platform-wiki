---
type: feature
nav_path: "Orders → COD sync → Polling job"
route_name: admin.orders.sync.cod
route_path: /admin/orders/sync/cod
aliases: ["COD sync polling job", "COD sync background job", "COD sync schedule", "COD sync throughput", "COD sync rate limit"]
tags: [orders, cod, sync, background-job, courier-integration]
plan_gates: ["shipping_payment_sync"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---
# COD sync — polling job

> Part of [[orders-sync-cod]]. See the hub for related aspects (log view, eligibility, status flip, errors, quota, manual alternatives).

## Purpose

Describes the **automatic background process** that drives COD sync: how often it runs, how many orders it processes per run, the per-courier throttle, and the site-level pre-checks it does before touching any order. The merchant never starts this — it is fully platform-managed.

## Where to find it

No merchant control surface. The job is queued on the platform's background-job system; the merchant can inspect overall queue status via [[settings-queue-view]] but cannot edit, re-prioritise, or pick orders for a specific COD-sync run.

## What the merchant can do here

- Observe that the job ran by checking new rows on [[orders-sync-cod-log-view]].
- Inspect background-queue health via [[settings-queue-view]].
- Nothing else — the merchant cannot configure the job's schedule or throughput.

## Settings & fields

### Schedule and queue

The COD-sync job is queued on the platform's `system3` background queue and is re-fired automatically by the platform's scheduler — not visible to or controllable by the merchant. Runs are typically several hours apart depending on courier rate limits.

### Throughput cap — 100 orders per job invocation

Each run processes **up to 100 eligible orders**. Larger backlogs (e.g., after a courier outage) take multiple invocations to clear.

### Rapido throttle — 1.1s sleep between API calls

For Rapido specifically (aggressive rate limits), the platform pauses **1.1 seconds** between consecutive COD-payment API calls during the same job run. Other couriers don't have this throttle. With Rapido as the COD-sync provider, effective max throughput is roughly **50–60 orders per run** (vs ~100 for other couriers).

### Job-level pre-checks (before any order is touched)

Each run checks the site first and exits early if any fail:

1. **Site exists and not plan-expired** — if the site's plan has expired, the job exits silently.
2. **Site not in maintenance** — if the site is in maintenance, the job exits.
3. **Platform match** — on multi-platform deployments, a job running on the wrong platform migrates itself to the correct one.
4. **Plan capacity available** — if the COD-sync (`shipping_payment_sync`) capacity is unavailable on the active plan manager, the job stops with an access-denied-by-plan condition. See [[orders-sync-cod-quota]].

So a merchant whose site is suspended / in maintenance / plan-expired won't see any sync events recorded — even if their courier reports the COD as collected.

## Business rules

- **The merchant cannot force a run from this page** — there is no per-order Sync button. The only levers are the global queue trigger or waiting for the schedule; see [[orders-sync-cod-manual]].
- **Backlogs clear over multiple runs** — after a courier outage, the 100-orders cap means a large backlog of newly-eligible orders is processed across several scheduled runs, not all at once.
- **Rapido stores are slower to reconcile** — the 1.1s throttle roughly halves per-run throughput, so a Rapido-heavy backlog takes about twice as long to clear.
- **Plan / site state silently blocks sync** — the job-level pre-checks mean an expired or suspended store gets no sync at all; this is often mistaken for a courier problem.
- Orders that survive the pre-checks are then filtered by the eligibility rules on [[orders-sync-cod-eligibility]] before any courier API call is made.

## Related

- [[orders-sync-cod]] — hub.
- [[settings-queue-view]] — background-queue status surface; the only place the merchant sees the queue.
- [[orders-sync-cod-eligibility]] — per-order filter applied after the site pre-checks pass.
- [[orders-sync-cod-quota]] — the plan capacity that pre-check 4 validates.

## Open questions

- Exact scheduler interval between COD-sync runs is courier-dependent and not surfaced to the merchant. (verify)
