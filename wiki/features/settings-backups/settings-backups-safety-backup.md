---
type: feature
nav_path: "Settings → Backup & Restore → Safety backup"
route_name: backups.settings
route_path: /admin/settings/backups
aliases: ["Safety backup", "Pre-restore snapshot", "Rollback point", "is_safety badge", "Safety backup deletion"]
tags: [settings, backups, safety-backup, rollback]
plan_gates: ["backups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-backups]]. See the hub for the other aspects (subscription gates, list view, full restore, partial restore, 2FA gate, restore progress).

# Backups — safety backup

## Purpose

Before any restore (full or partial) runs, the platform automatically takes a **safety backup** of the current live state. This is a pre-restore snapshot tagged `is_safety=true` that appears in the same backup list as the daily backups, and gives the merchant a rollback point if the restore turns out badly.

The merchant doesn't trigger safety backups — they're a side effect of every restore call. They cannot be turned off.

## Where to find it

Safety backups appear in the standard backups list at Sidebar → Settings → **Backup & Restore** ([[settings-backups-list-view]]). The row carries a *"safety"* badge to distinguish it from regular daily backups.

## What the merchant can do here

- Identify safety backups by the *"safety"* badge in the list.
- Use a safety backup as the source for a follow-up restore (full or partial) — same row-level **Restore** / **Partial Restore** buttons as any other backup.
- Effectively roll back from a bad restore by full-restoring from the safety backup that was created just before that restore.

### What the merchant CANNOT do

- Trigger a safety backup manually outside of a restore — they only exist as a side effect of restores.
- Delete a safety backup directly — they expire on the same retention window as daily backups, or are auto-deleted when the merchant cancels the partial restore that created them.

## Settings & fields

### Identification — the `is_safety` flag

A backup row gets the *"safety"* badge when the platform tags the file with `is_safety=true`. This flag is set when the restore job creates the pre-restore snapshot. There's no other way for `is_safety` to be true — daily auto-backups don't set it, and there's no manual UI to mark a backup as safety.

The list table renders the safety badge as a chip in the row alongside the date / file size / server / created-at columns ([[settings-backups-list-view]]).

## Business rules

### Auto-created right before every restore

Both the full-restore and partial-restore job include a `creating_safety_backup` step early in their step sequence (see [[settings-backups-restore-progress]] for the full step list). The step:

- Takes a snapshot of the current live database.
- Uploads it to backup storage (via `sftp -b` to create the remote directory structure if needed, then `scp` to upload the `.sql.gz` file).
- Inserts a corresponding row with `is_safety=true`.

This happens BEFORE the destructive import phase (full restore) or BEFORE the temp-DB import (partial restore), so the safety backup captures the state at the moment the merchant pressed Restore.

### Same retention rules as daily backups

Safety backups are stored in the same backup table as the regular daily backups and are subject to the same retention rules (see [[settings-backups-list-view]]'s retention cutoff). Once they age past the merchant's configured retention window (in days, per the `backups` subscription pack — see [[settings-backups-subscription-gates]]), they expire along with regular daily backups.

So a merchant performing many restores in a short period accumulates more safety backups, but the oldest still drop off when the window passes. Practical implication: if the merchant performs a restore today, they have until the retention window expires to revert via the safety backup; after that, the safety snapshot is gone.

### Cancel during partial restore — safety backup auto-deleted

When the merchant cancels an in-progress partial restore (see [[settings-backups-restore-progress]] for the Cancel button), the platform also automatically deletes the safety backup that was created for that specific restore (via the controller's `deleteSafetyBackup` step). So a cancelled partial restore leaves no trace in the backup list — neither the temp DB nor the safety backup persists.

This is the only path that deletes a safety backup before its retention window expires. Full restore is non-cancellable, so its safety backup always lives out the retention window normally.

### Visible alongside daily backups

There's no separate "safety backups" tab — they appear in the same list and are pickable as the source for further restores. The merchant can deliberately use the safety backup of a botched restore as the starting point for a full restore back to the pre-botch state.

### Storage path is the same as daily backups

Safety backups are stored on the same remote Storage Box as daily backups, under the same path convention (`{DD-MM-YYYY}/{server-hostname}/{store-id}_{date}_{...}.sql.gz` — see [[settings-backups-list-view]]). The platform doesn't segregate safety files into a separate directory — only the database-level `is_safety` flag distinguishes them.

## Related

- [[settings-backups]] — hub.
- [[settings-backups-list-view]] — where the safety badge surfaces.
- [[settings-backups-full-restore]] — non-cancellable; its safety backup lives out the retention window normally.
- [[settings-backups-partial-restore]] — cancellable; its safety backup is auto-deleted on cancel.
- [[settings-backups-restore-progress]] — the `creating_safety_backup` step in the restore step sequence.
- [[settings-backups-subscription-gates]] — the retention pack (in days) that decides when safety backups expire.
- [[backup]] — entity page.

## Open questions

- Whether the `is_safety` flag is filterable in any list query (verify).
