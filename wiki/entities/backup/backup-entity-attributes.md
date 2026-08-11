---
type: entity
aliases: ["Backup attributes", "Backup fields", "Backup list columns", "Backup ID", "Backup date", "Backup file size", "Safety flag", "Retention window"]
tags: [settings, ops, backups, entity, fields]
created: 2026-06-10
updated: 2026-06-10
source_count: 0
---

> Part of [[backup]]. See the hub for the other aspects (identity, lifecycle, gating, restore pipeline, storage and scope).

# Backup — Attributes

## Identity

This page lists every field that exists on a Backup row — both the columns the merchant sees in the [[settings-backups]] list and the underlying values the platform stores. None of these fields are merchant-editable; every one is auto-assigned at creation time or derived from the merchant's Backups-subscription pack.

The merchant's only direct interaction with a Backup's data is to read the row (Backup date + file size + safety badge) and decide whether to click **Restore** or **Partial Restore** on it.

## Aliases

- **Backup attributes** — the canonical wiki term.
- **Backup fields** — equivalent.
- **Backup list columns** — the subset visible in the list view.
- **Backup metadata** — informal phrasing for the same set of fields.

## Key Attributes

| Attribute | What the merchant controls | Notes |
|-----------|----------------------------|-------|
| **Backup ID** | n/a (auto-assigned) | Unique identifier the platform uses internally and in the partial-restore URL (`/admin/settings/backups/:backupId/partial-restore`). |
| **Backup date** (`backup_date`) | n/a (auto, set at creation) | When the snapshot was taken. The list view is default-sorted by this descending (newest first). |
| **File size** (`file_size_formatted` + `file_size_kb`) | n/a (auto) | Human-formatted (e.g., "245.3 MB") and raw KB. Visible in the list column. Reflects the compressed `.sql.gz` size, not uncompressed database size. |
| **Server** | n/a (informational) | Which CloudCart backend server stored the file. Behind-the-scenes detail for CloudCart support diagnostics — merchant-irrelevant; restore performs equally regardless of which server holds the file. |
| **Safety flag** (`is_safety`) | n/a (auto-derived from filename) | When `true`, the safety badge appears in the list. Daily auto-backups have `is_safety=false`; pre-restore snapshots have `is_safety=true`. The classification is derived from the snapshot's stored filename containing `_safety`. Both flavors age out with the same retention rules. |
| **Created at** | n/a (auto) | When the row was added to the system. Typically equal to or within seconds of `backup_date`. |
| **Retention window (days)** | Purchased via the merchant's specific backups subscription pack | Different packs sell different retention windows (typical: 7, 30, 60, 90 days). Backups older than the window are hidden from the merchant's list and eventually purged. Surfaced in the page meta as `subscription_days`. |
| **Subscription start lower bound** | n/a (enforced by the platform) | Backups from BEFORE the merchant's subscription start date are hidden too — even if the platform took backups daily before they subscribed, only post-subscription Backups are surfaced. The "no retroactive data" rule. |
| **Contents** | n/a (the entire store database) | One Backup = everything. There is no "partial backup" or "selective backup" — the merchant cannot pick which entities to include. Granular control happens only at RESTORE time via the Partial Restore segment picker. |
| **Storage location** | n/a (off-platform, opaque) | Backups are physically stored on a separate off-platform storage location managed by CloudCart infrastructure. The merchant cannot download, view contents, or see the storage location. See [[backup-entity-storage-and-scope]]. |

## Field visibility in the list

The [[settings-backups]] list view shows the merchant-facing subset of these fields as columns:

- **Date** — `backup_date`, formatted for the merchant's locale.
- **Size** — `file_size_formatted`.
- **Safety badge** — rendered only when `is_safety=true`.
- **Actions** — Restore (always) + Partial Restore (when the `partial_restore` add-on is active).

Backup ID, Created at, Server, retention window, and storage location are NOT visible per-row — they're either platform-internal (ID, server) or page-level meta (retention window via `subscription_days`).

## What the merchant CANNOT see

- The contents of the `.sql.gz` file (no preview, no browse, no decompress).
- A diff between two Backups (no "what changed between backup A and backup B" tool).
- An entity-level breakdown (no "this Backup contains 4,231 products and 1,082 orders" panel).
- The age in days remaining before age-out (only the absolute `backup_date` is shown; the merchant computes "is this nearing retention?" themselves from the pack's window).

## What the merchant CANNOT edit

- No rename. Backups have no merchant-supplied label.
- No tag. Backups have no merchant-supplied tag.
- No description / note. Backups have no annotation field.
- No retention override per Backup. Retention is dictated by the active Backups-subscription pack and applies to all Backups uniformly.
- No "pin" or "exclude from purge". Aged Backups age out regardless.

## Where it appears

- [[settings-backups]] — the list view that renders these attributes per row.
- [[backup-entity-lifecycle]] — how `backup_date` + retention window + subscription start interact to decide visibility.

## Related

- [[backup]] — hub.
- [[settings-backups]] — the screen that displays these attributes.
- [[plan-feature]] — the Backups subscription pack that dictates the retention window.

## Open Questions

None.
