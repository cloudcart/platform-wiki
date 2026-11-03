---
type: entity
aliases: ["Backup gating", "Backup plan feature", "Backup three gates", "Backups subscription", "Partial restore add-on", "settings.backups permission", "PAST_DUE backups grace"]
tags: [settings, ops, backups, plan-feature, permissions, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[backup]]. See the hub for the other aspects (identity, attributes, lifecycle, restore pipeline, storage and scope).

# Backup — Gating

## Identity

Backups are a **paid plan-gated add-on**, not a free platform service. Three independent gates must all clear before the merchant can see ANY Backup on [[settings-backups]]: their [[plan|Plan]] must include the `backups` plan-feature, they must have an active Backups subscription on top of the Plan, and for the optional Partial Restore mode they need a separate `partial_restore` add-on subscription. On top of that, staff users need the `settings.backups` permission to reach the screen at all.

Without these, [[settings-backups]] shows a marketing splash + checkout flow instead of the Backup list — even if backup files physically exist for the Site on CloudCart storage.

## Aliases

- **Backup gating** — canonical phrasing.
- **Backups plan-feature** — the `backups` plan-feature key on [[plan|Plan]].
- **Backups subscription** — the merchant's active subscription to the Backups service.
- **Partial restore add-on** — the `partial_restore` subscription that unlocks the per-segment restore mode.
- **Backups permission** — the `settings.backups` staff permission.

## Key Attributes

| Gate | What it checks | Failure mode |
|------|----------------|--------------|
| **Plan-level** (`backups` plan-feature) | The merchant's active [[plan|Plan]] includes the `backups` feature (`feature_enabled=true`). | Some basic plans don't include it — the merchant sees an upgrade prompt first and the `settings.backups` permission is hidden from staff-role pickers. |
| **Service subscription** | The merchant has subscribed to the Backups service explicitly (`subscribed=true`) on top of the Plan. | [[settings-backups]] is a marketing/sales page with subscribe call-to-action. No Backups visible. |
| **Partial-restore add-on** (`partial_restore`) | Optional. The merchant has subscribed to the `partial_restore` pack. | The list still shows daily Backups + full Restore action; only the per-row Partial Restore action is hidden. |
| **Subscription state** | The Backups subscription is in `ACTIVE` or `PAST_DUE`. | Once the subscription transitions out of `PAST_DUE`, the merchant loses VISIBILITY into existing Backups (no rows on [[settings-backups]]) — see [[backup-entity-lifecycle]]. |
| **Staff permission** (`settings.backups`) | The signed-in staff user's role grants `settings.backups`. | Sidebar item / route returns 403. |

The four feature-level gates (Plan, Subscription, Partial-restore, Subscription state) are independent — each failure shows a different fallback. The permission gate is layered on top: a merchant-admin (account owner) bypasses it; sub-users without the role do not.

## Three independent feature gates

### Plan-level: `backups` plan-feature

The merchant's [[plan|Plan]] must include the `backups` plan-feature. The check is binary — feature enabled or not. Some basic plans don't have it; on those, [[settings-backups]] shows an upgrade prompt directing the merchant to switch plans first.

### Service subscription: ACTIVE or PAST_DUE

Even on a plan that includes Backups, the merchant must subscribe to the Backups service explicitly. Subscription state can be:

- `ACTIVE` — full access.
- `PAST_DUE` — full access (grace period after a missed renewal payment).
- Anything else (cancelled, exhausted, never-subscribed) — no access; [[settings-backups]] is a sales page.

Without subscription, [[settings-backups]] is a sales page with a marketing splash and a checkout button — even if backup files physically exist on CloudCart storage for the Site.

### Partial-restore add-on: optional, on top of Backups

The optional Partial Restore mode requires a separate `partial_restore` pack subscription ON TOP of the base Backups subscription. Without it:

- The list view still shows daily Backups.
- The per-row **Restore** (full) action is still available.
- The per-row **Partial Restore** action and the segment-picker form are hidden.
- The page header shows a "Subscribe to Partial Restore" call-to-action button.

See [[backup-entity-restore-pipeline]] for the partial-restore mechanics that this gate unlocks.

## PAST_DUE grace + lapse aftermath

`PAST_DUE` is the platform-wide grace state for a subscription that missed its renewal payment. While in `PAST_DUE`, the merchant retains full access to the Backups feature — they can still list, restore, and run partial restores. This is intentional: the merchant most needs a restore right when their billing situation is messy.

Once the subscription transitions out of `PAST_DUE` (full cancellation, exhausted retries, plan downgrade that drops the `backups` feature):

- The list of Backups disappears (no rows visible).
- Restore and Partial Restore actions are gone.
- The Extend Period upgrade is gone.
- The page shows the marketing splash + checkout — same UI as a brand-new merchant.

Underlying files may be retained on CloudCart storage for some additional time but are no longer visible to the merchant. Recovery requires reactivating the subscription or contacting CloudCart support. See [[backup-entity-lifecycle]] for the lifecycle-side view of the lapse.

## Staff permission: `settings.backups`

Access to [[settings-backups]] for non-owner staff users is gated by the `settings.backups` staff permission. Per [[settings-staff]], this permission row appears in the staff role's Access tree ONLY when the merchant's [[plan|Plan]] has the `backups` feature enabled — otherwise it's silently hidden from the permission picker.

Effect: a sub-user role on a plan WITHOUT the `backups` feature cannot even be granted the permission. On a plan WITH the feature, the permission must be explicitly granted to the role before sub-users can reach the screen. The merchant-admin (account owner) always has access regardless.

## Where it appears

- [[settings-backups]] — every gate is evaluated at page load; the fallback UI changes accordingly.
- [[settings-staff]] — the `settings.backups` permission row appears conditionally based on the Plan gate.
- [[plan-gates]] — the broader plan-feature gating concept.

## Related

- [[backup]] — hub.
- [[plan]] — `backups` and `partial_restore` plan-features.
- [[plan-feature]] — subscription-on-top-of-Plan mechanics, `ACTIVE` / `PAST_DUE` states.
- [[plan-gates]] — plan-feature gating concept across the platform.
- [[settings-staff]] — the staff permission picker.

## Open Questions

None.
