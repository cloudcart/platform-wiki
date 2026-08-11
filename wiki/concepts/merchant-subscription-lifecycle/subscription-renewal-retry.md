---
type: concept
nav_path: "Concept → Merchant subscription lifecycle → Renewal + retry schedule"
aliases: ["Subscription renewal", "Renewal retry schedule", "5-attempt retry", "Past due retry loop", "Subscription dunning", "Pre-billing notification", "Renew button", "Free reactivation", "canActivate"]
tags: [billing, subscription, plan, renewal, retry, lifecycle, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[merchant-subscription-lifecycle]]. See the hub for the other aspects (states, expiration, cancellation, feature packs, payment methods, invoices, support flow).

# Subscription renewal + retry schedule

## Definition

Every active subscription with `next_billing_amount > 0` is charged automatically on or after `next_billing_date` via a daily background job (`subscription_payments` → artisan `renew:subscriptions`). If the first charge fails, the platform retries on a **fixed 5-attempt schedule with widening gaps of 2 / 3 / 4 / 5 days between attempts**. After 5 failed attempts the auto-retry loop stops; the subscription stays Past due waiting for either a manual **Renew** click, an updated card, or the [[subscription-expiration|1-month expiry sweep]].

A parallel daily job (`subscription_payments_notify`) fires the `subscription.upcoming.payment` webhook **7 days before `next_billing_date`** so integrations and the merchant's notification stack can warn the merchant to update [[billing-cards|the card on file]] before the first auto-charge.

## Scope

What this page covers:

- The daily auto-renewal pipeline + the filters that decide which subscriptions are picked up each day.
- The 5-attempt retry schedule with 2 / 3 / 4 / 5 day gaps.
- The 7-day pre-billing `subscription.upcoming.payment` webhook.
- The manual **Renew** button on [[subscriptions]] (immediate charge or free reactivation).
- Discount carry-over + promo first-cycle pricing at renewal.

What it does NOT cover:

- What happens after attempt #5 (the Past due → Expired transition) — see [[subscription-expiration]].
- The Cancel button + the 4 states the subscription can be in — see [[subscription-states]] + [[subscription-cancellation]].
- How the saved card on file is updated mid-cycle — see [[subscription-payment-methods]].

## Contrasts

- **Auto-renewal vs manual Renew** — the daily job charges automatically when due. The manual **Renew** button on [[subscriptions]] fires an IMMEDIATE charge regardless of `next_billing_date` (useful for "fix Past due NOW" recovery, or to switch a Canceled subscription back to Active).
- **Pre-billing notify vs failure email** — `subscription.upcoming.payment` fires 7 days BEFORE the charge as a heads-up. There is no built-in CloudCart per-attempt failure email after a charge fails — the failure surfaces via the `subscription.renew` webhook with `failed_attempts > 0` and through the merchant's own notification configuration. See [[notification-delivery]].
- **Renew with charge vs free reactivation (`canActivate`)** — if the merchant has paid time remaining on a Canceled subscription (`next_billing_date > today end-of-day`), Renew flips the state to Active for FREE with no new charge. Outside that window, Renew always charges [[billing-cards|the saved card]].

## Where it applies

### The daily auto-renewal pipeline

The `subscription_payments` daily job (runs once per 24h on the `cc-system8` queue) sweeps every subscription matching ALL of these filters:

- `next_billing_amount > 0`
- `lta_contract_id IS NULL` (LTA contracts run a separate flow — see [[expired-subscription]])
- `reseller_id IS NULL` (reseller payouts run a separate, largely-deactivated flow)
- `status` is Active or Past due
- `failed_attempts < 5`
- `next_billing_date <= today`
- `last_try_at` is NULL or beyond the per-attempt cooldown

For each matching subscription the job charges the saved card via the merchant's billing-side gateway ([[subscription-payment-methods|Stripe or Braintree]]).

**On success**:

- The renewal cycle resets — new invoice issued, `next_billing_date` advanced by `billing_cycle` months, `failed_attempts` zeroed.
- Invoice PDF auto-emailed to the recipient on file (see [[subscription-invoices]]).
- App re-installed (for app subscriptions that had been uninstalled).
- Feature-pack quota re-applied; the plan-feature cache is flushed.
- The `SubscriptionRenew` + `InvoiceCreate` events fire (downstream webhooks: `subscription.renew`, `invoice.create`).

**On failure**:

- `failed_attempts` increments.
- `last_try_at` set to now (used as the per-attempt cooldown anchor).
- The status flips to Past due (if not already Past due / Expired).

### The 5-attempt retry schedule

Once a subscription is Past due, the daily job retries on a fixed schedule with widening gaps between attempts:

| Attempt # | When it runs (relative to previous attempt) | On failure | On success |
|-----------|---------------------------------------------|------------|------------|
| 1 (the original `next_billing_date` charge) | scheduled — daily job picks it up on day 0 | `failed_attempts = 1`, status → Past due | Active, cycle reset |
| 2 | **2 days** after attempt #1 | `failed_attempts = 2` | Active, cycle reset, `failed_attempts → 0` |
| 3 | **3 days** after attempt #2 | `failed_attempts = 3` | Active, cycle reset, `failed_attempts → 0` |
| 4 | **4 days** after attempt #3 | `failed_attempts = 4` | Active, cycle reset, `failed_attempts → 0` |
| 5 (last auto-attempt) | **5 days** after attempt #4 | `failed_attempts = 5` — auto-loop STOPS | Active, cycle reset, `failed_attempts → 0` |
| (no further auto-attempts) | — | Subscription stays Past due indefinitely, waiting for [[subscription-expiration|the 1-month expiry sweep]] OR a manual Renew | — |

**Total auto-retry window**: ~14 days from the original `next_billing_date` to attempt #5. After that the subscription waits in Past due until the 1-month grace from `next_billing_date` runs out.

### 7-day pre-billing notification

A parallel daily job (`subscription_payments_notify`) fires the `subscription.upcoming.payment` webhook event **7 days before `next_billing_date`** for subscriptions where ALL of:

- `failed_attempts < 3`
- `next_billing_amount > 0`
- A `next_billing_date` exists
- Status = Active (Past-due and free / complimentary subscriptions do NOT get the pre-notify)

The merchant uses this 7-day window to update [[subscription-payment-methods|the card on file]] before the first auto-charge fires. The actual email / SMS / push the merchant sees is delivered by their own notification configuration consuming this webhook — see [[notification-delivery]].

### Manual Renew button

The merchant can click **Renew** in the Actions column of any Past due / Canceled / Expired row on [[subscriptions]] to fire an IMMEDIATE charge.

- **Charge succeeds** → cycle resets to Active, `failed_attempts → 0`, new invoice issued.
- **Charge fails** → `failed_attempts++`, status → Past due.
- **Free reactivation** (Canceled row, `next_billing_date > today end-of-day`) → state flips to Active without a charge.

**Plan-subscription Renew extras**:

- If the underlying plan record is no longer active (CloudCart retired it), Renew forces Past due + redirects to [[plans]] with *"This plan is not active. You can buy a new plan to renew the subscription."*.
- If the merchant has unpaid plan turnover (overage on metered usage), Renew first pays the turnover invoice; only then does the regular renewal proceed.

### Discount carry-over + promo first-cycle pricing

Subscriptions with a `discount_id` on them automatically apply the same discount at each renewal — the merchant doesn't reapply codes per cycle.

When the merchant buys with a discounted first cycle (e.g., via a promo landing URL), the FIRST charge is the promo price but the platform stores the regular price in `next_billing_amount`. At renewal time, the regular price (the higher of `price` and `next_billing_amount`) takes over. The merchant sees the regular price in the **Next billing amount** column from day one — it's NOT a surprise at renewal.

## Related

- [[merchant-subscription-lifecycle]] — hub.
- [[subscription-states]] — what the badge says during each retry stage.
- [[subscription-expiration]] — what happens after attempt #5 + the 1-month grace.
- [[subscription-payment-methods]] — updating the card mid-retry to let the next auto-attempt rescue the subscription.
- [[subscriptions]] — the list with the manual Renew button.
- [[notification-delivery]] — the pipeline that turns the `subscription.upcoming.payment` / `subscription.renew` webhooks into merchant-facing notifications.
- [[background-queue-inventory]] — the `subscription_payments` + `subscription_payments_notify` daily jobs.
- [[expired-subscription]] — destination when the 5-attempt loop and 1-month grace both run out for a plan subscription.

## Open Questions

None.
