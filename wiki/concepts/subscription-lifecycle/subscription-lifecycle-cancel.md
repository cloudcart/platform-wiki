---
type: concept
nav_path: "Concept → Subscription lifecycle → Cancel & blockers"
aliases: ["Subscription cancel", "Soft cancel", "Cancel doesn't terminate immediately", "LTA contract block", "Unpaid turnover block", "canActivate free reactivation", "Меко отменяне", "Отказ от абонамент"]
tags: [subscriptions, billing, lifecycle, cancel, lta, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[subscription-lifecycle]]. See the hub for the other aspects (states, renewal-retry, renew, cascades, cache-audit).

# Subscription lifecycle — cancel & blockers

## Definition

The **Cancel** action moves a subscription from Active or Past due into the Canceled state. The single most-misunderstood rule on the entire subscription model is that **Cancel is soft** — it does NOT immediately terminate the merchant's access to the service. The platform keeps treating the subscription as paid until `next_billing_date` passes, then stops including it in active-feature checks.

Cancel is rejected in two specific cases: **LTA contracts** (long-term agreement subscriptions; only the account manager can cancel) and **unpaid plan turnover** (metered usage overage that must be settled first). A complementary rule, **canActivate**, governs the inverse case: when a Canceled subscription still has paid time remaining, clicking Renew skips the charge step and just flips status back to Active for free.

## Scope

Covered:

- The soft-cancel semantics — status flips immediately, access continues until `next_billing_date`.
- No proration, no partial refund, no end-of-period grace beyond the already-paid cycle.
- Cancel never deletes the subscription row — transactions and invoices remain downloadable forever.
- The two cancel-rejection cases (LTA contract; unpaid plan turnover) and their verbatim error messages.
- The `canActivate` free-reactivation rule.

Not covered here:

- The Renew button's paid-charge flow — see [[subscription-lifecycle-renew]].
- Per-type side effects of Cancel (plan / feature-pack / app / service / theme) — see [[subscription-lifecycle-cascades]].
- The status enum and the auto-retry budget that interacts with Cancel — see [[subscription-lifecycle-states]] and [[subscription-lifecycle-renewal-retry]].

## Contrasts

- **Soft cancel vs. immediate termination** — Cancel writes a Canceled state and stops FUTURE charges; the CURRENT paid cycle still runs to completion. This is the source of "I cancelled and was still charged" misunderstandings. The actual flow is: "I cancelled, the platform stopped scheduling more charges, the cycle I had already paid for finished out."
- **Cancel vs. canActivate Renew** — Cancel moves Active / Past due into Canceled. canActivate is the inverse: it lets the merchant flip a Canceled subscription back to Active for free as long as `next_billing_date > now`. The merchant hasn't lost the paid time; they're just un-cancelling.
- **LTA-blocked cancel vs. turnover-blocked cancel** — LTA-blocked subscriptions have a `lta_contract_id` and their entire lifecycle is owned by the account manager. Turnover-blocked subscriptions are technically cancellable but require settling unpaid metered overage first. The merchant sees a different error message in each case.

## Where it applies

### Cancel is "soft" — does NOT immediately terminate access

Clicking **Cancel**:

1. Sets the subscription's `status` to Canceled.
2. Does NOT cut off the service mid-cycle.
3. The merchant keeps using the feature / app / plan until `next_billing_date` passes (because the platform's `isPaid` check returns true while `now < next_billing_date && status == Canceled`).
4. After `next_billing_date` passes, the platform stops including this subscription in active-feature checks — the service stops.

**No proration / no partial refund / no end-of-period grace beyond the already-paid cycle.** The merchant pays for the full cycle they're in, even if they cancel one day after renewal.

Cancel writes a Canceled state but **never deletes the subscription row** — cancelled subscriptions stay in [[subscriptions]] filtered by Status = Canceled, with their transaction history and invoices remaining downloadable forever. See [[subscription-lifecycle-cache-audit]] for the audit-trail rules.

### Cancel rejection — LTA contracts

When the subscription has an `lta_contract_id`, the backend rejects Cancel with:

> *"This subscription has a related contract. Contact your account manager!"*

LTA-contract subscriptions also have the Action column **empty** in [[subscriptions]] — both Cancel and Renew are managed through the contract's flow. Renewals follow the contract's offer-item flow rather than the standard pipeline.

### Cancel rejection — unpaid plan turnover

When the subscription has unpaid metered overage (variable / turnover-based billing), Cancel is rejected with:

> *"This subscription has unpaid turnover amount. Contact your account manager!"*

The merchant must settle the turnover invoice before the subscription can be cancelled. This is distinct from the Renew-time turnover check (see [[subscription-lifecycle-renew]]); both surfaces enforce the rule but produce different downstream actions.

### canActivate — when Renew is a "free reactivation"

If the subscription was Canceled but the merchant still has paid time remaining (`next_billing_date > now`), Renew does NOT make a new charge. Instead it just flips status back to Active for free — the platform's `canActivate` check returns true and skips the charge step.

This handles the "I cancelled by mistake, restore me" use case. The merchant gets back to Active without losing money. Once `next_billing_date` has passed, canActivate returns false and Renew falls back to the normal paid-charge flow — see [[subscription-lifecycle-renew]].

### What Cancel does NOT do

- Does not delete the subscription record.
- Does not refund any money.
- Does not immediately uninstall the app / lock the feature / disable the theme — the cascade fires at `next_billing_date`, not at the Cancel click. See [[subscription-lifecycle-cascades]].
- Does not reset `failed_attempts` — but it also doesn't matter, because the daily renewal job no longer picks up Canceled subscriptions.

## Related

- [[subscription-lifecycle]] — hub.
- [[subscription-lifecycle-states]] — sibling aspect; the enum that Cancel transitions through.
- [[subscription-lifecycle-renew]] — sibling aspect; the inverse action and the canActivate free-reactivation path.
- [[subscription-lifecycle-cascades]] — sibling aspect; what happens per subscription type when the paid cycle finally ends.
- [[subscriptions]] — the My subscriptions list with the Cancel button per row.
- [[subscriptions-detail]] / [[subscription-details]] — per-subscription detail screen with Cancel action.
- [[billing-cards]] — saved cards; the merchant can update these and still cancel later without re-charging.

## Open Questions

None.
