---
type: feature
nav_path: "Settings → Backup & Restore → Full restore"
route_name: backups.settings
route_path: /admin/settings/backups
aliases: ["Full restore", "Restore backup", "Restore everything", "Storefront maintenance during restore", "Maintenance mode restore"]
tags: [settings, backups, restore, maintenance, full-restore]
plan_gates: ["backups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-backups]]. See the hub for the other aspects (subscription gates, list view, partial restore, safety backup, 2FA gate, restore progress).

# Backups — full restore

## Purpose

A **full restore** replaces every product, order, customer, setting, etc. in the live store with the snapshot from the chosen backup. Any data added since the backup was taken is lost. While the restore runs, the storefront is in **maintenance mode** — customers see the platform's maintenance page, not products. Full restore is the heavyweight option: it's destructive, non-cancellable, and gated by a mandatory 2FA challenge.

## Where to find it

Sidebar → Settings → **Backup & Restore** → **Restore** button on any backup row in the list ([[settings-backups-list-view]]).

## What the merchant can do here

- Click **Restore** on a backup row → opens the full-restore confirmation modal.
- Confirm via the modal → opens the 2FA challenge modal ([[settings-backups-2fa-gate]]).
- After 2FA passes → the restore is dispatched as a background job; the active-restore banner appears ([[settings-backups-restore-progress]]).

### What the merchant CANNOT do

- Cancel a full restore once started — the cancel endpoint explicitly rejects full restores (see below).
- Restore selected segments — that's [[settings-backups-partial-restore]].
- Schedule the restore for later — restores fire immediately on confirmation.

## Settings & fields

### Full-restore confirmation modal

Triggered by clicking the **Restore** button on a backup row. The standard confirmation modal opens with:

- **Title**: *"Full Restore"*.
- **Body (rich HTML)**:
  - *"Are you sure you want to restore your store to the state from `{backup_date}`?"*
  - *"This will put your store in maintenance mode. A safety backup will be created before the restore."*
  - Blue info callout: *"Please note that only database records will be restored. Images and files stored in the Files section are not affected."*
- **Yes button**: *"Yes, restore"* (red / danger variant).
- **No button**: *"Cancel"*.

Clicking Yes does NOT immediately fire the restore — instead it dismisses the confirmation modal and opens the **2FA challenge modal** ([[settings-backups-2fa-gate]]). The actual restore API call is fired only after the 2FA challenge returns a valid single-use hash.

## Business rules

### Full restore replaces EVERYTHING

`POST /backups/{id}/restore` triggers a full restore: every product, order, customer, setting, page, blog post, etc. is replaced with the snapshot from the chosen backup. Any data added since the backup was taken is lost. There is no merging — the live DB is overwritten from the backup dump.

### Storefront DOES go into maintenance mode

A full restore is NOT zero-downtime. The restore job sets the site's `maintenance` flag to ON before importing the backup and removes it only after the import completes. While maintenance is enabled, customers visiting the storefront see the platform's maintenance page (not normal product pages, not stale data, not any 5xx error). For typical store sizes the maintenance window is a few minutes to an hour; for very large stores (100k+ products, millions of orders) it can run for hours.

Operationally, the maintenance flag is flipped via the **Router DB** — the job writes directly to `eu_cc_router.sites.maintenance` (the cross-store domain router) and flushes the domain cache so the change is visible immediately. The flag is cleared again at the end of the restore.

### Practical guidance

Merchants planning a full restore should:

- Schedule it during low-traffic hours.
- Warn any active customers via their own channels first (email, social).
- Expect a maintenance window proportional to the store size.
- Commit only when there's no realistic chance they'll need to abort — full restore is **NOT cancellable**.

### Full restore is NOT cancellable — only partial

The cancel endpoint (`POST /backups/restore/{id}/cancel`) explicitly rejects cancellation of a full restore with the message *"Only partial restores can be cancelled"*. Once a merchant kicks off a full restore, it runs to completion (or fails on its own). Maintenance stays on the whole time. See [[settings-backups-restore-progress]] for the steps the restore goes through and what failure looks like.

### Only one restore at a time

If `meta.has_active_restore=true` (another restore — full or partial — is already running), the platform blocks new starts. The merchant has to wait for the active restore to complete. See [[settings-backups-restore-progress]] for how the banner surfaces this.

### Safety backup auto-created before the restore

Right before the import phase, the job creates a pre-restore safety backup tagged `is_safety=true` and pushes it to backup storage. This becomes a rollback point if the restore turns out badly — the merchant can full-restore from the safety backup to roll back. See [[settings-backups-safety-backup]] for identification + retention behaviour.

### Mandatory 2FA on every restore

`POST /backups/{id}/restore` requires a verified single-use 2FA task hash with action `restore_backup`. Without it the API returns 422 *"Two-factor verification required"* / *"Invalid or expired verification"*. See [[settings-backups-2fa-gate]].

### What's NOT covered by the database backup

Full restore replaces only DATABASE records. The confirmation modal's blue callout explicitly says: *"Images and files stored in the Files section are not affected."* File-manager media (product images, custom uploads) lives in CloudCart's separate file storage and is backed up at the file-storage level, not as part of the database snapshot. See [[settings-files]].

A few other things to verify before relying on full restore for a complex migration: API keys / PAT tokens, geo-zone polygons, app-specific data. The full backup *appears* to bundle store-level settings and shipping configuration, but for full coverage details the merchant should contact CloudCart support.

### Email notification on completion

When the job finishes, the platform sends a localised email (`backup_restore_subject` / `backup_restore_body` strings) to the store owner's email address (`site->user->email`). The locale is picked from `site->language_cp` or `site->language`, falling back to English if the lang file is missing. This is useful since the job can run for an hour+ on large stores and the merchant probably navigated away.

## Related

- [[settings-backups]] — hub.
- [[settings-backups-list-view]] — the per-row Restore button that opens the modal.
- [[settings-backups-2fa-gate]] — the mandatory 2FA challenge.
- [[settings-backups-safety-backup]] — the pre-restore snapshot auto-created before the import.
- [[settings-backups-restore-progress]] — the active-restore banner, step labels, and completion email.
- [[settings-backups-partial-restore]] — the additive alternative when the merchant only wants to recover specific data.
- [[settings-files]] — file-manager media is NOT part of the database backup.
- [[backups-and-restore]] — concept page.

## Open questions

- Exact list of what's included in the database backup vs CloudCart's file-storage backups (the wiki's claim is bundled, but a full source-of-truth list would help — verify).
