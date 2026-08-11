---
type: concept
nav_path: "Concept → Background processes → Recurring platform processes"
aliases: ["Recurring scheduled processes", "Scheduled jobs", "Platform schedule", "Daily jobs", "Hourly jobs", "Cron-driven background work"]
tags: [background, async, scheduled, cron, support, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[background-queue-inventory]]. See the hub for related aspects (imports/exports, the search index sync, order side-effects, Queue View, process catalogue).

# Background processes — recurring platform schedule

## Definition

**Recurring scheduled processes** are the background jobs the platform fires on a fixed cadence regardless of whether the merchant did anything. They run every few minutes, every hour, every few hours, or once a day — driven by the platform's own scheduler. The merchant cannot start, stop, or reschedule them. Some are visible on [[settings-queue-view]]; most run silently because they are platform-internal housekeeping.

These are the jobs that keep the site working day-to-day: abandoned-cart emails get sent, subscription renewals get attempted, SSL certificates get renewed, statistics dashboards stay fresh, expired discounts stop applying, badges (`New`, `Featured`) age out, and the platform garbage-collects its own stale data.

## Scope

Covered:

- The full recurrence inventory grouped by domain (cart / order recovery, subscriptions and billing, SSL renewal, statistics and analytics, catalogue maintenance, platform housekeeping).
- Per-process cadence (3 min, every hour, every 4 hours, every 6 hours, every 12 hours, daily, twice daily).
- Per-process Queue View visibility — whether the merchant sees it.

Not covered:

- On-demand processes triggered by merchant or customer actions — see [[background-queue-imports-exports]] + [[background-queue-order-side-effects]].
- the search index sync chain — see [[background-queue-search-sync]].
- Stuck-process diagnosis — see [[background-queue-view-and-stuck]].
- Internal-identifier reference — see [[background-queue-process-catalogue]].

## Contrasts

- **Recurring vs on-demand.** Recurring fires by the clock; on-demand fires by trigger. A subscription renewal runs nightly even if no merchant logged in. A CSV import runs only after upload — see [[background-queue-imports-exports]].
- **Visible vs hidden recurring.** Subscription renewals, settlement batches, currency sync are visible on [[settings-queue-view]] because the merchant has an actionable interest in them. SSL renewal, statistics rollup, badge maintenance run silently because they are platform internals.
- **Process schedule vs job lifecycle.** This aspect lists the schedule (when the platform decides to start the process). The individual lifecycle of a single execution (started / running / finished / failed) is [[queue-job]].

## Where it applies

### Cart and order recovery

| What happens | How often | Visible on Queue View |
|---|---|---|
| Looks for abandoned carts past the recovery threshold and sends the customer the recovery email (when [[abandoned-cart-recovery]] is enabled on the merchant's plan + active on the customer's cart) | Every 3 minutes | No |
| Inactive carts older than the merchant's age-out threshold are removed from the active list (the customer can start a fresh cart at any time) | Every hour | No |
| Stale "safe-delete" carts (checkout started but never finalised) are cleaned up | Every hour | No |
| Active expired discounts are de-activated so the storefront stops applying them | Every hour | No |

### Subscriptions, billing, and account state

| What happens | How often | Visible on Queue View |
|---|---|---|
| Subscription renewal charges (plan renewals, feature-pack renewals, app subscriptions) are attempted | Daily | Yes |
| Renewal failures trigger the merchant notification | Daily | Yes |
| Expired subscriptions are marked expired (the merchant loses access to the paid feature) | Daily | Yes |
| Free-trial sites approaching expiry notify the merchant | Daily | No |
| Site status (active / suspended / disabled) and database state are reconciled | Daily | No |
| Reseller payouts are calculated and queued for transfer | Daily | Yes |
| Settlement batches (for [[payment-providers-cloudcart-pay]] merchants) are generated | Daily | Yes |
| Active offer-based discounts that have reached their end-date are expired | Daily | No |
| Apps the merchant has not paid for are uninstalled | Twice daily | No |
| Functionality on plans the merchant has downgraded out of is disabled | Twice daily | No |

### SSL certificate renewal

| What happens | How often | Visible on Queue View |
|---|---|---|
| Approaching-expiry SSL certs for the merchant's custom domain are renewed (Let's Encrypt) | Daily | No |
| SSL for the platform's own `cloudcart.com` and CC link domains is renewed | Daily | No |

### Statistics and analytics aggregations

| What happens | How often | Visible on Queue View |
|---|---|---|
| Order-fulfillment statistics (fulfilled vs unfulfilled per day) are rolled up | Daily | No |
| Order-payment statistics (paid vs unpaid per day) are rolled up | Daily | No |
| Cross-platform industry statistics are recomputed | Daily | No |
| Marketing dashboard statistics (campaign opens, clicks, conversions) are refreshed | Every 6 hours | No |
| Currency-exchange rates are synced from the upstream provider | Every 12 hours | Yes |

### Catalogue maintenance

| What happens | How often | Visible on Queue View |
|---|---|---|
| Product "New" badge is removed once the new-arrival window has elapsed | Every 4 hours | No |
| Product "Featured" badge is removed when the featured period ends | Every 4 hours | No |
| Product primary-image flag is reconciled (so each product has exactly one primary image) | Every hour | No |
| Permanently-deleted products and their derived data (image files, search index, cached pages) are fully removed | Every 12 hours | No |

A nightly search-index price re-sync also runs every 24 h to catch drift between the primary database and the search index, alongside a nightly orphan cleanup that removes search-index docs whose primary-database row was deleted — both detailed in [[background-queue-search-sync]].

### Platform housekeeping

| What happens | How often | Visible on Queue View |
|---|---|---|
| Long-running internal processes that have hung past their budget are killed | Every 2 minutes | No |
| Daily CSV-import staging tables are cleaned up | Daily | No |
| Modoboa mailbox accounts are reconciled with the [[settings-emails]] subscription state | Daily | No |
| Worker daemons report their health (visible to CloudCart on-call) | Every 2 minutes | No |
| Records from failed global imports that have aged out are removed | Daily | No |

The 2-minute hung-process watchdog is the safety net for stuck visible processes — see [[background-queue-view-and-stuck]].

**What this means for support tickets.** When a merchant asks *"why did the New / Featured badge disappear from my product?"* or *"why did my discount stop applying overnight?"* — the answer is one of these recurring jobs hit its trigger condition (the badge window ended, the discount end-date passed). The merchant edits the underlying data (window length, end-date) to change the outcome; the schedule itself is not configurable. When a renewal-related ticket arrives, confirm the daily run completed on Queue View first.

## Related

- [[background-queue-inventory]] — hub.
- [[settings-queue-view]] — visible-process diagnostics surface.
- [[abandoned-cart-recovery]] — the 3-min cart-recovery cadence.
- [[payment-providers-cloudcart-pay]] — daily settlement batch.
- [[settings-emails]] — Modoboa mailbox reconciliation source.
- [[background-queue-process-catalogue]] — internal-identifier mapping for each row above.

## Open Questions

None.
