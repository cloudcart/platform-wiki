---
type: concept
nav_path: "Concept → Subscription lifecycle → States & transitions"
aliases: ["Subscription states", "Subscription status enum", "Subscription state transitions", "Active Past due Canceled Expired", "Once subscription", "Състояния на абонамент"]
tags: [subscriptions, billing, lifecycle, status, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[subscription-lifecycle]]. See the hub for the other aspects (renewal-retry, cancel, renew, cascades, cache-audit).

# Subscription lifecycle — states & transitions

## Definition

Every subscription on the merchant's account carries a `status` value that locks the per-row buttons in [[subscriptions]] and decides whether the platform will attempt another renewal. The enum has **four** recurring states plus one **non-recurring** variant.

| Status | Numeric value | Meaning |
|--------|---------------|---------|
| **Active** | 1 | Successfully charged or within paid period. Default for a newly purchased subscription. |
| **Past due** | 2 | Last renewal charge failed AND `failed_attempts > 0`. Platform retries on a backoff schedule — see [[subscription-lifecycle-renewal-retry]]. |
| **Canceled** | 0 | Merchant clicked Cancel (or platform cancelled on the merchant's behalf). Subscription remains usable until `next_billing_date` if still inside the paid period. |
| **Expired** | 3 | Terminal state after exhausting all retry attempts on a Past due subscription. No more auto-retries; manual Renew only. |

Plus the special **One-time** variant (`billing_period == 'once'`) — no `next_billing_date`, no Cancel / Renew buttons, just a record that the purchase happened. One-time service subscriptions still appear in [[subscriptions]] so the merchant can download invoices, but they are not subject to the recurring lifecycle.

Default list sort on [[subscriptions]] is `status DESC` — Active rows surface first, then Past due, Canceled, Expired in that order.

## Scope

Covered:

- The four recurring states + the one-time variant.
- All UI-driven transitions (Cancel, Renew).
- All backend-driven transitions (successful renewal, failed renewal, daily expire sweep, plan-deprecation force).
- The `failed_attempts >= 5` boundary and why it does NOT immediately move the subscription to Expired.
- The Past-due-vs-Expired distinction.

Not covered here:

- The retry-attempt schedule and the daily renewal job — see [[subscription-lifecycle-renewal-retry]].
- The Cancel button's full UX, LTA / turnover blocks, and the canActivate free-reactivation rule — see [[subscription-lifecycle-cancel]].
- The Renew button's immediate-charge flow and the plan-deprecation redirect — see [[subscription-lifecycle-renew]].

## Contrasts

- **Past due vs. Expired** — Past due means "renewal failed, the auto-retry loop is still in scope" — the merchant can rescue by updating the card and waiting for the next auto-attempt OR by clicking Renew for an immediate fresh charge. Expired is the terminal state after the daily `expire:subscriptions` sweep finds the subscription past the 1-month threshold (or the day after for Canceled subscriptions). Both look red in the UI; the distinguishing factor is the `status` value (2 = Past due, 3 = Expired). The platform stops auto-retrying once `failed_attempts >= 5`, but the subscription does NOT immediately flip to Expired at that moment — it stays Past due until the next daily expiry sweep.
- **Cancel vs. Expire** — Cancel is a deliberate merchant action that stops auto-renewal but keeps the subscription usable through the paid cycle. Expire is the platform's terminal state after 5 failed renewal attempts on a Past due subscription — the merchant didn't act and the platform gave up. Both end at "no longer billed", but the merchant arrived differently. From the merchant UI: Cancel is intentional; Expire is "I forgot to update my card".
- **Active vs. Once** — Active is a recurring-billing state with a `next_billing_date`. Once is a non-recurring purchase record with no `next_billing_date` and no auto-renewal — it never transitions to Past due or Expired.

## Where it applies

### State transitions surfaced via UI buttons

- **Cancel** (Active or Past due → Canceled) — soft cancellation; access continues until `next_billing_date`. See [[subscription-lifecycle-cancel]] for the LTA / turnover blocks and the canActivate rule.
- **Renew** (Past due, Canceled, or Expired → Active) — immediate charge attempt; on success → Active with a new `next_billing_date`; on failure → Past due. See [[subscription-lifecycle-renew]] for the plan-deprecation redirect and app re-install side-effect.

### Backend-driven transitions

- **Successful renewal** (Active → Active, with `next_billing_date` advanced and `failed_attempts` reset to 0).
- **Failed renewal** (Active → Past due, or Past due → Past due with `failed_attempts` incremented; `last_try_at` set to now).
- **Auto-retry loop ends at `failed_attempts >= 5`** — the daily renewal job stops scheduling further attempts. The subscription stays Past due, NOT Expired, until the daily sweep.
- **Daily `expire:subscriptions` sweep flips to Expired** when `status != EXPIRED` AND `next_billing_date <= now - 1 month`, OR `status == CANCELED` AND `next_billing_date <= today`. This is what actually moves the subscription into the terminal Expired state.
- **Plan deprecation on Renew** — when the merchant clicks Renew on a Plan subscription whose underlying plan is no longer in the catalog, the platform forces Past due and redirects to [[plans]] with the message *"This plan is not active. You can buy a new plan to renew the subscription."*

### Where the status is read

The per-row Action column in [[subscriptions]] keys off the status: Active shows **Cancel**; Past due shows **Renew + Cancel**; Canceled shows **Renew** (free if canActivate, paid otherwise); Expired shows **Renew** (always paid); Once shows no action. LTA-contract subscriptions show no Action regardless of status — see [[subscription-lifecycle-cancel]].

## Related

- [[subscription-lifecycle]] — hub.
- [[subscription-lifecycle-renewal-retry]] — sibling aspect; what fills the time between Active and Expired.
- [[subscription-lifecycle-cancel]] — sibling aspect; how Active / Past due become Canceled.
- [[subscription-lifecycle-renew]] — sibling aspect; how Past due / Canceled / Expired return to Active.
- [[subscriptions]] — the My subscriptions list where the status drives the per-row buttons.
- [[subscriptions-detail]] / [[subscription-details]] — per-subscription detail screen with the status badge.
- [[plans]] — where a deactivated plan subscription redirects on Renew.
- [[expired-subscription]] — the takeover screen the merchant sees when their plan subscription has fully expired.

## Open Questions

None.
