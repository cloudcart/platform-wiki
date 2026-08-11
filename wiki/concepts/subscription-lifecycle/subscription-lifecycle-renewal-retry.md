---
type: concept
nav_path: "Concept → Subscription lifecycle → Renewal retry & pre-billing"
aliases: ["Subscription renewal retry", "Renewal backoff schedule", "Past due retry loop", "Pre-billing notification", "Daily renewal job", "Daily expiry sweep", "Просрочен абонамент опити", "График на повторни опити"]
tags: [subscriptions, billing, lifecycle, renewal, retry, notifications, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[subscription-lifecycle]]. See the hub for the other aspects (states, cancel, renew, cascades, cache-audit).

# Subscription lifecycle — renewal retry & pre-billing

## Definition

When an Active subscription's renewal charge fails on its `next_billing_date`, the platform does NOT immediately give up. It schedules a series of automatic retry attempts on a fixed backoff, then — once the auto-retry budget is spent — it waits roughly a month and finally flips the subscription to Expired on a daily sweep. To give the merchant a chance to keep the cycle from ever entering Past due, the platform also dispatches a **pre-billing notification 7 days before `next_billing_date`** so they can update their saved card on [[billing-cards]] in advance.

| Attempt | Days waited since `last_try_at` |
|---------|---------------------------------|
| Attempt #1 (initial) | no wait — fires the day `next_billing_date <= today` |
| Attempt #2 (after attempt #1 failed) | 2 days |
| Attempt #3 (after attempt #2 failed) | 3 days |
| Attempt #4 (after attempt #3 failed) | 4 days |
| Attempt #5 (after attempt #4 failed) | 5 days |

So a subscription that fails on day 0 retries on day 2 (attempt 2), day 5 (attempt 3), day 9 (attempt 4), and day 14 (attempt 5). After the 5th attempt fails (`failed_attempts = 5`), the daily renewal job no longer picks up the subscription — the auto-retry loop ends. The subscription stays in **Past due** until the next daily expire sweep finds it 1 month past `next_billing_date` and flips it to **Expired**. The merchant can still rescue the subscription during this entire window by clicking **Renew** manually (see [[subscription-lifecycle-renew]]) — that fires an immediate fresh charge regardless of `failed_attempts`.

## Scope

Covered:

- The 5-attempt schedule (1 initial + 4 retries) with 2 / 3 / 4 / 5-day spacing.
- What `failed_attempts` and `last_try_at` track.
- The four daily jobs that drive the lifecycle (renewal, pre-billing notify, expire sweep, free-site notify).
- The 7-day pre-billing email and its gating conditions.
- Where the next attempt date is computed and why retries don't accidentally schedule in the past.

Not covered here:

- The state transitions themselves — see [[subscription-lifecycle-states]].
- The Renew button's manual-charge flow that bypasses the auto-retry budget — see [[subscription-lifecycle-renew]].
- The Cancel-side-effects that suspend the renewal pipeline — see [[subscription-lifecycle-cancel]].

## Contrasts

- **Auto-retry vs. manual Renew** — auto-retry fires up to 5 times on the platform's schedule and stops. Manual Renew fires an immediate fresh charge from the merchant clicking the button; it is not bound by the 5-attempt budget. The merchant can rescue a subscription during the full Past-due window via manual Renew even after the auto-retry loop has stopped.
- **Pre-billing notification vs. renewal-failure email** — the pre-billing notification fires 7 days BEFORE `next_billing_date` only when the subscription is Active, `failed_attempts < 3`, `next_billing_amount > 0`, and `next_billing_date` exists. The renewal-failure email fires AFTER each failed attempt. Past due subscriptions do NOT get the pre-billing notification — they only get per-attempt failure emails.
- **Attempt-count budget vs. expiry window** — the auto-retry budget exhausts at `failed_attempts >= 5` (typically by day 14 after the initial failure). The Expiry flip happens on the daily sweep when the subscription is past 1 month from `next_billing_date`. There is a window of ~16 days where the subscription is no longer being auto-retried but is also not yet Expired.

## Where it applies

### The 7-day pre-billing notification

To give the merchant a window to update [[billing-cards]] before the first renewal attempt fires, the platform sends a pre-billing email **7 days before `next_billing_date`** when ALL of:

- Status is Active.
- `failed_attempts < 3` (so heavily-failing subscriptions don't re-spam the merchant).
- `next_billing_amount > 0` (free / complimentary subscriptions don't notify).
- `next_billing_date` exists (not a one-time / fully cancelled subscription).

A complementary daily job fires the **`subscription.upcoming.payment`** webhook event at the same point and logs a site-event entry so the renewal pre-notification can also be delivered downstream (e.g., to external billing tools listening via [[settings-hooks]]).

### The four daily jobs that drive the lifecycle

All four run **once per day** (interval 86 400 s, single-flighted) on the `cc-system8` queue:

- **`renew:subscriptions`** — picks up subscriptions where `failed_attempts < 5` AND `last_try_at` was at least N days ago per the schedule above (or `last_try_at IS NULL` for the very first attempt) and attempts a charge against the saved card on file.
- **Pre-billing notify** — fires the 7-days-before pre-billing email and the `subscription.upcoming.payment` webhook described above.
- **`expire:subscriptions`** — flips Past due / Canceled subscriptions to Expired when past the threshold (1 month past `next_billing_date` for Past due; the day after for Canceled).
- **Expire-free-sites notify** — notifies free-tier stores before their cleanup.

The renewal pipeline is documented under the queue index — see [[background-queue-inventory]].

### `failed_attempts` and `last_try_at` semantics

Each retry tracks two fields:

- **`failed_attempts`** — increments on every failed charge attempt; resets to 0 on any successful charge (auto or manual Renew). The auto-retry loop stops once this reaches 5.
- **`last_try_at`** — the time of the most recent attempt. The next attempt fires when `now - last_try_at >= the scheduled wait for this attempt count`.

The backoff is per-subscription — different subscriptions on the same merchant's card retry independently.

### Next-billing-date computation on successful renewal

On a successful renewal, `next_billing_date` is computed as `last_next_billing_date + billing_cycle months`. If the last date was already more than a month in the past (e.g., the subscription was Past due for weeks and the merchant just renewed manually), the platform takes `now + billing_cycle` instead — so renewals never accidentally schedule the next charge in the past. See [[subscription-lifecycle-cache-audit]] for the related discount-carry-over rule.

### What stops the retry loop

The retry loop stops on any of:

1. **Successful charge** — `failed_attempts` resets to 0, status → Active, `next_billing_date` advances.
2. **`failed_attempts >= 5`** — auto-retry budget exhausted. Status stays Past due; manual Renew is the only path back to Active until the daily sweep flips to Expired.
3. **Cancel** — see [[subscription-lifecycle-cancel]]. Cancel from Past due puts the subscription into Canceled; the renewal pipeline stops picking it up.

## Related

- [[subscription-lifecycle]] — hub.
- [[subscription-lifecycle-states]] — sibling aspect; the status enum + transition matrix this retry loop drives.
- [[subscription-lifecycle-renew]] — sibling aspect; the manual-charge flow that rescues Past due subscriptions outside the auto-retry budget.
- [[subscription-lifecycle-cancel]] — sibling aspect; the off-ramp that stops the retry loop.
- [[billing-cards]] — saved card used at each renewal attempt; the pre-billing notification is the merchant's signal to update it.
- [[settings-hooks]] — webhook configuration; the `subscription.upcoming.payment` event fires through here.
- [[background-queue-inventory]] — catalogue of background jobs; documents the daily renewal, pre-billing-notify, expire-sweep, and free-site-notify cadence.
- [[notification-delivery]] — pre-billing notification, renewal-failure email, and admin alerts dispatch via this pipeline.

## Open Questions

None.
