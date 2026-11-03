---
type: feature
nav_path: "Details → Billing → Retry schedule"
route_name: billing-list
route_path: /admin/details/billing
aliases: ["Billing retry schedule", "Failed renewal retries", "Retry table", "Past due window", "Failed charge schedule", "График за повторни опити"]
tags: [accountdetails, details, billing, transactions, retry, renewal]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 6
---
# Billing — failed-renewal retry schedule

> Part of [[details-billing]]. See the hub for related aspects (transaction list, statuses, invoice download).

## Purpose

This aspect explains the rows the merchant sees on the *Details → Billing* tab when a renewal **fails**: the auto-retry schedule that generates a new transaction row per attempt, how long the merchant has before the subscription flips to EXPIRED, why pre-flight rejections never produce a row, and the only ways the merchant can force a fresh attempt. This answers *"why do I have several failed charges in a row / how long until my store is locked / how do I retry?"*.

## Where to find it

- **Details (sidebar) → Billing** tab — each retry attempt appears as its own row (a *Failed* status, then eventually a *Success*; see [[details-billing-statuses]]).
- URL pattern: `/admin/details/billing`.

## What the merchant can do here

- **Watch the retry sequence unfold** — every attempt records its own row, so the merchant can see how many tries have happened and when.
- **Force a fresh attempt by replacing the card** — the merchant cannot click "retry" here. The platform auto-retries on its own schedule; to push an immediate fresh attempt the merchant replaces the card on [[billing-cards]] (the next charge attempt uses the new card), or contacts support.

## What the merchant cannot do here

- **Re-attempt a failed charge directly** — there is no retry button on a row.
- **See charges that never hit the gateway** — pre-flight rejections (no card on file, no invoice details) don't generate a transaction row at all; only attempts actually sent to the gateway appear.

## Settings & fields

### Failed-renewal retry schedule

When a renewal charge fails, the underlying subscription's `failed_attempts` counter increments and the next retry is scheduled:

| `failed_attempts` after this attempt | Days waited since `last_try_at` |
|--------------------------------------|----------------------------------|
| 1 (initial attempt failed) | (no wait — the initial attempt fires the day `next_billing_date <= today`) |
| 2 | 2 days after attempt 1 |
| 3 | 3 days after attempt 2 |
| 4 | 4 days after attempt 3 |
| 5 | 5 days after attempt 4 |

Each retry creates a new transaction row on this tab.

## Business rules

### PAST_DUE vs EXPIRED — the ~30-day window

After the 5th attempt fails (`failed_attempts = 5`), the auto-retry loop stops, but the subscription stays **PAST_DUE** — it does NOT immediately flip to EXPIRED. The status only flips to EXPIRED when the daily `expire:subscriptions` sweep finds the subscription with `next_billing_date <= now - 1 month`. So the merchant has roughly **30 days** from the first failed renewal to fix billing before the site-level EXPIRED takeover kicks in. See [[subscriptions]] and [[expired-subscription]].

### Pre-flight rejections don't create a row

Only transactions actually attempted by the gateway show on the Billing tab. If there's no card on file or no invoice details, the charge is rejected before it reaches the gateway and no transaction row is created — which is why a merchant with a missing card may see the subscription failing without a corresponding *Failed* row for every cycle.

### Forcing a fresh attempt

The merchant has two levers: replace the card on [[billing-cards]] (the next scheduled attempt then uses the new card — note this does not bypass the schedule's wait, it just changes which card is charged), or contact CloudCart support. There is no manual "charge now" control on this screen.

## Related

- [[details-billing]] — hub.
- [[details-billing-transaction-list]] — where each retry attempt appears as a row.
- [[details-billing-statuses]] — the *Failed* then *Success* badges a retry sequence produces.
- [[billing-cards]] — replacing the card is the merchant's lever to change which card the next attempt charges.
- [[subscriptions]] — the recurring item whose `failed_attempts` / `next_billing_date` drive the schedule.
- [[expired-subscription]] — the takeover that follows the ~30-day PAST_DUE window.

## Open questions

(All resolved.)
