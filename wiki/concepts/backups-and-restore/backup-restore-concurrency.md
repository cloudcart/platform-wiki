---
type: concept
nav_path: "Concept → Backups and restore → Concurrency, 2FA, permission"
aliases: ["One restore at a time", "Restore concurrency", "Restore 2FA gate", "Cancel partial restore", "Cancel full restore", "settings.backups permission", "Едно възстановяване в момента", "Двуфакторно възстановяване"]
tags: [backups, ops, concurrency, 2fa, permission, cancellation, concepts]
plan_gates: ["backups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[backups-and-restore]]. See the hub for the other aspects (cadence, subscription gates, retention, full restore, partial restore, safety backup).

# Backups — concurrency, 2FA, and permission

## Definition

The platform enforces three guard rails around every restore. **Concurrency** — only one restore (full OR partial) can run at a time, system-wide for the store; a second start attempt is blocked. **2FA** — every restore (full or partial) requires a one-time two-factor code before the job is enqueued, with no "remember device" or skip for trusted admins. **Permission** — access to [[settings-backups]] is gated by the `settings.backups` staff permission, which only appears in the Access tree on [[settings-staff]] when the plan includes the `backups` feature.

The most-asked operational question is "I started a restore — can I cancel it?" The answer depends on the mode: **partial restores ARE cancellable**, **full restores are NOT cancellable from admin**. This is the asymmetry that surprises merchants — a full restore stuck for an hour cannot be killed without contacting CloudCart support.

## Scope

Covered:

- The one-restore-at-a-time rule and the blocked-banner behaviour.
- The 2FA gate before every restore (no skip / no remember-device).
- The cancellable / non-cancellable asymmetry between partial and full restores.
- The cancelled-mid-import outcomes for partial restores.
- The `settings.backups` staff permission and its plan-feature visibility rule.

Not covered here:

- The pipeline of a full restore — see [[backup-restore-full-restore]].
- The pipeline of a partial restore — see [[backup-restore-partial-restore]].
- The safety-backup auto-delete on cancellation — see [[backup-restore-safety-backup]].
- The three-layer subscription gate — see [[backup-restore-subscription-gates]].

## Contrasts

- **Concurrency lock vs. Subscription gate**: the subscription gate determines IF the merchant can start a restore; the concurrency lock determines WHEN (only when no other restore is running). Both must pass.
- **2FA gate vs. Permission gate**: 2FA is per-restore (every Restore click prompts for a code); the permission is per-staff-role (does the moderator see the screen at all). Both are independent — a staff member with `settings.backups` permission still has to pass 2FA on every restore.
- **Cancellable partial vs. Non-cancellable full**: partial restores can be cancelled mid-merge; full restores cannot be cancelled mid-SQL-import. The reason is that a partially-imported SQL would leave the database in an inconsistent state.

## Where it applies

### Only one restore at a time — system-wide for the store

The platform allows only one restore (full OR partial) to run at a time, system-wide for the store. If a restore is in progress, the merchant sees the banner on [[settings-backups]]:

> *"A restore is already in progress. Please wait for it to complete before starting a new one."*

And the start button is blocked. The block applies across:

- Multiple administrators in the same store (a second admin in a separate browser tab cannot start a competing restore).
- Multiple browser sessions of the same administrator.
- API-driven restore attempts (if any exist) — the lock is enforced server-side, not just in the UI.

Cross-store concurrency is NOT an issue — the lock is per-store. A multi-store merchant can run a restore on store A and another on store B simultaneously.

### Two-factor verification required before every restore

Both the full Restore and Partial Restore actions REQUIRE a 2FA verification step before the job is dispatched. The merchant:

1. Clicks Restore (full) or Partial Restore on a backup row.
2. Reviews the confirmation dialog (with the safety-backup notice).
3. Requests a one-time code via the 2FA flow (email, SMS, or authenticator app per the merchant's 2FA setup).
4. Enters the code in the dialog.
5. Only THEN does the restore job get enqueued.

A request with a missing or expired verification returns the validation error:

> *"Two-factor verification required."*

This applies to **every restore** — there is no "remember device" or skip for trusted admins. The reasoning is that a restore is destructive (full restore replaces everything; partial restore can flood the live store with records that haven't been seen in days). The 2FA gate is the platform's stop-loss against a compromised admin session triggering a catastrophic restore.

### Only partial restores are cancellable

The cancellable / non-cancellable asymmetry between the two modes:

**Partial restore — IS cancellable.**

The merchant can cancel a running partial restore via the active-restore banner on [[settings-backups]] or via [[settings-queue-view]]. Cancellation stops the additive merge mid-record, drops any orphaned temporary databases, auto-deletes the safety backup that was created for the cancelled restore (see [[backup-restore-safety-backup]]), and leaves no trace in the backup list.

The data state depends on how far the merge got — could be partially restored, could be fully rolled back, could be a mix. Cancellation should be treated as "I no longer want this restore", not "undo restore I just started" — if the merchant needs the pre-restore state back precisely, they should restore from the safety backup BEFORE cancelling.

**Full restore — is NOT cancellable from admin.**

The Cancel action on a running full restore (visible via [[settings-queue-view]] or the active-restore banner on [[settings-backups]]) returns the validation error:

> *"Only partial restores can be cancelled."*

If a full restore is in trouble, the merchant must contact CloudCart support. The reasoning is that a partially-applied SQL import would leave the database in an inconsistent state if killed mid-import; the platform forces the restore to run to completion or be reverted by support manually.

### Permission — `settings.backups` staff row

Access to [[settings-backups]] is gated by the `settings.backups` staff permission. Per [[settings-staff]], this permission row appears in the staff role's Access tree **ONLY when the merchant's plan has the `backups` feature enabled** — otherwise it's silently hidden from the permission picker. A moderator without the permission cannot see the screen at all (the sidebar entry is hidden too).

Two implications:

- Granting the permission on a staff role to a merchant whose plan doesn't have `backups` is impossible — the picker doesn't show the row.
- If the merchant downgrades their plan to one without `backups`, all staff roles silently lose the permission row from their Access tree (it's not "kept but inactive" — it disappears entirely until the plan-feature is re-enabled).

A staff member with the permission can do everything the administrator can do on [[settings-backups]] — start restores, see the list, click Extend Period — but each restore still requires their own 2FA code (no per-staff-role bypass).

### No automated "restore complete" notification

The restore job is a long-running background process. There's no automated email or admin alert when a restore completes — no `restore.completed` event in [[settings-hooks]], no admin email in [[settings-admin-notifications]]. The merchant must manually check [[settings-backups]] or [[settings-queue-view]] to verify. See [[notification-delivery]] for the broader pattern.

## Related

- [[backups-and-restore]] — hub.
- [[settings-backups]] — the admin screen with the Restore and Cancel actions.
- [[settings-queue-view]] — where the running restore surfaces and can be cancelled (partial only).
- [[settings-staff]] — the `settings.backups` permission row.
- [[plan]] — plan-feature `backups` controls permission-row visibility.
- [[backup-restore-full-restore]] — the non-cancellable restore mode.
- [[backup-restore-partial-restore]] — the cancellable restore mode.
- [[backup-restore-safety-backup]] — auto-deleted when a partial restore is cancelled.
- [[notification-delivery]] — no automated "restore complete" email; merchant polls.
- [[settings-hooks]] — no `restore.completed` webhook exists.

## Open Questions

None — all previously-flagged items in this aspect resolved.
