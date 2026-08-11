---
type: feature
nav_path: "Profile → My subscriptions → Renewal retry"
route_name: subscriptions-list
route_path: /admin/details/subscriptions
aliases: ["Subscription renewal retry", "Renewal retry schedule", "Failed renewal attempts", "Subscription backoff", "Expire subscriptions sweep", "Подновяване на абонамент опити"]
tags: [subscriptions, renewal, retry, backoff, billing]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[subscriptions]]. See the hub for the other aspects (list columns, actions, status state machine, types, notifications & pricing).

# Subscriptions — renewal retry schedule

## Purpose

This aspect documents the **automatic retry pipeline** that fires when a recurring renewal charge fails: the 5-attempt backoff schedule (2 / 3 / 4 / 5 days), the daily renewal-pipeline gating conditions, the daily `expire:subscriptions` sweep that finally flips Past-due rows to Expired, and the important distinction between "auto-retry stopped" and "subscription expired" — they are NOT the same event.

## Where to find it

There is no UI surface for "edit the retry schedule" — the pipeline is fully managed by the platform. The merchant sees its effects in two columns on [[subscriptions]]:

- **Failed attempts** column — counts consecutive failed renewal charges (0 when healthy).
- **Status** column — flips to Past due after the first failed charge, eventually to Expired after the sweep.

See [[subscriptions-feature-list-columns]] for the column context.

## What the merchant can do here

- Read **Failed attempts** on any row to see how many retries have already fired.
- Click **Renew** manually at any point — this fires an immediate fresh charge regardless of the backoff schedule. See [[subscriptions-feature-actions]] for the manual Renew flow.
- Update the saved card at [[billing-cards]] **before** the next attempt to give the next retry a working card.
- (Cannot) change the schedule, skip attempts, or extend the retry window. The pipeline is read-only from the merchant's side.

## Settings & fields

There are no editable fields for retry behaviour. The visible indicator is the **Failed attempts** column on [[subscriptions]] — see [[subscriptions-feature-list-columns]] for its placement.

## Business rules

### Renewal retry schedule (up to 5 attempts, backoff)

When a renewal charge fails, the platform increments `failed_attempts` and schedules the next attempt on a fixed backoff. The daily renewal pipeline picks up subscriptions with `failed_attempts < 5`:

| `failed_attempts` value after this attempt | Days waited since `last_try_at` |
|---------------------------------------------|----------------------------------|
| 1 (initial attempt failed) | (no wait — initial attempt fires the day `next_billing_date <= today`) |
| 2 | 2 days after attempt 1 |
| 3 | 3 days after attempt 2 |
| 4 | 4 days after attempt 3 |
| 5 | 5 days after attempt 4 |

So a subscription that fails on day 0 retries on day 2 (attempt 2), day 5 (attempt 3), day 9 (attempt 4), and day 14 (attempt 5). After the 5th attempt fails (`failed_attempts = 5`), the auto-retry loop **stops** — the subscription stays Past due, NOT Expired.

### Renewal pipeline gating

The background renewal pipeline picks up subscriptions where:

- `next_billing_amount > 0`
- `lta_contract_id IS NULL` (reseller-flagged / LTA-contract subscriptions go through a separate pipeline — see [[subscriptions-feature-types]])
- Status is Active or Past due
- `failed_attempts < 5`
- `DATE(next_billing_date) <= today`
- `last_try_at` is null OR last try was at least N days ago (per the retry schedule above).

These constraints mean a subscription that's overdue by exactly 1 day will retry today; one that already retried today will wait per the backoff.

### Auto-retry stopping is NOT the same event as Expired

This is the most common merchant confusion. After `failed_attempts = 5`:

1. The auto-retry loop **stops** — the platform will not attempt any more charges automatically.
2. The status stays **Past due** — NOT yet Expired.
3. The merchant can still manually click **Renew** (see [[subscriptions-feature-actions]]) to fire a fresh charge — manual Renew bypasses the `failed_attempts < 5` gate.
4. The status only flips to **Expired** when the daily `expire:subscriptions` sweep finds the subscription with `next_billing_date <= now - 1 month` (typically ~30 days after the first failed renewal).

Until the sweep runs, the merchant has a window to update [[billing-cards]] and click manual Renew. After the sweep flips Expired, the manual Renew still works (it tries a fresh charge from scratch) — see [[subscriptions-feature-status-state-machine]] for the Expired-to-Active transition.

### Daily `expire:subscriptions` sweep

A daily background sweep checks every subscription and flips terminal-state subscriptions to Expired:

- **For non-Canceled subscriptions** (Past due, Active-but-overdue): Expired when `next_billing_date <= now - 1 month`. The full month grace window gives the merchant time to react after the per-attempt failure emails.
- **For Canceled subscriptions**: Expired when `next_billing_date <= yesterday`. Cancelled subscriptions don't need a grace window — they expire the day after their paid period ends.

The sweep is daily — there is no merchant-visible "this will expire tonight" warning beyond the per-attempt failure emails and the [[expired-subscription]] takeover screen that appears when the Plan subscription expires.

### Per-attempt failure emails — one per retry

Each retry attempt that fails fires a notification email (one per attempt, on the 2 / 3 / 4 / 5 / 5-day backoff schedule). There is NO separate "you entered Past Due" status-change notification — the merchant only learns about Past due via the per-attempt failure emails. See [[subscriptions-feature-notifications-pricing]] for the full notification surface.

### Manual Renew bypasses the schedule

The retry schedule applies to **automatic** renewals only. The merchant can click **Renew** at any point — this fires an immediate fresh charge regardless of `failed_attempts` or `last_try_at`. The schedule is a back-off for the platform's auto-pipeline; the merchant's manual action is always honoured. See [[subscriptions-feature-actions]].

### Promo-priced first cycle doesn't affect retry behaviour

When a subscription was bought with promo / first-cycle pricing, the **second** charge uses the regular price stored in `next_billing_amount`. If that second charge fails (e.g., the merchant's card hits a limit on the higher amount), the retry schedule above kicks in on the regular price. See [[subscriptions-feature-notifications-pricing]] for promo first-cycle semantics.

## Related

- [[subscriptions]] — hub.
- [[subscriptions-feature-status-state-machine]] — what Past due and Expired mean.
- [[subscriptions-feature-actions]] — manual Renew that bypasses the schedule.
- [[subscriptions-feature-notifications-pricing]] — per-attempt failure emails.
- [[billing-cards]] — saved card used for the retry charge.
- [[expired-subscription]] — takeover screen after the sweep flips Plan subscriptions to Expired.

## Open questions

(None.)
