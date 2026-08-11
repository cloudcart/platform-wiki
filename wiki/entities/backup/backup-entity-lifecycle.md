---
type: entity
aliases: ["Backup lifecycle", "Backup creation", "Backup aging", "Daily backup creation", "Safety backup creation", "Backup retention", "Cancelled restore safety auto-delete", "Subscription lapse backup access"]
tags: [settings, ops, backups, lifecycle, retention, entity]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[backup]]. See the hub for the other aspects (identity, attributes, gating, restore pipeline, storage and scope).

# Backup — Lifecycle

## Identity

This page documents how a Backup comes into existence, becomes visible to the merchant, gets used (or not), and is eventually purged. There are two creation paths (daily auto + pre-restore auto) and several exit paths (age-out, cancelled-restore auto-delete, subscription lapse). At no point does the merchant directly create or delete a Backup — every transition is platform-managed.

## Aliases

- **Backup lifecycle** — canonical phrasing.
- **Backup creation** — the daily and pre-restore pipelines.
- **Backup aging** — the retention window purge.
- **Retention window** — the merchant-facing term for the age limit.

## Key Attributes

A Backup moves through these phases:

1. **Daily creation (auto)** — every day, while the merchant's backups subscription is active, the platform takes a Backup. New row appears in the [[settings-backups]] list with `is_safety=false`. Cadence is platform-managed; merchant cannot change it. There is NO "back up now" button.
2. **Pre-restore creation (auto)** — right before every full or partial restore, the platform takes a Backup with `is_safety=true`. Surfaces in the same list with the safety badge. See [[backup-entity-restore-pipeline]].
3. **Visible to merchant** — Backup appears in the [[settings-backups]] list. Per-row Restore and Partial Restore actions are available.
4. **Used for restore (optional)** — the merchant clicks Restore or Partial Restore. The Backup is read; restore pipeline runs. The Backup itself is unchanged (restores are read-only against the source Backup file).
5. **Aged out** — once the Backup's age exceeds the retention window the merchant purchased (typical 7 / 30 / 60 / 90 days), it is hidden from the merchant's list and eventually purged from storage. Both daily Backups AND safety Backups age out with the SAME retention window.
6. **Cancelled-restore safety auto-delete** — if the merchant cancels an in-progress partial restore from [[settings-queue-view]], the platform automatically deletes the safety Backup that was created for that specific restore. The cancelled restore leaves no trace in the list.
7. **Subscription lapse → loss of access** — if the backups subscription transitions out of `ACTIVE` / `PAST_DUE` (cancellation, payment exhaustion, plan downgrade), the merchant loses VISIBILITY into existing Backups. Underlying files may be retained on CloudCart storage for some additional time but the merchant cannot access them.

## Daily auto-cadence — no manual trigger

CloudCart takes a Backup of every subscribed Site every day automatically. The merchant cannot:

- Trigger a manual "back up now".
- Change the schedule.
- See a scheduler UI on [[settings-backups]].

Backups just appear in the list each day. Merchants planning a risky operation should subscribe at least 24 hours BEFORE so that one Backup exists by the time they need it — see [[backup-entity-identity]] for the "not retroactive" rule.

## Retention window — dynamic per subscription pack

The retention window (in days) is dictated by the merchant's specific Backups-subscription pack. Different packs sell different windows. The merchant sees their current pack's day-count in the page meta (`subscription_days`). The **Extend Period** button (shown when `has_upgrade=true`) lets them upgrade to a larger pack for more days of history.

Safety Backups DO count toward the retention window — so a merchant performing many restores in a short period accumulates more safety Backups, but the oldest ones still drop off when the window passes.

When a Backup ages out:

1. It is hidden from the merchant's [[settings-backups]] list.
2. After some additional grace, the underlying file is purged from off-platform storage.
3. The merchant has no UI to recover an aged-out Backup. Recovery requires contacting CloudCart support BEFORE the storage-level purge.

## Cancelled-restore safety auto-delete

The merchant can cancel a running **partial** restore via [[settings-queue-view]] / the active-restore banner. When cancellation happens:

1. The queued partial-restore job is dropped.
2. Any orphaned temporary databases the partial restore created are removed.
3. The safety Backup that was auto-created at the start of the cancelled restore is **deleted**.
4. The result: a cancelled partial restore leaves NO trace in the [[settings-backups]] list — no orphan safety Backup confusing the merchant about whether the restore happened.

Full restores **cannot be cancelled** — see [[backup-entity-restore-pipeline]]. So the safety Backup created for a full restore always remains in the list (subject to normal aging).

## Subscription lapse → grace period via PAST_DUE, then no access

The Backups feature surfaces are gated on the merchant's subscription being either `ACTIVE` or `PAST_DUE`. A subscription that missed its renewal payment still grants access during a grace period (subscription enters `PAST_DUE`). Once the subscription transitions out of `PAST_DUE` (cancellation, exhaustion), the merchant loses access to:

- The list of Backups (no rows visible — the page shows the marketing splash + checkout).
- The Restore and Partial Restore actions.
- The Extend Period upgrade.

Underlying files may be retained on CloudCart storage for some additional time but are no longer visible to the merchant. Recovery beyond that requires reactivating the subscription or contacting CloudCart support. **Do NOT let the Backups subscription lapse if there's any chance the merchant might need a restore.** See [[backup-entity-gating]] for the full gating model.

## Where it appears

- [[settings-backups]] — where Backups appear (and disappear) per the lifecycle above.
- [[settings-queue-view]] — long-running restore jobs surface here; cancellation lives here for partials.

## Related

- [[backup]] — hub.
- [[backup-entity-restore-pipeline]] — the restore step that triggers pre-restore creation + the cancellation rules.
- [[backup-entity-gating]] — `ACTIVE` / `PAST_DUE` subscription-state gates.
- [[plan-feature]] — the Backups subscription pack and its retention window.
- [[settings-queue-view]] — where the restore queue surfaces.

## Open Questions

None.
