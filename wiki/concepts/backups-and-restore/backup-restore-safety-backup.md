---
type: concept
nav_path: "Concept → Backups and restore → Safety backup"
aliases: ["Safety backup", "Pre-restore safety snapshot", "Restore rollback point", "Safety badge backup", "Cancelled restore safety auto-delete", "Безопасен бекъп", "Предварителен бекъп преди възстановяване"]
tags: [backups, ops, safety-backup, rollback, concepts]
plan_gates: ["backups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 1
---

> Part of [[backups-and-restore]]. See the hub for the other aspects (cadence, subscription gates, retention, full restore, partial restore, concurrency).

# Backups — safety backup

## Definition

A **safety backup** is a backup snapshot the platform auto-creates of the pre-restore state right BEFORE every restore (full or partial). The safety backup appears in the same list on [[settings-backups]] as daily backups, distinguished by the **safety** badge in the list row. Its purpose is to give the merchant an automatic rollback point — if the restore turns out badly, the merchant can restore from the safety backup to recover the state that was live moments before the restore started.

Safety backups are the merchant's **second chance** after a bad restore. The most-misunderstood detail is the retention rule: safety backups count toward the retention window just like daily backups, so they age out and are purged when the window passes. A merchant who performs a high-stakes restore on a 7-day retention pack has only 7 days to revert via the safety backup before it disappears.

The second-most-misunderstood detail is the auto-delete-on-cancel rule: if the merchant cancels an in-progress restore, the safety backup that was auto-created for that specific restore is also deleted automatically (so a cancelled restore leaves no trace in the list).

## Scope

Covered:

- The auto-creation rule (every restore, full or partial, creates a safety backup before starting).
- The visibility of safety backups in the [[settings-backups]] list and the safety badge.
- The retention behaviour (same window as daily backups; age out under the retention rule).
- The auto-delete-on-cancellation rule (safety backup goes away when the restore that created it is cancelled).
- The second-chance role after a bad restore.
- Practical guidance for extending retention before a high-stakes restore.

Not covered here:

- The retention window itself — see [[backup-restore-retention]].
- The full-restore pipeline that creates the safety backup — see [[backup-restore-full-restore]].
- The partial-restore pipeline that creates the safety backup — see [[backup-restore-partial-restore]].
- Concurrency / cancellation mechanics — see [[backup-restore-concurrency]].

## Contrasts

- **Safety backup vs. Daily backup**: both are snapshots stored in the same list. The daily backup is auto-created on the daily schedule; the safety backup is auto-created right before every restore. Both age out under the same retention window. Distinguished by the safety badge on the list row.
- **Safety backup vs. Manual rollback**: there is no manual "create restore point" trigger. The merchant cannot ask the platform to take a safety backup at an arbitrary moment — they only get one as a side-effect of starting a restore.
- **Restoring from a safety backup vs. Restoring from a daily backup**: identical mechanics. Both run the same pipeline (full or partial), both create their OWN safety backup before running, both can be cancelled under the same rules.

## Where it applies

### Auto-created before every restore

Every restore (full or partial) auto-creates a safety backup of the pre-restore state. The safety-backup step happens in the restore pipeline:

- For [[backup-restore-full-restore]]: step 2 of the 7-step pipeline (after maintenance mode is enabled, before the SQL import).
- For [[backup-restore-partial-restore]]: created before the additive merge starts.

The merchant doesn't trigger the safety-backup creation manually — it's an unconditional part of the restore pipeline. There is no setting to disable it. Every restore creates one safety backup; restoring from a safety backup also creates a new safety backup (the chain can compound during high-volume support intervention).

### Visibility in the [[settings-backups]] list

Safety backups appear in the same list as daily backups, **distinguished by the safety badge** in the list row. The list is default-sorted by backup date descending, so a freshly-created safety backup appears at the top right after the restore starts (and the daily-backup row from earlier the same day is just below it).

The safety badge is the merchant's signal that the row was auto-created by a restore — not by the daily schedule. The merchant can restore from it the same way as a daily backup; the Restore and Partial Restore actions behave identically on safety-badged rows.

### Counts toward the retention window

Safety backups are subject to the same retention rules as daily backups — they age out and are deleted when the retention window passes. A merchant performing a restore today has only **UNTIL THE RETENTION WINDOW EXPIRES** to revert via the safety backup. After that, the safety snapshot is gone and the restore is permanent. Merchants doing high-stakes restores should consider extending their retention pack first — see [[backup-restore-retention]].

### Auto-deleted when the restore that created it is cancelled

If the merchant cancels an in-progress restore (only possible for partial restores — see [[backup-restore-concurrency]]), the safety backup that was auto-created for that specific restore is **also deleted automatically**. The platform's reasoning:

- A cancelled restore should leave no trace in the list.
- The pre-cancel state IS the current state (the cancellation rolled back any partial changes).
- The safety backup is no longer needed as a rollback point.

So a cancelled partial restore leaves both the cancelled job AND its safety backup gone. The merchant sees no badge / no row indicating "you tried to restore and cancelled" — the list looks the same as before the restore was attempted.

### Second chance after a bad restore

The primary role of a safety backup is the **second chance**: if the restore completed but the result is bad (wrong backup chosen, corrupted snapshot, unexpected side-effect), the merchant can restore from the safety backup to recover the pre-restore state. The procedure:

1. Open [[settings-backups]].
2. Find the safety-badged row created at the moment the bad restore started.
3. Click Restore (full) or Partial Restore on that safety row.
4. The platform runs the same restore pipeline against the safety backup — creating yet another safety backup before doing so.

This second-restore is itself a restore — with all the rules that apply (storefront downtime for full mode, append-only for partial mode, post-backup data loss for full mode, etc.).

### Practical guidance — extend retention before a high-stakes restore

Merchants about to do a high-stakes restore (hack recovery, botched bulk import) should:

- Extend their retention pack BEFORE the restore — preserving the safety backup that the restore will auto-create.
- Schedule the restore during low-traffic hours (see [[backup-restore-full-restore]] for the scheduling guidance).
- Document the safety-backup date / time externally so they know which row to restore from if rollback is needed.
- Avoid restoring from a 7-day pack if there's any chance the bad restore won't be discovered within the week.

## Related

- [[backups-and-restore]] — hub.
- [[settings-backups]] — the admin screen where safety backups appear with the safety badge.
- [[backup-restore-full-restore]] — the restore mode that creates a safety backup before the SQL import.
- [[backup-restore-partial-restore]] — the restore mode that creates a safety backup before the additive merge.
- [[backup-restore-retention]] — the same retention window applies; extend it before high-stakes restores.
- [[backup-restore-concurrency]] — cancellation rules that trigger the auto-delete-on-cancel behaviour.
- [[backup]] — the backup entity; the `is_safety` flag is what drives the badge.

## Open Questions

None — all previously-flagged items in this aspect resolved.
