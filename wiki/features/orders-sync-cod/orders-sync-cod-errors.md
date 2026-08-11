---
type: feature
nav_path: "Orders → COD sync → Errors"
route_name: admin.orders.sync.cod
route_path: /admin/orders/sync/cod
aliases: ["COD sync errors", "COD sync error categorisation", "COD sync error buckets", "COD sync error messages", "COD sync quota-burn protection"]
tags: [orders, cod, sync, errors, courier-integration]
plan_gates: ["shipping_payment_sync"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---
# COD sync — errors

> Part of [[orders-sync-cod]]. See the hub for related aspects (log view, eligibility, polling job, status flip, quota, manual alternatives).

## Purpose

Describes how the COD-sync job **categorises courier errors** and what each category does to the order. Most of this is invisible to the merchant — they only see the final error string in the Action column of [[orders-sync-cod-log-view]] — but understanding the buckets explains why some failing orders keep retrying and others get silently dropped.

## Where to find it

No control surface. The merchant sees only the final error string on [[orders-sync-cod-log-view]]; the categorisation happens inside the background job.

## What the merchant can do here

- Read the verbatim error string in the Action column on [[orders-sync-cod-log-view]].
- Use the string to diagnose a misconfiguration (e.g., wrong credentials, missing waybill).
- The merchant cannot change how errors are bucketed.

## Settings & fields

### Error categorisation — four buckets

The job sorts each courier error message fragment into one of four buckets:

**Ignore list** (warning logged, no `sync_payment_error` saved — silent skip):
- `Не е намерена пратка` (Bulgarian: "Shipment not found")
- `is not authorized to access BOL`

**Continue list** (the order's response is set to `-1` and retried next cycle):
- `looks like we got no XML document`

**Search list** (logged to the system error store for diagnosis but otherwise treated as a warning):
- `is not authorized to access BOL`
- `Invalid billOfLading`
- `Клиент със споразумение за` (Bulgarian: "Client with agreement for")
- the platform code
- the platform code

**Restart list** (the whole job aborts gracefully; the queue worker picks it up again on the next scheduled run):
- `temporarily unavailable`
- `failed to load external entity`

### Quota-burn protection — counter jumped to 15

When an exception's message contains `is not authorized to access`, `There is not enough quantity for`, or `Няма достатъчно количество за`, the order's `sync_payment` counter is jumped straight to **15** — effectively banning the order from future sync attempts. This protects the merchant's quota from being burned on permanent configuration problems. See [[orders-sync-cod-eligibility]] for the 15-attempt cap mechanics and [[orders-sync-cod-quota]] for why quota matters.

## Business rules

- **The merchant sees only the final error string** — the bucket logic (ignore / continue / search / restart) is internal. A row in the log with an error string means the latest sync attempt failed with that message.
- **"Restart" errors are courier-wide, not order-specific** — `temporarily unavailable` / `failed to load external entity` abort the entire run, so a courier outage stalls all that courier's pending orders until the next scheduled run.
- **Auth / credential errors are usually permanent** — the platform code and the "not authorized" messages indicate the courier integration credentials are wrong; the order will stop retrying once the counter hits 15. Fix the credentials in [[apps]] / [[shipping]] and re-fulfil if needed.
- **"There is not enough quantity" jumping to 15 is intentional** — an inventory error on the courier side is treated as permanent for that order so it doesn't waste 14 more polls.

## Related

- [[orders-sync-cod]] — hub.
- [[orders-sync-cod-log-view]] — where the verbatim error string is shown.
- [[orders-sync-cod-eligibility]] — the 15-attempt cap that error categorisation feeds.
- [[orders-sync-cod-quota]] — why protecting the attempt counter protects quota.
- [[apps]] / [[shipping]] — where courier credentials are fixed when auth errors appear.

## Open questions

None.
