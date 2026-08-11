---
type: concept
nav_path: "Concept → Backups and restore → Subscription gates"
aliases: ["Backups subscription gates", "Three-layer gate", "Backups PAST_DUE grace period", "Subscription lapse access loss", "Partial restore add-on", "Backups plan-feature", "Гейтове за бекъп абонамент"]
tags: [backups, ops, plan-feature, subscription, gates, concepts]
plan_gates: ["backups", "partial_restore"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[backups-and-restore]]. See the hub for the other aspects (cadence, retention, full restore, partial restore, safety backup, concurrency).

# Backups — subscription gates

## Definition

Access to the backups feature is controlled by **three independent gates** that all must clear before the merchant can see ANY backup on [[settings-backups]]. The first gate is plan-level (the `backups` plan-feature must be enabled on the merchant's plan), the second is service-level (the merchant must be actively subscribed to the backups pack on top of the plan), and the third is add-on-level (partial restore needs a separate `partial_restore` subscription on top of the base backups subscription). Some basic plans don't have the `backups` plan-feature at all — those merchants see an upgrade prompt for the plan first.

The "subscription is separate from the plan" detail is the most-confused gate. A merchant upgrading their CloudCart plan to a tier that *includes* the `backups` feature does NOT automatically get backups — they still have to subscribe to the backups service explicitly. Without that subscription, [[settings-backups]] is a sales page with a marketing splash and a checkout flow instead of the list of available backups.

When the subscription lapses, the merchant loses access via the same three gates — but a grace period applies first via the `PAST_DUE` state.

## Scope

Covered:

- The three-layer gate (plan-feature, active subscription, partial-restore add-on).
- The ACTIVE / PAST_DUE access window and the grace-period rule.
- What the merchant loses when the subscription transitions out of PAST_DUE.
- Per-store subscription scoping on multi-store accounts.
- The `settings.backups` permission row's plan-level visibility rule.

Not covered here:

- The retention pack and Extend Period upgrade — see [[backup-restore-retention]].
- The daily-snapshot cadence the gates control — see [[backup-restore-cadence-content]].
- The general plan-feature mechanism — see [[plan-gates]].
- Permission gating per-staff-role — covered in [[backup-restore-concurrency]].

## Contrasts

- **Plan feature vs. service subscription**: the plan-feature gate determines IF the merchant can subscribe; the service-subscription gate determines IF they actually have. Both must be `true`.
- **`backups` pack vs. `partial_restore` pack**: the base `backups` pack covers the daily snapshot + full restore. The `partial_restore` pack is an add-on on top that unlocks the segment-based partial restore mode. A merchant subscribed only to `backups` can do full restores but not partial ones.
- **ACTIVE vs. PAST_DUE**: both grant access — PAST_DUE is the grace period after a missed renewal payment. Once the subscription transitions out of PAST_DUE (cancellation, exhaustion), access drops.

## Where it applies

### Three-layer subscription gate

The backups feature has THREE independent gates the merchant must clear:

1. **Plan-level**: the merchant's [[plan]] must include the `backups` feature. Some basic plans don't — the merchant sees an upgrade prompt for the plan first.
2. **Service subscription**: even on a plan that includes backups, the merchant must subscribe to the backups service explicitly. Without subscription, the [[settings-backups]] screen is a sales page with a marketing splash + checkout flow.
3. **Partial-restore add-on**: the optional Partial Restore mode needs a separate `partial_restore` pack subscription on TOP of the base backups subscription. A merchant subscribed only to `backups` sees the **Subscribe to Partial Restore** button in the [[settings-backups]] header instead of the Partial Restore action.

Some merchants think upgrading the plan auto-enables backups; it doesn't. The plan unlocks the *ability* to subscribe; the subscription itself is a separate recurring purchase.

### ACTIVE / PAST_DUE — grace period before access drops

The backups feature surfaces are gated on the merchant's subscription being in either of two states:

- **ACTIVE** — the subscription is current; daily backups are taken; the full backup list is visible on [[settings-backups]]; Restore and Partial Restore actions work normally.
- **PAST_DUE** — the subscription missed its renewal payment but is still within the grace period. Access continues exactly as ACTIVE — the merchant can still restore. This grace period exists to avoid catastrophic data loss when a payment fails on a card that the merchant simply forgot to update.

Once the subscription transitions OUT of PAST_DUE — either because the merchant cancelled, or the platform terminated the lapsed sub after the grace window — the merchant loses access to:

- The list of backups (no rows visible on [[settings-backups]]).
- The Restore and Partial Restore actions.
- The Extend period upgrade.

The underlying backup files may be retained on CloudCart storage for some additional time but are no longer visible to the merchant. Recovery beyond that requires reactivating the subscription or contacting CloudCart support.

**Practical guidance**: do NOT let the backups subscription lapse if there's any chance the merchant might need a restore. The cost of reactivation + lost-data risk far outweighs the monthly pack price.

### Per-store subscription (multi-store accounts)

Backups subscriptions are scoped to a specific store. A merchant who manages two stores under one account does NOT get a combined subscription — each store needs:

- Its own active `backups` subscription.
- Its own `partial_restore` add-on if partial restore is wanted.
- Its own retention pack (the days purchased on one store don't apply to the other).

A merchant subscribing the main store while leaving the secondary store unsubscribed gets daily backups on the main store only. See [[backup-restore-cadence-content]] for the per-store cadence rule.

### Plan-feature visibility of the staff permission row

The `settings.backups` staff permission row in the Access tree on [[settings-staff]] appears **only when the merchant's plan has the `backups` feature enabled**. On plans without the feature, the permission row is silently hidden from the picker — the staff role cannot be configured to grant or revoke access to a screen the merchant doesn't have. This is a plan-level visibility rule; the service-subscription gate doesn't affect it (a merchant on a backups-capable plan but not subscribed still sees the permission row, and granting it on a staff role still works — that staff member just sees the same marketing splash the administrator sees).

## Related

- [[backups-and-restore]] — hub.
- [[plan]] — the plan-feature `backups` and `partial_restore`.
- [[plan-gates]] — the general plan-feature gating mechanism.
- [[settings-backups]] — the admin screen the gates control.
- [[settings-staff]] — the `settings.backups` permission row.
- [[backup-restore-retention]] — the retention pack purchased as part of the subscription.
- [[backup-restore-cadence-content]] — the daily snapshot the subscription pays for.

## Open Questions

None — all previously-flagged items in this aspect resolved.
