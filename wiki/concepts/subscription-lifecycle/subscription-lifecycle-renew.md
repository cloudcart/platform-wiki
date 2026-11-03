---
type: concept
nav_path: "Concept → Subscription lifecycle → Renew action"
aliases: ["Subscription renew", "Renew immediate charge", "Plan deprecation on renew", "App re-install on renew", "Feature pack re-apply on renew", "Подновяване на абонамент", "Ръчно подновяване"]
tags: [subscriptions, billing, lifecycle, renew, concepts]
plan_gates: []
created: 2026-06-10
updated: 2026-06-10
source_count: 2
---

> Part of [[subscription-lifecycle]]. See the hub for the other aspects (states, renewal-retry, cancel, cascades, cache-audit).

# Subscription lifecycle — renew action

## Definition

The **Renew** button is the merchant's manual escape hatch out of any non-Active state. Clicking it on a Past due, Canceled, or Expired subscription fires an **immediate fresh charge** against the saved card on file (see [[billing-cards]]). On success the cycle resets and the subscription returns to Active; on failure `failed_attempts` increments and the status drops to (or stays) Past due.

Renew is NOT bound by the 5-attempt auto-retry budget — the merchant can rescue a Past due subscription during the entire window between `failed_attempts >= 5` and the daily expire sweep flipping it to Expired. Plan-subscription renewals have two extra checks: if the underlying plan is no longer in the catalog the platform forces Past due and redirects to [[plans]]; if there is unpaid metered turnover, that invoice must clear before the regular renewal proceeds. App-subscription successful late renew also automatically **re-installs the app**; feature-pack renewal **re-applies the pack's limits** to the merchant's plan-feature quota.

A special-case shortcut on Renew — **canActivate** — skips the charge entirely when a Canceled subscription still has paid time remaining; see [[subscription-lifecycle-cancel]].

## Scope

Covered:

- The immediate-charge flow on Renew + the success / failure branches.
- The plan-deprecation check that forces Past due + redirect to [[plans]].
- The unpaid-turnover gate that runs before the regular plan renewal.
- The app re-install side effect on successful late Renew.
- The feature-pack quota re-apply side effect on successful Renew.
- The interaction with `next_billing_amount` (pricing protection on the renewal) — but pricing semantics are documented under [[subscription-lifecycle-cache-audit]].

Not covered here:

- The canActivate free-reactivation rule — see [[subscription-lifecycle-cancel]].
- The auto-retry pipeline that the manual Renew bypasses — see [[subscription-lifecycle-renewal-retry]].
- Per-type cascades that fire when Renew is NOT clicked in time — see [[subscription-lifecycle-cascades]].

## Contrasts

- **Manual Renew vs. auto-retry** — the auto-retry pipeline fires up to 5 times on the platform's schedule (see [[subscription-lifecycle-renewal-retry]]). Manual Renew fires an immediate fresh charge from the merchant click, regardless of `failed_attempts`. Manual Renew is the only way to rescue a subscription after the auto-retry budget exhausts but before the daily expire sweep.
- **Renew (paid) vs. canActivate (free reactivation)** — clicking Renew on a Canceled or Expired subscription normally fires an immediate fresh charge. The exception is canActivate: when the subscription was Canceled but `next_billing_date` is still in the future, Renew just flips status back to Active for free with no new charge. canActivate does NOT apply to Past due (where the charge attempt is by definition needed) or to Expired (where the paid time has already lapsed).
- **Plan-deprecation Renew vs. standard Renew** — if the merchant clicks Renew on a plan subscription whose underlying plan is no longer in the catalog, the platform forces Past due and redirects to [[plans]] for a fresh purchase instead of attempting the charge. The merchant cannot un-deprecate a retired plan.
- **App Renew with reinstall vs. feature-pack Renew with quota re-apply** — both are subscription types that have additional side effects on successful late Renew. Apps are automatically re-installed (the merchant does not need to click Install again on [[plan-apps]]); feature packs re-add their quota to the merchant's plan-feature lookup. See [[subscription-lifecycle-cascades]] for the per-type cascades.

## Where it applies

### Renew triggers an immediate charge

Clicking **Renew** on a Past due, Canceled, or Expired subscription:

1. Fires an immediate charge against the saved card on file (see [[billing-cards]]).
2. **On success**: cycle resets — new invoice issued, new `next_billing_date` set to `now + billing_cycle months`, `failed_attempts` zeroed, invoice email sent to the configured recipient (see [[details-billing]] for the recipient setting).
3. **On failure**: `failed_attempts` increments; status flips (or stays) Past due.

### Plan-deprecation Renew

When the merchant clicks Renew on a Plan subscription whose underlying plan record is no longer active in the catalog, the platform:

1. Forces the subscription to Past due.
2. Redirects to [[plans]] with the message *"This plan is not active. You can buy a new plan to renew the subscription."*
3. Does NOT attempt the charge — the merchant must select a current plan from [[plans-purchase]].

### Unpaid-turnover gate (plan subscriptions only)

If the plan subscription has unpaid metered overage (turnover-based billing), the regular renewal does NOT proceed. The merchant must pay the turnover invoice first; only after the turnover clears does Renew run the standard immediate-charge flow.

This is parallel to the Cancel-side turnover block — see [[subscription-lifecycle-cancel]] — but with a different downstream action: Cancel rejects outright, Renew defers until the turnover is settled.

### App re-install on successful Renew

If an app subscription went past `next_billing_date` and the platform uninstalled the app from the store (see [[subscription-lifecycle-cascades]] for the cascade), a successful late Renew **re-installs the app automatically** — no manual reinstall needed. The merchant just clicks Renew on [[plan-apps]] or [[subscriptions]] and the app is back.

### Feature-pack re-apply on successful Renew

Feature-pack subscription that went past `next_billing_date` had its quota removed from the plan-feature lookup (see [[plan-gates]]). Successful Renew **re-adds the quota** so the merchant's effective limit jumps back up immediately — the plan-feature cache invalidates on the subscription change. See [[subscription-lifecycle-cache-audit]] for the cache rule.

### The "free reactivation" exception (canActivate)

If the subscription is Canceled and `next_billing_date > now`, Renew skips the charge step entirely and just flips status back to Active. Documented under [[subscription-lifecycle-cancel]].

## Related

- [[subscription-lifecycle]] — hub.
- [[subscription-lifecycle-states]] — sibling aspect; the status enum Renew transitions out of.
- [[subscription-lifecycle-cancel]] — sibling aspect; the canActivate exception that turns Renew into a free flip.
- [[subscription-lifecycle-renewal-retry]] — sibling aspect; the auto-retry pipeline manual Renew bypasses.
- [[subscription-lifecycle-cascades]] — sibling aspect; what gets undone by a successful late Renew (app reinstall, feature-pack quota re-apply).
- [[subscriptions]] — the My subscriptions list with the Renew button per row.
- [[subscriptions-detail]] / [[subscription-details]] — per-subscription detail screen with Renew action.
- [[billing-cards]] — saved card used for the immediate Renew charge.
- [[details-billing]] — invoicing recipient applied to each Renew invoice.
- [[plans]] — where a deactivated plan subscription redirects on Renew.
- [[plans-purchase]] — the flow the merchant lands in after a plan-deprecated Renew.
- [[plan-apps]] — paid app catalog; Renew here re-installs the app on success.
- [[plan-features]] — feature-pack catalog; Renew here re-adds the quota on success.

## Open Questions

None.
