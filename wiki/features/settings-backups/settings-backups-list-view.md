---
type: feature
nav_path: "Settings → Backup & Restore → Backups list"
route_name: backups.settings
route_path: /admin/settings/backups
aliases: ["Backups list", "Backup table", "Backup columns", "Extend period", "Backup retention cutoff"]
tags: [settings, backups, list, table, retention]
plan_gates: ["backups"]
created: 2026-06-10
updated: 2026-06-10
source_count: 3
---

> Part of [[settings-backups]]. See the hub for the other aspects (subscription gates, full restore, partial restore, safety backup, 2FA gate, restore progress).

# Backups — list view

## Purpose

When the merchant has the `backups` subscription, the page shows a paginated table of all available backups inside their retention window. Each row is a candidate for full restore (always) or partial restore (if the `partial_restore` add-on is subscribed). The list also drives the merchant's awareness of safety backups and the "Extend period" upgrade CTA.

## Where to find it

Sidebar → Settings → **Backup & Restore**. The list renders inside the main page (route `backups.settings`, path `/admin/settings/backups`) once `meta.subscribed=true` ([[settings-backups-subscription-gates]]).

## What the merchant can do here

- See the paginated table of all backups in their retention window.
- Click **Restore** on any row → opens the full-restore confirmation modal (see [[settings-backups-full-restore]]).
- Click **Partial Restore** on any row → navigates to the partial-restore form for that backup (visible only when `partial_restore_subscribed=true`, see [[settings-backups-partial-restore]]).
- See the *"safety"* badge on rows where `is_safety=true` (see [[settings-backups-safety-backup]]).
- Click **Extend period** in the header to upgrade to a longer-retention pack (only when `meta.has_upgrade=true`, see [[settings-backups-subscription-gates]]).
- See the active-restore banner when a restore is in progress (see [[settings-backups-restore-progress]]).

## Settings & fields

### List table columns

| Column | What it shows |
|---|---|
| **Backup date** (`backup_date`) | When this backup was taken. |
| **File size** (`file_size_formatted`) | Human-formatted size (e.g., "245.3 MB"). Raw KB available as `file_size_kb`. |
| **Server** | Which CloudCart backend server stored the file. Informational only (see "Server column is informational"). |
| **Safety badge** | Shown when `is_safety=true` — auto-created pre-restore snapshot. See [[settings-backups-safety-backup]]. |
| **Created at** | When the backup record was added to the system. |
| **Restore action** | Per-row button → opens the full-restore confirmation modal. |
| **Partial restore action** | Per-row link → opens the partial-restore form for this backup. Visible only when `partial_restore` is subscribed. |

### Meta fields surfaced to the UI

| Meta key | Drives |
|---|---|
| `feature_enabled` | Plan includes the backups plan-feature. |
| `subscribed` | Backups subscription is active. False = marketing splash, not the list. |
| `partial_restore_subscribed` | Partial-restore add-on is active. Controls visibility of the per-row Partial Restore button. |
| `partial_restore_pack` | Whether the plan OFFERS a `partial_restore` pack at all. |
| `has_upgrade` | A longer-retention `backups` pack is available — shows the "Extend period" button. |
| `has_active_restore` | A restore is currently running — drives the active-restore banner and disables new starts. See [[settings-backups-restore-progress]]. |
| `subscription_days` | Current retention window in days. |

The list query is paginated and refetched on standard intervals. The `subscriptionStatus` (`GET /backups/subscription-status`) and `restoreStatus` (`GET /backups/restore-status`) probes are SEPARATE from the main `index` query and may have different caching behaviour.

## Business rules

### What backups appear (retention cutoff)

Two combined filters decide which backups are listed (see [[settings-backups-subscription-gates]] for the retention-pack mechanics):

- Backups older than `subscription.value` days are hidden.
- Backups from before the merchant's subscription `created_at` are hidden — even if the platform took daily backups before subscription, only post-subscription backups surface.

The effective cutoff is the platform code (verify).

### Safety backups count toward retention

Safety backups (auto-created before every restore, see [[settings-backups-safety-backup]]) are stored in the same backup table as regular daily backups and are subject to the same retention rules. They expire alongside daily backups when the window passes. Merchants performing many restores in a short period accumulate more rows, but the oldest still drop off.

### Server column is informational only

The "Server" column shows which CloudCart backend server stored the backup file (behind-the-scenes infrastructure detail). It has NO practical implication for the merchant — restore performs equally regardless of which server the file lives on. The column exists primarily for support diagnostics and can be safely ignored by store owners.

### Where backup files physically live

Backups are physically stored on **an off-platform storage location separate from the live store database** — a remote Storage Box reached via SSH (the host / user / SSH-key / port 23 are CloudCart-infrastructure config, not exposed to the merchant). Path convention on storage: `{DD-MM-YYYY}/{server-hostname}/{store-id}_{date}_{...}.sql.gz` (verify). Restore uses `scp` to download the `.sql.gz` to a temp dir, gunzips it, then imports. For very large stores, the download + import phase takes significantly longer than the original backup creation.

The merchant doesn't see this storage location directly — it's managed by CloudCart infrastructure.

### Extend-period upgrade

The "Extend period" button in the header surfaces only when `has_upgrade=true` — meaning the merchant's plan has a `backups` pack with a `value` (days) higher than the current pack. Clicking it opens the plan-upgrade modal which moves the merchant to the longer pack at the difference in price (standard subscription upgrade flow). After upgrade, more historical backups become visible on the list as the cutoff recedes.

### No raw download

There is no way to download a backup file directly from the list. Restores are server-side operations — the file is consumed by the restore job, not handed to the merchant. For migration scenarios where the merchant needs the raw file, support has to intervene.

## Related

- [[settings-backups]] — hub.
- [[settings-backups-subscription-gates]] — the retention-pack-as-days mechanics that decide the cutoff.
- [[settings-backups-safety-backup]] — the safety-badge rows and how they enter the list.
- [[settings-backups-restore-progress]] — the active-restore banner that overlays the list while a restore runs.
- [[settings-backups-full-restore]] — what happens when the merchant clicks Restore.
- [[settings-backups-partial-restore]] — what happens when the merchant clicks Partial Restore.
- [[backup]] — entity page.

## Open questions

- Exact pagination defaults + total-count strategy (verify).
