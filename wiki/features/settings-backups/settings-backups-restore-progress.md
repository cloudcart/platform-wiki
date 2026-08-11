---
type: feature
nav_path: "Settings → Backup & Restore → Restore progress"
route_name: backups.settings
route_path: /admin/settings/backups
aliases: ["Restore progress", "Active restore banner", "Restore steps", "has_active_restore", "Cancel restore", "Restore completion email"]
tags: [settings, backups, restore, progress, banner, polling]
plan_gates: ["backups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 4
---

> Part of [[settings-backups]]. See the hub for the other aspects (subscription gates, list view, full restore, partial restore, safety backup, 2FA gate).

# Backups — restore progress

## Purpose

While a restore (full or partial) is running, the backups page shows an **active-restore banner** with a live-updating step label so the merchant knows roughly where the job is in its sequence. For partial restores only, the banner carries a Cancel button. When the job finishes (success or failure), the platform sends an email to the store owner. This page documents the banner, the polling cadence, the internal step labels, the cancel modal, and the completion email.

## Where to find it

The active-restore banner renders at the top of Sidebar → Settings → **Backup & Restore** (the main list page, [[settings-backups-list-view]]) and at the top of the partial-restore segment-picker page ([[settings-backups-partial-restore]]) whenever `meta.has_active_restore=true`.

## What the merchant can do here

- See the current restore type / date / step in the banner.
- For partial restores only — click **Cancel** to abort the running restore.
- Wait for the email notification when the restore completes.

### What the merchant CANNOT do

- Start a second restore while one is active — the *"Restore selected segments"* button on the partial-restore page is disabled and the per-row buttons on the list page are blocked.
- Cancel a FULL restore — only partial restores can be cancelled.

## Settings & fields

### Active-restore banner

When `meta.has_active_restore=true`, a blue banner appears at the top of the page with a spinner, the restore type / date, and the current step (live-translated from the platform's internal step names):

> *"Restoring from backup `{backup_date}` — `{current_step}`"*

For **partial restores only**, the banner also has a red **Cancel** button to its right.

### Restore steps the merchant might see ticking through

The job updates `step` on the restore-request row in a fixed order so the polling UI can show progress. The platform-internal step keys (translated to merchant-facing labels at render time):

**Full restore step sequence:**

1. `starting`
2. `verifying_database`
3. `enabling_maintenance`
4. `creating_safety_backup`
5. `downloading_backup`
6. (decompress, implicit — no separate step)
7. `restoring_database`
8. `verifying`
9. `disabling_maintenance`

**Partial-restore step sequence:**

1. `starting`
2. `creating_safety_backup`
3. `downloading_backup`
4. (decompress, implicit)
5. `importing_to_temp_db`
6. `extracting_segments`
7. `restoring_segments`
8. `cleaning_up`

Either job ends with `status=completed` and `step=null`. Failure sets `status=failed` with an `error_message` (surfaced in the failure email — see below).

### Cancel modal (partial restore only)

Clicking the red **Cancel** button opens a second confirmation modal:

- **Title**: *"Cancel Restore"*.
- **Body**: *"Are you sure you want to cancel the partial restore? The temporary database and safety backup will be removed."*
- **Yes button**: *"Yes, cancel"* (red).
- **No button**: *"No, keep restoring"*.

The cancel endpoint is `POST /backups/restore/{id}/cancel`. On confirmation, the platform:

- Drops the temp database on the db-services host (`cleanupTempDatabases`).
- Auto-deletes the safety backup created for this restore (`deleteSafetyBackup` — see [[settings-backups-safety-backup]]).
- Marks the restore-request row as cancelled.

The same endpoint, called for a full restore, rejects with *"Only partial restores can be cancelled"*.

## Business rules

### Polling cadence — every 5 seconds while a restore is active

The page polls the backups index endpoint every 5 seconds while a restore is active to update the step label live. The polling stops automatically when `has_active_restore` becomes false (success toast *"Backup restore completed successfully"* fires when transitioning from active → not active).

The polling target is the standard backups index (the same endpoint that drives [[settings-backups-list-view]]) — there's no separate streaming channel. The platform also exposes a lightweight `GET /backups/restore-status` probe, but the in-page progress UI uses the index endpoint (verify whether `restore-status` is used purely by the dashboard banner).

### Only one restore at a time

The platform prevents concurrent restores to avoid data races. Both the partial-restore page (`Restore selected segments` button disabled) and the list page (per-row Restore buttons blocked) check `has_active_restore` and refuse to dispatch new restore calls while one is active. The merchant has to wait.

### Cancel handling — full vs partial

| Type | Cancellable? | What happens on cancel |
|---|---|---|
| Full restore | No (rejected with *"Only partial restores can be cancelled"*) | n/a — the job runs to completion or fails on its own. |
| Partial restore | Yes | Temp DB dropped, safety backup deleted, restore-request marked cancelled. Live DB state depends on how far the restore got — possibly partially restored, possibly not started. |

Practical implication: a merchant who cancels mid-`restoring_segments` may have some segments fully imported and others not. The merchant should expect a mixed state needing further intervention.

### Email notification — on completion AND on failure

Both the full and the partial restore jobs send an email to the store owner via the platform's mail manager, using localised translation strings (`backup_restore_subject` / `backup_restore_body`). Target address: `site->user->email`. Locale picked from `site->language_cp` or `site->language`, falling back to English if the lang file is missing.

The email fires for any terminal status (completed OR failed). It's useful because the job can run for an hour+ on large stores and the merchant probably navigated away.

### Restore jobs run on the platform's system queue

Both full and partial restore jobs declare `$queue = 'system7'` (verify) — they run on the platform's high-priority system queue, not the regular store-scoped jobs queue. Practical implication for support: large-store restores are queued centrally and may share capacity with other system-7 jobs (cron health checks, infra tasks). Backup restore failures are logged via the platform's exception store.

The merchant has no way to see this queue directly from the backup UI; the `step` updates are the only visible progress signal. (Some staff with deep diagnostics may inspect [[settings-queue-view]] (verify) for system queue visibility.)

### What the merchant sees on failure

If `status=failed`, the active-restore banner disappears (since `has_active_restore` becomes false), the failure email is sent to the store owner, and the merchant is left in a state where:

- For full restore: the storefront's maintenance flag may have been left ON if the failure happened mid-import — the restore job is supposed to clear it in the `disabling_maintenance` step, but a crash before that step won't run the cleanup. Support intervention may be needed to lift maintenance manually.
- For partial restore: the temp DB may leak (the `cleanupTempDatabases` safety net runs from the cancel handler; a failure path that doesn't go through cancel may not trigger it — verify).

## Related

- [[settings-backups]] — hub.
- [[settings-backups-list-view]] — the page that hosts the active-restore banner.
- [[settings-backups-partial-restore]] — also hosts the banner; the only restore type that can be cancelled.
- [[settings-backups-full-restore]] — non-cancellable; the `enabling_maintenance` / `disabling_maintenance` steps wrap its sequence.
- [[settings-backups-safety-backup]] — `creating_safety_backup` step + auto-deletion on partial-restore cancel.
- [[settings-queue-view]] — system queue visibility for restore jobs (verify).

## Open questions

- Does a hard failure (job crash) clear the maintenance flag on full restore, or does the storefront stay in maintenance until support intervenes?
- Whether `restore-status` probe is used by the in-page progress UI in addition to the dashboard banner (verify).
