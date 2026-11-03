---
type: feature
nav_path: "Expired Subscription → Paid-plan timing"
route_name: expired-subscription
route_path: /admin/expired-subscription
aliases: ["Expired subscription paid timing", "Plan dunning window", "1 month grace period", "Renewal retry schedule", "Reactivation after renew", "Грейс период платен план", "Дунинг при неуспешно плащане"]
tags: [base, core, expired-subscription, subscriptions, billing, blocking-screen]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

# Expired Subscription — paid-plan timing & recovery

> Part of [[expired-subscription]]. See the hub for related aspects (redirect & allowlist, free Start Up plan, data lifecycle).

## Purpose

This aspect explains, for **paid-plan merchants**, exactly WHEN the takeover starts, how long the merchant has to recover before the site-level Expired flip, what the auto-retry schedule looks like, and what happens the moment a renewal succeeds. The short version: the merchant is gated as soon as the first renewal fails, but has roughly **30 days from `next_billing_date`** before the site is swept to fully Expired, and re-activation after a successful Renew is **immediate**.

## Where to find it

This is reached via the standard redirect — see [[expired-subscription-redirect]]. A paid merchant first hits the takeover as soon as their plan subscription drops to Past due (after the first failed renewal). The merchant's path forward is always the [[subscriptions]] list via the modal's *Subscriptions* button.

## What the merchant can do here

A paid merchant in the takeover can recover three ways, all from the allowlisted billing screens:

- **Click Renew on the failing plan row** in [[subscriptions]] — fires an immediate fresh charge against the saved card.
- **Update the saved card** in [[billing-cards]] and let the next daily auto-retry succeed.
- **Buy a new plan** from [[plans]] when the old plan is no longer in the catalogue.

The page does NOT auto-renew — no background activity on the takeover screen fires a charge. The merchant must click Renew or wait for the next daily auto-retry.

## Settings & fields

No merchant-editable settings on this aspect. The timing values below are platform constants, not store settings:

| Value | What it controls |
|-------|------------------|
| Retry backoff (2 / 3 / 4 / 5 days) | Spacing between the 5 in-window auto-retry attempts after the first failed renewal. |
| ~14 days | Approximate span across which the 5 in-window retries occur after `next_billing_date`. |
| 1 month past `next_billing_date` | When the daily site-expiry sweep flips the site to EXPIRED. |
| ~30 days from `next_billing_date` | Effective recovery window before the site-level EXPIRED takeover. |

## Business rules

### Paid-plan timing — 1 month past `next_billing_date`

After the first failed renewal attempt, the platform retries on the standard backoff (2 / 3 / 4 / 5 days between attempts — see [[subscription-lifecycle]]). The 5 in-window retries happen across roughly the first **~14 days** after `next_billing_date`. The site itself is NOT auto-flipped to EXPIRED until the daily site-expiry sweep finds the site with `next_billing_date <= now − 1 month` AND `status IN (Active, Past due)`. So merchants have approximately **30 days from `next_billing_date`** to recover before the site-level EXPIRED takeover fires.

Two important nuances:

- The merchant is **redirected to the takeover earlier** — as soon as the plan subscription drops to Past due (after the first failed renewal). This is the dunning takeover, which begins well before the site-level Expired flip. See [[expired-subscription-redirect]] for the two trigger conditions.
- A **CANCELED** plan subscription is expired at the site level on the very next day after `next_billing_date` passes (no 1-month grace for cancellations) — the merchant explicitly chose to stop, so the platform doesn't extend.

### Re-activation is immediate

When the merchant successfully renews on [[subscriptions]] (clicks Renew + the charge succeeds), the site's `status` flips back to `Active`, the `next_billing_date` advances by `billing_cycle` months, `failed_attempts` zeroes, and the `plan_expired` flag clears. The merchant's next admin request no longer hits the takeover redirect — they go back to the dashboard normally. There is NO cache window the merchant has to wait through.

For an EXPIRED plan whose underlying plan record is no longer active (deprecated by CloudCart), Renew on [[subscriptions]] redirects to [[plans]] with the message *"This plan is not active. You can buy a new plan to renew the subscription."* — the merchant must buy a new plan to unblock.

### Unpaid bank-transfer invoices — separate grace window

For merchants paying by bank transfer (not card), an unpaid bank-transfer invoice has its own grace period before the platform treats it as a problem:

- **Standard merchants** — 30 days of unpaid bank-transfer invoices before the platform considers them a problem.
- **Reseller-onboarded merchants** (with `reseller_id` set) — 90 days of grace.

This check can surface as a warning banner or as access restriction depending on how long the bank invoice has been unpaid. It is independent of the card-renewal retry flow described above.

## Related

- [[expired-subscription]] — hub.
- [[subscriptions]] — where the merchant clicks Renew on the failing plan row to recover immediately.
- [[subscription-lifecycle]] — the state machine + the 2 / 3 / 4 / 5-day retry schedule that this timing depends on.
- [[billing-cards]] — saved card used for auto-retries; typically updated before clicking Renew.
- [[billing-invoicing]] — invoice details required for any plan purchase.
- [[plans]] — destination when the expired plan is no longer in the catalogue.
- [[plans-purchase]] — the per-plan purchase flow.
- [[details-billing]] — transaction history showing the failed renewal attempts.
- [[background-queue-inventory]] — the daily renewal-retry and site-expiry jobs that drive this timing.

## Open questions

(All resolved.)
