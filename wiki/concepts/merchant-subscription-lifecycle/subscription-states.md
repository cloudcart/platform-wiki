---
type: concept
nav_path: "Concept → Merchant subscription lifecycle → States (Active / Past due / Canceled / Expired)"
aliases: ["Subscription states", "Subscription status enum", "Active / Past due / Canceled / Expired", "Subscription state machine merchant view", "Past due vs Expired"]
tags: [billing, subscription, plan, lifecycle, states, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[merchant-subscription-lifecycle]]. See the hub for the other aspects (renewal-retry, expiration, cancellation, feature packs, payment methods, invoices, support flow).

# Subscription states

## Definition

Every paid recurring item on the merchant's CloudCart account — plan, feature pack, paid app, expert service, paid theme — lives in **one of four states** plus an optional one-time variant for non-recurring purchases. The merchant sees the current state in the **Status** column of [[subscriptions]] (default sort = Active rows first), and the state directly controls what the merchant can DO with the subscription (Cancel button visible only on Active / Past due rows; Renew button visible on Past due / Canceled / Expired rows).

| State | Merchant-visible badge | Meaning | Renew button | Cancel button |
|-------|------------------------|---------|--------------|---------------|
| `Active` | green | Paid and renewing. `next_billing_date > today`, `failed_attempts < 5`. | hidden | visible |
| `Past due` | red | A renewal charge failed. The merchant still has the option to fix it before [[subscription-expiration|expiration]]. `failed_attempts >= 1`. | visible | visible |
| `Canceled` | grey | Merchant clicked Cancel. Auto-renewal is OFF but access continues until `next_billing_date`. | visible (free reactivation if still inside paid period) | hidden |
| `Expired` | red | 1 month past `next_billing_date` (failed renewals) OR 1 day past `next_billing_date` (cancelled). For plan subscriptions, the merchant hits the [[expired-subscription]] takeover on login. | visible | hidden |
| `Once` | grey | One-time purchase (e.g., a one-off Expert Service or theme-setup pack) that never renews. Effectively "Completed". | hidden | hidden |

## Scope

What this page covers:

- The four merchant-visible states + the `Once` variant.
- How the state is set initially and by which daily job each state-change is driven.
- Which buttons / actions are visible per state on [[subscriptions]].

What it does NOT cover:

- The retry schedule that drives the Active → Past due → Past due → ... loop — see [[subscription-renewal-retry]].
- The expiry sweep that drives Past due → Expired and Canceled → Expired — see [[subscription-expiration]].
- The Cancel button's side effects per subscription type — see [[subscription-cancellation]].

## Contrasts

- **Past due vs Expired** — Past due is recoverable (the merchant can click **Renew** OR update [[billing-cards|the saved card]] and wait for the next auto-retry). Expired means the auto-retry loop has ended AND the 1-month grace ran out; for plan subscriptions, the [[expired-subscription]] takeover is active.
- **Canceled vs Expired** — Canceled means the merchant chose to stop auto-renewal but they still have paid time. Expired means access is OVER. A Canceled subscription becomes Expired the day after `next_billing_date` (not after a 1-month grace — see [[subscription-cancellation]]).
- **Active vs Past due** — Active = renewal charges have all succeeded. Past due = the most recent renewal charge failed and `failed_attempts >= 1`. The transition happens automatically inside the daily renewal pipeline (see [[subscription-renewal-retry]]).
- **`Once` vs `Canceled`** — `Once` is a one-time purchase that was never recurring (one-off services / packs). `Canceled` is a previously-recurring subscription whose auto-renewal was turned off. Neither charges further, but the `Once` row never had a `next_billing_date` to begin with.

## Where it applies

The state appears in multiple merchant surfaces:

- **[[subscriptions]]** — Status column with the default sort placing Active rows first; per-row Cancel / Renew buttons are gated on the current state.
- **[[subscriptions-detail]]** — the Details info card shows the Status alongside Type, Period, and `next_billing_date`.
- **[[details-billing]]** — the transaction history records the state at the time of each charge attempt.
- **Site banner** (when a plan-type subscription is Past due) — the platform sets the site to Past due if ANY subscription is Past due (even non-plan), but the [[expired-subscription]] middleware redirect only fires when a **plan-type** subscription itself is Past due / Expired.

### How transitions happen

Every state transition is driven by one of three sources:

1. **The daily `renew:subscriptions` job** (the `subscription_payments` daily job) — drives Active ↔ Past due transitions on every renewal attempt. See [[subscription-renewal-retry]] for the retry schedule.
2. **The daily `expire:subscriptions` job** (the `expire_subscriptions` daily job) — drives Past due → Expired (after 1-month grace) and Canceled → Expired (next day after `next_billing_date`). See [[subscription-expiration]].
3. **The merchant clicking Cancel / Renew** on a [[subscriptions]] row — immediate state transition via the `admin.subscriptions.cancel` / `admin.subscriptions.renew` endpoints.

LTA-contract subscriptions follow a separate flow (the platform code) and free Start Up inactivity expiry uses its own `expire:free-sites` sweep with by-issuer thresholds (see [[expired-subscription]]).

### Free reactivation (`canActivate`)

If the subscription was Canceled but the merchant still has paid time remaining (`next_billing_date > today end-of-day`), clicking **Renew** DOES NOT make a new charge — it just flips the state back to Active for free. This handles "I cancelled by mistake, restore me". Once `next_billing_date` passes, `canActivate` returns false and Renew fires a real charge against [[billing-cards|the saved card on file]]. See [[subscription-cancellation]] for the full restoration playbook.

### Site status mirrors the plan subscription

The store's site status field is updated to match the **plan-type subscription's** status on every state transition. Non-plan subscriptions (apps, packs, services, themes) only update the site status indirectly — specifically, the platform sets the site to Past due if ANY of the merchant's subscriptions are Past due (even if the plan itself is Active). The site-level Past due is what makes the *"You have unpaid subscriptions!"* indicator surface in the admin's profile dropdown even when the plan is fine.

## Related

- [[merchant-subscription-lifecycle]] — hub.
- [[subscription-lifecycle]] — the canonical state machine + full transition table at the developer level.
- [[subscriptions]] — the list where Status is rendered.
- [[subscriptions-detail]] — per-subscription detail with the Status info card.
- [[expired-subscription]] — the admin-blocking takeover that fires when a plan-type subscription becomes Expired.
- [[background-queue-inventory]] — catalogue of the daily jobs (`subscription_payments`, `expire_subscriptions`) that drive state transitions.

## Open Questions

None.
